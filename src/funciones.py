#Funciones auxiliares 

import hashlib

def codificarMensaje(inputValue, clave):
    mensyClave = (inputValue+str(clave)).encode("utf-8")
    hasheo =  hashlib.sha3_256(mensyClave).hexdigest()
    #print("Hash del mensaje: " + str(hasheo))
    mensajeConc = inputValue + "\n" + str(hasheo)
    mensByte = mensajeConc.encode("utf-8")
    return mensByte


def decodificarMensajeyClave(data, conn, clave):
    dataString = data.decode("utf-8")
    trozos = dataString.split("\n")
    mensyClave = (str(trozos[0]) + str(clave)).encode("utf-8")
    hasheo =  hashlib.sha3_256(mensyClave).hexdigest()
    if str(hasheo) == str(trozos[1]):
        #codificarMensaje("Transferencia realizada con exito", clave)
        conn.sendall(codificarMensaje("Transferencia realizada con exito", clave))
        #print("Received " + str(mensyClave))
    else:
        conn.sendall(codificarMensaje("Ha habido un error de integridad en la transmision, realice de nuevo la transferencia", 
                                      clave))

def sacarPalabrasDelDiccionario(file):
    diccionario = {}
    with open(file, encoding="utf-8") as f:
        for linea in f:
            trozos = linea.split(":")
            diccionario[trozos[0]] = int(trozos[0], 36) 
    return diccionario


if __name__ == '__main__':
    diccionario = sacarPalabrasDelDiccionario("./diccionario/diccionarioPalabras.txt")
    for key in diccionario:
        print("KEY: " + str(key) + " - VALUE: " + str(diccionario[key]))