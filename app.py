from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)

CORS(app)

# =========================================================
# CONFIGURAÇÃO DO MONGODB
# =========================================================

# MongoDB local
# app.config["MONGO_URI"] = "mongodb://localhost:27017/aulaCrudMongo"

# MongoDB Atlas
app.config["MONGO_URI"] = "mongodb+srv://maylon:131995@cluster0.4mptx.mongodb.net/aulaCrudMongo"

mongo = PyMongo(app)


# =========================================================
# PRODUTOS
# =========================================================

# CREATE - Criar produto
@app.route('/produtos', methods=['POST'])
def criar_produto():

    dados = request.json

    produto = {
        "nome": dados["nome"],
        "preco": dados["preco"]
    }

    resultado = mongo.db.produtos.insert_one(produto)

    produto["_id"] = str(resultado.inserted_id)

    return jsonify(produto), 201


# READ - Listar produtos
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


# UPDATE - Atualizar produto
@app.route('/produtos/<id>', methods=['PUT'])
def atualizar_produto(id):

    dados = request.json

    resultado = mongo.db.produtos.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": {
                "nome": dados["nome"],
                "preco": dados["preco"]
            }
        }
    )

    if resultado.matched_count == 0:
        return jsonify({
            "msg": "Produto não encontrado"
        }), 404

    return jsonify({
        "msg": "Produto atualizado"
    })


# DELETE - Deletar produto
@app.route('/produtos/<id>', methods=['DELETE'])
def deletar_produto(id):

    resultado = mongo.db.produtos.delete_one({
        "_id": ObjectId(id)
    })

    if resultado.deleted_count == 0:
        return jsonify({
            "msg": "Produto não encontrado"
        }), 404

    return jsonify({
        "msg": "Produto deletado"
    })


# =========================================================
# TAREFAS
# =========================================================

# CREATE - Criar tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():

    dados = request.json

    tarefa = {
        "titulo": dados["titulo"],
        "descricao": dados["descricao"],
        "prioridade": dados.get("prioridade", "media"),
        "concluida": dados.get("concluida", False)
    }

    resultado = mongo.db.tarefas.insert_one(tarefa)

    tarefa["_id"] = str(resultado.inserted_id)

    return jsonify(tarefa), 201


# READ - Listar todas as tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():

    tarefas = []

    for tarefa in mongo.db.tarefas.find():

        tarefas.append({
            "_id": str(tarefa["_id"]),
            "titulo": tarefa["titulo"],
            "descricao": tarefa["descricao"],
            "prioridade": tarefa.get("prioridade", "media"),
            "concluida": tarefa.get("concluida", False)
        })

    return jsonify(tarefas)


# READ - Buscar uma tarefa pelo ID
@app.route('/tarefas/<id>', methods=['GET'])
def buscar_tarefa(id):

    tarefa = mongo.db.tarefas.find_one({
        "_id": ObjectId(id)
    })

    if not tarefa:
        return jsonify({
            "msg": "Tarefa não encontrada"
        }), 404

    return jsonify({
        "_id": str(tarefa["_id"]),
        "titulo": tarefa["titulo"],
        "descricao": tarefa["descricao"],
        "prioridade": tarefa.get("prioridade", "media"),
        "concluida": tarefa.get("concluida", False)
    })


# UPDATE - Atualizar tarefa
@app.route('/tarefas/<id>', methods=['PUT'])
def atualizar_tarefa(id):

    dados = request.json

    resultado = mongo.db.tarefas.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": {
                "titulo": dados["titulo"],
                "descricao": dados["descricao"],
                "prioridade": dados["prioridade"],
                "concluida": dados["concluida"]
            }
        }
    )

    if resultado.matched_count == 0:
        return jsonify({
            "msg": "Tarefa não encontrada"
        }), 404

    return jsonify({
        "msg": "Tarefa atualizada"
    })


# DELETE - Deletar tarefa
@app.route('/tarefas/<id>', methods=['DELETE'])
def deletar_tarefa(id):

    resultado = mongo.db.tarefas.delete_one({
        "_id": ObjectId(id)
    })

    if resultado.deleted_count == 0:
        return jsonify({
            "msg": "Tarefa não encontrada"
        }), 404

    return jsonify({
        "msg": "Tarefa deletada"
    })


# =========================================================
# INICIAR API
# =========================================================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=3000,
        debug=True
    )


# =========================================================
# INSTALAÇÃO DAS DEPENDÊNCIAS
# =========================================================

# Instalação normal:
#
# pip install flask pymongo flask-pymongo flask-cors
#
#
# Instalação usando a pasta dependencias:
#
# pip install --no-index --find-links=dependencias -r requirements.txt
#
# ou:
#
# pip install --no-index --find-links=dependencias flask pymongo flask-pymongo flask-cors