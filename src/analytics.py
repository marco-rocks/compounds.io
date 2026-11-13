import gc
import pandas as pd
import yfinance as yf
from datetime import datetime
from src.scraper import obter_lista_besst

"""
    Executando a varreadura completa nas ações
    dos setores BESST
    
    Regras de filtragem:
    1. Lucros positivos nos últimos 10 anos
    2. Dividend Yield histórico dos últimos anos
    deve ter uma taxa maior que 6%
"""
current_year = datetime.now().year

def _verificar_lucros_consistentes(stock):
    try:
        dre = stock.income_stmt
        
        if dre.empty or "Net Income" not in dre.index:
            return False
        
        lucros_serie = dre.loc["Net Income"].dropna()
        lucros_serie.index = pd.to_datetime(lucros_serie.index)
        
        limite_ano = current_year - 10
        lucros_filtrados = lucros_serie[lucros_serie.index.year >= limite_ano]
        
        if lucros_filtrados.empty:
            return False
        
        return bool((lucros_filtrados > 0).all())
    
    except Exception:
        return False

def _calcular_media_dividendos(stock):
    try:
        dividendos = stock.dividends
        
        if dividendos.empty:
            return 0.0
        
        dividendos.index = pd.to_datetime(dividendos.index)
        dividendos_filtrados = dividendos[dividendos.index.year >= current_year - 5]
        
        if dividendos_filtrados.empty:
            return 0.0
        
        media_anual = dividendos_filtrados.resample("YE").sum().mean()
        
        return float(media_anual)
    
    except Exception:
        return 0.0

def _obter_preco_atual(stock):

    """
    Buscando preço de fechamento mais recente da ação
    """
    
    try:     
        hist = stock.history(period='5d')
        
        if hist.empty:
            return 0.0
        
        return float(hist['Close'].iloc[-1])
    except Exception:
        return 0.0
    
def processar_analise_besst(limite_testes = None):
    """
    Estrutura de varredura completa nas ações dos
    setores BESST, aplicando as regras de lucros
    consistentes e indicador de retorno mínimo (Otimizada para RAM)
    """
    
    tickers, dict_nomes = obter_lista_besst()
    
    if not tickers:
        return pd.DataFrame()
    
    resultados = []
    
    if limite_testes:
        tickers = tickers[:limite_testes]
    
    for t in tickers: 
        print(f"Analisando {t}...")
        stock = None
        try:
            stock = yf.Ticker(t)
            
            # 1. Valida regra de lucros (10 anos)
            if not _verificar_lucros_consistentes(stock):
                continue
            
            # 2. Calculo da média de dividendos (5 anos)
            media_dividendos = _calcular_media_dividendos(stock)
            
            if media_dividendos <= 0:
                continue
            
            preco_fechamento = _obter_preco_atual(stock)
            
            if preco_fechamento <= 0:
                continue
            
            # 4. Calcula o indicador de retorno aplicando o filtro de (>= 6%)
            taxa_retorno = (media_dividendos / preco_fechamento) * 100
            
            if taxa_retorno < 6.0:
                continue
            
            ticker_limpo = t.replace('.SA', "")
            
            nome_empresa = dict_nomes.get(
                ticker_limpo, dict_nomes.get(ticker_limpo + "F", "Desconhecido")
            )
        
            resultados.append({
                "Ticker": ticker_limpo,
                "Nome": nome_empresa,
                "Preço Atual (R$)": round(preco_fechamento, 2),
                "Média Div. (5 anos)": round(media_dividendos, 4),
                "Indicador (%)": round(taxa_retorno, 2),
            })
        
        except Exception as e:
            print(f"Erro ao processar {t}: {e}")
            continue
            
        finally:
            # Força o descarte do objeto da memória a cada ciclo do loop
            if stock is not None:
                del stock
            gc.collect()
        
    df_resultado = pd.DataFrame(resultados)
    
    if not df_resultado.empty:
        df_resultado = df_resultado.sort_values(
            by="Indicador (%)",
            ascending=False
        ).reset_index(drop=True)
        
    return df_resultado

def processar_ativo_individual(ticker_str):
    
    """
    Recebe um ticker bruto (ex: 'PETR4' ou 'PETR4.SA'),
    consulta o yfinance e retorna todos os indicadores fundamentalistas
    sob a ótica da metodologia, independentemente de passar ou não no filtro final.
    """
    
    try:
        
        t = ticker_str.strip().upper()
        
        if t.endswith("F") and len(t):
            t = t[:-1]
            
        t = t + ".SA"
        
        ticker_limpo = t.replace(".SA", "")
        stock = yf.Ticker(t)
        
        passou_lucro = _verificar_lucros_consistentes(stock)
        media_dividendos = _calcular_media_dividendos(stock)
        preco = _obter_preco_atual(stock)
        
        if preco <= 0:
            return {"erro": "O ativo solicitado não foi encontrado ou a cotação está indisponível"}
        
        taxa_retorno = (
            (media_dividendos/preco) * 100
            if media_dividendos > 0
            else 0
        )
        
        return{
            "Ticker": ticker_limpo,
            "Preço Atual (R$)": round(preco, 2),
            "Média Div. (5 anos)": round(media_dividendos, 4),
            "Indicador (%)": round(taxa_retorno, 2),
            "Criterio_Lucro_10anos": passou_lucro,
            "Criterio_Yield_Maior_6porcento": taxa_retorno >= 6.0,
            "Aprovado_Geral": (
                passou_lucro and media_dividendos > 0 and taxa_retorno >= 6.0
            ),
        }
    
    except Exception as e:
        return {"erro": str(e)}