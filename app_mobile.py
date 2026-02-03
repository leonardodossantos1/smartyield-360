import streamlit as st
import pandas as pd
from main import analisar_tudo_v4

st.set_page_config(page_title="SmartYield 360", layout="centered")

# CSS para esconder os índices das tabelas e melhorar visual - NÃO MUDADO
st.markdown("""
    <style>
    .stTable [data-testid="stTableTrendsCol"] { display: none; }
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    .best-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #00d4ff;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 SmartYield 360")

valor = st.number_input("Quanto vai aportar hoje? (R$)", min_value=10.0, value=1000.0)

if st.button("ANALISAR MELHORES DO MÊS"):
    df_rf, df_acoes = analisar_tudo_v4(valor)
    
    # --- LÓGICA DO MELHOR DO MÊS ---
    top_acao = df_acoes.sort_values(by="Score", ascending=False).iloc[0]
    top_rf = df_rf.sort_values(by="Mensal Líq.", ascending=False).iloc[0]

    st.markdown(f"""
        <div class="best-card">
            <h2 style='color: #00d4ff; margin:0;'>🏆 MELHOR DO MÊS</h2>
            <p style='color: white; font-size: 20px; margin:10px;'><b>{top_acao['Ativo']}</b> (Ações)</p>
            <p style='color: #2ecc71; margin:0;'>Renda Mensal Estimada: R$ {top_acao['Mensal Líq.']:.2f}</p>
        </div>
    """, unsafe_allow_html=True)

    aba1, aba2 = st.tabs(["🔒 RENDA FIXA", "📊 AÇÕES"])

    with aba1:
        st.write("### 💰 Onde o banco paga mais:")
        rf_clean = df_rf[['Ativo', 'Onde', 'Mensal Líq.', 'Evolução 1 Ano']].copy()
        rf_clean.columns = ['Investimento', 'Instituição', 'Renda Mensal', 'Total em 1 Ano']
        st.table(rf_clean.style.format({"Renda Mensal": "R$ {:.2f}", "Total em 1 Ano": "R$ {:.2f}"}))
        
        st.info(f"💡 Dica: O **{top_rf['Ativo']}** na **{top_rf['Onde']}** é sua melhor opção em segurança hoje.")

    with aba2:
        st.write("### 📈 Radar de Dividendos B3:")
        if not df_acoes.empty:
            # Mostramos a tabela
            acoes_clean = df_acoes[['Ativo', 'Mensal Líq.', 'Margem', 'Status']].copy()
            acoes_clean.columns = ['Empresa', 'Renda Estimada', 'Margem Segurança', 'Status']
            st.table(acoes_clean.style.format({"Renda Estimada": "R$ {:.2f}"}))
            
            # CORREÇÃO DO ERRO AQUI: Usando os nomes originais das colunas (Ativo e Margem)
            st.success(f"🔥 **Foco do Mês:** {top_acao['Ativo']} devido à margem de {top_acao['Margem']}.")
        else:
            st.error("Erro ao carregar dados da B3.")

st.caption("Filtro aplicado: Escolhendo a melhor entrada do dia (Somente 1 por categoria).")
