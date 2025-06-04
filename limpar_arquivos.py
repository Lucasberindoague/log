import os
import shutil

# Lista de arquivos para remover
arquivos_para_remover = [
    'verificar_colunas.py',
    'remover_colunas_sensiveis.py',
    'atualizar_scripts.py',
    'renomear_colunas.py',
    '.DS_Store'
]

# Lista de diretórios para remover
diretorios_para_remover = [
    'graficos_etapa3',
    'graficos_etapa5'
]

print("Iniciando limpeza de arquivos...")

# Removendo arquivos
for arquivo in arquivos_para_remover:
    if os.path.exists(arquivo):
        try:
            os.remove(arquivo)
            print(f"Arquivo removido: {arquivo}")
        except Exception as e:
            print(f"Erro ao remover arquivo {arquivo}: {e}")

# Removendo diretórios
for diretorio in diretorios_para_remover:
    if os.path.exists(diretorio):
        try:
            shutil.rmtree(diretorio)
            print(f"Diretório removido: {diretorio}")
        except Exception as e:
            print(f"Erro ao remover diretório {diretorio}: {e}")

print("Processo de limpeza concluído!") 