# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
# import das variaveis de amviente

#petroleo, ouro e prata
commodities = ['CL=F', 'GC=F', 'SI=F']

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def buscar_dados_commodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)

    #Retorna um Dataframe eu só quero a coluna "close"
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo

    return dados

def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        todos_dados.append(buscar_dados_commodities(simbolo))
    
    return pd.concat(todos_dados)

def salvar_no_postgres(df, schema='public'):
    df.to_sql(
        'commodities', 
        engine, 
        if_exists='replace', 
        index=True, 
        index_label='Date', 
        schema=schema
    )

if __name__ == "__main__":
    print("BATATA >>>>>>>>>>>>>>>>")

    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados, schema='public')

# pegar cotação dos meus ativos

# concatenar os meus ativos (1.2.3) -> (1)

# salvar nos bancos de dados

