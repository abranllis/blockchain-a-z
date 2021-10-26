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
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() 
            if hash_operation[:4]=='0000': # el hash es correcto, cumple la condicion
                check_proof = True
            else:          
                new_proof +=1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(encoded_block).hexdigest()
    
    # debemos validar que el hash previo de todos los bloques es correcto y el hash tb
    #validamos toda la cadena de bloques
    def is_chain_valid (self, chain): 
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            
        
        
        

                
                
                       
            
               
               
#Parte 2 - Minado de un bloque de la cadena
