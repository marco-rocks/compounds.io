# compounds.io

> *"O poder da consistência e dos juros composts aplicado à B3."*

O **compounds.io** é uma plataforma e API REST desenvolvida em Python para seleção automatizada de ações da B3.

Inspirado nos princípios clássicos de investimento de longo prazo (*Buy and Hold*), o projeto rastreia empresas pereneres pertecentes aos setores essenciais (**BESST**: Bancos, Energia, Saneamento, Seguros e Telecomunicações) que unem duas premissas fundamentais:

1. **Consistência de Resultados:** Histórico estrito de lucros líquidos positivos nos últimos 10 anos.
2. **Retorno Atrativo:** Indicador de retorno via dividendos (Yield médio dos últimos 5 anos sobre o preço atual) superior a 6%.


## Tecnologias Utilizadas
* **Python 3.10+**
* **Flask** (Framework para construção da API REST e endpoints JSON)
* **Pandas** (Manipulação, estruturação e ordenação de dados quantitativos)
* **yfinance** (Extração automatizada de cotações, dividendos e demonstrativos financeiros DRE)
* **Requests** (Consumo da API de listagem da B3)

## Estrutura do Projeto
```text
compounds-io/
│
├── data/
│   ├── raw/               # Dados brutos
│   └── processed/         # Relatórios e CSVs exportados
│
├── src/
│   ├── __init__.py        # Inicializador do pacote source
│   ├── config.py          # Configurações globais e mapeamento dos setores BESST
│   ├── scraper.py         # Coleta e tratamento de ativos da B3
│   └── analytics.py       # Regras de negócio, lucros (10 anos) e DY (5 anos)
│
├── .gitignore             # Arquivos ignorados pelo Git
├── requirements.txt       # Dependências do projeto
├── app.py                 # Servidor Flask e rotas da API
└── README.md              # Documentação oficial do projeto
```

## Executando o projeto localmente
### 1. Clonando o repositório
```
git clone https://github.com/marco-rocks/compunds.io.git
cd compunds.io
```
### 2. Criando e ativando um ambiente virtual
```
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
```
### 3. Instalando dependências
```
pip install -r requirements.txt
```
### 4. Executar a API Flask
```
python app.py
```
O servidor estará ativo em **http://127.0.0.1:5000**.

## ⚠️ Disclaimer

Este software possui caráter estritamente de pesquisa. Os dados gerados não constituem recomendação de investimento ou aconselhamento financeiro.