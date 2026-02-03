import streamlit as st
import pandas as pd
from main import analisar_tudo_v4

# 1. CONFIGURAÇÃO DE TEMA E PÁGINA
st.set_page_config(
    page_title="SmartYield 360", 
    page_icon="💰", 
    layout="centered"
)

# Custom CSS para deixar com cara de App de Investimento
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stNumberInput div div input { color: #f0f2f6; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #00d4ff; }
    .stButton>button { 
        width: 100%; 
        background-color: #00d4ff; 
        color: white; 
        font-weight: bold; 
        border-radius: 20px;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO
st.title("🏦 SmartYield 360")
st.caption("Consultoria Inteligente • B3 & Renda Fixa")

# 3. ENTRADA DE DADOS COM ESTILO
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        valor = st.number_input("Quanto vai aportar hoje?", min_value=10.0, value=1000.0, step=100.0)
    with col2:
        st.write("") # Espaçador
        st.write("") 
        botao = st.button("ANALISAR")

if botao:
    with st.spinner('Sincronizando com o mercado...'):
        df_rf, df_acoes = analisar_tudo_v4(valor)
        
        # DASHBOARD DE RESUMO
        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Aporte Atual", f"R$ {valor:,.2026.2f}")
        with c2:
            if not df_acoes.empty:
                melhor = df_acoes.sort_values(by="Score", ascending=False).iloc[0]
                st.metric("Top Pick", melhor['Ativo'])

        # ABAS ESTILO BANCO
        aba1, aba2 = st.tabs(["🔒 RENDA FIXA", "📊 AÇÕES B3"])

        with aba1:
            st.write("#### Melhores Taxas de Hoje")
            # Estilizando a tabela de Renda Fixa
            st.dataframe(df_rf.style.format({"Mensal Líq.": "R$ {:.2f}", "Evolução 1 Ano": "R$ {:.2f}"})
                         .highlight_max(axis=0, subset=['Score'], color='#004d4d'), 
                         width='stretch')

        with aba2:
            if not df_acoes.empty:
                st.write("#### Radar de Oportunidades")
                
                # Função para colorir o status
                def color_status(val):
                    color = '#2ecc71' if 'OPORTUNIDADE' in val else '#f1c40f'
                    return f'color: {color}; font-weight: bold'

                # Exibindo tabela de ações com estilo de "Home Broker"
                st.dataframe(
                    df_acoes.style.applymap(color_status, subset=['Status'])
                    .format({"Mensal Líq.": "R$ {:.2f}", "Evolução 1 Ano": "R$ {:.2f}"}),
                    width='stretch'
                )
            else:
                st.warning("Aguardando conexão com a B3... Tente novamente em instantes.")

# RODAPÉ
st.markdown("---")
st.caption("⚠️ Dados simulados baseados em indicadores de mercado. Invista com consciência.")
