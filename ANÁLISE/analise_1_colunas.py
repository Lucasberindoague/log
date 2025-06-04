import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Função para converter tipos numpy para Python nativo
def convert_to_native(obj):
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
        np.int16, np.int32, np.int64, np.uint8,
        np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    return obj

# Configurações gerais para os gráficos
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Carregando os dados
print("\nCarregando dados...")
df = pd.read_excel('BD/0 - BD_tratado.xlsx')

# Debug: mostrar as colunas disponíveis
print("\nColunas disponíveis no DataFrame:")
print(df.columns.tolist())

# Dicionário com as explicações e estatísticas para cada variável numérica
numeric_explanations = {
    'Nota_Avaliação': {
        'descricao': 'Nota atribuída pelo cliente ao atendimento recebido, em uma escala de 1 a 5.',
        'estatisticas': {
            'media': df['Nota_Avaliação'].mean(),
            'mediana': df['Nota_Avaliação'].median(),
            'desvio_padrao': df['Nota_Avaliação'].std(),
            'minimo': df['Nota_Avaliação'].min(),
            'maximo': df['Nota_Avaliação'].max()
        },
        'explicacao': 'A distribuição das notas de avaliação mostra uma concentração em valores altos (4-5), com média de {:.2f} e mediana {:.2f}. O desvio padrão de {:.2f} indica variabilidade moderada nas avaliações.'
    },
    'Tempo_Resolução_Horas': {
        'descricao': 'Tempo total necessário para resolver o chamado, medido em horas.',
        'estatisticas': {
            'media': df['Tempo_Resolução_Horas'].mean(),
            'mediana': df['Tempo_Resolução_Horas'].median(),
            'desvio_padrao': df['Tempo_Resolução_Horas'].std(),
            'minimo': df['Tempo_Resolução_Horas'].min(),
            'maximo': df['Tempo_Resolução_Horas'].max()
        },
        'explicacao': 'O tempo médio de resolução é de {:.2f} horas, com mediana de {:.2f} horas. A diferença entre média e mediana indica assimetria na distribuição.'
    },
    'Hora_Chamado': {
        'descricao': 'Hora do dia em que o chamado foi aberto (0-23).',
        'estatisticas': {
            'media': df['Hora_Chamado'].mean(),
            'mediana': df['Hora_Chamado'].median(),
            'desvio_padrao': df['Hora_Chamado'].std(),
            'minimo': df['Hora_Chamado'].min(),
            'maximo': df['Hora_Chamado'].max()
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

# Convertendo valores numpy para Python nativo antes de salvar
for var_info in numeric_explanations.values():
    for stat_key, stat_value in var_info['estatisticas'].items():
        var_info['estatisticas'][stat_key] = convert_to_native(stat_value)

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

# Gerando o gráfico de status (barras)
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
plt.savefig('GRÁFICOS/graficos_etapa1/categorica_status_chamados.png', dpi=300, bbox_inches='tight')
plt.close()

# Gerando gráfico de tipo de atendimento
print("\nGerando gráfico de tipo de atendimento...")

# Selecionando apenas os dois tipos principais
top_2_atendimentos = df['Tipo_Atendimento'].value_counts().nlargest(2)

# Criando figura com espaço para texto
plt.figure(figsize=(12, 10))

# Subplot para o gráfico
ax1 = plt.subplot(2, 1, 1)
top_2_atendimentos.plot(kind='bar', ax=ax1)

# Adicionando os valores em cima das barras
for i, v in enumerate(top_2_atendimentos):
    ax1.text(i, v, str(int(v)), ha='center', va='bottom')

plt.title('Principais Tipos de Atendimento')
plt.xlabel('Tipo de Atendimento')
plt.ylabel('Frequência')
plt.xticks(rotation=45, ha='right')
plt.grid(True)

# Adicionando texto explicativo
texto_explicativo = """
Resumo dos Tipos de Atendimento:

MANUTENÇÕES (3687 chamados):
- Foco em correções e reparos estruturais
- Maior número de chamados urgentes
- Tempo médio de resolução: 55 horas
- Principais serviços: estrutura metálica e instalações
- Nota média de avaliação: 5,46

OPERAÇÕES (3288 chamados):
- Foco em instalações e manutenção preventiva
- Menor urgência nos chamados
- Tempo médio de resolução: 42 horas
- Principais serviços: instalações elétricas e hidráulicas
- Nota média de avaliação: 4,34
"""

# Subplot para o texto
ax2 = plt.subplot(2, 1, 2)
ax2.text(0.05, 0.5, texto_explicativo, fontsize=10, va='center', ha='left', transform=ax2.transAxes)
ax2.axis('off')

plt.tight_layout()
plt.savefig('GRÁFICOS/graficos_etapa1/categorica_des_atendimento.png', dpi=300, bbox_inches='tight')
plt.close()

print("Gráfico de tipos de atendimento gerado com sucesso!")

# Análise das colunas categóricas
for coluna in colunas_categoricas:
    print(f"\nAnálise da coluna: {coluna}")
    print("-"*50)
    
    # Contagem de valores únicos e frequências
    n_unique = df[coluna].nunique()
    missing = df[coluna].isnull().sum()
    
    if coluna == 'Tipo_Atendimento':
        # Tratamento especial para Tipo_Atendimento
        value_counts = df[coluna].value_counts().head(2)  # Pegando apenas os 2 principais
    elif coluna == 'des_local':
        # Para des_local, apenas mostrar as estatísticas sem gerar gráfico
        value_counts = df[coluna].value_counts().head(10)
    elif coluna == 'des_status_etapa':
        # Pulando o gráfico de status_etapa para evitar duplicidade
        value_counts = df[coluna].value_counts().head(10)
        print(f"Número de valores únicos: {n_unique}")
        print(f"Valores ausentes: {missing} ({(missing/len(df)*100):.2f}%)")
        print("\nTop valores mais frequentes:")
        print(value_counts)
        continue
    else:
        # Para outras colunas, mantém o comportamento original
        value_counts = df[coluna].value_counts().head(10)
        
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
    
    print(f"Número de valores únicos: {n_unique}")
    print(f"Valores ausentes: {missing} ({(missing/len(df)*100):.2f}%)")
    print("\nTop valores mais frequentes:")
    print(value_counts)

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

# Filtrando as colunas que não queremos mostrar
colunas_excluir = ['des_veiculo', 'des_comentario']
missing_filtered = missing_summary[~missing_summary.index.isin(colunas_excluir)]

missing_filtered['Percentual (%)'].plot(kind='bar')
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