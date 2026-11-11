import pandas as pd
import requests
from src.config import BEST_SECTORS, BRAPI_URL

def obter_lista_besst():
    response = requests.get(BRAPI_URL)
    
    if response.status_code != 200:
        return pd.DataFrame(), {}
    
    dados = response.json()
    df_mercado = pd.DataFrame(dados['stocks'])
    
    # Utiliza a lista de setores importadas do config.py
    df_besst = df_mercado[df_mercado['sector'].isin(BEST_SECTORS)]
    
    # Criando dicionário de nomes para mapear futuramente
    dict_nomes = dict(zip(df_besst['stock'], df_besst['name']))
    
    # Tratamento dos tickers
    tickers_tratados = []
    
    for t in df_besst['stock'].tolist():
        
        if t.endswith("F") and len(t):
            t = t[:-1]
            
        t_sa = t + ".SA"
        
        if t_sa not in tickers_tratados:
            tickers_tratados.append(t_sa)
    
    return tickers_tratados, dict_nomes
        
        
    