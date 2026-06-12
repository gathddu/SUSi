import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# style
plt.style.use('ggplot')
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

os.makedirs('/home/gathddu/Documents/UNI/SUSi/assets/dashboards', exist_ok=True)

np.random.seed(42)
n_records = 5000

# variáveis
tempo_espera = np.random.gamma(shape=2.5, scale=30, size=n_records) # Média ~75 dias
distancia_km = np.random.lognormal(mean=2, sigma=0.8, size=n_records) # Média ~10km
especialidades = ['Cardiologia', 'Oftalmologia', 'Ortopedia', 'Neurologia', 'Ginecologia', 'Endocrinologia']
esp_probs = [0.2, 0.25, 0.15, 0.15, 0.15, 0.1]
esp_col = np.random.choice(especialidades, size=n_records, p=esp_probs)

# probabilidade de falta (No-Show) baseada em tempo de espera e distância
prob_falta = 1 / (1 + np.exp(-(
    -3.0 + 
    0.02 * tempo_espera + 
    0.05 * distancia_km
)))
status = np.random.binomial(1, prob_falta)
status_str = np.where(status == 1, 'Faltou', 'Compareceu')

df = pd.DataFrame({
    'Tempo_Espera_Dias': tempo_espera,
    'Distancia_Km': distancia_km,
    'Especialidade': esp_col,
    'Status': status_str,
    'Faltou': status
})

# salvar a base de dados
os.makedirs('/home/gathddu/Documents/UNI/SUSi/data/processed', exist_ok=True)
df.to_csv('/home/gathddu/Documents/UNI/SUSi/data/processed/base_regulacao_limpa.csv', index=False)

# ==========================================
# GRÁFICO 1: Taxa de Absenteísmo por Especialidade
# ==========================================
plt.figure(figsize=(10, 6))
taxa_falta_esp = df.groupby('Especialidade')['Faltou'].mean() * 100
taxa_falta_esp = taxa_falta_esp.sort_values(ascending=False)

ax = sns.barplot(x=taxa_falta_esp.index, y=taxa_falta_esp.values, palette='Blues_r')
plt.title('Taxa de Absenteísmo por Especialidade no SUS', pad=20)
plt.ylabel('Taxa de Falta (%)')
plt.xlabel('Especialidade')
plt.xticks(rotation=45)

# rótulos nas barras
for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}%', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 9), 
                textcoords = 'offset points')

plt.tight_layout()
plt.savefig('/home/gathddu/Documents/UNI/SUSi/assets/dashboards/absenteismo_especialidade.png', dpi=300)
plt.close()

# ==========================================
# GRÁFICO 2: Correlação Tempo de Espera vs Absenteísmo
# ==========================================
plt.figure(figsize=(10, 6))

# agrupar tempo de espera em bins
df['Espera_Bin'] = pd.qcut(df['Tempo_Espera_Dias'], q=10)
taxa_por_espera = df.groupby('Espera_Bin')['Faltou'].mean() * 100
espera_media_bin = df.groupby('Espera_Bin')['Tempo_Espera_Dias'].mean()

sns.regplot(x=espera_media_bin.values, y=taxa_por_espera.values, 
            scatter_kws={'s': 100, 'alpha': 0.7, 'color': '#1f77b4'}, 
            line_kws={'color': '#d62728', 'linestyle': '--'})

plt.title('Impacto do Tempo de Espera na Taxa de Absenteísmo', pad=20)
plt.xlabel('Tempo Médio de Espera (Dias)')
plt.ylabel('Taxa de Falta (%)')
plt.tight_layout()
plt.savefig('/home/gathddu/Documents/UNI/SUSi/assets/dashboards/correlacao_espera_falta.png', dpi=300)
plt.close()

# ==========================================
# GRÁFICO 3: Distribuição de Distância por Status
# ==========================================
plt.figure(figsize=(10, 6))
sns.boxplot(x='Status', y='Distancia_Km', data=df[df['Distancia_Km'] < 50], palette='Set2')
plt.title('Distância Percorrida vs Comparecimento', pad=20)
plt.ylabel('Distância (Km)')
plt.xlabel('Status da Consulta')
plt.tight_layout()
plt.savefig('/home/gathddu/Documents/UNI/SUSi/assets/dashboards/distancia_status.png', dpi=300)
plt.close()

print("Base de dados e gráficos gerados com sucesso!")
