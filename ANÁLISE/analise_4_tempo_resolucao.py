import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
# INÍCIO DA ANÁLISE DO TEMPO DE RESOLUÇÃO
# =============================================================================

print("\n" + "="*80)
print("ANÁLISE DO TEMPO DE RESOLUÇÃO DOS CHAMADOS")
print("="*80)

# Carregando os dados
print("\nCarregando dados...")
df = pd.read_excel('0 - BD_tratado.xlsx')

# Documentando as colunas utilizadas
print("\n# Colunas utilizadas na análise do tempo de resolução:")
print("# - dat_criacao: Data de criação do chamado")
print("# - dat_resolucao: Data de resolução do chamado")
print("# - cod_uf: Estado do chamado")
print("# - des_tipo_servico: Tipo de serviço")
print("# - des_condominio: Descrição/localização do condomínio")
print("# - des_prioridade: Prioridade do chamado")
print("# - des_status: Status do chamado")

# Convertendo datas para datetime
print("\nConvertendo colunas temporais...")
df['dat_criacao'] = pd.to_datetime(df['dat_criacao'])
df['dat_resolucao'] = pd.to_datetime(df['dat_resolucao'])

# Criando coluna de tempo de resolução em dias
print("\nCriando coluna de tempo de resolução...")
print("# Nova coluna criada:")
print("# - tempo_resolucao_dias: Diferença em dias entre data de resolução e criação")
df['tempo_resolucao_dias'] = (df['dat_resolucao'] - df['dat_criacao']).dt.total_seconds() / (24*60*60)

# Criando diretório para gráficos
Path('graficos_etapa4').mkdir(exist_ok=True)

# 1. Análise Estatística do Tempo de Resolução
print("\nAnalisando estatísticas do tempo de resolução...")
stats_tempo = df['tempo_resolucao_dias'].describe()
ausentes = df['tempo_resolucao_dias'].isnull().sum()
percentual_ausentes = (ausentes / len(df)) * 100

print("\nEstatísticas do Tempo de Resolução (em dias):")
print(stats_tempo)
print(f"\nChamados sem tempo de resolução: {ausentes} ({percentual_ausentes:.1f}%)")

# 2. Histograma do Tempo de Resolução
print("\nGerando visualizações do tempo de resolução...")
tempo_valido = df[df['tempo_resolucao_dias'] > 0]['tempo_resolucao_dias']

plt.figure(figsize=(12, 6))
plt.hist(tempo_valido[tempo_valido <= 200], bins=40, edgecolor='black')
plt.title('Distribuição do Tempo de Resolução')
plt.xlabel('Tempo (dias)')
plt.ylabel('Frequência')
plt.xlim(0, 200)
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa4/histograma_tempo_resolucao.png')
plt.close()

# 3. Boxplot do Tempo de Resolução
plt.figure(figsize=(10, 6))
plt.boxplot(tempo_valido, vert=False)
plt.title('Boxplot do Tempo de Resolução')
plt.xlabel('Tempo (dias)')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa4/boxplot_tempo_resolucao.png')
plt.close()

# 4. Gráfico de Densidade
plt.figure(figsize=(12, 6))
sns.kdeplot(data=tempo_valido, fill=True)
plt.title('Densidade do Tempo de Resolução')
plt.xlabel('Tempo (dias)')
plt.ylabel('Densidade')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa4/densidade_tempo_resolucao.png')
plt.close()

# 5. Tempo Médio por Estado
print("\nAnalisando tempo médio por estado...")
tempo_por_estado = df.groupby('cod_uf')['tempo_resolucao_dias'].agg(['mean', 'count', 'std']).round(2)
tempo_por_estado = tempo_por_estado.sort_values('mean', ascending=True)

plt.figure(figsize=(12, 6))
tempo_por_estado['mean'].plot(kind='bar')
plt.title('Tempo Médio de Resolução por Estado')
plt.xlabel('Estado')
plt.ylabel('Tempo Médio (dias)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa4/barras_tempo_medio_por_estado.png')
plt.close()

# 6. Tempo Médio por Tipo de Serviço
print("\nAnalisando tempo médio por tipo de serviço...")
tempo_por_servico = df.groupby('des_tipo_servico')['tempo_resolucao_dias'].agg(['mean', 'count', 'std']).round(2)
tempo_por_servico = tempo_por_servico[tempo_por_servico['count'] >= 10]  # Filtrando serviços com pelo menos 10 chamados
tempo_por_servico = tempo_por_servico.sort_values('mean', ascending=True)

plt.figure(figsize=(15, 6))
tempo_por_servico['mean'].plot(kind='bar')
plt.title('Tempo Médio de Resolução por Tipo de Serviço')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Tempo Médio (dias)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa4/barras_tempo_medio_por_servico.png')
plt.close()

# 7. Tempo Médio por Prioridade
print("\nAnalisando tempo médio por prioridade...")
tempo_por_prioridade = df.groupby('des_prioridade')['tempo_resolucao_dias'].agg(['mean', 'count', 'std']).round(2)
tempo_por_prioridade = tempo_por_prioridade.sort_values('mean', ascending=True)

plt.figure(figsize=(10, 6))
tempo_por_prioridade['mean'].plot(kind='bar')
plt.title('Tempo Médio de Resolução por Prioridade')
plt.xlabel('Prioridade')
plt.ylabel('Tempo Médio (dias)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa4/barras_tempo_medio_por_prioridade.png')
plt.close()

# 8. Boxplot por Prioridade
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='des_prioridade', y='tempo_resolucao_dias')
plt.title('Distribuição do Tempo de Resolução por Prioridade')
plt.xlabel('Prioridade')
plt.ylabel('Tempo (dias)')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa4/boxplot_tempo_por_prioridade.png')
plt.close()

# 9. Evolução do Tempo de Resolução ao Longo do Tempo
print("\nAnalisando evolução temporal do tempo de resolução...")
tempo_medio_mensal = df.groupby(df['dat_criacao'].dt.to_period('M'))['tempo_resolucao_dias'].mean()

plt.figure(figsize=(15, 6))
tempo_medio_mensal.plot(kind='line', marker='o')
plt.title('Evolução do Tempo Médio de Resolução')
plt.xlabel('Mês')
plt.ylabel('Tempo Médio (dias)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('graficos_etapa4/linha_evolucao_tempo_resolucao.png')
plt.close()

# 10. Heatmap de Tempo por Estado e Tipo de Serviço
print("\nGerando heatmap de tempo por estado e tipo de serviço...")
pivot_estado_servico = df.pivot_table(
    values='tempo_resolucao_dias',
    index='cod_uf',
    columns='des_tipo_servico',
    aggfunc='mean'
)

plt.figure(figsize=(15, 8))
sns.heatmap(pivot_estado_servico, cmap='YlOrRd', annot=True, fmt='.1f', cbar_kws={'label': 'Tempo Médio (dias)'})
plt.title('Heatmap: Tempo Médio de Resolução por Estado e Tipo de Serviço')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Estado')
plt.tight_layout()
plt.savefig('graficos_etapa4/heatmap_tempo_estado_servico.png')
plt.close()

# 11. Análise de Outliers
print("\nAnalisando outliers do tempo de resolução...")
q1 = tempo_valido.quantile(0.25)
q3 = tempo_valido.quantile(0.75)
iqr = q3 - q1
limite_superior = q3 + 1.5 * iqr
outliers = tempo_valido[tempo_valido > limite_superior]
percentual_outliers = (len(outliers) / len(tempo_valido)) * 100

# 12. Distribuição dos Outliers por Status
print("\nAnalisando distribuição dos outliers por status...")
status_outliers = df[df['tempo_resolucao_dias'] > limite_superior]['des_status'].value_counts()

plt.figure(figsize=(10, 6))
status_outliers.plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribuição dos Outliers por Status')
plt.axis('equal')
plt.savefig('graficos_etapa4/pizza_outliers_por_status.png')
plt.close()

# Conclusões da Análise do Tempo de Resolução
print("\n" + "="*80)
print("CONCLUSÕES DA ANÁLISE DO TEMPO DE RESOLUÇÃO")
print("="*80)

print("""
# RESUMO DA ANÁLISE DO TEMPO DE RESOLUÇÃO

## 1. Estatísticas Gerais
- Tempo médio de resolução: {:.1f} dias
- Mediana: {:.1f} dias
- Desvio padrão: {:.1f} dias
- Mínimo: {:.1f} dias
- Máximo: {:.1f} dias
- Chamados sem tempo de resolução: {:.1f}%

## 2. Análise de Outliers
- Q1 (25%): {:.1f} dias
- Q3 (75%): {:.1f} dias
- IQR: {:.1f} dias
- Limite para outliers: {:.1f} dias
- Percentual de outliers: {:.1f}%

## 3. Análise por Estado
- Estado mais rápido: {} (média de {:.1f} dias)
- Estado mais lento: {} (média de {:.1f} dias)
- Variação entre estados: {:.1f}x

## 4. Análise por Tipo de Serviço
- Serviço mais rápido: {} (média de {:.1f} dias)
- Serviço mais lento: {} (média de {:.1f} dias)
- {:.1f}% dos tipos de serviço têm média acima de 30 dias

## 5. Observações Importantes
- Existe grande variação no tempo de resolução entre diferentes estados
- Alguns tipos de serviço apresentam tempos consistentemente mais altos
- {:.1f}% dos chamados são resolvidos em até 7 dias
- {:.1f}% dos chamados levam mais de 30 dias para resolução

## 6. Recomendações
1. Investigar causas de outliers acima de {:.1f} dias
2. Estabelecer metas específicas por tipo de serviço
3. Padronizar processos nos estados com maiores tempos
4. Criar alertas para chamados que ultrapassem {:.1f} dias (percentil 90)
5. Focar melhorias nos tipos de serviço com médias acima de 30 dias
""".format(
    stats_tempo['mean'],
    stats_tempo['50%'],
    stats_tempo['std'],
    stats_tempo['min'],
    stats_tempo['max'],
    percentual_ausentes,
    q1,
    q3,
    iqr,
    limite_superior,
    percentual_outliers,
    tempo_por_estado.index[0],
    tempo_por_estado['mean'].iloc[0],
    tempo_por_estado.index[-1],
    tempo_por_estado['mean'].iloc[-1],
    tempo_por_estado['mean'].iloc[-1] / tempo_por_estado['mean'].iloc[0],
    tempo_por_servico.index[0],
    tempo_por_servico['mean'].iloc[0],
    tempo_por_servico.index[-1],
    tempo_por_servico['mean'].iloc[-1],
    (tempo_por_servico['mean'] > 30).mean() * 100,
    (tempo_valido <= 7).mean() * 100,
    (tempo_valido > 30).mean() * 100,
    limite_superior,
    tempo_valido.quantile(0.90)
)) 