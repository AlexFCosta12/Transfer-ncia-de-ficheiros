from socket import *
from time import ctime
import sys
import glob

def escreve(BUFSIZ,cliente,func):
    nome_fich=input("nome do ficheiro sff:\n")
    cliente.send((nome_fich).encode('utf-8')) 
    warning = cliente.recv(BUFSIZ).decode('utf-8')
    if(warning!='1'):
        print(warning)
    else:
        f = open(nome_fich,'wb')
        l = 1
        while(l):
            l = cliente.recv(1024)
            while (l):
                f.write(l)
                l = cliente.recv(1024)
            f.close() 
        print("download efetuado")
        if (func=='1'):
            menu_log(BUFSIZ,cliente)
        else:
            buf2()        
      
    
def le(BUFSIZ,cliente,func):
    nome_fich=input("nome do ficheiro sff:")
    if nome_fich in (glob.glob("*.*")):
        cliente.send((nome_fich).encode('utf-8'))
        f=open (nome_fich, "rb") 
        l = f.read(1024)
        while (l):
            cliente.send(l)
            l = f.read(1024)
        cliente.close()
        f.close()
   
    else:
        print("o ficheiro que esta a tentar fazer o upload nao existe")
    if (func=='1'):
        menu_log(BUFSIZ,cliente)
    else:
        buf2()      

def listagem(cliente,BUFSIZ,func):
    lista = cliente.recv(BUFSIZ).decode('utf-8')
    if (lista=='nao existem ficheiros'):
        print(lista)
    else:
        lista=lista.split()
        for i in range(len(lista)):
            print(i,'-',lista[i])
    i=0    
    if (func=='1'):
        menu_log(BUFSIZ,cliente)
    else:
        buf2()
    
def menu_log(BUFSIZ,cliente): 
    while True:
        escolha=eval(input("1-download\n2-upload\n3-ficheiros disponiveis para o download\n4-sair\n"))
        cliente.send((str(escolha)).encode('utf-8'))
        if(escolha==1):
            escreve(BUFSIZ,cliente,'1')
            
        elif(escolha==2):
            le(BUFSIZ,cliente,'1')
    
        elif(escolha==3):
            listagem(cliente,BUFSIZ,'1')
            
               
        elif(escolha==4):
            nova_data=cliente.recv(BUFSIZ).decode('utf-8')
            print(nova_data)
            print("log out")
            break


    
def buf1():
    HOST = 'localhost'
    PORT = 21567
    BUFSIZ = 1024
    ADDR = (HOST, PORT)  
    cliente = socket(AF_INET, SOCK_STREAM)
    cliente.connect(ADDR)
    nova_data='0'
    while(nova_data!='1'):
        username=input('username:\n')
        password=input('password:\n') 
        cliente.send(('login'+' '+username+' '+password).encode('utf-8'))
        nova_data=cliente.recv(BUFSIZ).decode('utf-8')
        if(nova_data!='1'):
            print("username ou password errada")
    nova_data='0'
    menu_log(BUFSIZ,cliente)
            
def inicial():
    buffer=0    
    while(buffer!='1' and buffer!='2' and buffer!='3'):
        print("/''''''''''''''''''''''\ \n|---------MENU---------|\n\______________________/")
        buffer=input('1-fazer login\n2-entrar sem login\n3-sair\n')
        buffer=str(buffer)
        if(buffer.isdigit()==False or (buffer!='1' and buffer!='2' and buffer!='3')):
            print("por favor escolha uma opcao valida")
    if(buffer=='1'):
        buf1()
    elif(buffer=='2'):
        buf2()     
    elif(buffer=='3'):
        buf3()            
         
            

       
def buf2(): 
    HOST = 'localhost'
    PORT = 20000
    BUFSIZ = 1024
    ADDR = (HOST, PORT)  
    cliente = socket(AF_INET, SOCK_STREAM)
    cliente.connect(ADDR)  
    escolha=eval(input("1-download\n2-upload\n3-ficheiros disponiveis para o download\n4-voltar atras\n"))
    cliente.send(str(escolha).encode('utf-8'))
    if(escolha==1):
        escreve(BUFSIZ,cliente,'2')
        
    elif(escolha==2):
        le(BUFSIZ,cliente,'2')
        
    elif(escolha==3):
        listagem(cliente,BUFSIZ,'2')
    elif(escolha==4):
        inicial()
        
        
        
def buf3(): 
    sys.exit(0)
    print("opcao invalida4")
    
inicial()


