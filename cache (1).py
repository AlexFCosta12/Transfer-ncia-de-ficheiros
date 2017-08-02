from socket import *    
from time import ctime
import glob

HOST = ""
PORT = 20000
BUFSIZ = 1024
ADDR = (HOST, PORT)

servidor = socket(AF_INET, SOCK_STREAM)
servidor.bind(ADDR)
servidor.listen(5)

confirmado=0
def le(cliente,data):
    f=open (data, "rb") 
    l = f.read(1024)
    while (l):
        cliente.send(l)
        l = f.read(1024)
    cliente.close() 
    f.close()
def escreve(servidor,data):  
    f = open(data,'wb')
    l = 1
    while(l):
        l = servidor.recv(1024)
        while (l):
            f.write(l)
            l = servidor.recv(1024)
        f.close()  
    
def cache_liga(servidor,addr,BUFSIZ):
    print("waiting for a connection.....")
    servidor, addr= servidor.accept()
    print("....connected from:", addr)
    opc(servidor,addr,BUFSIZ)

def opc(servidor,addr,BUFSIZ):
    data = servidor.recv(BUFSIZ).decode('utf-8') 
    if(data=='1'):
        data = servidor.recv(BUFSIZ).decode('utf-8')
        if data in glob.glob("*.*"):
            string='1'
            servidor.send((string).encode('utf-8'))
            le(servidor,data)
                
                
        else:
            HOST = 'localhost'
            PORT = 21567
            BUFSIZ = 1024
            ADDR = (HOST, PORT)  
            cliente = socket(AF_INET, SOCK_STREAM)
            cliente.connect(ADDR)                 
            cliente.send(('convidado'+' '+'download'+' '+data).encode('utf-8'))
            nova_data = cliente.recv(BUFSIZ).decode('utf-8')
            if(nova_data=='1'):
                servidor.send((nova_data).encode('utf-8'))
                escreve(cliente,data)
                le(servidor,data)

            else:
                servidor.send((data).encode('utf-8'))
                
    elif(data=='2'):
        data = servidor.recv(BUFSIZ).decode('utf-8')
        escreve(servidor,data)
            
        HOST = 'localhost'
        PORT = 21567
        BUFSIZ = 1024
        ADDR = (HOST, PORT)  
        cliente = socket(AF_INET, SOCK_STREAM)
        cliente.connect(ADDR)  
        cliente.send(('convidado'+' '+'upload'+' '+data).encode('utf-8'))
        le(cliente,data) #mandar o upload para o servidor
            
    elif(data=='3'):
        HOST = 'localhost'
        PORT = 21567
        BUFSIZ = 1024
        ADDR = (HOST, PORT)  
        cliente = socket(AF_INET, SOCK_STREAM)
        cliente.connect(ADDR)  
        cliente.send(('convidado'+' '+'listar').encode('utf-8'))  
        lista = cliente.recv(BUFSIZ).decode('utf-8')
        servidor.send((lista).encode('utf-8'))  
            
    elif(data=='4'):
        cliente.send(('acabar').encode('utf-8')) 
        
        
        
        
cache_liga(servidor,ADDR,BUFSIZ)