import os
import shutil

def mover_graficos(origem, destino):
    """Move os gráficos de uma pasta para outra, substituindo se necessário"""
    if not os.path.exists(origem):
        print(f"Pasta de origem não existe: {origem}")
        return
    
    if not os.path.exists(destino):
        os.makedirs(destino)
    
    for arquivo in os.listdir(origem):
        origem_arquivo = os.path.join(origem, arquivo)
        destino_arquivo = os.path.join(destino, arquivo)
        
        if os.path.isfile(origem_arquivo):
            shutil.copy2(origem_arquivo, destino_arquivo)
            print(f"Arquivo copiado: {arquivo}")

# Mover gráficos da etapa 3 e 4 para a pasta GRÁFICOS
etapas = ['3', '4']
for etapa in etapas:
    origem = f"ANÁLISE/graficos_etapa{etapa}"
    destino = f"GRÁFICOS/graficos_etapa{etapa}"
    
    print(f"\nProcessando etapa {etapa}...")
    mover_graficos(origem, destino)
    
    # Remover a pasta de origem após mover os arquivos
    if os.path.exists(origem):
        shutil.rmtree(origem)
        print(f"Pasta removida: {origem}")

print("\nOrganização dos gráficos concluída!") 