import streamlit as st
import pandas as pd
import plotly.express as px
import os

# settings
st.set_page_config(page_title="SUSi - Dashboard de Regulação", page_icon="🏥", layout="wide")

st.markdown("""
<style>
    .kpi-card {
        background-color: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .kpi-title {
        color: #64748B;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        color: #0F172A;
        font-size: 2rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    caminho = '/home/gathddu/Documents/UNI/SUSi/data/processed/base_regulacao_limpa.csv'
    if os.path.exists(caminho):
        return pd.read_csv(caminho)
    return pd.DataFrame()

def main():
    st.title("SUSi - Sistema Único de Saúde Intelligence")
    st.markdown("### Painel de Monitoramento de Ineficiências Estruturais")
    
    df = carregar_dados()
    if df.empty:
        st.error("Base de dados não encontrada. Execute o script de geração de dados.")
        return
        
    # filtros
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logo_SUS.svg/1200px-Logo_SUS.svg.png", width=150)
    st.sidebar.header("Filtros")
    
    especialidades = ['Todas'] + list(df['Especialidade'].unique())
    esp_selecionada = st.sidebar.selectbox("Especialidade", especialidades)
    
    status_lista = ['Todos'] + list(df['Status'].unique())
    status_selecionado = st.sidebar.selectbox("Status da Consulta", status_lista)
    
    # aplicar filtros
    df_filtrado = df.copy()
    if esp_selecionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Especialidade'] == esp_selecionada]
    if status_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Status'] == status_selecionado]
        
    # KPIs Customizados
    col1, col2, col3, col4 = st.columns(4)
    total_agendamentos = len(df_filtrado)
    taxa_falha = (df_filtrado['Faltou'].mean() * 100) if total_agendamentos > 0 else 0
    tempo_medio = df_filtrado['Tempo_Espera_Dias'].mean() if total_agendamentos > 0 else 0
    distancia_media = df_filtrado['Distancia_Km'].mean() if total_agendamentos > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total de Agendamentos</div>
            <div class="kpi-value">{total_agendamentos:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #EF4444;">
            <div class="kpi-title">Taxa de Absenteísmo</div>
            <div class="kpi-value">{taxa_falha:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #F59E0B;">
            <div class="kpi-title">Tempo Médio de Espera</div>
            <div class="kpi-value">{tempo_medio:.0f} dias</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-title">Distância Média</div>
            <div class="kpi-value">{distancia_media:.1f} km</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # gráficos
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Tempo de Espera vs. Status")
        fig_tempo = px.box(df_filtrado, x='Status', y='Tempo_Espera_Dias', color='Status', 
                          color_discrete_map={'Compareceu': '#10B981', 'Faltou': '#EF4444'},
                          title="Distribuição do Tempo de Espera por Desfecho")
        st.plotly_chart(fig_tempo, use_container_width=True)
        
    with col_graf2:
        st.subheader("Distância vs. Status")
        df_dist = df_filtrado[df_filtrado['Distancia_Km'] < 50] # Remover outliers extremos
        fig_dist = px.box(df_dist, x='Status', y='Distancia_Km', color='Status',
                         color_discrete_map={'Compareceu': '#10B981', 'Faltou': '#EF4444'},
                         title="Distribuição da Distância por Desfecho")
        st.plotly_chart(fig_dist, use_container_width=True)
        
    st.divider()
    
    st.subheader("Taxa de Absenteísmo por Especialidade")
    df_esp = df_filtrado.groupby('Especialidade')['Faltou'].mean().reset_index()
    df_esp['Faltou'] = df_esp['Faltou'] * 100
    df_esp = df_esp.sort_values('Faltou', ascending=False)
    
    fig_esp = px.bar(df_esp, x='Faltou', y='Especialidade', orientation='h',
                    title="Taxa de Falta por Especialidade (%)",
                    color='Faltou', color_continuous_scale='Reds',
                    labels={'Faltou': 'Taxa de Absenteísmo (%)', 'Especialidade': 'Especialidade'})
    fig_esp.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_esp, use_container_width=True)
    
    st.markdown("---")
    st.markdown("Desenvolvido por **Jess Forster** e **Lucas Almeida** | Projeto Integrador I - Ciência da Computação")

if __name__ == "__main__":
    main()
