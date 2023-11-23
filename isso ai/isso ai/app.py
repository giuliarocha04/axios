from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

try:
    with open('index.js', 'x') as arquivo:
        arquivo.write("ID,TAREFA\n")
except FileExistsError:
    pass

def carregar_tarefas():
    return pd.read_json('index.json')

def salvar_tarefas(tarefas):
    tarefas.to_json('index.json', index=False)

@app.route("/list", methods=['GET'])
def listarTarefas():
    tarefas = carregar_tarefas().to_dict('records')
    return jsonify(tarefas)

@app.route("/add", methods=['POST'])
def addTarefas():
    item = request.json
    tarefas = carregar_tarefas()
    id = tarefas['ID'].max() + 1 if not tarefas.empty else 1
    tarefas = tarefas.append({'ID': id, 'TAREFA': item['Tarefa']}, ignore_index=True)
    salvar_tarefas(tarefas)
    return jsonify(tarefas.to_dict('records'))

@app.route("/delete", methods=['DELETE'])
def deleteTarefa():
    data = request.json
    id = data.get('id')

    if id is None:
        return jsonify({"error": "ID da tarefa não fornecido"}), 400

    tarefas = carregar_tarefas()

    if id not in tarefas['ID'].values:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    tarefas = tarefas[tarefas['ID'] != id]
    salvar_tarefas(tarefas.reset_index(drop=True))
    return jsonify(tarefas.to_dict('records'))

@app.route("/update", methods=["PUT"])
def update_task():
    data = request.json
    id = data.get('id')
    nova_tarefa = data.get('nova_tarefa')

    if id is None or nova_tarefa is None:
        return jsonify({"error": "ID da tarefa e/ou nova tarefa não fornecidos"}), 400

    tarefas = carregar_tarefas()

    if id not in tarefas['ID'].values:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    tarefas.loc[tarefas['ID'] == id, 'TAREFA'] = nova_tarefa
    salvar_tarefas(tarefas)
    return jsonify(tarefas.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
