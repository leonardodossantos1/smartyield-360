import yfinance as yf
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- CONFIGURAÇÕES DE MERCADO 2026 ---
SELIC = 0.1225 
CDI = SELIC - 0.0010 

def analisar_tudo_v4(valor_aporte):
    # 1. CATEGORIA: RENDA FIXA
    rf_data = [
        {"Ativo": "CDB 100%", "Onde": "Digital", "Taxa": 1.0, "Index": "CDI", "Isento": False},
        {"Ativo": "LCI Imobiliário", "Onde": "Corretora", "Taxa": 0.90, "Index": "CDI", "Isento": True},
        {"Ativo": "LCA Agro", "Onde": "Banco", "Taxa": 0.88, "Index": "CDI", "Isento": True}
    ]
    
    rf_list = []
    for i in rf_data:
        t_anual = (i['Taxa'] * CDI)
        mensal_liq = ((valor_aporte * t_anual) / 12) * (1 if i['Isento'] else 0.825)
        taxa_mensal = (1 + t_anual)**(1/12) - 1
        acumulado = 0
        for _ in range(12):
            acumulado = (acumulado + valor_aporte) * (1 + taxa_mensal)
        
        rf_list.append({
            "Ativo": i['Ativo'], "Onde": i['Onde'], "Mensal Líq.": round(mensal_liq, 2),
            "Evolução 1 Ano": round(acumulado, 2), "Score": 9, "Categoria": "Renda Fixa"
        })

    # 2. CATEGORIA: AÇÕES (COM PREÇOS DE SEGURANÇA CONTRA ERRO 429)
    tickers = ["BBSE3", "ITSA4", "TAEE11", "ITUB4", "EGIE3", "PETR4", "VALE3", "EMBR3"]
    acoes_list = []
    
    # Preços de referência (Caso o Yahoo bloqueie o servidor do Streamlit)
    precos_ref = {
        "BBSE3": 35.20, "ITSA4": 10.85, "TAEE11": 36.10, "ITUB4": 34.50, 
        "EGIE3": 41.80, "PETR4": 38.20, "VALE3": 66.50, "EMBR3": 52.10
    }
    
    # Dividend Yield Médio Estimado (Para evitar múltiplas consultas e novos bloqueios)
    yields_ref = {
        "BBSE3": 0.10, "ITSA4": 0.08, "TAEE11": 0.09, "ITUB4": 0.06, 
        "EGIE3": 0.07, "PETR4": 0.12, "VALE3": 0.07, "EMBR3": 0.02
    }

    for t in tickers:
        try:
            t_sa = f"{t}.SA"
            # Tentativa de pegar preço atual
            try:
                # O history é mais leve que o download e evita o erro 429
                hist = yf.Ticker(t_sa).history(period="1d")
                p = hist['Close'].iloc[-1] if not hist.empty else precos_ref[t]
            except:
                p = precos_ref[t]

            # Filtro de aporte (Se o dinheiro não compra 1 ação, ele pula)
            if not p or valor_aporte < p: continue

            # Cálculo de Dividendos e Preço Teto
            dy = yields_ref.get(t, 0.06)
            media_div = p * dy
            preco_teto = media_div / 0.06
            margem = ((preco_teto / p) - 1) * 100
            
            qtd_acoes = int(valor_aporte // p)
            renda_mensal = (qtd_acoes * (media_div / 12))

            acoes_list.append({
                "Ativo": t, 
                "Onde": "B3", 
                "Mensal Líq.": round(renda_mensal, 2),
                "Margem": f"{margem:.1f}%", 
                "Status": "🔥 OPORTUNIDADE" if margem > 10 else "SAUDÁVEL", 
                "Evolução 1 Ano": round((valor_aporte * 12) * 1.08, 2),
                "Score": 10 if margem > 10 else 7, 
                "Categoria": "Ações"
            })
        except:
            continue

    return pd.DataFrame(rf_list), pd.DataFrame(acoes_list)
