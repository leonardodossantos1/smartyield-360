import yfinance as yf
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- CONFIGURAÇÕES DE MERCADO 2026 ---
SELIC = 0.1225  # Taxa Selic 12.25%
CDI = SELIC - 0.0010 

def analisar_tudo_v4(valor_aporte):
    # 1. CATEGORIA: RENDA FIXA (Cálculos matemáticos internos - não falha)
    rf_data = [
        {"Ativo": "CDB 100%", "Onde": "Digital", "Taxa": 1.0, "Index": "CDI", "Isento": False},
        {"Ativo": "LCI Imobiliário", "Onde": "Corretora", "Taxa": 0.90, "Index": "CDI", "Isento": True},
        {"Ativo": "LCA Agro", "Onde": "Banco", "Taxa": 0.88, "Index": "CDI", "Isento": True}
    ]
    
    rf_list = []
    for i in rf_data:
        t_anual = (i['Taxa'] * CDI)
        mensal_liq = ((valor_aporte * t_anual) / 12) * (1 if i['Isento'] else 0.825)
        
        # Projeção 1 ano (Aportes mensais + Juros Compostos)
        taxa_mensal = (1 + t_anual)**(1/12) - 1
        acumulado = 0
        for _ in range(12):
            acumulado = (acumulado + valor_aporte) * (1 + taxa_mensal)
        
        rf_list.append({
            "Ativo": i['Ativo'], "Onde": i['Onde'], "Mensal Líq.": round(mensal_liq, 2),
            "Evolução 1 Ano": round(acumulado, 2), "Score": 9, "Categoria": "Renda Fixa"
        })

    # 2. CATEGORIA: AÇÕES (LISTA: BBSE3, ITSA4, TAEE11, ITUB4, EGIE3, PETR4, VALE3, EMBR3)
    tickers = ["BBSE3", "ITSA4", "TAEE11", "ITUB4", "EGIE3", "PETR4", "VALE3", "EMBR3"]
    acoes_list = []
    
    # Preços reserva caso o Yahoo Finance bloqueie o servidor (Valores aprox. 2026)
    precos_reserva = {
        "BBSE3": 35.0, "ITSA4": 11.0, "TAEE11": 36.0, "ITUB4": 34.0, 
        "EGIE3": 42.0, "PETR4": 38.0, "VALE3": 65.0, "EMBR3": 50.0
    }

    # Tenta baixar preços em lote (mais rápido e seguro)
    try:
        dados = yf.download([f"{t}.SA" for t in tickers], period="5d", interval="1d", progress=False)
        precos_atuais = dados['Close'].iloc[-1]
    except:
        precos_atuais = pd.Series()

    for t in tickers:
        try:
            t_sa = f"{t}.SA"
            # Prioridade 1: Preço ao vivo da B3
            p = precos_atuais[t_sa] if t_sa in precos_atuais else None
            
            # Prioridade 2: Busca individual
            if p is None or pd.isna(p):
                tk = yf.Ticker(t_sa)
                p = tk.fast_info.get('last_price') or tk.info.get('currentPrice')
            
            # Prioridade 3: Preço reserva (Evita erro de "Aporte Baixo")
            if p is None or pd.isna(p):
                p = precos_reserva.get(t)

            # Filtro de Aporte
            if not p or valor_aporte < p: continue

            # Busca Dividendos para cálculo de Preço Teto
            acao = yf.Ticker(t_sa)
            divs = acao.dividends
            
            if not divs.empty:
                # Média de dividendos dos últimos 5 anos
                cinco_anos = datetime.now(timezone.utc) - timedelta(days=1825)
                media_5y = divs[divs.index > cinco_anos].sum() / 5
            else:
                # Se não houver histórico, estimamos 6% do preço atual
                media_5y = p * 0.06

            preco_teto = media_5y / 0.06
            margem = ((preco_teto / p) - 1) * 100
            
            qtd_acoes = int(valor_aporte // p)
            rendimento_mensal = (qtd_acoes * (media_5y / 12))

            acoes_list.append({
                "Ativo": t, 
                "Onde": "Corretora (B3)", 
                "Mensal Líq.": round(rendimento_mensal, 2),
                "Margem": f"{margem:.1f}%", 
                "Status": "🔥 OPORTUNIDADE" if margem > 15 else "SAUDÁVEL", 
                "Evolução 1 Ano": round((valor_aporte * 12) + (valor_aporte * 0.08), 2),
                "Score": 10 if margem > 15 else 7, 
                "Categoria": "Ações"
            })
        except:
            continue

    return pd.DataFrame(rf_list), pd.DataFrame(acoes_list)
