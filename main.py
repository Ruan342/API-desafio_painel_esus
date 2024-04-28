#importação das bibliotecas
from flask import Flask, request, jsonify
#pandas para tratar os dados
import pandas as pd
#json para retornar os dados
import json
#datetime para converter os formatos em algumas datas 
from datetime import datetime


app = Flask(__name__)

# Função para extrair a parte da data do formato 'YYYY-MM-DD HH:MM:SS'
def extrair_data(data_com_hora):
    return data_com_hora.split()[0]

# Função para converter data para o formato desejado
def converter_data(data):
    try:
        return datetime.strptime(data, '%d %B, %Y').strftime('%Y-%m-%d')
    except ValueError:
        return data

# Rota para filtrar dados
@app.route('/api/v1/atendimentos', methods=['GET'])
def filtrar_dados():
    filtros = request.args
    #filtragem realizada pela biblioteca pandas
    df = pd.read_csv('atendimentos.csv')
    for chave, valor in filtros.items():
        df = df[df[chave] == valor]
    df['data_atendimento'] = df['data_atendimento'].apply(extrair_data)
    df['data_atendimento'] = df['data_atendimento'].apply(converter_data)
    for chave, valor in filtros.items():
        df = df[df[chave] == valor]

    # Conversão para JSON
    dados_json = json.dumps(df.to_dict(orient='records'), ensure_ascii=False, indent=4)
    return dados_json, 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='localhost', port=8001, debug=True)
