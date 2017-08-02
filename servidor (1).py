from socket import *    
from time import ctime
import glob
import os, sys
import shutil
HOST = ""
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
servidor = socket(AF_INET, SOCK_STREAM)
servidor.bind(ADDR)
servidor.listen(5)  
                
print("waiting for a connection.....")
servidor, addr= servidor.accept()
print("....connected from:", addr)


def login_srv(user,data,servidor,BUFSIZ,AF_INET, SOCK_STREAM):
    confirmado='0'               
    f=open("users.txt","r")
    users=f.readlines()
    for linhas in users:
        verifica=linhas[:-1].split()
        if(verifica[0]==user[1] and verifica[1]==user[-1]):
            confirmado='1'
    servidor.send((confirmado).encode('utf-8'))
    while(confirmado!='1'): 
        f=open("users.txt","r")
        users=f.readlines()
        data=data.split()
        for linhas in users:
            verifica=linhas[:-1].split()
            if(verifica[0]==data[1] and verifica[1]==data[2]):
                confirmado='1'  
                servidor.send((confirmado).encode('utf-8')) 
            if(confirmado!='1'):
                confirmado='0'
        data = servidor.recv(BUFSIZ).decode('utf-8')               
        f.close()
    #confirmado='0'

    newpath = ((r'%s') % (user[1])) 
    if not os.path.exists(newpath):
        os.makedirs(newpath)  
    while True:
        data = servidor.recv(BUFSIZ).decode('utf-8')
        if (data=='1'):
            dw_srv(data,user,servidor,AF_INET, SOCK_STREAM)
        elif(data=='2'):
            upl_srv(data,user,servidor)
        elif(data=='3'):
            lts_srv(user,servidor)
        elif(data=='4'):
            servidor.send(('sessao terminada').encode('utf-8'))


        
        
        
def dw_srv(data,user,servidor,AF_INET, SOCK_STREAM):
    data = servidor.recv(BUFSIZ).decode('utf-8')    
    diretoria=("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\%s\\*.*") % user[1]
    fich_down=("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\%s\\%s") % (user[1],data)
    lista_ficheiros=[]
    for ficheiro in (glob.glob(str(diretoria))):
        ficheiro=ficheiro.split(user[1])
        lista_ficheiros.append(ficheiro[1][1:])
    if(data in lista_ficheiros):
        string='1'
        servidor.send((string).encode('utf-8'))
        f=open(fich_down, "rb") 
        l = f.read(1024)
        while (l):
            servidor.send(l)
            l = f.read(1024)
        servidor.close()
    else:
        string='nao existe tal ficheiro'
        servidor.send((string).encode('utf-8'))

                
def upl_srv(data,user,servidor):
    data = servidor.recv(BUFSIZ).decode('utf-8')
    f =open(data,'wb')
    l = 1
    while(l):
        l = servidor.recv(1024)
        while (l):
            f.write(l)
            l = servidor.recv(1024)

        f.close() 
    origem=("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\%s" % (data))
    destino=("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\%s" % (user[1]))
    shutil.move(origem,destino)

    
def lts_srv(user,servidor):
        lista_ficheiros=[]
        string=''
        diretoria=("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\%s\\*.*") % user[1]
        for ficheiro in (glob.glob(str(diretoria))):
            ficheiro=ficheiro.split(user[1])
            lista_ficheiros.append(ficheiro[1][1:]) 
        for i in range(len(lista_ficheiros)):
            string=string+lista_ficheiros[i]+' '
        servidor.send((string).encode('utf-8'))

        
def convi_srv(user,servidor,addr,BUFSIZ):                    
    origem="C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\default\\*.*"
    if(user[1]=='download'):
        lista_ficheiros=[]
        for ficheiro in (glob.glob(str(origem))):
            ficheiro=ficheiro.split('default')
            lista_ficheiros.append(ficheiro[1][1:])
        if user[2] in lista_ficheiros:
            string='1'
            servidor.send((string).encode('utf-8'))
            diretorio=("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\default\\%s") % (user[2])
            f=open (diretorio, "rb")
            l = f.read(1024)
            while (l):
                servidor.send(l)
                l = f.read(1024)
            servidor.close() 
            f.close()
        else:
            string='nao existe o ficheiro desejado'
            servidor.send((string).encode('utf-8'))

    elif(user[1]=='upload'):
        f = open(user[2],'wb')
        l = 1
        while(l):
            l = servidor.recv(1024)
            while (l):
                f.write(l)
                l = servidor.recv(1024)
            f.close() 
        origem=("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\%s" % (user[2]))
        destino=("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\default")
        shutil.move(origem,destino)                
    elif(user[1]=='listar'):
        lista_ficheiros=[]
        string=''
        for ficheiro in (glob.glob("C:\\Users\\ASUS\\Desktop\\novo python\\servidor\\default\\*.*")):
            ficheiro=ficheiro.split('default')
            lista_ficheiros.append(ficheiro[1][1:])
        if not lista_ficheiros:
            string='nao existem ficheiros'
        else:
            for i in range(len(lista_ficheiros)):
                string=string+lista_ficheiros[i]+' '
        servidor.send((string).encode('utf-8')) 

  
def lista(servidor,addr,BUFSIZ,AF_INET, SOCK_STREAM):
    data = servidor.recv(BUFSIZ).decode('utf-8')
    user=data.split()
    if(user[0]=='login'):
        login_srv(user,data,servidor,BUFSIZ,AF_INET, SOCK_STREAM)
    elif(user[0]=='convidado'):
        convi_srv(user,servidor,addr,BUFSIZ)



if __name__ == '__main__':           
    lista(servidor,ADDR,BUFSIZ,AF_INET, SOCK_STREAM)