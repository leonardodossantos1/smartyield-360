import streamlit as st
import pandas as pd
from main import analisar_tudo_v4 # Reaproveita sua inteligência do PC

# Configuração da página para Mobile
st.set_page_config(page_title="SmartYield 360", page_icon="🏦", layout="centered")

# Estilo customizado para parecer App
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #27ae60; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 SmartYield 360")
st.subheader("Inteligência Financeira Pro")

# Campo de entrada
valor_aporte = st.number_input("Quanto vai investir hoje?", min_value=10.0, value=35.0, step=10.0)

if st.button("🚀 ANALISAR AGORA"):
    with st.spinner('Consultando o mercado...'):
        df_rf, df_acoes = analisar_tudo_v4(valor_aporte)
        
        # --- VEREDITO EM DESTAQUE ---
        df_total = pd.concat([df_rf, df_acoes], ignore_index=True)
        melhor = df_total.sort_values(by=["Score", "Mensal Líq."], ascending=False).iloc[0]
        
        st.success(f"🏆 **MELHOR OPÇÃO:** {melhor['Ativo']}")
        st.info(f"📍 **ONDE:** {melhor['Onde']}\n\n💰 **ESTIMATIVA 1 ANO:** R$ {melhor['Evolução 1 Ano']}")

        # --- ABAS PARA ORGANIZAR NO CELULAR ---
        tab1, tab2 = st.tabs(["🛡️ Renda Fixa", "📈 Ações"])
        
        with tab1:
            for _, row in df_rf.iterrows():
                with st.expander(f"{row['Ativo']} - R$ {row['Mensal Líq.']}/mês"):
                    st.write(f"**Onde:** {row['Onde']}")
                    st.write(f"**Em 1 ano:** R$ {row['Evolução 1 Ano']}")
        
        with tab2:
            if not df_acoes.empty:
                for _, row in df_acoes.iterrows():
                    cor_status = "🟢" if "SAUDÁVEL" in row['Status'] else "🔥"
                    with st.expander(f"{cor_status} {row['Ativo']} - Margem: {row['Margem']}"):
                        st.write(f"**Status:** {row['Status']}")
                        st.write(f"**Rendimento Mensal:** R$ {row['Mensal Líq.']}")
                        st.write(f"**Acumulado 1 ano:** R$ {row['Evolução 1 Ano']}")
            else:
                st.warning("Aporte baixo para ações hoje.")