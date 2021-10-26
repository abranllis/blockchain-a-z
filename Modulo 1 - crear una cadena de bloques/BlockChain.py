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
    
   


#Parte 2 - Minado de un bloque de la cadena

