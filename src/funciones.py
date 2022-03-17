#Funciones auxiliares 

import hashlib
from datetime import datetime
import numpy as np
from randomgen import ChaCha

global fechaIni
global diccPalSeed
global seed
global contadorTransacciones

def codificarMensaje(inputValue, clave):
    ### Generar nonce a partir de seed y del número de transaccion
    mensyClave = (inputValue+str(clave)).encode("utf-8")
    hasheo =  hashlib.sha3_256(mensyClave).hexdigest()
    #print("Hash del mensaje: " + str(hasheo))
    mensajeConc = inputValue + "\n" + str(hasheo)
    mensByte = mensajeConc.encode("utf-8")
    return mensByte


def decodificarMensaje(data):
    dataString = data.decode("utf-8")
    trozos = dataString.split("\n")
    return trozos
        
def comprobarIntegridad(trozos, clave):
    mensyClave = (str(trozos[0]) + str(clave)).encode("utf-8")
    hasheo =  hashlib.sha3_256(mensyClave).hexdigest()
    if str(hasheo) == str(trozos[1]):
        #codificarMensaje("Transferencia realizada con exito", clave)
        #conn.sendall(codificarMensaje("Transferencia realizada con exito", clave))
        #print("Received " + str(mensyClave))
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
        f.write(str(fecha))

def importar():
    with open("./configuracion/config.txt", "r") as f:
        global fechaIni
        fechaIni = datetime.strptime(f.readline(), "%d-%m-%Y")
    
    global diccPalSeed
    diccPalSeed = sacarPalabrasDelDiccionario("./diccionario/diccionarioPalabras.txt")
    
    fechaHoy = datetime.today()
    indiceSeed = (fechaHoy-fechaIni).days
    keys = []
    for k in diccPalSeed.keys(): 
        keys.append(k)
    pal = keys[indiceSeed]
    global seed
    seed = diccPalSeed[pal]
    
    
    
        


if __name__ == '__main__':
    iniciar()
    importar()
    print(diccPalSeed["Abad"])
    print(seed)
    
    #diccionario = sacarPalabrasDelDiccionario("./diccionario/diccionarioPalabras.txt")
    #for key in diccionario:
    #    print("KEY: " + str(key) + " - VALUE: " + str(diccionario[key]))