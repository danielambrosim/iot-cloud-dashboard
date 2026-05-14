import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from database import DB_NAME, limpar_dados_antigos, listar_locais

# Configuração da página
st.set_page_config(
    page_title="Dashboard IoT",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard IoT - Monitoramento Ambiental")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Seleção de localização
    st.subheader("📍 Filtrar por Local")
    locais = listar_locais()
    
    if locais:
        local_selecionado = st.selectbox(
            "Escolha o local para visualizar:",
            ["Todos os locais"] + locais
        )
    else:
        local_selecionado = "Todos os locais"
        st.warning("Nenhum dado encontrado. Execute o main.py primeiro!")
    
    st.markdown("---")
    
    if st.button("🗑️ Limpar dados >30 dias"):
        removidos = limpar_dados_antigos()
        st.success(f"Removidas {removidos} leituras antigas!")
        st.rerun()
    
    st.markdown("---")
    st.caption(f"🕐 Última atualização: {datetime.now().strftime('%H:%M:%S')}")
    st.caption("🔄 Dados atualizados a cada 5 segundos")

# Função para carregar dados
@st.cache_data(ttl=5)
def carregar_dados(local_filtro):
    """Carrega os dados do banco SQLite com filtro opcional"""
    conn = sqlite3.connect(DB_NAME)
    
    data_limite = (datetime.now() - timedelta(days=30)).isoformat()
    
    if local_filtro == "Todos os locais":
        query = """
            SELECT timestamp, localizacao, temperatura, umidade, fonte 
            FROM leituras 
            WHERE timestamp >= ?
            ORDER BY timestamp ASC
        """
        params = (data_limite,)
    else:
        query = """
            SELECT timestamp, localizacao, temperatura, umidade, fonte 
            FROM leituras 
            WHERE timestamp >= ? AND localizacao = ?
            ORDER BY timestamp ASC
        """
        params = (data_limite, local_filtro)
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

# Carregar dados
df = carregar_dados(local_selecionado)

# Métricas
col1, col2, col3, col4 = st.columns(4)

if not df.empty:
    ultima_temp = df['temperatura'].iloc[-1]
    ultima_umid = df['umidade'].iloc[-1]
    temp_max = df['temperatura'].max()
    temp_min = df['temperatura'].min()
    local_info = df['localizacao'].iloc[-1] if local_selecionado == "Todos os locais" else local_selecionado
    
    with col1:
        st.metric("🌡️ Temperatura Atual", f"{ultima_temp}°C", help=f"Última leitura - {local_info}")
    
    with col2:
        st.metric("💧 Umidade Atual", f"{ultima_umid}%")
    
    with col3:
        st.metric("📈 Temp. Máxima (30d)", f"{temp_max}°C")
    
    with col4:
        st.metric("📉 Temp. Mínima (30d)", f"{temp_min}°C")
else:
    for col in [col1, col2, col3, col4]:
        with col:
            st.metric("---", "Sem dados")
    st.warning("⚠️ Nenhum dado encontrado para o filtro selecionado.")

st.markdown("---")

# Gráficos
if not df.empty:
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("🌡️ Temperatura ao Longo do Tempo")
        fig_temp = px.line(
            df, 
            x='timestamp', 
            y='temperatura',
            color='localizacao' if local_selecionado == "Todos os locais" else None,
            title=f'Evolução da Temperatura - {local_selecionado}',
            labels={'temperatura': 'Temperatura (°C)', 'timestamp': 'Data/Hora', 'localizacao': 'Local'},
            color_discrete_sequence=['#ff4b4b']
        )
        fig_temp.update_layout(hovermode='x unified')
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col_graf2:
        st.subheader("💧 Umidade ao Longo do Tempo")
        fig_umid = px.bar(
            df,
            x='timestamp',
            y='umidade',
            color='localizacao' if local_selecionado == "Todos os locais" else None,
            title=f'Evolução da Umidade - {local_selecionado}',
            labels={'umidade': 'Umidade (%)', 'timestamp': 'Data/Hora', 'localizacao': 'Local'},
            color_discrete_sequence=['#4b9eff']
        )
        fig_umid.update_layout(hovermode='x unified')
        st.plotly_chart(fig_umid, use_container_width=True)
    
    # Gráfico combinado
    st.subheader("📈 Comparativo: Temperatura vs Umidade")
    fig_combo = go.Figure()
    
    fig_combo.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['temperatura'],
        name='Temperatura (°C)',
        line=dict(color='#ff4b4b', width=2),
        yaxis='y1'
    ))
    
    fig_combo.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['umidade'],
        name='Umidade (%)',
        line=dict(color='#4b9eff', width=2, dash='dash'),
        yaxis='y2'
    ))
    
    fig_combo.update_layout(
        title=f'Temperatura e Umidade - {local_selecionado}',
        xaxis=dict(title='Data/Hora'),
        yaxis=dict(
            title=dict(text='Temperatura (°C)', font=dict(color='#ff4b4b'))
        ),
        yaxis2=dict(
            title=dict(text='Umidade (%)', font=dict(color='#4b9eff')),
            overlaying='y',
            side='right'
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_combo, use_container_width=True)
    
    # Tabela de dados recentes
    st.subheader("📋 Últimas Leituras")
    df_recente = df.tail(10).copy()
    df_recente['timestamp'] = df_recente['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_recente = df_recente[['timestamp', 'localizacao', 'temperatura', 'umidade']]
    df_recente.columns = ['Data/Hora', 'Local', 'Temperatura (°C)', 'Umidade (%)']
    
    st.dataframe(df_recente, use_container_width=True)
    
    # Estatísticas por local (se tiver múltiplos locais)
    if local_selecionado == "Todos os locais" and len(df['localizacao'].unique()) > 1:
        st.subheader("📊 Comparativo entre Locais")
        
        estatisticas = df.groupby('localizacao').agg({
            'temperatura': ['mean', 'max', 'min'],
            'umidade': ['mean']
        }).round(1)
        
        estatisticas.columns = ['Temp Média', 'Temp Máx', 'Temp Mín', 'Umid Média']
        st.dataframe(estatisticas, use_container_width=True)

else:
    st.info("📭 Nenhum dado disponível. Execute o main.py para começar a coletar dados!")

# Footer
st.markdown("---")
st.caption("🔌 Sistema IoT com armazenamento local | Dados mantidos por 30 dias | Dashboard atualizada automaticamente")