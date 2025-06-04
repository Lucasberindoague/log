import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from pathlib import Path

# Configurações gerais para os gráficos
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Configurando o display do pandas para mostrar mais colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# =============================================================================
# INÍCIO DA ANÁLISE REGIONAL
# =============================================================================

print("\n" + "="*80)
print("ANÁLISE REGIONAL DOS CHAMADOS")
print("="*80)

# Carregando os dados
print("\nCarregando dados...")
df = pd.read_excel('BD/0 - BD_tratado.xlsx')

# Documentando as colunas utilizadas
print("\n# Colunas utilizadas na análise regional:")
print("# - cod_uf: Estado do chamado")
print("# - des_condominio: Descrição/localização do condomínio")
print("# - dat_criacao: Data de criação do chamado")
print("# - dat_resolucao: Data de resolução do chamado")

# Convertendo datas para cálculo do tempo de resolução
df['Data_Criação'] = pd.to_datetime(df['Data_Criação'])
df['Data_Resolução'] = pd.to_datetime(df['Data_Resolução'])
df['Tempo_Resolução_Horas'] = (df['Data_Resolução'] - df['Data_Criação']).dt.total_seconds() / (24*60*60)  # em dias

# Criando diretório para gráficos
Path('GRÁFICOS/graficos_etapa3').mkdir(parents=True, exist_ok=True)

# Análise da distribuição por estado
print("\nAnalisando distribuição por estado...")
estado_counts = df['Estado_UF'].value_counts()
total_chamados = len(df)

# Preparando os dados para o mapa de calor
df['Data_Criação'] = pd.to_datetime(df['Data_Criação'])
df['Mês'] = df['Data_Criação'].dt.strftime('%Y-%m')

# Gerando o mapa de calor da distribuição temporal por estado
pivot_estado_mes = df.pivot_table(
    index='Estado_UF',
    columns='Mês',
    values='Código_Chamado',
    aggfunc='count',
    fill_value=0
)

# Normalizando os valores por estado
pivot_estado_mes_norm = pivot_estado_mes.div(pivot_estado_mes.sum(axis=1), axis=0) * 100

plt.figure(figsize=(15, 8))
sns.heatmap(pivot_estado_mes_norm, 
           cmap='YlOrRd',
           cbar_kws={'label': 'Percentual de Chamados (%)'},
           fmt='.1f')
plt.title('Mapa de Calor - Concentração de Chamados por Estado')
plt.xlabel('Mês')
plt.ylabel('Estado')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/mapa_distribuicao_estados.png', dpi=300, bbox_inches='tight')
plt.close()

# Gerando gráfico de barras da distribuição por estado
plt.figure(figsize=(12, 6))
estado_counts.plot(kind='bar')
plt.title('Distribuição dos Chamados por Estado')
plt.xlabel('Estado')
plt.ylabel('Número de Chamados')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/barras_distribuicao_estados.png', dpi=300, bbox_inches='tight')
plt.close()

# 1. Análise por Estado
print("\nAnalisando distribuição por estado...")
chamados_por_estado = df['Estado_UF'].value_counts()

# Gráfico de barras dos chamados por estado
plt.figure(figsize=(12, 6))
chamados_por_estado.plot(kind='bar')
plt.title('Quantidade de Chamados por Estado')
plt.xlabel('Estado')
plt.ylabel('Quantidade de Chamados')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/barras_chamados_por_estado.png')
plt.close()

# Gráfico de pizza dos chamados por estado
plt.figure(figsize=(10, 10))
plt.pie(chamados_por_estado, labels=chamados_por_estado.index, autopct='%1.1f%%')
plt.title('Distribuição Percentual de Chamados por Estado')
plt.axis('equal')
plt.savefig('GRÁFICOS/graficos_etapa3/pizza_chamados_por_estado.png')
plt.close()

# 2. Análise por Condomínio
print("\nAnalisando distribuição por condomínio...")
chamados_por_condominio = df['Condomínio'].value_counts().head(10)

plt.figure(figsize=(15, 6))
chamados_por_condominio.plot(kind='bar')
plt.title('Top 10 Condomínios com Maior Volume de Chamados')
plt.xlabel('Condomínio')
plt.ylabel('Quantidade de Chamados')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/barras_top_10_condominios.png')
plt.close()

# 3. Análise do Tempo de Resolução por Estado
print("\nAnalisando tempo de resolução por estado...")
tempo_medio_por_estado = df.groupby('Estado_UF')['Tempo_Resolução_Horas'].agg(['mean', 'std', 'count']).round(2)
tempo_medio_por_estado = tempo_medio_por_estado.sort_values('mean', ascending=True)

# Gráfico de barras do tempo médio por estado
plt.figure(figsize=(12, 6))
tempo_medio_por_estado['mean'].plot(kind='bar')
plt.title('Tempo Médio de Resolução por Estado')
plt.xlabel('Estado')
plt.ylabel('Tempo Médio (dias)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/barras_tempo_medio_por_estado.png')
plt.close()

# Boxplot do tempo de resolução por estado
plt.figure(figsize=(15, 6))
sns.boxplot(data=df, x='Estado_UF', y='Tempo_Resolução_Horas')
plt.title('Distribuição do Tempo de Resolução por Estado')
plt.xlabel('Estado')
plt.ylabel('Tempo de Resolução (dias)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/boxplot_tempo_por_estado.png')
plt.close()

# 4. Análise do Tempo de Resolução por Condomínio
print("\nAnalisando tempo de resolução por condomínio...")
tempo_medio_por_condominio = df.groupby('Condomínio')['Tempo_Resolução_Horas'].agg(['mean', 'count'])
tempo_medio_por_condominio = tempo_medio_por_condominio[tempo_medio_por_condominio['count'] >= 10]  # Filtrando condomínios com pelo menos 10 chamados
tempo_medio_por_condominio = tempo_medio_por_condominio.sort_values('mean', ascending=True)

# Top 10 condomínios com menor e maior tempo médio
top_10_rapidos = tempo_medio_por_condominio.head(10)
top_10_lentos = tempo_medio_por_condominio.tail(10)

# Gráfico de tempo médio para os extremos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

top_10_rapidos['mean'].plot(kind='bar', ax=ax1)
ax1.set_title('Top 10 Condomínios com Menor Tempo de Resolução')
ax1.set_xlabel('Condomínio')
ax1.set_ylabel('Tempo Médio (dias)')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True)

top_10_lentos['mean'].plot(kind='bar', ax=ax2)
ax2.set_title('Top 10 Condomínios com Maior Tempo de Resolução')
ax2.set_xlabel('Condomínio')
ax2.set_ylabel('Tempo Médio (dias)')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True)

plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/barras_tempo_medio_condominios_extremos.png')
plt.close()

# 5. Heatmap do Tempo de Resolução por Estado e Mês
print("\nGerando heatmap do tempo de resolução por estado e mês...")
pivot_estado_mes = df.pivot_table(
    values='Tempo_Resolução_Horas',
    index='Estado_UF',
    columns=df['Data_Criação'].dt.to_period('M'),
    aggfunc='mean'
)

plt.figure(figsize=(15, 8))
sns.heatmap(pivot_estado_mes, cmap='YlOrRd', annot=True, fmt='.1f', cbar_kws={'label': 'Tempo Médio (dias)'})
plt.title('Heatmap: Tempo Médio de Resolução por Estado e Mês')
plt.xlabel('Mês')
plt.ylabel('Estado')
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/heatmap_tempo_estado_mes.png')
plt.close()

# 6. Análise de Volume por Estado e Mês
print("\nGerando heatmap do volume de chamados por estado e mês...")
pivot_volume_estado_mes = df.pivot_table(
    values='Tempo_Resolução_Horas',
    index='Estado_UF',
    columns=df['Data_Criação'].dt.to_period('M'),
    aggfunc='count'
)

plt.figure(figsize=(15, 8))
sns.heatmap(pivot_volume_estado_mes, cmap='YlOrRd', annot=True, fmt='g', cbar_kws={'label': 'Quantidade de Chamados'})
plt.title('Heatmap: Volume de Chamados por Estado e Mês')
plt.xlabel('Mês')
plt.ylabel('Estado')
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/heatmap_volume_estado_mes.png')
plt.close()

# 7. Análise de Eficiência Regional
print("\nAnalisando eficiência regional...")
eficiencia_regional = df.groupby('Estado_UF').agg({
    'Tempo_Resolução_Horas': ['mean', 'count'],
    'Código_Chamado': 'count'
}).round(2)

eficiencia_regional.columns = ['tempo_medio', 'chamados_resolvidos', 'total_chamados']
eficiencia_regional['taxa_resolucao'] = (eficiencia_regional['chamados_resolvidos'] / eficiencia_regional['total_chamados'] * 100).round(2)

# Gráfico de dispersão da eficiência regional
plt.figure(figsize=(12, 8))
plt.scatter(eficiencia_regional['tempo_medio'], eficiencia_regional['taxa_resolucao'])
for i, estado in enumerate(eficiencia_regional.index):
    plt.annotate(estado, (eficiencia_regional['tempo_medio'][i], eficiencia_regional['taxa_resolucao'][i]))
plt.title('Relação entre Tempo Médio e Taxa de Resolução por Estado')
plt.xlabel('Tempo Médio de Resolução (dias)')
plt.ylabel('Taxa de Resolução (%)')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa3/dispersao_eficiencia_regional.png')
plt.close()

# Análise específica de Minas Gerais
print("\nAnálise específica de Minas Gerais...")
mg_stats = df[df['Estado_UF'] == 'MG']['Tempo_Resolução_Horas'].describe()
outros_stats = df[df['Estado_UF'] != 'MG']['Tempo_Resolução_Horas'].describe()

# Conclusões da Análise Regional
print("\n" + "="*80)
print("CONCLUSÕES DA ANÁLISE REGIONAL")
print("="*80)

print("""
# RESUMO DA ANÁLISE REGIONAL DOS CHAMADOS

## 1. Distribuição por Estado
- Total de estados atendidos: {}
- Estado com maior volume: {} ({:.1f}% dos chamados)
- Estado com menor volume: {} ({:.1f}% dos chamados)

## 2. Análise dos Condomínios
- Total de condomínios atendidos: {}
- Condomínio com maior volume: {} ({} chamados)
- Top 10 condomínios representam {:.1f}% do total de chamados

## 3. Tempo de Resolução por Estado
- Estado mais eficiente: {} (média de {:.1f} dias)
- Estado menos eficiente: {} (média de {:.1f} dias)
- Minas Gerais (sede):
  * Tempo médio: {:.1f} dias
  * Mediana: {:.1f} dias
  * Comparação com média geral: {:.1f}% {}

## 4. Tempo de Resolução por Condomínio
- Condomínio mais eficiente: {} (média de {:.1f} dias)
- Condomínio menos eficiente: {} (média de {:.1f} dias)
- {:.1f}% dos condomínios têm tempo médio abaixo de 30 dias

## 5. Observações Importantes
- A análise considera apenas condomínios com 10 ou mais chamados para médias confiáveis
- Existe grande variação no tempo de resolução entre estados
- MG apresenta desempenho {} que a média nacional
- Alguns condomínios apresentam tempos muito acima da média geral

## 6. Recomendações
1. Investigar as práticas do estado {} para replicar sua eficiência
2. Avaliar processos nos estados com tempo médio superior a {} dias
3. Estabelecer metas regionais considerando as particularidades de cada estado
4. Priorizar melhorias nos {} condomínios com maiores tempos de resolução
5. Implementar monitoramento específico para unidades com tempo médio > {} dias
""".format(
    len(chamados_por_estado),
    chamados_por_estado.index[0],
    (chamados_por_estado.iloc[0] / len(df)) * 100,
    chamados_por_estado.index[-1],
    (chamados_por_estado.iloc[-1] / len(df)) * 100,
    df['Condomínio'].nunique(),
    chamados_por_condominio.index[0],
    chamados_por_condominio.iloc[0],
    (chamados_por_condominio.sum() / len(df)) * 100,
    tempo_medio_por_estado.index[0],
    tempo_medio_por_estado['mean'].iloc[0],
    tempo_medio_por_estado.index[-1],
    tempo_medio_por_estado['mean'].iloc[-1],
    mg_stats['mean'],
    mg_stats['50%'],
    ((mg_stats['mean'] / outros_stats['mean']) - 1) * 100,
    'acima' if mg_stats['mean'] > outros_stats['mean'] else 'abaixo',
    top_10_rapidos.index[0],
    top_10_rapidos['mean'].iloc[0],
    top_10_lentos.index[-1],
    top_10_lentos['mean'].iloc[-1],
    (tempo_medio_por_condominio[tempo_medio_por_condominio['mean'] < 30].shape[0] / tempo_medio_por_condominio.shape[0]) * 100,
    'inferior' if mg_stats['mean'] < outros_stats['mean'] else 'superior',
    tempo_medio_por_estado.index[0],
    tempo_medio_por_estado['mean'].quantile(0.75),
    len(top_10_lentos),
    tempo_medio_por_estado['mean'].quantile(0.75)
)) 