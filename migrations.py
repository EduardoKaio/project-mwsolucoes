import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

USER = "admin"
PASSWORD = "mwsolucoesDB"
HOST = "localhost"
PORT = "8812"
DATABASE = "qdb"

def create_table_if_not_exists(engine):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS clientes (
            statusCliente BOOLEAN,
            ipConcentrador SYMBOL,
            nomeConcentrador SYMBOL,
            conexaoCliente SYMBOL,
            latitudeCliente STRING,
            longitudeCliente STRING,
            conexaoInicial TIMESTAMP,
            conexaoFinal TIMESTAMP,
            tempoConectado LONG,
            consumoDownload LONG,
            consumoUpload LONG,
            motivoDesconexao SYMBOL,
            popCliente SYMBOL,
            nomeCliente SYMBOL,
            enderecoCliente SYMBOL,
            bairroCliente SYMBOL,
            cidadeCliente SYMBOL,
            contratoStatus LONG,
            planoContrato SYMBOL,
            statusInternet LONG,
            downloadCliente LONG,
            uploadCliente LONG,
            valorPlano FLOAT,
            timestamp TIMESTAMP
        );
    """
    
    with engine.connect() as connection:
        connection.execute(text(create_table_query))
        st.success("Tabela 'clientes' criada com sucesso ou já existe.")

def insert_data_to_questdb(df):
    try:
        engine = create_engine(f"postgresql://{USER}:{PASSWORD}@questdb:{PORT}/{DATABASE}")

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            st.success("Conexão estabelecida com sucesso ao QuestDB!")

            create_table_if_not_exists(engine)

            Session = sessionmaker(bind=engine)
            session = Session()

            count_query = text("SELECT COUNT(*) FROM clientes")
            result = session.execute(count_query)
            total_records = result.scalar()

            if total_records > 0:
                st.warning("Dados já existem na tabela 'clientes'. Nenhuma nova inserção será realizada.")
                return
            try:
                for _, row in df.iterrows():
                    values = {
                        'statusCliente': bool(row['statusCliente']),
                        'ipConcentrador': row['ipConcentrador'],
                        'nomeConcentrador': row['nomeConcentrador'],
                        'conexaoCliente': str(row['conexaoCliente']),
                        'latitudeCliente': str(row['latitudeCliente']) if pd.notnull(row['latitudeCliente']) else None,
                        'longitudeCliente': str(row['longitudeCliente']) if pd.notnull(row['longitudeCliente']) else None,
                        'conexaoInicial': row['conexaoInicial'].isoformat() if pd.notnull(row['conexaoInicial']) else None,
                        'conexaoFinal': row['conexaoFinal'].isoformat() if pd.notnull(row['conexaoFinal']) else None,
                        'tempoConectado': row['tempoConectado'],
                        'consumoDownload': row['consumoDownload'],
                        'consumoUpload': row['consumoUpload'],
                        'motivoDesconexao': row['motivoDesconexao'] if pd.notnull(row['motivoDesconexao']) else None,
                        'popCliente': row['popCliente'] if pd.notnull(row['popCliente']) else None,
                        'nomeCliente': row['nomeCliente'],
                        'enderecoCliente': row['enderecoCliente'],
                        'bairroCliente': row['bairroCliente'],
                        'cidadeCliente': row['cidadeCliente'],
                        'contratoStatus': row['contratoStatus'],
                        'planoContrato': row['planoContrato'],
                        'statusInternet': row['statusInternet'],
                        'downloadCliente': row['downloadCliente'],
                        'uploadCliente': row['uploadCliente'],
                        'valorPlano': float(str(row['valorPlano']).replace('.', '').replace(',', '.')) if pd.notnull(row['valorPlano']) else None,
                        'timestamp': row['timestamp'].isoformat() if pd.notnull(row['timestamp']) else None
                    }

                    session.execute(text("""
                        INSERT INTO clientes (
                            statusCliente, ipConcentrador, nomeConcentrador, conexaoCliente,
                            latitudeCliente, longitudeCliente, conexaoInicial, conexaoFinal,
                            tempoConectado, consumoDownload, consumoUpload, motivoDesconexao,
                            popCliente, nomeCliente, enderecoCliente, bairroCliente,
                            cidadeCliente, contratoStatus, planoContrato, statusInternet,
                            downloadCliente, uploadCliente, valorPlano, timestamp
                        ) VALUES (
                            :statusCliente, :ipConcentrador, :nomeConcentrador, :conexaoCliente,
                            :latitudeCliente, :longitudeCliente, :conexaoInicial, :conexaoFinal,
                            :tempoConectado, :consumoDownload, :consumoUpload, :motivoDesconexao,
                            :popCliente, :nomeCliente, :enderecoCliente, :bairroCliente,
                            :cidadeCliente, :contratoStatus, :planoContrato, :statusInternet,
                            :downloadCliente, :uploadCliente, :valorPlano, :timestamp
                        )
                    """), values)

                session.commit()

                count_query = text("SELECT COUNT(*) FROM clientes")
                result = session.execute(count_query)
                total_records = result.scalar()

                st.success(f"Dados inseridos com sucesso no QuestDB! Total de registros na tabela: {total_records}")

            except Exception as e:
                session.rollback()  
                st.error(f"Erro ao inserir dados: {e}")

            finally:
                session.close()  

    except Exception as e:
        st.error(f"Erro ao conectar ao QuestDB: {e}")

st.title("Painel de Upload de Dados para QuestDB")

csv_file_path = "./questdb.csv"

df = pd.read_csv(csv_file_path)

df['conexaoInicial'] = pd.to_datetime(df['conexaoInicial'], errors='coerce')
df['conexaoFinal'] = pd.to_datetime(df['conexaoFinal'], errors='coerce')
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

st.write("Pré-visualização dos dados:")
st.dataframe(df.head())

insert_data_to_questdb(df)
