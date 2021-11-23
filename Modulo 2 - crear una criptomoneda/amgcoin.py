# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 12:36:48 2021

@author: abmartinez
"""

# Módulo 2 - Crear una criptomoneda

# Para Instalar:
# Flask==1.1.2: pip install Flask==1.1.2
# Cliente HTTP Postman: https://www.getpostman.com/
#requests==2.18.4: pip install requests==2.18.4    librería para hacer peticiones HTTP

# Importar las librerías
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


# Parte 1 - Crear la Cadena de Bloques
class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []        
        self.create_block(proof = 1, previous_hash = '0') #creamos el bloque GENESIS
        self.nodes = set()        #creamos un conjunto y no una lista ordenada, no tiene orden nodos de la cadena de bloques
        
        
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash': previous_hash,
                 'transactions' : self.transactions}
        self.transactions = [] #una vez minado borramos las transacciones
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else: 
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction (self, sender, receiver, amount ):
        self.transactions.append({'sender':sender, 'receiver': receiver, 'amount':amount})        
        previous_block = self.previous_block()
        return previous_block['index']+1
    
    def add_node(self, address):          #añadimos un nodo a la blockchain
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    #todos los nodos de la cadena llamaran a esta funcion y se reemplazaran si no son los mas largos
    def replace_chain(self, ): #revisamos que todos los nodos de la cadena esten correctos, el que no se reemplaza
         network = self.nodes
         longest_chain = None
         max_length = len(self.chain)
         for node in network : #recorremos los nodos de la red y mostramos la cadena
             response = requests.get(f'http://{node}/get_chain')
             if response.status == 200 :
                 length = response.json()['length']
                 chain = response.json()['chain']    
                 if length > max_length and self.is_chain_valid(chain):
                     max_length = length
                     longest_chain = chain
         if longest_chain:  #hay una cadena mas larga asi que actualizamos
            self.chain = longest_chain
            return True
         return False
    
    
        
            
                     
         
         
    
# Parte 2 - Minado de un Bloque de la Cadena

# Crear una aplicación web
app = Flask(__name__)
# Si se obtiene un error 500, actualizar flask, reiniciar spyder y ejecutar la siguiente línea
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Crear una Blockchain
blockchain = Blockchain()


# Minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : '¡Enhorabuena, has minado un nuevo bloque!', 
                'index': block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'HASH del BLOQUE previo' : block['previous_hash']}
    return jsonify(response), 200

# Obtener la cadena de bloques al completo
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain' : blockchain.chain, 
                'length' : len(blockchain.chain)}
    return jsonify(response), 200

# Comprobar si la cadena de bloques es válida
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'Todo correcto. La cadena de bloques es válida.'}
    else:
        response = {'message' : 'Houston, tenemos un problema. La cadena de bloques no es válida.'}
    return jsonify(response), 200  



#Parte 3 - Descentralizar la cadena de bloques



# Ejecutar la app
app.run(host = '0.0.0.0', port = 8080, debug = True)





