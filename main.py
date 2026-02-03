import yfinance as yf
import pandas as pd
from datetime import datetime, timezone, timedelta

# CONFIGURAÇÕES DE MERCADO 2026
SELIC = 0.1175
CDI = SELIC - 0.0010 

def analisar_tudo_v4(valor_aporte):
    # 1. CATEGORIA: RENDA FIXA
    rf_data = [
        {"Ativo": "CDB Emergência", "Onde": "Nubank / Inter", "Taxa": 1.0, "Index": "CDI", "Isento": False},
        {"Ativo": "LCI Imobiliário", "Onde": "BTG Pactual / XP", "Taxa": 0.90, "Index": "CDI", "Isento": True},
        {"Ativo": "LCA Agronegócio", "Onde": "Banco do Brasil / Itaú", "Taxa": 0.88, "Index": "CDI", "Isento": True}
    ]
    
    rf_list = []
    for i in rf_data:
        t_anual = (i['Taxa'] * CDI) if i['Index'] == "CDI" else i['Taxa']
        mensal_liq = ((valor_aporte * t_anual) / 12) * (1 if i['Isento'] else 0.825)
        
        taxa_mensal = (1 + t_anual)**(1/12) - 1
        acumulado_12m = 0
        for _ in range(12):
            acumulado_12m = (acumulado_12m + valor_aporte) * (1 + taxa_mensal)
        
        rf_list.append({
            "Ativo": i['Ativo'],
            "Onde": i['Onde'],
            "Mensal Líq.": round(mensal_liq, 2),
            "Evolução 1 Ano": round(acumulado_12m, 2),
            "Score": 9,
            "Categoria": "Renda Fixa"
        })

    # 2. CATEGORIA: AÇÕES
    tickers = ["BBSE3", "ITSA4", "TAEE11", "ITUB4", "EGIE3", "SANB11", "VIVT3", "CPLE3"]
    acoes_list = []
    
    for t in tickers:
        try:
            acao = yf.Ticker(f"{t}.SA")
            p = acao.info.get('currentPrice') or acao.info.get('previousClose')
            divs = acao.dividends
            if divs.empty or not p or (valor_aporte < p): continue
            
            cinco_anos = datetime.now(timezone.utc) - timedelta(days=1825)
            media_5y = divs[divs.index > cinco_anos].sum() / 5
            preco_teto = media_5y / 0.06
            margem = ((preco_teto / p) - 1) * 100
            
            qtd = int(valor_aporte // p)
            mensal_liq = (qtd * (media_5y / 12))
            evolucao_12m = (valor_aporte * 12) + (mensal_liq * 6.5)

            status = "🔥 OPORTUNIDADE OURO" if margem > 20 else "SAUDÁVEL"

            acoes_list.append({
                "Ativo": t,
                "Onde": "Corretora (B3)",
                "Mensal Líq.": round(mensal_liq, 2),
                "Margem": f"{margem:.1f}%",
                "Status": status,
                "Evolução 1 Ano": round(evolucao_12m, 2),
                "Score": 10 if margem > 20 else 7,
                "Categoria": "Ações"
            })
        except: continue

    return pd.DataFrame(rf_list), pd.DataFrame(acoes_list)