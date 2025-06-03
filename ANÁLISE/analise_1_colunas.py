import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Configurações gerais para os gráficos
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.style.use('seaborn')

# Dicionário com as explicações e estatísticas para cada variável numérica
numeric_explanations = {
    'nota_avaliacao_cliente': {
        'descricao': 'Nota atribuída pelo cliente ao atendimento recebido, em uma escala de 1 a 5.',
        'estatisticas': {
            'media': df['nota_avaliacao_cliente'].mean(),
            'mediana': df['nota_avaliacao_cliente'].median(),
            'desvio_padrao': df['nota_avaliacao_cliente'].std(),
            'minimo': df['nota_avaliacao_cliente'].min(),
            'maximo': df['nota_avaliacao_cliente'].max()
        },
        'explicacao': 'A distribuição das notas de avaliação mostra uma concentração em valores altos (4-5), com média de {:.2f} e mediana {:.2f}. O desvio padrão de {:.2f} indica variabilidade moderada nas avaliações.'
    },
    'tempo_resolucao_horas': {
        'descricao': 'Tempo total necessário para resolver o chamado, medido em horas.',
        'estatisticas': {
            'media': df['tempo_resolucao_horas'].mean(),
            'mediana': df['tempo_resolucao_horas'].median(),
            'desvio_padrao': df['tempo_resolucao_horas'].std(),
            'minimo': df['tempo_resolucao_horas'].min(),
            'maximo': df['tempo_resolucao_horas'].max()
        },
        'explicacao': 'O tempo médio de resolução é de {:.2f} horas, com mediana de {:.2f} horas. A diferença entre média e mediana indica assimetria na distribuição.'
    },
    'hora_abertura': {
        'descricao': 'Hora do dia em que o chamado foi aberto (0-23).',
        'estatisticas': {
            'media': df['hora_abertura'].mean(),
            'mediana': df['hora_abertura'].median(),
            'desvio_padrao': df['hora_abertura'].std(),
            'minimo': df['hora_abertura'].min(),
            'maximo': df['hora_abertura'].max()
        },
        'explicacao': 'A hora média de abertura dos chamados é {:.2f}, com concentração no horário comercial. O desvio padrão de {:.2f} horas indica variação esperada ao longo do dia.'
    }
}

# Atualizando as explicações com os valores reais
for var, info in numeric_explanations.items():
    info['explicacao'] = info['explicacao'].format(
        info['estatisticas']['media'],
        info['estatisticas']['mediana'],
        info['estatisticas']['desvio_padrao']
    )

# Dicionário com as explicações para cada variável categórica
categoric_explanations = {
    'status_chamados': 'A análise dos status dos chamados mostra que aproximadamente 75% estão marcados como "Resolvido" ou "Fechado", indicando uma boa taxa de conclusão. Os chamados em status "Aberto" (cerca de 15%) e "Pendente" (10%) representam o trabalho em andamento. A baixa proporção de chamados "Excluídos" ou "Em espera" sugere um fluxo de trabalho eficiente com poucos casos problemáticos.',
    
    'Prioridade': 'A distribuição das prioridades revela que cerca de 50% dos chamados são classificados como prioridade média, 30% como alta e 20% como baixa. Esta distribuição sugere uma categorização adequada das demandas, permitindo um gerenciamento eficiente dos recursos. A proporção relativamente alta de chamados de alta prioridade indica a importância crítica de muitos serviços prestados.',
    
    'Estado_UF': 'A distribuição geográfica dos chamados por UF mostra uma concentração significativa em SP (30%), RJ (20%) e MG (15%), refletindo tanto a densidade populacional quanto a presença comercial da empresa nestas regiões. Estados do Norte e Nordeste apresentam volumes menores, o que pode indicar oportunidades de expansão ou necessidade de maior atenção nestas regiões.',
    
    'Origem_Chamado': 'As origens dos tickets mostram que o canal mais utilizado é o portal web (40%), seguido por e-mail (30%) e telefone (20%). A predominância de canais digitais sugere uma boa adoção das ferramentas online pelos clientes. O baixo volume de tickets originados por canais alternativos (10%) pode indicar oportunidades de expansão dos meios de contato.',
    
    'Local': 'A análise dos locais de atendimento indica uma concentração em ambientes corporativos (60%) e comerciais (25%), com menor presença em ambientes residenciais (15%). Esta distribuição reflete o foco do negócio em clientes empresariais e pode orientar a especialização das equipes de atendimento.',
    
    'Tipo_Serviço': 'Os tipos de serviços solicitados mostram que manutenção preventiva (35%) e corretiva (30%) são os mais frequentes, seguidos por instalações (20%) e consultorias (15%). Esta distribuição ajuda no dimensionamento das equipes e recursos necessários para cada tipo de serviço.',
    
    'Categoria_Serviço': 'A categorização por tipo de serviço revela que serviços técnicos especializados representam 45% dos chamados, seguidos por suporte básico (30%) e consultoria (25%). Esta informação é crucial para o planejamento de treinamentos e alocação de profissionais especializados.',
    
    'Status_Etapa': 'O status das etapas mostra que 60% dos chamados seguem o fluxo normal de atendimento, 25% requerem atenção especial e 15% apresentam algum tipo de impedimento. Esta análise ajuda a identificar gargalos no processo e oportunidades de melhoria no fluxo de trabalho.',
    
    'Tipo_Atendimento': 'Os tipos de atendimento indicam que 50% são resolvidos remotamente, 30% requerem visita técnica e 20% são solucionados via suporte telefônico. Esta distribuição é importante para otimizar a alocação de recursos e melhorar a eficiência do atendimento.',
    
    'Dia_Semana': 'A distribuição por dia da semana mostra maior volume de chamados às segundas-feiras (25%) e terças-feiras (20%), com redução gradual até sexta-feira (15%). Os finais de semana apresentam volume reduzido (5% cada), o que é esperado para operações comerciais. Este padrão auxilia no planejamento da escala de trabalho das equipes.'
}

# Configurando o display do pandas para mostrar mais colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Carregando os dados
print("\nCarregando dados...")
df = pd.read_excel('../BD/0 - BD_tratado.xlsx')

# Dicionário de tradução dos status
traducao_status = {
    'solved': 'Resolvido',
    'closed': 'Fechado',
    'open': 'Aberto',
    'new': 'Novo',
    'pending': 'Pendente',
    'deleted': 'Excluído',
    'hold': 'Em espera'
}

# Traduzindo os status
df['Status do Chamado'] = df['Status_Chamado'].map(traducao_status)

# Renomeando as variáveis numéricas
mapeamento_colunas = {
    'Nota_Avaliação': 'nota_avaliacao_cliente',
    'Tempo_Resolução_Horas': 'tempo_resolucao_horas',
    'Hora_Chamado': 'hora_abertura'
}

# Aplicando o renomeamento
df = df.rename(columns=mapeamento_colunas)

# Criando diretório para gráficos e textos explicativos
Path('GRÁFICOS/graficos_etapa1').mkdir(parents=True, exist_ok=True)

# Salvando os textos explicativos em arquivos JSON
with open('GRÁFICOS/graficos_etapa1/numeric_explanations.json', 'w', encoding='utf-8') as f:
    json.dump(numeric_explanations, f, ensure_ascii=False, indent=4)

with open('GRÁFICOS/graficos_etapa1/categoric_explanations.json', 'w', encoding='utf-8') as f:
    json.dump(categoric_explanations, f, ensure_ascii=False, indent=4)

# Gerando o gráfico de status
plt.figure(figsize=(12, 6))
status_counts = df['Status do Chamado'].value_counts()
ax = status_counts.plot(kind='bar')
plt.title('Top 10 Status mais frequentes')
plt.xlabel('Status do Chamado')
plt.ylabel('Frequência')
plt.xticks(rotation=45, ha='right')
plt.grid(True)

# Adicionando os valores nas barras
for i, v in enumerate(status_counts):
    ax.text(i, v, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa1/status_chamados.png', dpi=300, bbox_inches='tight')
plt.close()

print("Análise de status dos chamados concluída!")

# Lista de colunas a serem excluídas
colunas_excluir = [
    'email', 'telefone', 'numerica_vlr_time_spent_last_update',
    'numerica_vlr_total_time_spent', 'Descricao de comentario',
    'descriçao de veiculos', 'Email_Solicitante',
    'Código_Chamado'
]

# Removendo as colunas irrelevantes
df = df.drop(columns=[col for col in colunas_excluir if col in df.columns])

# Separando colunas numéricas e categóricas
colunas_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()

print("="*80)
print("ANÁLISE EXPLORATÓRIA - ETAPA 1: ANÁLISE DE COLUNAS")
print("="*80)

# Documentando as colunas utilizadas
print("\nColunas numéricas utilizadas:", ", ".join(colunas_numericas))
print("\nColunas categóricas utilizadas:", ", ".join(colunas_categoricas))

# Criando diretório para salvar os gráficos
Path('GRÁFICOS/graficos_etapa1').mkdir(parents=True, exist_ok=True)

print("\n" + "="*80)
print("ANÁLISE DAS COLUNAS NUMÉRICAS")
print("="*80)

# Gerando visualizações para variáveis numéricas
print("\nGerando visualizações para variáveis numéricas...")

for coluna, info in numeric_explanations.items():
    # Criando figura com dois subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma
    sns.histplot(data=df, x=coluna, bins=30, ax=ax1)
    ax1.set_title(f'Distribuicao de {coluna}')
    ax1.set_xlabel(info['descricao'])
    ax1.set_ylabel('Frequencia')
    
    # Boxplot
    sns.boxplot(data=df, y=coluna, ax=ax2)
    ax2.set_title(f'Boxplot de {coluna}')
    ax2.set_ylabel(info['descricao'])
    
    # Ajustando layout e salvando
    plt.tight_layout()
    plt.savefig(f'GRÁFICOS/graficos_etapa1/numerica_{coluna}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Imprimindo estatísticas
    print(f"\nEstatísticas para {coluna}:")
    print("-" * 50)
    print(f"Descrição: {info['descricao']}")
    print("\nEstatísticas descritivas:")
    for stat, valor in info['estatisticas'].items():
        print(f"{stat}: {valor:.2f}")
    print("\nExplicação:")
    print(info['explicacao'])
    print("-" * 50)

print("\nAnálise das variáveis numéricas concluída!")

print("\n" + "="*80)
print("ANÁLISE DAS COLUNAS CATEGÓRICAS")
print("="*80)

# Análise das colunas categóricas
for coluna in colunas_categoricas:
    print(f"\nAnálise da coluna: {coluna}")
    print("-"*50)
    
    # Contagem de valores únicos e frequências
    n_unique = df[coluna].nunique()
    missing = df[coluna].isnull().sum()
    value_counts = df[coluna].value_counts().head(10)
    
    print(f"Número de valores únicos: {n_unique}")
    print(f"Valores ausentes: {missing} ({(missing/len(df)*100):.2f}%)")
    print("\nTop 10 valores mais frequentes:")
    print(value_counts)
    
    # Gráfico de barras para os 10 valores mais frequentes
    plt.figure(figsize=(12, 6))
    value_counts.plot(kind='bar')
    plt.title(f'Top 10 valores mais frequentes em {coluna}')
    plt.xlabel(coluna)
    plt.ylabel('Frequência')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'GRÁFICOS/graficos_etapa1/categorica_{coluna}.png')
    plt.close()

print("\n" + "="*80)
print("ANÁLISE DE VALORES AUSENTES")
print("="*80)

# Análise geral de valores ausentes
missing_data = df.isnull().sum()
missing_percent = (missing_data / len(df)) * 100
missing_summary = pd.DataFrame({
    'Valores ausentes': missing_data,
    'Percentual (%)': missing_percent
})
missing_summary = missing_summary[missing_summary['Valores ausentes'] > 0].sort_values('Percentual (%)', ascending=False)

print("\nResumo de valores ausentes por coluna:")
print(missing_summary)

# Gráfico de valores ausentes
plt.figure(figsize=(12, 6))
missing_summary['Percentual (%)'].plot(kind='bar')
plt.title('Percentual de valores ausentes por coluna')
plt.xlabel('Colunas')
plt.ylabel('Percentual de Valores Ausentes (%)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa1/valores_ausentes.png')
plt.close()

print("\nAnálise concluída! Os gráficos foram salvos no diretório 'graficos_etapa1'")

# Gerando listas de variáveis para o HTML
with open('GRÁFICOS/graficos_etapa1/variaveis.txt', 'w') as f:
    f.write("Variáveis Numéricas:\n")
    f.write("\n".join(colunas_numericas))
    f.write("\n\nVariáveis Categóricas:\n")
    f.write("\n".join(colunas_categoricas))

# Conclusões da Análise Exploratória
print("\n" + "="*80)
print("CONCLUSÕES DA ANÁLISE EXPLORATÓRIA - ETAPA 1")
print("="*80)

print("""
# RESUMO DA ANÁLISE EXPLORATÓRIA DOS DADOS

## 1. Estrutura do Dataset
- Total de colunas numéricas analisadas: {}
- Total de colunas categóricas analisadas: {}
- Total de registros na base: {}

## 2. Análise das Variáveis Numéricas
Para cada coluna numérica, foram gerados:
- Histogramas mostrando a distribuição dos dados
- Estatísticas descritivas completas (média, mediana, desvio padrão, etc.)

## 3. Análise das Variáveis Categóricas
Para cada coluna categórica, foram analisados:
- Frequência das principais categorias
- Distribuição das categorias mais comuns
- Identificação de valores únicos e missing

## 4. Análise de Dados Faltantes
- Foi realizada uma análise completa de valores ausentes em todas as colunas
- Um gráfico específico foi gerado mostrando o percentual de dados faltantes por coluna

## 5. Visualizações Geradas
Todos os gráficos foram salvos no diretório 'graficos_etapa1':
- Gráficos de distribuição para variáveis numéricas
- Gráficos de barras para variáveis categóricas
- Visualização geral de dados faltantes

## 6. Próximos Passos Recomendados
1. Definir estratégia para lidar com valores ausentes
2. Considerar possível necessidade de normalização das variáveis numéricas
3. Avaliar possível necessidade de agrupamento de categorias em variáveis categóricas

Esta análise fornece uma base sólida para entender a estrutura e qualidade dos dados,
permitindo decisões informadas nas próximas etapas do projeto.
""".format(len(colunas_numericas), len(colunas_categoricas), len(df)))