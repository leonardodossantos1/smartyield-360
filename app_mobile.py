import streamlit as st
import pandas as pd
from main import analisar_tudo_v4

# 1. FORÇAR TEMA DARK E CORES NO TOPO
st.set_page_config(page_title="SmartYield 360", page_icon="🏦")

# CSS CORRETIVO - Garante que o texto seja legível
st.markdown("""
    <style>
    /* Fundo da página */
    .stApp { background-color: #0e1117; }
    
    /* Forçar cor dos textos e números para Branco/Cinza Claro */
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    
    /* Estilo dos inputs */
    .stNumberInput div div input { color: #ffffff !important; background-color: #1e2130 !important; }
    
    /* Estilo das tabelas (Dataframes) */
    .stDataFrame { background-color: #1e2130; border-radius: 10px; }
    
    /* Botão Principal */
    .stButton>button { 
        width: 100%; 
        background-color: #00d4ff; 
        color: #ffffff !important; 
        font-weight: bold; 
        border-radius: 10px;
        border: none;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 SmartYield 360")
st.write("Seu consultor de aportes atualizado.")

# ENTRADA
valor = st.number_input("Valor do aporte (R$):", min_value=10.0, value=1000.0)

if st.button("ANALISAR MERCADO"):
    with st.spinner('Buscando dados...'):
        df_rf, df_acoes = analisar_tudo_v4(valor)
        
        # Abas para organizar no celular
        aba1, aba2 = st.tabs(["🔒 RENDA FIXA", "📊 AÇÕES"])

        with aba1:
            st.subheader("Onde render mais com segurança:")
            # Exibe a tabela sem filtros de cor complexos para evitar erros
            st.table(df_rf[['Ativo', 'Onde', 'Mensal Líq.', 'Evolução 1 Ano']])

        with aba2:
            if not df_acoes.empty:
                st.subheader("Radar de Oportunidades B3:")
                # Mostra a melhor escolha do dia em destaque
                top_acao = df_acoes.sort_values(by="Score", ascending=False).iloc[0]
                st.success(f"⭐ MELHOR ENTRADA: {top_acao['Ativo']}")
                
                # Tabela de ações
                st.table(df_acoes[['Ativo', 'Mensal Líq.', 'Margem', 'Status']])
            else:
                st.warning("Aporte insuficiente para as ações da lista ou erro de conexão.")

st.caption("Versão 4.2 - 2026 • Dados protegidos")
