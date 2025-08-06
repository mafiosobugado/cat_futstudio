import cv2
import os
import numpy as np
import json # Usaremos JSON para salvar o mapeamento de IDs

print("Iniciando o processo de treinamento do modelo de cartas...")

# Usaremos o LBPH, pois é excelente para texturas e robusto à iluminação
reconhecedor = cv2.face.LBPHFaceRecognizer_create()

def carregar_dados_cartas(base_folder='templates_cartas/'):
    """
    Lê a pasta de templates, atribui um ID numérico para cada carta,
    e retorna as imagens e os IDs prontos para o treinamento.
    """
    faces_cartas = []
    ids_cartas = []
    mapa_id_nome = {}
    id_atual = 0

    print(f"Lendo arquivos de '{base_folder}'...")

    for nome_naipe in os.listdir(base_folder):
        path_naipe = os.path.join(base_folder, nome_naipe)
        if not os.path.isdir(path_naipe): continue

        for nome_valor in os.listdir(path_naipe):
            path_valor = os.path.join(path_naipe, nome_valor)
            if not os.path.isdir(path_valor): continue

            # Nome único da carta (ex: 'copas_2')
            nome_carta = f"{nome_naipe}_{nome_valor}"

            if nome_carta not in mapa_id_nome.values():
                mapa_id_nome[id_atual] = nome_carta
                id_numerico = id_atual
                id_atual += 1
            else:
                # Se já viu essa carta, pega o ID existente
                id_numerico = [id for id, name in mapa_id_nome.items() if name == nome_carta][0]
            
            for nome_arquivo in os.listdir(path_valor):
                path_imagem = os.path.join(path_valor, nome_arquivo)
                imagem = cv2.imread(path_imagem, cv2.IMREAD_GRAYSCALE)
                
                if imagem is not None:
                    faces_cartas.append(imagem)
                    ids_cartas.append(id_numerico)

    print(f"{len(faces_cartas)} imagens carregadas para {len(mapa_id_nome)} cartas únicas.")
    return np.array(ids_cartas), faces_cartas, mapa_id_nome

# Carrega os dados
ids, faces, mapa_nomes = carregar_dados_cartas()

# Salva o mapa de nomes para ser usado no reconhecimento
os.makedirs('classifier_cartas', exist_ok=True)
with open('classifier_cartas/mapeamento_nomes.json', 'w') as f:
    json.dump(mapa_nomes, f)
print("Mapeamento de nomes salvo em 'mapeamento_nomes.json'")

# Treina o modelo
print("\nIniciando treinamento do modelo LBPH...")
reconhecedor.train(faces, ids)
reconhecedor.write('classifier_cartas/classificadorCartasLBPH.yml')
print("Treinamento concluído com sucesso! Modelo salvo em 'classificadorCartasLBPH.yml'")