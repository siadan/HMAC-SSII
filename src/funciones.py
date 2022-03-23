#Funciones auxiliares 

import hashlib
from datetime import datetime
import numpy as np
from randomgen import ChaCha


def codificarMensaje(inputValue, clave):
    seed = importarSeed()
    nonce = generarNonce(seed)
    mensyClave = (str(nonce)+inputValue+str(clave)).encode("utf-8")
    hasheo =  hashlib.sha3_256(mensyClave).hexdigest()
    mensajeConc = inputValue + "\n" + str(hasheo)
    mensByte = mensajeConc.encode("utf-8")
    return mensByte


def decodificarMensaje(data):
    dataString = data.decode("utf-8")
    trozos = dataString.split("\n")
    return trozos
        
def comprobarIntegridad(trozos, clave):
    seed = importarSeed()
    nonce = generarNonce(seed)
    mensyClave = (str(nonce) + str(trozos[0]) + str(clave)).encode("utf-8")
    hasheo =  hashlib.sha3_256(mensyClave).hexdigest()
    if str(hasheo) == str(trozos[1]):
        return True
    else:
        return False
    
def enviarConfimación(conn, clave):
    mens = codificarMensaje("Transferencia realizada con exito", clave)
    conn.sendall(mens)
    
def enviarNegativa(conn, clave):
    mens = codificarMensaje("Se ha producido un error de integridad, vuelva a realizar la transferencia", clave)
    conn.sendall(mens)
    
        

def sacarPalabrasDelDiccionario(file):
    diccionario = {}
    with open(file, encoding="utf-8") as f:
        for linea in f:
            trozos = linea.split(":")
            diccionario[trozos[0]] = int(trozos[0], 36) 
    return diccionario


def iniciar():
    fecha = datetime.today().strftime("%d-%m-%Y")
    with open("./configuracion/config.txt", "w") as f:
        f.write("Fecha Config=" + str(fecha) + "\n")
        f.write("Fecha Ultima=" + str(fecha) + "\n")
        f.write("Numero Comunicacion=" + str(0))
    
def importarSeed():
    with open("./configuracion/config.txt", "r") as f:
        fechaStr = f.readline().split("=")[1].strip()
        fechaIni = datetime.strptime(fechaStr, "%d-%m-%Y")
    
    diccPalSeed = sacarPalabrasDelDiccionario("./diccionario/diccionarioPalabras.txt")
    
    fechaHoy = datetime.today()
    indiceSeed = (fechaHoy-fechaIni).days % 165
    keys = []
    for k in diccPalSeed.keys(): 
        keys.append(k)
    pal = keys[indiceSeed]
    seed = diccPalSeed[pal]
    return seed

def generarNonce(seed):
    with open("./configuracion/config.txt", "r") as f:
        next(f)
        next(f)
        numMens = int(f.readline().split("=")[1])
    rg = np.random.Generator(ChaCha(seed=seed, rounds=8))
    nonces = rg.integers(1,9000,size=9999)
    return nonces[numMens]

def comprobarContador():
    hoy = datetime.today().strftime("%d-%m-%Y")
    f = open("./configuracion/config.txt", "r")
    lineas = f.readlines()
    fechaUlt = lineas[1].split("=")[1].strip()
    if fechaUlt != str(hoy):
        lineas[1] = "Fecha Ultima="+str(hoy)+"\n"
        lineas[2] = "Numero Comunicacion=0"
        f = open("./configuracion/config.txt", "w")
        f.writelines(lineas)
    f.close()
  
def actualizarContador():  
    f = open("./configuracion/config.txt", "r")
    lineas = f.readlines()
    numComm = int(lineas[2].split("=")[1].strip())
    lineas[2] = "Numero Comunicacion="+str(numComm+1)
    f = open("./configuracion/config.txt", "w")
    f.writelines(lineas)
    f.close()
    
    
    
    
        


if __name__ == '__main__':
    iniciar()