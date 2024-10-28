import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Configurações de conexão com o QuestDB
USER = "admin"
PASSWORD = "mwsolucoesDB"
HOST = "localhost"
PORT = "8812"
DATABASE = "qdb"

# Função para conectar ao QuestDB
def get_connection():
    engine = create_engine(f"postgresql://{USER}:{PASSWORD}@questdb:{PORT}/{DATABASE}")
    return engine

# Função para ler uma consulta SQL de um arquivo
def read_query_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Função para executar uma consulta SQL e retornar o DataFrame
def execute_query(query):
    with get_connection().connect() as connection:
        result = connection.execute(text(query))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

# Função para formatar números com ponto como separador de milhar
def format_number(value):
    if pd.notnull(value):  # Verifica se o valor não é nulo
        return f"{value:,.0f}".replace(",", ".")  # Formata e substitui vírgulas por pontos
    return value  # Retorna o valor original se for nulo

# Interface Streamlit
st.title("Visualização de Dados")

# Selecionar a consulta a ser executada
query_options = {
    "Contagem de Clientes Online e Offline": "consultas_sql/contagem_clientes_online_offline.sql",
    "Contagem de Clientes por Plano": "consultas_sql/contagem_clientes_por_plano.sql",
    "Métricas Financeiras": "consultas_sql/metricas_financeiras.sql",
    "Informações de Consumo": "consultas_sql/informacoes_consumo_dados.sql",
    "Informações de Conectividade": "consultas_sql/informacoes_conectividade.sql",
    "Contagem de Clientes por bairro": "consultas_sql/contagem_clientes_bairro.sql",
    "Consumo Médio de Dados por Cliente": "consultas_sql/consumo_medio_dados_cliente.sql",
    "Razão de Desconexão": "consultas_sql/razao_desconexao.sql",
}

selected_query = st.selectbox("Selecione uma consulta SQL:", list(query_options.keys()))

# Executar a consulta ao selecionar
if st.button("Executar Consulta"):
    query_file_path = query_options[selected_query]
    query = read_query_from_file(query_file_path)
    
    try:
        data = execute_query(query)
        
        # Formatar os valores financeiros ou qualquer valor desejado
        for col in data.columns:
            if data[col].dtype in ['int64', 'float64']:  # Verifica se a coluna é numérica
                data[col] = data[col].apply(format_number)  # Aplica a formatação
        
        st.write(data)
        st.success("Consulta executada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao executar a consulta: {e}")