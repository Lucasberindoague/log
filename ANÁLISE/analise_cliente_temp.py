import pandas as pd

# Carregando os dados
df = pd.read_excel('../BD/0 - BD_tratado.xlsx')

# Analisando a distribuição de chamados por cliente
chamados_por_cliente = df['Nome_Cliente'].value_counts()
total_chamados = len(df)

# Encontrando o cliente com mais chamados
cliente_maior = chamados_por_cliente.index[0]
qtd_maior = chamados_por_cliente.iloc[0]
percentual_maior = (qtd_maior / total_chamados) * 100

print(f"\nTotal de chamados: {total_chamados}")
print(f"Cliente com mais chamados: {cliente_maior}")
print(f"Quantidade de chamados deste cliente: {qtd_maior}")
print(f"Percentual do total: {percentual_maior:.2f}%") 