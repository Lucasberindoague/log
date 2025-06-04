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
# INÍCIO DA ANÁLISE DA AVALIAÇÃO DO CLIENTE
# =============================================================================

print("\n" + "="*80)
print("ANÁLISE DA AVALIAÇÃO DO CLIENTE")
print("="*80)

print("\nCarregando dados...")
df = pd.read_excel('BD/0 - BD_tratado.xlsx')

# Renomeando a coluna de avaliação para facilitar o uso
df['num_avaliacao'] = df['Nota_Avaliação']

# Documentando as colunas utilizadas
print("\n# Colunas utilizadas na análise da avaliação:")
print("# - vlr_nota_avaliacao_cliente_atendimento: Nota dada pelo cliente (1 a 5)")
print("# - cod_uf: Estado do chamado")
print("# - des_tipo_servico: Tipo de serviço")
print("# - tempo_resolucao_dias: Tempo de resolução em dias")
print("# - des_prioridade: Prioridade do chamado")
print("# - des_status: Status do chamado")
print("# - des_comentario: Comentário do cliente")

# Convertendo datas e calculando tempo de resolução
df['Data_Criação'] = pd.to_datetime(df['Data_Criação'])
df['Data_Resolução'] = pd.to_datetime(df['Data_Resolução'])
df['tempo_resolucao_dias'] = (df['Data_Resolução'] - df['Data_Criação']).dt.total_seconds() / (24*60*60)

# Criando diretório para gráficos
Path('graficos_etapa5').mkdir(exist_ok=True)

# 1. Análise inicial das avaliações
print("\nAnalisando distribuição das avaliações...")
total_registros = len(df)
ausentes = df['num_avaliacao'].isnull().sum()
percentual_ausentes = (ausentes / total_registros) * 100

print(f"\nTotal de registros: {total_registros}")
print(f"Avaliações ausentes: {ausentes} ({percentual_ausentes:.1f}%)")

# Filtrando apenas avaliações válidas (1 a 5)
print("\nFiltrando avaliações válidas (1 a 5)...")
df_valid = df[df['num_avaliacao'].between(1, 5)]
total_validos = len(df_valid)
print(f"Total de avaliações válidas: {total_validos}")

# 2. Estatísticas descritivas das avaliações válidas
stats_aval = df_valid['num_avaliacao'].describe()
print("\nEstatísticas das avaliações válidas:")
print(stats_aval)

# 3. Distribuição das notas
dist_notas = df_valid['num_avaliacao'].value_counts().sort_index()
print("\nDistribuição das notas:")
print(dist_notas)

# 4. Gráfico de barras da distribuição das notas
plt.figure(figsize=(10, 6))
dist_notas.plot(kind='bar')
plt.title('Distribuição das Avaliações')
plt.xlabel('Nota')
plt.ylabel('Quantidade de Avaliações')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/barras_distribuicao_notas.png')
plt.close()

# 5. Gráfico de pizza da distribuição das notas
plt.figure(figsize=(10, 10))
plt.pie(dist_notas, labels=[f'Nota {i}' for i in dist_notas.index], autopct='%1.1f%%')
plt.title('Distribuição Percentual das Avaliações')
plt.axis('equal')
plt.savefig('GRÁFICOS/graficos_etapa5/pizza_distribuicao_notas.png')
plt.close()

# 6. Boxplot das avaliações
plt.figure(figsize=(8, 6))
plt.boxplot(df_valid['num_avaliacao'])
plt.title('Boxplot das Avaliações')
plt.ylabel('Nota')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/boxplot_avaliacoes.png')
plt.close()

# 7. Gráfico de densidade
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df_valid['num_avaliacao'], fill=True)
plt.title('Densidade das Avaliações')
plt.xlabel('Nota')
plt.ylabel('Densidade')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/densidade_avaliacoes.png')
plt.close()

# 8. Avaliação média por estado
print("\nAnalisando avaliação média por estado...")
aval_por_estado = df_valid.groupby('Estado_UF')['num_avaliacao'].agg(['mean', 'count', 'std']).round(2)
aval_por_estado = aval_por_estado.sort_values('mean', ascending=False)

plt.figure(figsize=(12, 6))
aval_por_estado['mean'].plot(kind='bar')
plt.title('Avaliação Média por Estado')
plt.xlabel('Estado')
plt.ylabel('Média das Avaliações')
plt.axhline(y=df_valid['num_avaliacao'].mean(), color='r', linestyle='--', label='Média Geral')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/barras_avaliacao_media_estado.png')
plt.close()

# 9. Avaliação média por tipo de serviço
print("\nAnalisando avaliação média por tipo de serviço...")
aval_por_servico = df_valid.groupby('Categoria_Serviço')['num_avaliacao'].agg(['mean', 'count', 'std']).round(2)
aval_por_servico = aval_por_servico[aval_por_servico['count'] >= 10]  # Filtrando serviços com pelo menos 10 avaliações
aval_por_servico = aval_por_servico.sort_values('mean', ascending=False)

plt.figure(figsize=(15, 6))
aval_por_servico['mean'].plot(kind='bar')
plt.title('Avaliação Média por Tipo de Serviço')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Média das Avaliações')
plt.axhline(y=df_valid['num_avaliacao'].mean(), color='r', linestyle='--', label='Média Geral')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/barras_avaliacao_media_servico.png')
plt.close()

# 10. Avaliação média por prioridade
print("\nAnalisando avaliação média por prioridade...")
aval_por_prioridade = df_valid.groupby('Prioridade')['num_avaliacao'].agg(['mean', 'count', 'std']).round(2)
aval_por_prioridade = aval_por_prioridade.sort_values('mean', ascending=False)

plt.figure(figsize=(10, 6))
aval_por_prioridade['mean'].plot(kind='bar')
plt.title('Avaliação Média por Prioridade')
plt.xlabel('Prioridade')
plt.ylabel('Média das Avaliações')
plt.axhline(y=df_valid['num_avaliacao'].mean(), color='r', linestyle='--', label='Média Geral')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/barras_avaliacao_media_prioridade.png')
plt.close()

# 11. Correlação entre tempo de resolução e avaliação
print("\nAnalisando correlação entre tempo de resolução e avaliação...")
correlacao = df_valid['num_avaliacao'].corr(df_valid['tempo_resolucao_dias'])

plt.figure(figsize=(10, 6))
plt.scatter(df_valid['tempo_resolucao_dias'], df_valid['num_avaliacao'], alpha=0.5)
plt.title('Correlação entre Tempo de Resolução e Avaliação')
plt.xlabel('Tempo de Resolução (dias)')
plt.ylabel('Avaliação')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/dispersao_tempo_avaliacao.png')
plt.close()

# 12. Evolução temporal das avaliações
print("\nAnalisando evolução temporal das avaliações...")
aval_media_mensal = df_valid.groupby(df_valid['Data_Criação'].dt.to_period('M'))['num_avaliacao'].mean()

plt.figure(figsize=(15, 6))
aval_media_mensal.plot(kind='line', marker='o')
plt.title('Evolução da Avaliação Média ao Longo do Tempo')
plt.xlabel('Mês')
plt.ylabel('Avaliação Média')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/linha_evolucao_avaliacoes.png')
plt.close()

# 13. Heatmap de avaliação por estado e tipo de serviço
print("\nGerando heatmap de avaliação por estado e tipo de serviço...")
pivot_estado_servico = df_valid.pivot_table(
    values='num_avaliacao',
    index='Estado_UF',
    columns='Categoria_Serviço',
    aggfunc='mean'
)

plt.figure(figsize=(15, 8))
sns.heatmap(pivot_estado_servico, cmap='YlOrRd', annot=True, fmt='.1f', cbar_kws={'label': 'Avaliação Média'})
plt.title('Heatmap: Avaliação Média por Estado e Tipo de Serviço')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Estado')
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/heatmap_avaliacao_estado_servico.png')
plt.close()

# 14. Análise de comentários
print("\nAnalisando comentários dos clientes...")
comentarios_por_nota = df_valid.groupby('num_avaliacao')['Comentário'].count()

plt.figure(figsize=(10, 6))
comentarios_por_nota.plot(kind='bar')
plt.title('Quantidade de Comentários por Nota')
plt.xlabel('Nota')
plt.ylabel('Quantidade de Comentários')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/barras_comentarios_por_nota.png')
plt.close()

# Adicionando análise dos fatores de influência
print("\nAnalisando fatores que influenciam a satisfação...")

# Criando um DataFrame com os fatores e seus impactos
fatores = pd.DataFrame({
    'Fator': [
        'Tempo de Resolução',
        'Qualidade do Atendimento',
        'Comunicação',
        'Tipo de Serviço',
        'Prioridade do Chamado'
    ],
    'Impacto': [
        df['Nota_Avaliação'].corr(df['Tempo_Resolução_Horas']) * -1,  # Invertendo pois menor tempo é melhor
        df.groupby('Status_Chamado')['Nota_Avaliação'].mean().std(),  # Variação por status
        df.groupby('Comentário')['Nota_Avaliação'].mean().std(),  # Variação por comunicação
        df.groupby('Tipo_Serviço')['Nota_Avaliação'].mean().std(),  # Variação por tipo de serviço
        df.groupby('Prioridade')['Nota_Avaliação'].mean().std()  # Variação por prioridade
    ]
})

# Normalizando os impactos para uma escala de 0 a 1
fatores['Impacto_Normalizado'] = (fatores['Impacto'] - fatores['Impacto'].min()) / (fatores['Impacto'].max() - fatores['Impacto'].min())

# Criando o gráfico de barras horizontais
plt.figure(figsize=(12, 6))
bars = plt.barh(fatores['Fator'], fatores['Impacto_Normalizado'], color='skyblue')
plt.title('Fatores que Influenciam a Satisfação do Cliente')
plt.xlabel('Impacto Normalizado')

# Adicionando os valores nas barras
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, 
             f'{fatores["Impacto_Normalizado"][i]:.2f}', 
             ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa5/fatores_satisfacao.png', dpi=300, bbox_inches='tight')
plt.close()

# Conclusões da Análise da Avaliação do Cliente
print("\n" + "="*80)
print("CONCLUSÕES DA ANÁLISE DA AVALIAÇÃO DO CLIENTE")
print("="*80)

print("""
# RESUMO DA ANÁLISE DA AVALIAÇÃO DO CLIENTE

## 1. Estatísticas Gerais
- Média geral das avaliações: {:.2f}
- Mediana: {:.2f}
- Desvio padrão: {:.2f}
- Total de avaliações válidas: {} ({:.1f}% do total)
- Avaliações ausentes: {:.1f}%

## 2. Distribuição das Notas
- Nota mais frequente: {} ({} ocorrências)
- Nota menos frequente: {} ({} ocorrências)
- Proporção de notas máximas (5): {:.1f}%
- Proporção de notas mínimas (1): {:.1f}%

## 3. Análise por Estado
- Estado com melhor avaliação: {} (média {:.2f})
- Estado com pior avaliação: {} (média {:.2f})
- Variação entre estados: {:.2f} pontos
- Estados acima da média geral: {:.1f}%

## 4. Análise por Tipo de Serviço
- Melhor serviço avaliado: {} (média {:.2f})
- Pior serviço avaliado: {} (média {:.2f})
- {:.1f}% dos serviços têm média acima de 4.0
- Serviços com maior variação: {}

## 5. Análise por Prioridade
- Prioridade melhor avaliada: {} (média {:.2f})
- Prioridade pior avaliada: {} (média {:.2f})
- Diferença entre prioridades: {:.2f} pontos

## 6. Correlação com Tempo de Resolução
- Coeficiente de correlação: {:.3f}
- Interpretação: {}

## 7. Evolução Temporal
- Tendência geral: {}
- Mês com melhor avaliação: {}
- Mês com pior avaliação: {}
- Variação ao longo do tempo: {:.2f} pontos

## 8. Análise de Comentários
- {:.1f}% dos chamados têm comentários
- Proporção de comentários por nota: {}
- Notas com mais comentários: {}

## 9. Observações Importantes
- {}
- {}
- {}
- {}

## 10. Recomendações
1. {}
2. {}
3. {}
4. {}
5. {}
""".format(
    stats_aval['mean'],
    stats_aval['50%'],
    stats_aval['std'],
    total_validos,
    (total_validos/total_registros)*100,
    percentual_ausentes,
    dist_notas.index[dist_notas.argmax()],
    dist_notas.max(),
    dist_notas.index[dist_notas.argmin()],
    dist_notas.min(),
    (dist_notas[5] / total_validos) * 100 if 5 in dist_notas else 0,
    (dist_notas[1] / total_validos) * 100 if 1 in dist_notas else 0,
    aval_por_estado.index[0],
    aval_por_estado['mean'].iloc[0],
    aval_por_estado.index[-1],
    aval_por_estado['mean'].iloc[-1],
    aval_por_estado['mean'].iloc[0] - aval_por_estado['mean'].iloc[-1],
    (aval_por_estado['mean'] > df_valid['num_avaliacao'].mean()).mean() * 100,
    aval_por_servico.index[0],
    aval_por_servico['mean'].iloc[0],
    aval_por_servico.index[-1],
    aval_por_servico['mean'].iloc[-1],
    (aval_por_servico['mean'] > 4.0).mean() * 100,
    aval_por_servico.nlargest(3, 'std').index.tolist(),
    aval_por_prioridade.index[0],
    aval_por_prioridade['mean'].iloc[0],
    aval_por_prioridade.index[-1],
    aval_por_prioridade['mean'].iloc[-1],
    aval_por_prioridade['mean'].iloc[0] - aval_por_prioridade['mean'].iloc[-1],
    correlacao,
    "Correlação negativa significativa" if correlacao < -0.3 else "Correlação positiva significativa" if correlacao > 0.3 else "Correlação fraca",
    "Tendência de melhoria" if aval_media_mensal.iloc[-1] > aval_media_mensal.iloc[0] else "Tendência de piora" if aval_media_mensal.iloc[-1] < aval_media_mensal.iloc[0] else "Estável",
    aval_media_mensal.index[aval_media_mensal.argmax()],
    aval_media_mensal.index[aval_media_mensal.argmin()],
    aval_media_mensal.max() - aval_media_mensal.min(),
    (df_valid['Comentário'].notna().sum() / len(df_valid)) * 100,
    dict(comentarios_por_nota / comentarios_por_nota.sum()),
    comentarios_por_nota.nlargest(2).index.tolist(),
    "A satisfação dos clientes apresenta padrão consistente ao longo do tempo" if aval_media_mensal.std() < 0.5 else "Existe variação significativa na satisfação ao longo do tempo",
    "Prioridade do chamado tem impacto direto na avaliação" if aval_por_prioridade['mean'].std() > 0.3 else "Prioridade tem pouco impacto na avaliação",
    "Existe correlação clara entre tempo de resolução e avaliação" if abs(correlacao) > 0.3 else "Tempo de resolução não é fator determinante na avaliação",
    "Comentários são mais frequentes em avaliações extremas" if comentarios_por_nota.iloc[0] + comentarios_por_nota.iloc[-1] > comentarios_por_nota.sum() * 0.5 else "Distribuição uniforme de comentários",
    "Implementar programa de melhoria focado nos estados com pior desempenho" if aval_por_estado['mean'].std() > 0.5 else "Manter padrão de atendimento entre estados",
    "Revisar processos dos serviços com avaliações mais baixas",
    "Criar canal de feedback específico para prioridades com pior avaliação",
    "Estabelecer meta de tempo máximo de resolução baseado na correlação com avaliações",
    "Desenvolver sistema de análise automática de comentários para identificar pontos críticos"
)) 