import streamlit as st
import pandas as pd
from main import analisar_tudo_v4

# Configuração da página para Mobile
st.set_page_config(page_title="SmartYield 360", page_icon="🏦", layout="centered")

st.title("🏦 SmartYield 360")
st.subheader("Onde investir seu aporte hoje?")

# Entrada de dados
valor = st.number_input("Quanto vai investir hoje? (R$)", min_value=10.0, value=1000.0, step=50.0)

if st.button("🚀 Analisar Melhores Entradas"):
    with st.spinner('Consultando B3 e Taxas atualizadas...'):
        df_rf, df_acoes = analisar_tudo_v4(valor)
        
        st.write("### 💰 Renda Fixa (Segurança)")
        st.dataframe(df_rf, use_container_width=True)
        
        st.write("### 📈 Ações (Renda Passiva)")
        if not df_acoes.empty:
            # Filtro para mostrar a melhor entrada do dia (Score mais alto)
            melhor_opcao = df_acoes.sort_values(by="Score", ascending=False).head(1)
            st.success(f"⭐ **Melhor Entrada Hoje:** {melhor_opcao['Ativo'].values[0]}")
            st.dataframe(df_acoes, use_container_width=True)
        else:
            st.warning("Aporte baixo para as ações selecionadas ou erro de conexão com a B3.")

st.info("Apenas 1 melhor entrada sugerida por dia com base na Margem de Segurança.")
