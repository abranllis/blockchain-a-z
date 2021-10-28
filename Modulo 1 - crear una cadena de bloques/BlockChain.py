# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 16:54:58 2021

@author: abmartinez
"""

# Módulo 1 - Crear una cadena de Bloques

#Para instalar:
# Flask==0.12.2: pip install Flask=0.12.2
#cliente HTTP Postman: https://www.getpostman.com/

#importar las librerias
import datetime #timestamp del blque
import hashlib #hashing
import json  #para crear ficheros json
from flask import Flask, jsonify #para crear objetos de la clase Flask y jsonify para devolver mensajes a postman


#Parte 1 - Crear la cadena de bloques
class Blockchain:   #nombre de la clase que estamos creando de cero
    
    #CONSTRUCTOR DE LA CLASE.inicializamos la Clase con el init - se construye una instancia del objeto.
    #el self hace referencia al propio objeto, variables 
    def __init__(self):                
        self.chain = [] #lista que contendrá todos los bloques
        self.create_block(proof = 1, previous_hash = '0') #llamada a la función para crear el primer bloque de la blockchain
        
    #self  para poder usar las variables del objeto
    #cuando llamamos a create block es poque ya tenemos el valor de proof
    def create_block(self, proof, previous_hash ):
        #variable local tipo diccionario que convertiremos en objeto JSON
        block = { 
                    'index' : len(self.chain)+1, #posición que ocupa el bloque en la cadena
                    'timestamp' : str(datetime.datetime.now()),
                    'proof' : proof,
                    'previous_hash' : previous_hash
                                        
            }
        self.chain.append(block)
        return block
    
    
    def get_previous_block(self): #con self ya tenemos toda la cadena y consultamos el ultimo bloque             
        return self.chain[-1] # devolvemos el ultimo bloque de la cadena
    
    # funcion proof of work - prueba de trabajo
    # es un número que los mineros deben encontrar para añadir el bloque a la cadena
    # definiremos un problema que será difícil de encontrar pero muy fácil de verificar
    # de este modo tiene valor la creación de bloques, de ese modo por ejemplo la criptomoneda no pierde su valor
    # dentro de la función resolveremos el problema y devolveremos el número correcto
    def proof_of_work (self, previous_proof): 
        new_proof = 1 # inicializo el valor de prueba
        check_proof = False #será True cuando encontremos la prueba
        #Cuantos mas 0 pidamos al inicio del Hash objetivo más complejo será resolver el poblema
        while check_proof is False:
            #debe ser una operación no simétrica, ponemos una sencilla   
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() ## ESTA ES LA PROOF OF WORK
            if hash_operation[:4]=='0000': # el hash es correcto, cumple la condicion
                check_proof = True
            else:          
                new_proof +=1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(encoded_block).hexdigest()
    
    #Comprobamos la cadena de bloques
    #por un lado el hash anterior en cada bloque
    #cada bloque su proof of work sea correcto    
    def is_chain_valid (self, chain): 
        previous_block = chain[0]
        block_index = 1
         #RECORREMOS TODOS LOS BLOQUES
        while block_index < len(chain):
            block = chain[block_index] #comprobamos que el campo hash previo coincide con el anterior
            
            #ALARMA LA CADENA NO ES VALIDA
            if block['previous_hash'] != self.hash(previous_block) :  
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()      
            #HASH NO CORRECTO comprobamos el HASH de cada BLOQUE
            if hash_operation[:4] != '0000' : 
                return False
            previous_block = block
            block_index += 1            
        return True
     
     
     
#Parte 2 - Minado de un bloque de la cadena

#NO NECESITA ARGUMENTOS, LA FUNCION UNICAMENTE MINARÁ UN NUEVO BLOQUE
def mine_block(): 
    previous_block = blockchain.get_previous_block() #obtenemos el ultimo bloque de la cadena
    previous_proof = previous_block['proof']  # proof del bloque previo 
    proof = blockchain.proof_of_work(previous_proof) #proof actual
    previous_hash = blockchain.hash(previous_block)  # hash previo
    block = blockchain.create_block(proof, previous_hash) #creamos el bloque nuevo
    response = {'message':'¡Enhorabuena, has minado un nuevo Bloque!',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']
                }
    return jsonify(response),200
   


#CREAMOS UNA APLICACION WEB  - usaremos FLASK
app = Flask(__name__)
#si se obtiene un error 500 actualizar Flask reiniciar spydier y ejecutar la linea de abajo
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False 



#MINAR UN NUEVO BLOQUE

@app.route('/mine_block', methods=['GET']) #lanzamos en FLASK la aplicación mine_block

           
#OBTENER LA CADENA DE BLOQUES AL COMPLETO y su longitud

def get_chain():
    response = {'chain', blockchain.chain,
                'length', len(blockchain.chain)                
                }
    return jsonify(response),200



#CREAMOS UN OBJETO DE LA CLASE BLOCKCHAIN - UNA CADENA DE BLOQUES
blockchain = Blockchain() 
    
#EJECUTAR LA APP
#app.run()
app.run(host = '0.0.0.0', port = 5000, debug=False)














    



















