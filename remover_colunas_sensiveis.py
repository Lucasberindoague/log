import pandas as pd
import os
import glob

# Função para remover as colunas sensíveis
def remover_colunas_sensiveis(df):
    colunas_para_remover = ['Telefone', 'Email_Solicitante']
    return df.drop(columns=colunas_para_remover, errors='ignore')

# Carregar e atualizar o BD tratado
print("Atualizando o banco de dados tratado...")
caminho_bd = "BD/0 - BD_tratado.xlsx"
df = pd.read_excel(caminho_bd)
df = remover_colunas_sensiveis(df)
df.to_excel(caminho_bd, index=False)

# Função para atualizar arquivos Python
def atualizar_arquivo_python(caminho):
    with open(caminho, 'r', encoding='utf-8') as file:
        conteudo = file.read()
    
    # Lista de substituições para remover referências às colunas
    substituicoes = [
        ("'Telefone'", "# 'Telefone' removido"),
        ('"Telefone"', '# "Telefone" removido'),
        ("'Email_Solicitante'", "# 'Email_Solicitante' removido"),
        ('"Email_Solicitante"', '# "Email_Solicitante" removido'),
        ("[,'Telefone']", ""),
        ('[,"Telefone"]', ""),
        ("[,'Email_Solicitante']", ""),
        ('[,"Email_Solicitante"]', ""),
        (",'Telefone'", ""),
        (',"Telefone"', ""),
        (",'Email_Solicitante'", ""),
        (',"Email_Solicitante"', "")
    ]
    
    for antigo, novo in substituicoes:
        conteudo = conteudo.replace(antigo, novo)
    
    with open(caminho, 'w', encoding='utf-8') as file:
        file.write(conteudo)

# Atualizar todos os scripts Python na pasta ANÁLISE
print("Atualizando scripts de análise...")
arquivos_python = glob.glob("ANÁLISE/*.py")
for arquivo in arquivos_python:
    print(f"Atualizando {arquivo}...")
    atualizar_arquivo_python(arquivo)

print("Processo concluído!") 