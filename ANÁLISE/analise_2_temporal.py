import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configurações gerais para os gráficos
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Carregando os dados
df = pd.read_excel('../BD/0 - BD_tratado.xlsx')

# Convertendo a coluna de data para datetime se necessário
df['Data_Criação'] = pd.to_datetime(df['Data_Criação'])

# Criando colunas de ano e mês
df['Ano'] = df['Data_Criação'].dt.year
df['Mês'] = df['Data_Criação'].dt.month

# Agrupando os dados por ano e mês
volume_mensal = df.groupby(['Ano', 'Mês']).size().reset_index(name='Quantidade')

# Criando o gráfico de linhas sobrepostas
plt.figure(figsize=(12, 6))

# Lista de cores para cada ano
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# Plotando uma linha para cada ano
for idx, ano in enumerate(volume_mensal['Ano'].unique()):
    dados_ano = volume_mensal[volume_mensal['Ano'] == ano]
    plt.plot(dados_ano['Mês'], dados_ano['Quantidade'], 
             marker='o', 
             linewidth=2,
             color=cores[idx],
             label=f'Ano {ano}')

# Configurando o gráfico
plt.title('Volume de Chamados por Mês - Comparação entre Anos', pad=20)
plt.xlabel('Mês')
plt.ylabel('Quantidade de Chamados')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Período', bbox_to_anchor=(1.05, 1), loc='upper left')

# Configurando os ticks do eixo X para mostrar os nomes dos meses
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
plt.xticks(range(1, 13), meses, rotation=45)

# Ajustando o layout para não cortar a legenda
plt.tight_layout()

# Criando diretório para salvar os gráficos se não existir
Path('graficos_etapa2').mkdir(exist_ok=True)

# Salvando o gráfico
plt.savefig('GRÁFICOS/graficos_etapa2/volume_mensal.png', dpi=300, bbox_inches='tight')
plt.close()

# Mantendo os outros gráficos da análise temporal
# Análise por dia da semana
plt.figure(figsize=(12, 6))
df['Dia_Semana'] = df['Data_Criação'].dt.day_name()
ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
volume_diario = df['Dia_Semana'].value_counts().reindex(ordem_dias)

sns.barplot(x=volume_diario.index, y=volume_diario.values)
plt.title('Volume de Chamados por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Quantidade de Chamados')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa2/volume_dia_semana.png')
plt.close()

# Análise do tempo de resolução
plt.figure(figsize=(12, 6))
df['Tempo_Resolução_Horas'] = (pd.to_datetime(df['Data_Resolução']) - pd.to_datetime(df['Data_Criação'])).dt.total_seconds() / 3600
sns.histplot(data=df, x='Tempo_Resolução_Horas', bins=50)
plt.title('Distribuição do Tempo de Resolução dos Chamados')
plt.xlabel('Tempo de Resolução (horas)')
plt.ylabel('Frequência')
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa2/tempo_resolucao.png')
plt.close() 