import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Configurações gerais para os gráficos
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Configurando o display do pandas para mostrar mais colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# =============================================================================
# INÍCIO DA ANÁLISE DE CORRELAÇÕES E PADRÕES
# =============================================================================

print("\n" + "="*80)
print("ANÁLISE DE CORRELAÇÕES E PADRÕES ENTRE VARIÁVEIS")
print("="*80)

# Carregando os dados
print("\nCarregando dados...")
df = pd.read_excel('../BD/0 - BD_tratado.xlsx')

# Análise de correlação entre condomínios
print("\nAnalisando correlações entre condomínios...")
# Criar uma tabela pivot com condomínios nas colunas e contagem de chamados por cliente
correlacao_condominios = pd.crosstab(
    df['Nome_Cliente'],
    df['Condomínio']
)

# Calcular a matriz de correlação entre condomínios
matriz_correlacao_condominios = correlacao_condominios.corr()

# Gerar o heatmap
plt.figure(figsize=(24, 20))
sns.heatmap(matriz_correlacao_condominios, 
            cmap='RdBu_r',
            center=0,
            annot=False,
            fmt='.2f',
            square=True,
            xticklabels=True,
            yticklabels=True)
plt.title('Correlação de Chamados por Condomínio', fontsize=16, pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('graficos_etapa8/correlacao_condominios.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
plt.close()

# Documentando as colunas utilizadas
print("\n# Colunas utilizadas na análise de correlações:")
print("# - dat_criacao: Data de criação do chamado")
print("# - dat_resolucao: Data de resolução do chamado")
print("# - cod_uf: Estado do chamado")
print("# - des_tipo_servico: Tipo de serviço")
print("# - vlr_nota_avaliacao_cliente_atendimento: Nota dada pelo cliente (1 a 5)")

# Preparação dos dados
print("\nPreparando dados para análise...")

# Convertendo datas e calculando tempo de resolução
df['Data_Criação'] = pd.to_datetime(df['Data_Criação'])
df['Data_Resolução'] = pd.to_datetime(df['Data_Resolução'])
df['tempo_resolucao_dias'] = (df['Data_Resolução'] - df['Data_Criação']).dt.total_seconds() / (24*60*60)

# Filtrando avaliações válidas (1 a 5)
df_valid = df[df['Nota_Avaliação'].between(1, 5)].copy()

# Criando diretório para gráficos
Path('graficos_etapa8').mkdir(exist_ok=True)

# 1. Matriz de Correlação entre Variáveis Numéricas
print("\nCalculando correlações entre variáveis numéricas...")
variaveis_numericas = ['tempo_resolucao_dias', 'Nota_Avaliação']
matriz_correlacao = df_valid[variaveis_numericas].corr(method='spearman')

plt.figure(figsize=(10, 8))
sns.heatmap(matriz_correlacao, annot=True, cmap='RdYlBu', center=0)
plt.title('Matriz de Correlação entre Variáveis Numéricas')
plt.tight_layout()
plt.savefig('graficos_etapa8/matriz_correlacao.png')
plt.close()

# 2. Scatter Plot: Tempo de Resolução vs Avaliação
print("\nAnalisando relação entre tempo de resolução e avaliação...")
plt.figure(figsize=(10, 6))
plt.scatter(df_valid['tempo_resolucao_dias'], df_valid['Nota_Avaliação'], alpha=0.5)
plt.title('Relação entre Tempo de Resolução e Avaliação')
plt.xlabel('Tempo de Resolução (dias)')
plt.ylabel('Avaliação do Cliente')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa8/scatter_tempo_avaliacao.png')
plt.close()

# 3. Análise por Estado
print("\nAnalisando padrões por estado...")
estado_stats = df_valid.groupby('Estado_UF').agg({
    'tempo_resolucao_dias': ['mean', 'std'],
    'Nota_Avaliação': ['mean', 'std'],
    'Categoria_Serviço': 'count'
}).round(2)

# Boxplot de Tempo de Resolução por Estado
plt.figure(figsize=(15, 6))
sns.boxplot(x='Estado_UF', y='tempo_resolucao_dias', data=df_valid)
plt.title('Distribuição do Tempo de Resolução por Estado')
plt.xlabel('Estado')
plt.ylabel('Tempo de Resolução (dias)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa8/boxplot_tempo_estado.png')
plt.close()

# 4. Análise por Tipo de Serviço
print("\nAnalisando padrões por tipo de serviço...")
servico_stats = df_valid.groupby('Categoria_Serviço').agg({
    'tempo_resolucao_dias': ['mean', 'std'],
    'Nota_Avaliação': ['mean', 'std'],
    'Estado_UF': 'count'
}).round(2)

# Top 10 tipos de serviço mais frequentes
top_10_servicos = df_valid['Categoria_Serviço'].value_counts().head(10).index

# Boxplot de Avaliação por Tipo de Serviço (Top 10)
plt.figure(figsize=(15, 6))
sns.boxplot(x='Categoria_Serviço', y='Nota_Avaliação', 
            data=df_valid[df_valid['Categoria_Serviço'].isin(top_10_servicos)])
plt.title('Distribuição da Avaliação por Tipo de Serviço (Top 10)')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Avaliação')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa8/boxplot_avaliacao_servico.png')
plt.close()

# 5. Análise Temporal
print("\nAnalisando padrões temporais...")
df_valid['mes_ano'] = df_valid['Data_Criação'].dt.to_period('M')
temporal_stats = df_valid.groupby('mes_ano').agg({
    'tempo_resolucao_dias': 'mean',
    'Nota_Avaliação': 'mean'
}).round(2)

plt.figure(figsize=(15, 6))
temporal_stats.plot(y=['tempo_resolucao_dias', 'Nota_Avaliação'], marker='o')
plt.title('Evolução Temporal: Tempo de Resolução e Avaliação Média')
plt.xlabel('Mês/Ano')
plt.ylabel('Valor')
plt.legend(['Tempo Médio (dias)', 'Avaliação Média'])
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa8/evolucao_temporal.png')
plt.close()

# 6. Análise de Clusters (K-means)
print("\nRealizando análise de clusters...")
# Preparando dados para clustering
X = df_valid[['tempo_resolucao_dias', 'Nota_Avaliação']].copy()
# Removendo linhas com valores NaN
X = X.dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicando K-means
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
X['cluster'] = kmeans.fit_predict(X_scaled)

# Visualizando clusters
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X['tempo_resolucao_dias'], 
                     X['Nota_Avaliação'], 
                     c=X['cluster'], 
                     cmap='viridis', 
                     alpha=0.5)
plt.colorbar(scatter)
plt.title('Clusters de Chamados por Tempo e Avaliação')
plt.xlabel('Tempo de Resolução (dias)')
plt.ylabel('Avaliação do Cliente')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa8/clusters.png')
plt.close()

# Verificando sazonalidade
has_seasonality = temporal_stats.index.size >= 12 and temporal_stats['tempo_resolucao_dias'].std() > temporal_stats['tempo_resolucao_dias'].mean() * 0.1

# Conclusões da Análise de Correlações
print("\n" + "="*80)
print("CONCLUSÕES DA ANÁLISE DE CORRELAÇÕES E PADRÕES")
print("="*80)

print("""
# RESUMO DA ANÁLISE DE CORRELAÇÕES E PADRÕES

## 1. Correlações Principais
- Correlação Tempo x Avaliação: {:.3f}
- Interpretação: {}

## 2. Padrões por Estado
- Estado com maior variabilidade no tempo: {} (std: {:.1f} dias)
- Estado com maior consistência nas avaliações: {} (std: {:.2f})
- Correlação entre volume e tempo médio: {}

## 3. Padrões por Tipo de Serviço
- Serviço com melhor relação tempo/avaliação: {}
- Serviço com pior relação tempo/avaliação: {}
- {:.1f}% dos serviços têm padrão consistente

## 4. Padrões Temporais
- Tendência no tempo de resolução: {}
- Tendência nas avaliações: {}
- Sazonalidade identificada: {}

## 5. Análise de Clusters
- Número de clusters identificados: {}
- Características do cluster principal: {}
- {:.1f}% dos chamados no cluster mais eficiente

## 6. Insights Principais
- {}
- {}
- {}

## 7. Recomendações
1. {}
2. {}
3. {}
4. {}
5. {}
""".format(
    matriz_correlacao.iloc[0,1],
    "Correlação negativa significativa" if matriz_correlacao.iloc[0,1] < -0.3 else "Correlação positiva significativa" if matriz_correlacao.iloc[0,1] > 0.3 else "Correlação fraca",
    estado_stats.index[estado_stats[('tempo_resolucao_dias', 'std')].argmax()],
    estado_stats[('tempo_resolucao_dias', 'std')].max(),
    estado_stats.index[estado_stats[('Nota_Avaliação', 'std')].argmin()],
    estado_stats[('Nota_Avaliação', 'std')].min(),
    "Positiva" if estado_stats[('tempo_resolucao_dias', 'mean')].corr(estado_stats[('Categoria_Serviço', 'count')]) > 0 else "Negativa",
    servico_stats.index[(servico_stats[('tempo_resolucao_dias', 'mean')] / servico_stats[('Nota_Avaliação', 'mean')]).argmin()],
    servico_stats.index[(servico_stats[('tempo_resolucao_dias', 'mean')] / servico_stats[('Nota_Avaliação', 'mean')]).argmax()],
    (servico_stats[('Nota_Avaliação', 'std')] < 1).mean() * 100,
    "Crescente" if temporal_stats['tempo_resolucao_dias'].corr(pd.Series(range(len(temporal_stats)))) > 0.3 else "Decrescente" if temporal_stats['tempo_resolucao_dias'].corr(pd.Series(range(len(temporal_stats)))) < -0.3 else "Estável",
    "Crescente" if temporal_stats['Nota_Avaliação'].corr(pd.Series(range(len(temporal_stats)))) > 0.3 else "Decrescente" if temporal_stats['Nota_Avaliação'].corr(pd.Series(range(len(temporal_stats)))) < -0.3 else "Estável",
    "Sim" if has_seasonality else "Não",
    n_clusters,
    "Tempo baixo e avaliação alta" if kmeans.cluster_centers_[0][0] < 0 and kmeans.cluster_centers_[0][1] > 0 else "Padrão médio",
    (X['cluster'] == 0).mean() * 100,
    "Existe correlação significativa entre tempo e avaliação" if abs(matriz_correlacao.iloc[0,1]) > 0.3 else "Não há correlação forte entre tempo e avaliação",
    "Há padrões claros por estado" if estado_stats[('tempo_resolucao_dias', 'std')].std() > 10 else "Comportamento uniforme entre estados",
    "Identificados grupos distintos de desempenho" if len(np.unique(X['cluster'])) >= 3 else "Comportamento homogêneo dos chamados",
    "Estabelecer metas específicas por cluster de desempenho",
    "Padronizar processos nos estados com maior variabilidade",
    "Implementar melhorias baseadas nos serviços melhor avaliados",
    "Criar sistema de monitoramento de padrões temporais",
    "Desenvolver indicadores compostos de eficiência"
)) 