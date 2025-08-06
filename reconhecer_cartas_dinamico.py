# -*- coding: utf-8 -*-

"""
================================================================
RECONHECEDOR DE CARTAS EM TEMPO REAL A PARTIR DA TELA
================================================================
Versão Final

Como funciona:
1. Carrega o modelo de reconhecimento treinado (classificadorLBPH.yml).
2. Carrega o mapeamento de IDs para nomes de cartas (mapeamento_nomes.json).
3. Pede ao usuário para selecionar a área da tela onde o jogo está.
4. Entra em um loop contínuo que:
   a. Captura a área selecionada.
   b. Procura por contornos retangulares que pareçam cartas.
   c. Para cada carta encontrada, tenta reconhecê-la usando o modelo.
   d. Exibe o resultado na tela e no terminal.
   
Pressione 'q' na janela de visualização para encerrar.
================================================================
"""

import cv2
import numpy as np
import json
import mss

# --- FUNÇÃO PARA SELECIONAR A ÁREA DE CAPTURA ---
def definir_area_de_captura():
    """
    Abre uma visualização da tela inteira e permite que o usuário 
    selecione uma Região de Interesse (ROI) para a captura.
    """
    print("--- PASSO 1: Seleção de Área ---")
    print("Uma janela com sua tela aparecerá.")
    print("Clique e arraste o mouse para selecionar a área do JOGO e depois pressione Enter.")
    
    with mss.mss() as sct:
        # Captura a tela inteira apenas para o momento da seleção
        frame_selecao = np.array(sct.grab(sct.monitors[1]))
        frame_selecao_bgr = cv2.cvtColor(frame_selecao, cv2.COLOR_BGRA2BGR)

    # Permite ao usuário selecionar a ROI
    roi_coords = cv2.selectROI("Selecione a area do JOGO e pressione Enter", frame_selecao_bgr, fromCenter=False, showCrosshair=False)
    
    # Verifica se uma área válida foi selecionada
    if roi_coords[2] == 0 or roi_coords[3] == 0:
        print("Nenhuma área selecionada. O programa será encerrado.")
        return None

    print(f"Área de captura definida com sucesso! Coordenadas: {roi_coords}")
    cv2.destroyWindow("Selecione a area do JOGO e pressione Enter")
    
    # Retorna as coordenadas no formato que o mss precisa
    return {'top': int(roi_coords[1]), 'left': int(roi_coords[0]), 'width': int(roi_coords[2]), 'height': int(roi_coords[3])}

# --- INÍCIO DO PROGRAMA PRINCIPAL ---

# 1. CARREGAR MODELO E DADOS
try:
    reconhecedor = cv2.face.LBPHFaceRecognizer_create()
    reconhecedor.read('classifier_cartas/classificadorCartasLBPH.yml')

    with open('classifier_cartas/mapeamento_nomes.json', 'r') as f:
        mapa_nomes = json.load(f)
    print("Modelo de reconhecimento e mapeamento de nomes carregados.")
except Exception as e:
    print(f"Erro ao carregar os arquivos de treinamento: {e}")
    print("Verifique se você executou o script 'treinar_modelo_cartas.py' primeiro e se a pasta 'classifier_cartas' existe.")
    exit()

# 2. DEFINIR ÁREA DE CAPTURA
area_de_captura = definir_area_de_captura()
if not area_de_captura:
    exit() # Encerra se nenhuma área for selecionada

# Configurações de exibição
LARGURA_PADRAO = 220  # Deve ser o mesmo tamanho usado nos templates
ALTURA_PADRAO = 300   # Deve ser o mesmo tamanho usado nos templates
font = cv2.FONT_HERSHEY_SIMPLEX

# 3. LOOP PRINCIPAL DE RECONHECIMENTO
print("\n--- PASSO 2: Iniciando reconhecimento ---")
print("Pressione 'q' na janela 'Visao do Jogo' para sair.")

with mss.mss() as sct:
    while True:
        # Captura apenas a área do jogo definida pelo usuário
        frame = np.array(sct.grab(area_de_captura))
        
        # Converte de BGRA (formato do mss) para BGR (formato do OpenCV)
        frame_visualizacao = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Pré-processamento para detecção de contornos
        gray = cv2.cvtColor(frame_visualizacao, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # Ajuste o primeiro valor (127) se a detecção de contornos estiver falhando
        _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)
        
        contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contornos:
            # Filtra os contornos por área para ignorar ruídos
            area = cv2.contourArea(cnt)
            if area > 4600: # Ajuste este valor dependendo do tamanho das cartas na tela
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                # Se o contorno tem 4 lados, é um bom candidato a ser uma carta
                if len(approx) == 4:
                    (x, y, w, h) = cv2.boundingRect(approx)
                    
                    # Recorta a carta encontrada da imagem em escala de cinza
                    carta_recortada = gray[y:y+h, x:x+w]
                    # Padroniza o tamanho da carta para o mesmo do treinamento
                    carta_padronizada = cv2.resize(carta_recortada, (LARGURA_PADRAO, ALTURA_PADRAO))

                    # Realiza a predição
                    id_predito, confianca = reconhecedor.predict(carta_padronizada)

                    # Avalia a confiança (para LBPH, menor é melhor)
                    if confianca < 100: # Ajuste este limiar conforme seus testes
                        nome_carta = mapa_nomes.get(str(id_predito), "Desconhecida")
                        
                        # Exibe o resultado no terminal
                        print(f"Identificado: {nome_carta} (Confiança: {confianca:.2f})")
                        
                        # Desenha o resultado na janela de visualização
                        cv2.rectangle(frame_visualizacao, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame_visualizacao, nome_carta, (x, y - 10), font, 0.8, (0, 255, 0), 2)
                    else:
                        # Opcional: desenhar um retângulo vermelho para cartas não identificadas
                        cv2.rectangle(frame_visualizacao, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(frame_visualizacao, "Nao Identificada", (x, y - 10), font, 0.8, (0, 0, 255), 2)

        cv2.imshow("Visao do Jogo", frame_visualizacao)
        
        # Encerra o programa se a tecla 'q' for pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Libera os recursos
cv2.destroyAllWindows()
print("\nPrograma encerrado.")