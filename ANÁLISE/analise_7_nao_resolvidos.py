import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

# Configurações gerais para os gráficos
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Configurando o display do pandas para mostrar mais colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# =============================================================================
# INÍCIO DA ANÁLISE DE CHAMADOS NÃO RESOLVIDOS
# =============================================================================

print("\n" + "="*80)
print("ANÁLISE DE CHAMADOS NÃO RESOLVIDOS")
print("="*80)

# Carregando os dados
print("\nCarregando dados...")
df = pd.read_excel('../BD/0 - BD_tratado.xlsx')

# Documentando as colunas utilizadas
print("\n# Colunas utilizadas na análise de chamados não resolvidos:")
print("# - dat_criacao: Data de criação do chamado")
print("# - dat_resolucao: Data de resolução do chamado (nula para chamados em aberto)")
print("# - cod_uf: Estado do chamado")
print("# - des_tipo_servico: Tipo de serviço")
print("# - des_condominio: Descrição/localização do condomínio")
print("# - des_prioridade: Prioridade do chamado")
print("# - des_status: Status do chamado")
print("# - des_assunto: Assunto do chamado")

# Convertendo datas
df['Data_Criação'] = pd.to_datetime(df['Data_Criação'])
df['Data_Resolução'] = pd.to_datetime(df['Data_Resolução'])

# Data atual para cálculo do tempo em aberto
data_atual = pd.Timestamp.now()

# 1. Identificação dos chamados não resolvidos
print("\nIdentificando chamados não resolvidos...")
df_nao_resolvidos = df[df['Data_Resolução'].isnull()]
total_nao_resolvidos = len(df_nao_resolvidos)
percentual_nao_resolvidos = (total_nao_resolvidos / len(df)) * 100

print(f"\nTotal de chamados não resolvidos: {total_nao_resolvidos}")
print(f"Percentual de chamados não resolvidos: {percentual_nao_resolvidos:.1f}%")

# 2. Cálculo do tempo em aberto
print("\nCalculando tempo em aberto...")
df_nao_resolvidos['tempo_em_aberto_dias'] = (data_atual - df_nao_resolvidos['Data_Criação']).dt.total_seconds() / (24*60*60)

# Estatísticas do tempo em aberto
stats_tempo_aberto = df_nao_resolvidos['tempo_em_aberto_dias'].describe()
print("\nEstatísticas do tempo em aberto (em dias):")
print(stats_tempo_aberto)

# Criando diretório para gráficos
Path('graficos_etapa7').mkdir(exist_ok=True)

# 3. Distribuição por Estado
print("\nAnalisando distribuição por estado...")
estado_nao_resolvidos = df_nao_resolvidos['Estado_UF'].value_counts()
estado_nao_resolvidos_pct = (estado_nao_resolvidos / total_nao_resolvidos * 100).round(2)

plt.figure(figsize=(12, 6))
estado_nao_resolvidos.plot(kind='bar')
plt.title('Distribuição de Chamados Não Resolvidos por Estado')
plt.xlabel('Estado')
plt.ylabel('Quantidade de Chamados')
plt.grid(True)
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/barras_nao_resolvidos_por_estado.png')
plt.close()

# Gráfico de pizza da distribuição por estado
plt.figure(figsize=(10, 10))
plt.pie(estado_nao_resolvidos_pct, labels=estado_nao_resolvidos.index, autopct='%1.1f%%')
plt.title('Distribuição Percentual de Chamados Não Resolvidos por Estado')
plt.axis('equal')
plt.savefig('../GRÁFICOS/graficos_etapa7/pizza_nao_resolvidos_por_estado.png')
plt.close()

# 4. Distribuição por Tipo de Serviço
print("\nAnalisando distribuição por tipo de serviço...")
servico_nao_resolvidos = df_nao_resolvidos['Categoria_Serviço'].value_counts()
servico_nao_resolvidos_pct = (servico_nao_resolvidos / total_nao_resolvidos * 100).round(2)

plt.figure(figsize=(15, 6))
servico_nao_resolvidos.head(10).plot(kind='bar')
plt.title('Top 10 Tipos de Serviço com Mais Chamados Não Resolvidos')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Quantidade de Chamados')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/barras_nao_resolvidos_por_servico.png')
plt.close()

# 5. Distribuição por Prioridade
print("\nAnalisando distribuição por prioridade...")
prioridade_nao_resolvidos = df_nao_resolvidos['Prioridade'].value_counts()
prioridade_nao_resolvidos_pct = (prioridade_nao_resolvidos / total_nao_resolvidos * 100).round(2)

plt.figure(figsize=(10, 6))
prioridade_nao_resolvidos.plot(kind='bar')
plt.title('Distribuição de Chamados Não Resolvidos por Prioridade')
plt.xlabel('Prioridade')
plt.ylabel('Quantidade de Chamados')
plt.grid(True)
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/barras_nao_resolvidos_por_prioridade.png')
plt.close()

# 6. Tempo Médio em Aberto por Estado
print("\nAnalisando tempo médio em aberto por estado...")
# Excluindo a categoria "X"
df_nao_resolvidos_filtered = df_nao_resolvidos[df_nao_resolvidos['Estado_UF'] != 'X']
tempo_medio_estado = df_nao_resolvidos_filtered.groupby('Estado_UF')['tempo_em_aberto_dias'].agg(['mean', 'count']).round(2)
tempo_medio_estado = tempo_medio_estado.sort_values('mean', ascending=False)

plt.figure(figsize=(12, 6))
tempo_medio_estado['mean'].plot(kind='bar')
plt.title('Tempo Médio em Aberto por Estado')
plt.xlabel('Estado')
plt.ylabel('Tempo Médio (dias)')
plt.grid(True)
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/barras_tempo_medio_aberto_estado.png')
plt.close()

# 7. Tempo Médio em Aberto por Tipo de Serviço
print("\nAnalisando tempo médio em aberto por tipo de serviço...")
# Excluindo a categoria "X"
df_nao_resolvidos_filtered = df_nao_resolvidos[df_nao_resolvidos['Categoria_Serviço'] != 'X']
tempo_medio_servico = df_nao_resolvidos_filtered.groupby('Categoria_Serviço')['tempo_em_aberto_dias'].agg(['mean', 'count']).round(2)
tempo_medio_servico = tempo_medio_servico[tempo_medio_servico['count'] >= 5]  # Filtrando serviços com pelo menos 5 chamados
tempo_medio_servico = tempo_medio_servico.sort_values('mean', ascending=False)

plt.figure(figsize=(15, 6))
tempo_medio_servico['mean'].head(10).plot(kind='bar')
plt.title('Top 10 Tipos de Serviço com Maior Tempo em Aberto')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Tempo Médio (dias)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/barras_tempo_medio_aberto_servico.png')
plt.close()

# 8. Tempo Médio em Aberto por Prioridade
print("\nAnalisando tempo médio em aberto por prioridade...")
tempo_medio_prioridade = df_nao_resolvidos.groupby('Prioridade')['tempo_em_aberto_dias'].agg(['mean', 'count']).round(2)
tempo_medio_prioridade = tempo_medio_prioridade.sort_values('mean', ascending=False)

plt.figure(figsize=(10, 6))
tempo_medio_prioridade['mean'].plot(kind='bar')
plt.title('Tempo Médio em Aberto por Prioridade')
plt.xlabel('Prioridade')
plt.ylabel('Tempo Médio (dias)')
plt.grid(True)
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/barras_tempo_medio_aberto_prioridade.png')
plt.close()

# 9. Análise de Chamados Muito Antigos
print("\nIdentificando chamados muito antigos...")
limite_dias = 90  # Definindo chamados com mais de 90 dias como muito antigos
chamados_antigos = df_nao_resolvidos[df_nao_resolvidos['tempo_em_aberto_dias'] > limite_dias]
total_antigos = len(chamados_antigos)
percentual_antigos = (total_antigos / total_nao_resolvidos) * 100

print(f"\nChamados em aberto há mais de {limite_dias} dias: {total_antigos}")
print(f"Percentual do total de não resolvidos: {percentual_antigos:.1f}%")

# 10. Distribuição dos Chamados Antigos por Prioridade
print("\nAnalisando distribuição dos chamados antigos por prioridade...")
antigos_por_prioridade = chamados_antigos['Prioridade'].value_counts()
antigos_por_prioridade_pct = (antigos_por_prioridade / total_antigos * 100).round(2)

plt.figure(figsize=(10, 6))
antigos_por_prioridade.plot(kind='bar')
plt.title(f'Distribuição dos Chamados > {limite_dias} dias por Prioridade')
plt.xlabel('Prioridade')
plt.ylabel('Quantidade de Chamados')
plt.grid(True)
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/barras_antigos_por_prioridade.png')
plt.close()

# 11. Evolução Temporal dos Chamados Não Resolvidos
print("\nAnalisando evolução temporal dos chamados não resolvidos...")
df_nao_resolvidos['mes_criacao'] = df_nao_resolvidos['Data_Criação'].dt.to_period('M')
evolucao_temporal = df_nao_resolvidos.groupby('mes_criacao').size()

plt.figure(figsize=(15, 6))
evolucao_temporal.plot(kind='line', marker='o')
plt.title('Evolução Temporal dos Chamados Não Resolvidos')
plt.xlabel('Mês de Criação')
plt.ylabel('Quantidade de Chamados')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/linha_evolucao_temporal.png')
plt.close()

# 12. Heatmap de Chamados Não Resolvidos por Estado e Tipo de Serviço
print("\nGerando heatmap de chamados não resolvidos...")
heatmap_data = pd.crosstab(df_nao_resolvidos['Estado_UF'], df_nao_resolvidos['Categoria_Serviço'])

plt.figure(figsize=(15, 8))
sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt='d')
plt.title('Heatmap: Chamados Não Resolvidos por Estado e Tipo de Serviço')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Estado')
plt.tight_layout()
plt.savefig('../GRÁFICOS/graficos_etapa7/heatmap_estado_servico.png')
plt.close()

# Conclusões da Análise de Chamados Não Resolvidos
print("\n" + "="*80)
print("CONCLUSÕES DA ANÁLISE DE CHAMADOS NÃO RESOLVIDOS")
print("="*80)

print("""
# RESUMO DA ANÁLISE DE CHAMADOS NÃO RESOLVIDOS

## 1. Visão Geral
- Total de chamados não resolvidos: {}
- Percentual da base total: {:.1f}%
- Tempo médio em aberto: {:.1f} dias
- Chamado mais antigo em aberto: {:.1f} dias

## 2. Distribuição Regional
- Estado com mais chamados em aberto: {} ({} chamados, {:.1f}%)
- Estado com menos chamados em aberto: {} ({} chamados, {:.1f}%)
- Estado com maior tempo médio em aberto: {} ({:.1f} dias)
- Estados com mais de 10% dos chamados: {}

## 3. Análise por Tipo de Serviço
- Serviço com mais chamados em aberto: {} ({} chamados)
- Serviço com maior tempo médio em aberto: {} ({:.1f} dias)
- {:.1f}% dos tipos de serviço têm média acima de 30 dias em aberto
- Serviços mais críticos: {}

## 4. Análise por Prioridade
- Prioridade com mais chamados: {} ({:.1f}%)
- Prioridade com maior tempo médio: {} ({:.1f} dias)
- Distribuição das prioridades: {}
- Tempo médio por prioridade: {}

## 5. Chamados Críticos
- Chamados em aberto há mais de {} dias: {} ({:.1f}%)
- Tipo de serviço com mais chamados críticos: {}
- Estado com mais chamados críticos: {}
- Prioridade com mais chamados críticos: {}

## 6. Evolução Temporal
- Tendência geral: {}
- Mês com mais chamados: {}
- Mês com menos chamados: {}
- Variação mensal média: {:.1f}%

## 7. Observações Importantes
- {}
- {}
- {}
- {}

## 8. Recomendações
1. {}
2. {}
3. {}
4. {}
5. {}
""".format(
    total_nao_resolvidos,
    percentual_nao_resolvidos,
    stats_tempo_aberto['mean'],
    stats_tempo_aberto['max'],
    estado_nao_resolvidos.index[0],
    estado_nao_resolvidos.iloc[0],
    estado_nao_resolvidos_pct.iloc[0],
    estado_nao_resolvidos.index[-1],
    estado_nao_resolvidos.iloc[-1],
    estado_nao_resolvidos_pct.iloc[-1],
    tempo_medio_estado.index[0],
    tempo_medio_estado['mean'].iloc[0],
    estado_nao_resolvidos_pct[estado_nao_resolvidos_pct > 10].index.tolist(),
    servico_nao_resolvidos.index[0],
    servico_nao_resolvidos.iloc[0],
    tempo_medio_servico.index[0],
    tempo_medio_servico['mean'].iloc[0],
    (tempo_medio_servico['mean'] > 30).mean() * 100,
    servico_nao_resolvidos.head(3).index.tolist(),
    prioridade_nao_resolvidos.index[0],
    prioridade_nao_resolvidos_pct.iloc[0],
    tempo_medio_prioridade.index[0],
    tempo_medio_prioridade['mean'].iloc[0],
    dict(prioridade_nao_resolvidos_pct),
    dict(tempo_medio_prioridade['mean']),
    limite_dias,
    total_antigos,
    percentual_antigos,
    chamados_antigos['Categoria_Serviço'].mode()[0],
    chamados_antigos['Estado_UF'].mode()[0],
    chamados_antigos['Prioridade'].mode()[0],
    "Tendência de aumento" if evolucao_temporal.iloc[-1] > evolucao_temporal.iloc[0] else "Tendência de redução",
    evolucao_temporal.index[evolucao_temporal.argmax()],
    evolucao_temporal.index[evolucao_temporal.argmin()],
    evolucao_temporal.pct_change().std() * 100,
    "Existe concentração significativa em poucos estados" if estado_nao_resolvidos_pct.iloc[0] > 30 else "Distribuição relativamente uniforme entre estados",
    "Tempo em aberto varia significativamente por tipo de serviço" if tempo_medio_servico['mean'].std() > 30 else "Tempo em aberto é relativamente uniforme entre serviços",
    "Alto percentual de chamados muito antigos" if percentual_antigos > 20 else "Baixo percentual de chamados muito antigos",
    "Prioridade não está sendo respeitada nos tempos de atendimento" if tempo_medio_prioridade.index[0] == 'high' else "Sistema de priorização está funcionando adequadamente",
    "Criar força-tarefa para resolver chamados com mais de {} dias".format(limite_dias),
    "Implementar gestão específica para os estados mais críticos",
    "Estabelecer SLAs por prioridade e monitorar cumprimento",
    "Desenvolver plano de ação para tipos de serviço mais problemáticos",
    "Criar sistema de alerta para chamados próximos ao limite de tempo"
)) 