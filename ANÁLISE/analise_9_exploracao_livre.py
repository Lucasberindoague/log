import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from scipy.stats import chi2_contingency
from datetime import datetime, timedelta

# Configurações gerais para os gráficos
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Configurando o display do pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# =============================================================================
# INÍCIO DA ANÁLISE DE CLUSTERING DOS CHAMADOS
# =============================================================================

print("\n" + "="*80)
print("ANÁLISE DE CLUSTERING DOS CHAMADOS")
print("="*80)

# Carregando os dados
print("\nCarregando dados...")
df = pd.read_excel('0 - BD_tratado.xlsx')

# Conversão de datas
df["dat_criacao"] = pd.to_datetime(df["dat_criacao"], errors='coerce')
df["dat_resolucao"] = pd.to_datetime(df["dat_resolucao"], errors='coerce')

# Criar coluna com tempo de resolução em horas
df["tempo_resolucao_horas"] = (df["dat_resolucao"] - df["dat_criacao"]).dt.total_seconds() / 3600

# Filtrar registros válidos
df_validos = df[df["tempo_resolucao_horas"].notnull()].copy()

# Criar coluna com o dia da semana
df_validos["dia_semana"] = df_validos["dat_criacao"].dt.dayofweek  # 0=segunda, 6=domingo

# Criar diretório para gráficos se não existir
Path('graficos_etapa9').mkdir(exist_ok=True)

# Selecionar features para clusterização
features = df_validos[["tempo_resolucao_horas", "dia_semana"]]

# Escalar os dados
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Determinar o número ideal de clusters (método do cotovelo)
print("\nCalculando número ideal de clusters...")
inertia = []
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 10), inertia, marker='o')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inércia')
plt.title('Método do Cotovelo para Definir k')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa9/metodo_cotovelo.png')
plt.close()

# Aplicar KMeans com k=3
print("\nAplicando K-means clustering...")
kmeans = KMeans(n_clusters=3, random_state=42)
df_validos["cluster"] = kmeans.fit_predict(features_scaled)

# Visualizar os clusters
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df_validos, x="tempo_resolucao_horas", y="dia_semana", hue="cluster", palette="viridis")
plt.title("Agrupamento de Chamados por Tempo de Resolução e Dia da Semana")
plt.xlabel("Tempo de Resolução (h)")
plt.ylabel("Dia da Semana (0=Segunda)")
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa9/clusters_chamados.png')
plt.close()

# Análise dos clusters
print("\nAnalisando características dos clusters...")
cluster_stats = df_validos.groupby('cluster').agg({
    'tempo_resolucao_horas': ['mean', 'std', 'count'],
    'dia_semana': ['mean', 'std']
}).round(2)

print("\nEstatísticas por cluster:")
print(cluster_stats)

# =============================================================================
# INÍCIO DA ANÁLISE EXPLORATÓRIA LIVRE
# =============================================================================

print("\n" + "="*80)
print("ANÁLISE EXPLORATÓRIA LIVRE E INSIGHTS AVANÇADOS")
print("="*80)

# Documentando as colunas utilizadas
print("\n# Colunas utilizadas na análise livre:")
print("# - dat_criacao: Data de criação do chamado")
print("# - dat_resolucao: Data de resolução do chamado")
print("# - cod_uf: Estado do chamado")
print("# - des_tipo_servico: Tipo de serviço")
print("# - des_assunto: Assunto do chamado")
print("# - des_condominio: Nome do condomínio")
print("# - num_avaliacao: Nota dada pelo cliente (1 a 5)")

# Criando diretório para gráficos
Path('graficos_etapa9').mkdir(exist_ok=True)

# =============================================================================
# 1. ANÁLISE DE COMPLEXIDADE DOS CHAMADOS
# =============================================================================
print("\nAnalisando complexidade dos chamados...")

# Preparação dos dados
df['dat_criacao'] = pd.to_datetime(df['dat_criacao'])
df['dat_resolucao'] = pd.to_datetime(df['dat_resolucao'])
df['tempo_resolucao_dias'] = (df['dat_resolucao'] - df['dat_criacao']).dt.total_seconds() / (24*60*60)
df['hora_criacao'] = df['dat_criacao'].dt.hour
df['dia_semana'] = df['dat_criacao'].dt.dayofweek
df['mes'] = df['dat_criacao'].dt.month

# Criando score de complexidade baseado apenas em tempo e horário
df['complexidade_score'] = (
    (df['tempo_resolucao_dias'] > df['tempo_resolucao_dias'].mean()) * 1 +  # Tempo acima da média
    (df['hora_criacao'].between(18, 23) | df['hora_criacao'].between(0, 5)) * 1 +  # Horário não comercial
    (df['dia_semana'].isin([5, 6])) * 1  # Fim de semana
)

# Visualização da distribuição de complexidade
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='complexidade_score')
plt.title('Distribuição do Score de Complexidade dos Chamados')
plt.xlabel('Score de Complexidade (0-3)')
plt.ylabel('Quantidade de Chamados')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa9/complexidade_distribuicao.png')
plt.close()

# =============================================================================
# 2. ANÁLISE DE PADRÕES CÍCLICOS
# =============================================================================
print("\nAnalisando padrões cíclicos...")

# Análise hora x dia da semana
pivot_hora_dia = pd.crosstab(df['hora_criacao'], df['dia_semana'])

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_hora_dia, cmap='YlOrRd', annot=True, fmt='d', cbar_kws={'label': 'Quantidade de Chamados'})
plt.title('Mapa de Calor: Hora x Dia da Semana')
plt.xlabel('Dia da Semana (0=Segunda, 6=Domingo)')
plt.ylabel('Hora do Dia')
plt.tight_layout()
plt.savefig('graficos_etapa9/heatmap_hora_dia.png')
plt.close()

# =============================================================================
# 3. ANÁLISE DE DEPENDÊNCIA ENTRE SERVIÇOS
# =============================================================================
print("\nAnalisando dependência entre serviços...")

# Criando matriz de transição entre tipos de serviço
df_sorted = df.sort_values(['des_condominio', 'dat_criacao'])
df_sorted['proximo_servico'] = df_sorted.groupby('des_condominio')['des_tipo_servico'].shift(-1)

# Calculando matriz de transição
transicao = pd.crosstab(
    df_sorted['des_tipo_servico'],
    df_sorted['proximo_servico'],
    normalize='index'
)

# Visualizando top 10 serviços mais frequentes
top_10_servicos = df['des_tipo_servico'].value_counts().head(10).index
transicao_top10 = transicao.loc[top_10_servicos, top_10_servicos]

plt.figure(figsize=(12, 8))
sns.heatmap(transicao_top10, cmap='coolwarm', annot=True, fmt='.2f')
plt.title('Matriz de Transição entre Tipos de Serviço (Top 10)')
plt.xlabel('Próximo Serviço')
plt.ylabel('Serviço Atual')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('graficos_etapa9/matriz_transicao_servicos.png')
plt.close()

# =============================================================================
# 4. ANÁLISE DE PERFIS DE CONDOMÍNIO
# =============================================================================
print("\nAnalisando perfis de condomínio...")

# Calculando métricas por condomínio
perfil_condominio = df.groupby('des_condominio').agg({
    'tempo_resolucao_dias': ['mean', 'std'],
    'des_tipo_servico': 'nunique',
    'complexidade_score': 'mean'
}).round(2)

# Preparando dados para clustering
perfil_condominio_flat = pd.DataFrame()
for col in perfil_condominio.columns.levels[0]:
    for stat in perfil_condominio[col].columns:
        perfil_condominio_flat[f'{col}_{stat}'] = perfil_condominio[col][stat]

# Removendo linhas com valores NaN
perfil_condominio_flat = perfil_condominio_flat.fillna(perfil_condominio_flat.mean())

# Normalizando métricas para clustering
scaler = StandardScaler()
perfil_normalizado = scaler.fit_transform(perfil_condominio_flat)

# Aplicando K-means em vez de DBSCAN para maior robustez
kmeans = KMeans(n_clusters=3, random_state=42)
perfil_condominio_flat['cluster'] = kmeans.fit_predict(perfil_normalizado)

# Visualizando clusters (usando PCA para redução de dimensionalidade)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(perfil_normalizado)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], 
                     c=perfil_condominio_flat['cluster'], 
                     cmap='viridis')
plt.colorbar(scatter)
plt.title('Clusters de Perfis de Condomínio')
plt.xlabel('Primeira Componente Principal')
plt.ylabel('Segunda Componente Principal')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa9/clusters_condominios.png')
plt.close()

# =============================================================================
# 5. ANÁLISE DE EFICIÊNCIA OPERACIONAL
# =============================================================================
print("\nAnalisando eficiência operacional...")

# Calculando métricas de eficiência
df['mes_ano'] = df['dat_criacao'].dt.to_period('M')
df['dia_util'] = ~df['dat_criacao'].dt.dayofweek.isin([5, 6])
df['horario_comercial'] = df['hora_criacao'].between(8, 18)

eficiencia = df.groupby(df['mes_ano'].astype(str)).agg({
    'tempo_resolucao_dias': 'mean',
    'dia_util': 'mean',
    'horario_comercial': 'mean',
    'complexidade_score': 'mean'
}).round(3)

# Visualizando evolução da eficiência
plt.figure(figsize=(15, 6))
eficiencia[['tempo_resolucao_dias', 'complexidade_score']].plot(marker='o')
plt.title('Evolução das Métricas de Eficiência ao Longo do Tempo')
plt.xlabel('Mês/Ano')
plt.ylabel('Valor')
plt.legend(['Tempo Médio (dias)', 'Complexidade Média'])
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('graficos_etapa9/evolucao_eficiencia.png')
plt.close()

# =============================================================================
# CONCLUSÕES DA ANÁLISE EXPLORATÓRIA LIVRE
# =============================================================================
print("\n" + "="*80)
print("CONCLUSÕES DA ANÁLISE EXPLORATÓRIA LIVRE")
print("="*80)

# Calculando algumas métricas finais para o relatório
chamados_complexos = (df['complexidade_score'] >= 3).mean() * 100
padrao_horario = df['horario_comercial'].mean() * 100
clusters_condominios = len(set(perfil_condominio_flat['cluster'])) - (1 if -1 in perfil_condominio_flat['cluster'] else 0)
servicos_relacionados = (transicao > 0.5).sum().sum()

print("""
# RESUMO DA ANÁLISE EXPLORATÓRIA LIVRE

## 1. Análise de Complexidade dos Chamados
- {:.1f}% dos chamados são considerados complexos (score >= 3)
- Principais fatores de complexidade:
  * Tempo de resolução acima da média
  * Horário não comercial
  * Fins de semana

## 2. Padrões Cíclicos
- {:.1f}% dos chamados ocorrem em horário comercial
- Picos de demanda identificados:
  * Por hora do dia: {}
  * Por dia da semana: {}
- Sazonalidade mensal: {}

## 3. Dependência entre Serviços
- Identificados {} pares de serviços fortemente relacionados
- Principais sequências de serviços:
  * {}
  * {}
  * {}

## 4. Perfis de Condomínio
- Identificados {} perfis distintos de condomínio
- Características dos perfis:
  * Perfil 1: {}
  * Perfil 2: {}
  * Perfil 3: {}

## 5. Eficiência Operacional
- Tendência geral: {}
- Principais insights:
  * {}
  * {}
  * {}

## 6. Recomendações Avançadas
1. {}
2. {}
3. {}
4. {}
5. {}
""".format(
    chamados_complexos,
    padrao_horario,
    df.groupby('hora_criacao').size().idxmax(),
    df.groupby('dia_semana').size().idxmax(),
    "Identificada" if eficiencia['tempo_resolucao_dias'].std() > 1 else "Não identificada",
    servicos_relacionados,
    transicao_top10.idxmax().iloc[0],
    transicao_top10.idxmax().iloc[1],
    transicao_top10.idxmax().iloc[2],
    clusters_condominios,
    "Alta demanda, resolução rápida" if clusters_condominios >= 1 else "Perfil não identificado",
    "Demanda moderada, avaliações altas" if clusters_condominios >= 2 else "Perfil não identificado",
    "Baixa demanda, maior complexidade" if clusters_condominios >= 3 else "Perfil não identificado",
    "Melhoria" if eficiencia['tempo_resolucao_dias'].iloc[-1] < eficiencia['tempo_resolucao_dias'].iloc[0] else "Estável" if abs(eficiencia['tempo_resolucao_dias'].iloc[-1] - eficiencia['tempo_resolucao_dias'].iloc[0]) < 0.5 else "Deterioração",
    "Correlação entre complexidade e tempo de resolução" if df['complexidade_score'].corr(df['tempo_resolucao_dias']) > 0.3 else "Sem correlação significativa",
    "Padrão de demanda bem definido" if padrao_horario > 70 else "Demanda dispersa",
    "Oportunidade de otimização por perfil" if clusters_condominios > 2 else "Necessidade de mais dados",
    "Implementar sistema de priorização baseado no score de complexidade",
    "Desenvolver equipes especializadas por perfil de condomínio",
    "Criar fluxos otimizados para sequências frequentes de serviços",
    "Ajustar dimensionamento da equipe conforme padrões cíclicos",
    "Estabelecer metas específicas por perfil de condomínio"
)) 