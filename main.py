import yfinance as yf
import pandas as pd
from datetime import datetime, timezone, timedelta

# CONFIGURAÇÕES DE MERCADO 2026
SELIC = 0.1225 
CDI = SELIC - 0.0010 

def analisar_tudo_v4(valor_aporte):
    # 1. RENDA FIXA
    rf_data = [
        {"Ativo": "CDB 100%", "Onde": "Digital", "Taxa": 1.0, "Index": "CDI", "Isento": False},
        {"Ativo": "LCI Imobiliário", "Onde": "Corretora", "Taxa": 0.90, "Index": "CDI", "Isento": True}
    ]
    
    rf_list = []
    for i in rf_data:
        t_anual = (i['Taxa'] * CDI)
        mensal_liq = ((valor_aporte * t_anual) / 12) * (1 if i['Isento'] else 0.825)
        taxa_mensal = (1 + t_anual)**(1/12) - 1
        acumulado = 0
        for _ in range(12): acumulado = (acumulado + valor_aporte) * (1 + taxa_mensal)
        
        rf_list.append({
            "Ativo": i['Ativo'], "Onde": i['Onde'], "Mensal Líq.": round(mensal_liq, 2),
            "Evolução 1 Ano": round(acumulado, 2), "Score": 9, "Categoria": "Renda Fixa"
        })

    # 2. AÇÕES (BUSCA ROBUSTA)
    tickers = ["BBSE3", "ITSA4", "TAEE11", "ITUB4", "EGIE3", "PETR4", "VALE3", "EMBR3"]
    acoes_list = []
    
    try:
        # Download em lote para evitar erro de conexão no Streamlit
        dados = yf.download([f"{t}.SA" for t in tickers], period="5d", interval="1d", progress=False)
        precos_atuais = dados['Close'].iloc[-1]
    except:
        precos_atuais = pd.Series()

    for t in tickers:
        try:
            t_sa = f"{t}.SA"
            p = precos_atuais[t_sa] if t_sa in precos_atuais else None
            
            if p is None or pd.isna(p):
                p = yf.Ticker(t_sa).info.get('currentPrice')

            if not p or p <= 0 or valor_aporte < p: continue

            acao = yf.Ticker(t_sa)
            divs = acao.dividends
            
            media_5y = 0
            if not divs.empty:
                cinco_anos = datetime.now(timezone.utc) - timedelta(days=1825)
                media_5y = divs[divs.index > cinco_anos].sum() / 5

            preco_teto = media_5y / 0.06 if media_5y > 0 else 0
            margem = ((preco_teto / p) - 1) * 100 if preco_teto > 0 else 0
            
            qtd = int(valor_aporte // p)
            renda = (qtd * (media_5y / 12)) if media_5y > 0 else 0

            acoes_list.append({
                "Ativo": t, "Onde": "B3", "Mensal Líq.": round(renda, 2),
                "Margem": f"{margem:.1f}%", "Status": "🔥 OPORTUNIDADE" if margem > 15 else "SAUDÁVEL",
                "Evolução 1 Ano": round((valor_aporte * 12) * 1.08, 2),
                "Score": 10 if margem > 15 else 7, "Categoria": "Ações"
            })
        except: continue

    return pd.DataFrame(rf_list), pd.DataFrame(acoes_list)
