from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)

CORS(app)

#app.config["MONGO_URI"] = "mongodb://localhost:27017/aulaCrudMongo"
app.config["MONGO_URI"] = "mongodb+srv://maylon:131995@cluster0.4mptx.mongodb.net/aulaCrudMongo"


mongo = PyMongo(app)

# CREATE
@app.route('/produtos', methods=['POST'])
def criar_produto():

    dados = request.json

    produto = {
        "nome": dados["nome"],
        "preco": dados["preco"]
    }

    resultado = mongo.db.produtos.insert_one(produto)

    produto["_id"] = str(resultado.inserted_id)

    return jsonify(produto)

# READ
@app.route('/produtos', methods=['GET'])
def listar_produtos():

    produtos = []

    for produto in mongo.db.produtos.find():

        produtos.append({
            "_id": str(produto["_id"]),
            "nome": produto["nome"],
            "preco": produto["preco"]
        })

    return jsonify(produtos)

# UPDATE
@app.route('/produtos/<id>', methods=['PUT'])
def atualizar_produto(id):

    dados = request.json

    mongo.db.produtos.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "nome": dados["nome"],
                "preco": dados["preco"]
            }
        }
    )

    return jsonify({"msg": "Atualizado"})

# DELETE
@app.route('/produtos/<id>', methods=['DELETE'])
def deletar_produto(id):

    mongo.db.produtos.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({"msg": "Deletado"})

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=3000,
        debug=True
    )
    
    
    
    
    
    #pip install --no-index --find-links=dependencias -r requirements.txt
    #ou
    #pip install --no-index --find-links=dependencias flask pymongo flask-pymongo