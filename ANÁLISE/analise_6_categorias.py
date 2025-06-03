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
# INÍCIO DA ANÁLISE DE CATEGORIAS DOS CHAMADOS
# =============================================================================

print("\n" + "="*80)
print("ANÁLISE DE CATEGORIAS DOS CHAMADOS")
print("="*80)

# Carregando os dados
print("\nCarregando dados...")
df = pd.read_excel('../BD/0 - BD_tratado.xlsx')

# Documentando as colunas utilizadas
print("\n# Colunas utilizadas na análise de categorias:")
print("# - des_tipo_servico: Tipo de serviço prestado")
print("# - des_assunto: Assunto do chamado")
print("# - des_classificacao: Classificação do chamado")
print("# - cod_uf: Estado do chamado")
print("# - vlr_nota_avaliacao_cliente_atendimento: Nota dada pelo cliente (1 a 5)")

# Convertendo datas e calculando tempo de resolução
df['Data_Criação'] = pd.to_datetime(df['Data_Criação'])
df['Data_Resolução'] = pd.to_datetime(df['Data_Resolução'])
df['tempo_resolucao_dias'] = (df['Data_Resolução'] - df['Data_Criação']).dt.total_seconds() / (24*60*60)

# Criando diretório para gráficos
Path('graficos_etapa6').mkdir(exist_ok=True)

# 1. Análise por Tipo de Serviço
print("\nAnalisando distribuição por tipo de serviço...")
tipo_servico = df['Categoria_Serviço'].value_counts()
tipo_servico_pct = (tipo_servico / len(df) * 100).round(2)

print("\nFrequência por tipo de serviço:")
for tipo, freq in tipo_servico.head(10).items():
    print(f"{tipo}: {freq} chamados ({tipo_servico_pct[tipo]:.1f}%)")

# Gráfico dos 10 tipos de serviço mais frequentes
plt.figure(figsize=(15, 6))
tipo_servico.head(10).plot(kind='bar')
plt.title('10 Tipos de Serviço Mais Frequentes')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Quantidade de Chamados')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa6/barras_top_10_tipos_servico.png')
plt.close()

# 2. Análise por Assunto
print("\nAnalisando distribuição por assunto...")
assunto = df['Assunto'].value_counts()
assunto_pct = (assunto / len(df) * 100).round(2)

print("\nFrequência por assunto:")
for ass, freq in assunto.head(10).items():
    print(f"{ass}: {freq} chamados ({assunto_pct[ass]:.1f}%)")

# Gráfico dos 10 assuntos mais frequentes
plt.figure(figsize=(15, 6))
assunto.head(10).plot(kind='bar')
plt.title('10 Assuntos Mais Frequentes')
plt.xlabel('Assunto')
plt.ylabel('Quantidade de Chamados')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa6/barras_top_10_assuntos.png')
plt.close()

# 3. Análise do Tempo Médio de Resolução por Categoria
print("\nAnalisando tempo médio de resolução por categoria...")

# Por tipo de serviço
tempo_medio_servico = df.groupby('Categoria_Serviço')['tempo_resolucao_dias'].agg(['mean', 'count']).round(2)
tempo_medio_servico = tempo_medio_servico[tempo_medio_servico['count'] >= 10]  # Filtrando categorias com pelo menos 10 chamados
tempo_medio_servico = tempo_medio_servico.sort_values('mean', ascending=False)

plt.figure(figsize=(15, 6))
tempo_medio_servico['mean'].head(10).plot(kind='bar')
plt.title('Tempo Médio de Resolução por Tipo de Serviço (Top 10)')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Tempo Médio (dias)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa6/barras_tempo_medio_por_servico.png')
plt.close()

# 4. Análise da Avaliação Média por Categoria
print("\nAnalisando avaliação média por categoria...")

# Filtrando avaliações válidas (1 a 5)
df_valid = df[df['Nota_Avaliação'].between(1, 5)]

# Por tipo de serviço
aval_media_servico = df_valid.groupby('Categoria_Serviço')['Nota_Avaliação'].agg(['mean', 'count']).round(2)
aval_media_servico = aval_media_servico[aval_media_servico['count'] >= 10]  # Filtrando categorias com pelo menos 10 avaliações
aval_media_servico = aval_media_servico.sort_values('mean', ascending=False)

plt.figure(figsize=(15, 6))
aval_media_servico['mean'].head(10).plot(kind='bar')
plt.title('Avaliação Média por Tipo de Serviço (Top 10)')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Avaliação Média')
plt.axhline(y=df_valid['Nota_Avaliação'].mean(), color='r', linestyle='--', label='Média Geral')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa6/barras_avaliacao_media_por_servico.png')
plt.close()

# 5. Análise Cruzada: Tipo de Serviço por Estado
print("\nAnalisando distribuição de tipos de serviço por estado...")
servico_estado = pd.crosstab(df['Categoria_Serviço'], df['Estado_UF'])
servico_estado_pct = servico_estado.div(servico_estado.sum(axis=0), axis=1) * 100

# Heatmap dos tipos de serviço mais frequentes por estado
plt.figure(figsize=(15, 8))
sns.heatmap(servico_estado_pct.head(10), annot=True, fmt='.1f', cmap='YlOrRd')
plt.title('Distribuição dos 10 Tipos de Serviço Mais Frequentes por Estado (%)')
plt.xlabel('Estado')
plt.ylabel('Tipo de Serviço')
plt.tight_layout()
plt.savefig('graficos_etapa6/heatmap_servico_estado.png')
plt.close()

# 6. Análise de Correlação: Tempo de Resolução vs Volume
print("\nAnalisando correlação entre volume e tempo de resolução...")
correlacao_volume_tempo = pd.DataFrame({
    'volume': tipo_servico,
    'tempo_medio': tempo_medio_servico['mean']
}).dropna()

plt.figure(figsize=(10, 6))
plt.scatter(correlacao_volume_tempo['volume'], correlacao_volume_tempo['tempo_medio'], alpha=0.5)
plt.title('Correlação entre Volume e Tempo Médio de Resolução')
plt.xlabel('Volume de Chamados')
plt.ylabel('Tempo Médio (dias)')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa6/dispersao_correlacao_volume_tempo.png')
plt.close()

# 7. Análise de Sazonalidade por Categoria
print("\nAnalisando sazonalidade por categoria...")
df['mes'] = df['Data_Criação'].dt.month
servico_mes = pd.crosstab(df['Categoria_Serviço'], df['mes'])
servico_mes_pct = servico_mes.div(servico_mes.sum(axis=0), axis=1) * 100

# Heatmap da sazonalidade dos tipos de serviço
plt.figure(figsize=(15, 8))
sns.heatmap(servico_mes_pct.head(10), annot=True, fmt='.1f', cmap='YlOrRd')
plt.title('Sazonalidade dos 10 Tipos de Serviço Mais Frequentes (%)')
plt.xlabel('Mês')
plt.ylabel('Tipo de Serviço')
plt.tight_layout()
plt.savefig('graficos_etapa6/heatmap_sazonalidade_servico.png')
plt.close()

# 8. Análise de Complexidade por Categoria
print("\nAnalisando complexidade por categoria...")
complexidade = df.groupby('Categoria_Serviço').agg({
    'tempo_resolucao_dias': ['mean', 'std'],
    'Assunto': 'nunique',
    'Estado_UF': 'nunique'
}).round(2)

complexidade.columns = ['tempo_medio', 'tempo_std', 'num_assuntos', 'num_estados']
complexidade = complexidade.sort_values('tempo_medio', ascending=False)

# Gráfico de dispersão da complexidade
plt.figure(figsize=(12, 6))
plt.scatter(complexidade['num_assuntos'], complexidade['tempo_medio'], 
           s=complexidade['num_estados']*50, alpha=0.5)
plt.title('Complexidade por Tipo de Serviço')
plt.xlabel('Número de Assuntos Diferentes')
plt.ylabel('Tempo Médio de Resolução (dias)')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos_etapa6/dispersao_complexidade_servico.png')
plt.close()

# Conclusões da Análise de Categorias
print("\n" + "="*80)
print("CONCLUSÕES DA ANÁLISE DE CATEGORIAS")
print("="*80)

print("""
# RESUMO DA ANÁLISE DE CATEGORIAS DOS CHAMADOS

## 1. Distribuição por Tipo de Serviço
- Total de tipos de serviço: {}
- Tipo mais frequente: {} ({:.1f}% dos chamados)
- Tipo menos frequente: {} ({:.1f}% dos chamados)
- Top 3 tipos representam {:.1f}% do total

## 2. Distribuição por Assunto
- Total de assuntos distintos: {}
- Assunto mais frequente: {} ({:.1f}% dos chamados)
- Assunto menos frequente: {} ({:.1f}% dos chamados)
- Top 3 assuntos representam {:.1f}% do total

## 3. Tempo de Resolução por Categoria
- Categoria mais rápida: {} (média {:.1f} dias)
- Categoria mais lenta: {} (média {:.1f} dias)
- {:.1f}% das categorias têm média acima de 30 dias

## 4. Avaliação por Categoria
- Categoria melhor avaliada: {} (média {:.2f})
- Categoria pior avaliada: {} (média {:.2f})
- {:.1f}% das categorias têm avaliação média acima de 4.0

## 5. Análise Regional
- Estado com maior diversidade de serviços: {}
- Estado com menor diversidade de serviços: {}
- Categoria mais uniforme entre estados: {}

## 6. Análise de Sazonalidade
- Mês com maior volume: {}
- Mês com menor volume: {}
- Categorias com maior variação sazonal: {}

## 7. Análise de Complexidade
- Categoria mais complexa: {}
- Categoria mais simples: {}
- Correlação volume vs tempo: {:.3f}

## 8. Observações Importantes
- {}
- {}
- {}
- {}

## 9. Recomendações
1. {}
2. {}
3. {}
4. {}
5. {}
""".format(
    len(tipo_servico),
    tipo_servico.index[0],
    tipo_servico_pct.iloc[0],
    tipo_servico.index[-1],
    tipo_servico_pct.iloc[-1],
    tipo_servico_pct.head(3).sum(),
    len(assunto),
    assunto.index[0],
    assunto_pct.iloc[0],
    assunto.index[-1],
    assunto_pct.iloc[-1],
    assunto_pct.head(3).sum(),
    tempo_medio_servico.index[-1],
    tempo_medio_servico['mean'].iloc[-1],
    tempo_medio_servico.index[0],
    tempo_medio_servico['mean'].iloc[0],
    (tempo_medio_servico['mean'] > 30).mean() * 100,
    aval_media_servico.index[0] if not aval_media_servico.empty else "N/A",
    aval_media_servico['mean'].iloc[0] if not aval_media_servico.empty else 0,
    aval_media_servico.index[-1] if not aval_media_servico.empty else "N/A",
    aval_media_servico['mean'].iloc[-1] if not aval_media_servico.empty else 0,
    (aval_media_servico['mean'] > 4.0).mean() * 100 if not aval_media_servico.empty else 0,
    servico_estado.sum().idxmax(),
    servico_estado.sum().idxmin(),
    servico_estado_pct.std().idxmin(),
    servico_mes.sum().idxmax(),
    servico_mes.sum().idxmin(),
    servico_mes_pct.std().nlargest(3).index.tolist(),
    complexidade.index[0],
    complexidade.index[-1],
    correlacao_volume_tempo['volume'].corr(correlacao_volume_tempo['tempo_medio']),
    "Existe grande concentração em poucos tipos de serviço" if tipo_servico_pct.head(3).sum() > 50 else "Há boa distribuição entre os tipos de serviço",
    "Tempo de resolução varia significativamente entre categorias" if tempo_medio_servico['mean'].std() > 10 else "Tempo de resolução é relativamente uniforme entre categorias",
    "Há clara sazonalidade em algumas categorias" if servico_mes_pct.std().max() > 5 else "Não há padrão sazonal significativo",
    "Complexidade está diretamente relacionada ao tempo de resolução" if complexidade['tempo_medio'].corr(complexidade['num_assuntos']) > 0.3 else "Complexidade não é determinante no tempo de resolução",
    "Priorizar melhorias nas categorias com maior volume e pior desempenho",
    "Padronizar processos nas categorias com tempo de resolução muito acima da média",
    "Implementar gestão de capacidade considerando a sazonalidade",
    "Desenvolver especialização por categoria nos estados com maior demanda",
    "Criar indicadores específicos de complexidade por categoria"
)) 