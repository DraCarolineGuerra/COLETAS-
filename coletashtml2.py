import streamlit as st
import pandas as pd
from PIL import Image
import os

# ======================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================
st.set_page_config(
    page_title="Coleta+ 🐾",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================
# FUNÇÕES AUXILIARES
# ======================================
@st.cache_data
def load_data():
    """Carrega os dados do arquivo CSV"""
    try:
        dados = pd.read_csv('BANCO_DE_DADOS.csv', encoding='latin1')
        dados.columns = dados.columns.str.strip()
        if 'CONTEÚDO' not in dados.columns:
            dados['CONTEÚDO'] = ''
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar o banco de dados:\n{e}")
        return pd.DataFrame(columns=['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 
                                  'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO'])

def load_logo():
    """Carrega a imagem do logo"""
    try:
        if os.path.exists('logo_hospital.png'):
            return Image.open('logo_hospital.png')
        return None
    except Exception as e:
        st.warning(f"Erro ao carregar logo: {e}")
        return None

def display_detalhes(detalhes):
    """Exibe os detalhes do exame"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("📋 Informações Básicas")
        st.markdown(f"**Código:** `{detalhes['CÓDIGO']}`")
        st.markdown(f"**Prazo:** `{detalhes['PRAZO']}`")
        st.markdown(f"**Tubo:** `{detalhes['TUBO']}`")
    
    with col2:
        st.subheader("📝 Detalhes")
        st.markdown(f"**Cuidados Especiais:**\n> {detalhes['CUIDADOS ESPECIAIS']}")
        st.markdown(f"**Laboratório:** `{detalhes['LABORATÓRIO']}`")
        st.markdown(f"**Conteúdo:**\n> {detalhes['CONTEÚDO']}")

# ======================================
# INTERFACE PRINCIPAL
# ======================================
# Carregar dados
dados = load_data()

# Sidebar
with st.sidebar:
    # Logo
    logo = load_logo()
    if logo:
        st.image(logo, width=100)
    else:
        st.markdown("""
        <div style='width:100px; height:100px; background-color:#f0f0f0; 
        border-radius:10px; display:flex; justify-content:center; 
        align-items:center; margin-bottom:20px;'>
        <span style='color:#999;'>Logo</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.title("Coleta+ 🐾")
    
    # Busca
    termo_busca = st.text_input(
        "🔍 Buscar exame:",
        placeholder="Digite o nome do exame",
        help="Busque por nome ou conteúdo do exame"
    )
    
    if st.button("🧹 Limpar busca", use_container_width=True):
        termo_busca = ""

# Área principal
st.header("Catálogo de Exames")

# Filtragem
if termo_busca:
    resultados = dados[
        dados['EXAMES'].fillna('').str.lower().str.contains(termo_busca.lower()) | 
        dados['CONTEÚDO'].fillna('').str.lower().str.contains(termo_busca.lower())
    ]
else:
    resultados = dados.copy()

# Exibição dos resultados
if not resultados.empty:
    exame_selecionado = st.selectbox(
        "Selecione um exame para ver detalhes:",
        resultados['EXAMES'].unique(),
        index=None,
        placeholder="Selecione um exame"
    )
    
    if exame_selecionado:
        detalhes = resultados[resultados['EXAMES'] == exame_selecionado].iloc[0]
        display_detalhes(detalhes)
else:
    st.warning("Nenhum exame encontrado com o termo buscado.")

# Rodapé
st.divider()
st.caption("© 2025 Coleta+ | Desenvolvido por Caroline Guerra 🐾")

# ======================================
# ESTILOS CSS ADICIONAIS
# ======================================
st.markdown("""
<style>
    /* Melhora o visual dos selects */
    div[data-baseweb="select"] {
        border: 1px solid #8a2be2 !important;
        border-radius: 8px !important;
    }
    
    /* Botão de limpar busca */
    div[data-testid="stButton"] button {
        background-color: #f5f0fa;
        color: #4b0082;
        border: 1px solid #8a2be2;
    }
    
    div[data-testid="stButton"] button:hover {
        background-color: #8a2be2 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)
