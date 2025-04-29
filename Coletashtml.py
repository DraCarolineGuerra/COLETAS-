import streamlit as st
import pandas as pd
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Coleta+ 🐾",
    page_icon="🐾",
    layout="wide"
)

# Carregar dados (igual ao seu código)
@st.cache_data  # Cache para performance
def load_data():
    try:
        dados = pd.read_csv('BANCO DE DADOS.csv', encoding='latin1')
        dados.columns = dados.columns.str.strip()
        if 'CONTEÚDO' not in dados.columns:
            dados['CONTEÚDO'] = ''
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar o banco de dados:\n{e}")
        return pd.DataFrame(columns=['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO'])

dados = load_data()

# --- Sidebar (Busca) ---
with st.sidebar:
    st.title("Coleta+ 🐾")
    st.image("logo_hospital.png", width=100) if "logo_hospital.png" else st.write("Logo aqui")
    
    termo_busca = st.text_input("🔍 Buscar exame:", help="Digite o nome ou conteúdo do exame")
    if st.button("Limpar busca"):
        termo_busca = ""

# --- Resultados ---
if termo_busca:
    resultados = dados[
        dados['EXAMES'].fillna('').str.lower().str.contains(termo_busca.lower()) | 
        dados['CONTEÚDO'].fillna('').str.lower().str.contains(termo_busca.lower())
    ]
else:
    resultados = dados.copy()

# --- Mostrar Detalhes ---
if not resultados.empty:
    exame_selecionado = st.selectbox(
        "Selecione um exame:",
        resultados['EXAMES'].unique()
    )
    
    detalhes = resultados[resultados['EXAMES'] == exame_selecionado].iloc[0]
    
    # Layout em colunas (similar ao seu Tkinter)
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("📋 Informações Básicas")
        st.markdown(f"**Código:** {detalhes['CÓDIGO']}")
        st.markdown(f"**Prazo:** {detalhes['PRAZO']}")
        st.markdown(f"**Tubo:** {detalhes['TUBO']}")
    
    with col2:
        st.subheader("📝 Detalhes")
        st.markdown(f"**Cuidados Especiais:**\n{detalhes['CUIDADOS ESPECIAIS']}")
        st.markdown(f"**Laboratório:** {detalhes['LABORATÓRIO']}")
        st.markdown(f"**Conteúdo:**\n{detalhes['CONTEÚDO']}")
else:
    st.warning("Nenhum exame encontrado. Tente outro termo de busca.")

# --- Rodapé ---
st.divider()
st.markdown("© 2025 Coleta+ | Desenvolvido por Caroline Guerra 🐾")
