# dashboard.py (versão com seletor de cidade)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from database import DB_NAME, limpar_dados_antigos, listar_locais

st.set_page_config(page_title="Dashboard IoT", page_icon="📊", layout="wide")

st.title("📊 Dashboard IoT - Monitoramento Climático")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    st.subheader("📍 Escolha uma cidade")
    locais = listar_locais()
    
    if locais:
        cidade_selecionada = st.selectbox(
            "Selecione a cidade para visualizar os dados:",
            locais
        )
    else:
        cidade_selecionada = None
        st.warning("⚠️ Nenhum dado disponível ainda. Aguarde a primeira coleta de dados.")
    
    st.markdown("---")
    
    if st.button("🗑️ Limpar dados >30 dias"):
        removidos = limpar_dados_antigos()
        st.success(f"Removidas {removidos} leituras antigas!")
        st.rerun()
    
    st.markdown("---")
    st.caption(f"🕐 Última atualização: {datetime.now().strftime('%H:%M:%S')}")

# Função para carregar dados da cidade selecionada
@st.cache_data(ttl=60)
def carregar_dados(cidade):
    """Carrega os dados da cidade selecionada"""
    if not cidade:
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_NAME)
    data_limite = (datetime.now() - timedelta(days=30)).isoformat()
    
    query = """
        SELECT timestamp, localizacao, temperatura, umidade, fonte 
        FROM leituras 
        WHERE timestamp >= ? AND localizacao = ?
        ORDER BY timestamp ASC
    """
    
    df = pd.read_sql_query(query, conn, params=(data_limite, cidade))
    conn.close()
    
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

# Carregar dados da cidade selecionada
if cidade_selecionada:
    df = carregar_dados(cidade_selecionada)
    
    if not df.empty:
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🌡️ Temperatura Atual", f"{df['temperatura'].iloc[-1]}°C")
        with col2:
            st.metric("💧 Umidade Atual", f"{df['umidade'].iloc[-1]}%")
        with col3:
            st.metric("📈 Temp. Máxima (30d)", f"{df['temperatura'].max()}°C")
        with col4:
            st.metric("📉 Temp. Mínima (30d)", f"{df['temperatura'].min()}°C")
        
        st.markdown("---")
        
        # Gráficos
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.subheader("🌡️ Temperatura ao Longo do Tempo")
            fig_temp = px.line(
                df, x='timestamp', y='temperatura',
                title=f'Temperatura - {cidade_selecionada}',
                labels={'temperatura': '°C', 'timestamp': 'Data'},
                color_discrete_sequence=['#ff4b4b']
            )
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col_graf2:
            st.subheader("💧 Umidade ao Longo do Tempo")
            fig_umid = px.bar(
                df, x='timestamp', y='umidade',
                title=f'Umidade - {cidade_selecionada}',
                labels={'umidade': '%', 'timestamp': 'Data'},
                color_discrete_sequence=['#4b9eff']
            )
            st.plotly_chart(fig_umid, use_container_width=True)
        
        # Tabela de dados recentes
        st.subheader("📋 Últimas Leituras")
        df_recente = df.tail(10).copy()
        df_recente['timestamp'] = df_recente['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df_recente = df_recente[['timestamp', 'temperatura', 'umidade']]
        df_recente.columns = ['Data/Hora', 'Temperatura (°C)', 'Umidade (%)']
        st.dataframe(df_recente, use_container_width=True)
        
    else:
        st.info(f"📭 Nenhum dado disponível para {cidade_selecionada}. Aguardando coleta de dados.")
else:
    st.info("🌍 Selecione uma cidade no menu lateral para visualizar os dados climáticos.")

st.markdown("---")
st.caption("📊 Dashboard atualizada automaticamente | Dados coletados a cada hora via GitHub Actions")