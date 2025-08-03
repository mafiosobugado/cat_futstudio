import cv2
import numpy as np
import os

def debug_deteccao_cartas(img):
    """
    Versão de debug da função original para visualizar cada etapa do processo.
    """
    print("Iniciando processo de debug da detecção...")

    # --- Etapa 1: Conversão para HSV ---
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print("Etapa 1: Imagem convertida para HSV.")

    # --- Etapa 2: Definição e Aplicação das Máscaras de Cor ---
    # Estes são os valores do seu código original. Eles são o ponto mais provável de falha.
    # Vermelho (Casa)
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # Azul (Visitante)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Criar máscaras
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.add(mask_red1, mask_red2)  # Usar cv2.add é mais seguro
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    print("Etapa 2: Máscaras de cor criadas.")
    
    # <<< VISUALIZAÇÃO DAS MÁSCARAS >>>
    # Esta é a etapa mais importante. As áreas de interesse (cartas) devem aparecer em branco.
    cv2.imshow('Debug - Mascara Vermelha', mask_red)
    cv2.imshow('Debug - Mascara Azul', mask_blue)


    # --- Etapa 3: Encontrar Contornos ---
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Etapa 3: Encontrados {len(contours_red)} contornos vermelhos e {len(contours_blue)} contornos azuis (antes de filtrar).")

    # --- Etapa 4: Desenhar TODOS os Contornos Encontrados (Antes de Filtrar) ---
    img_com_contornos = img.copy()
    # Desenha todos os contornos vermelhos em VERDE
    cv2.drawContours(img_com_contornos, contours_red, -1, (0, 255, 0), 2)
    # Desenha todos os contornos azuis em AMARELO
    cv2.drawContours(img_com_contornos, contours_blue, -1, (0, 255, 255), 2)
    
    # <<< VISUALIZAÇÃO DOS CONTORNOS >>>
    cv2.imshow('Debug - Todos os Contornos Encontrados', img_com_contornos)

    # --- Etapa 5: Filtragem (Lógica Original) ---
    print("\n--- Iniciando Filtragem ---")
    cartas_vermelhas_filtradas = 0
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 30 and h > 40:
                cartas_vermelhas_filtradas += 1
                # Desenha um retângulo na carta filtrada
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)

    cartas_azuis_filtradas = 0
    for contour in contours_blue:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 30 and h > 40:
                cartas_azuis_filtradas += 1
                # Desenha um retângulo na carta filtrada
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

    print(f"Etapa 5: Após filtrar, restaram {cartas_vermelhas_filtradas} cartas vermelhas e {cartas_azuis_filtradas} cartas azuis.")

    # <<< VISUALIZAÇÃO FINAL >>>
    cv2.imshow('Debug - Resultado Final (Cartas Identificadas)', img)


# --- SCRIPT PRINCIPAL ---
if __name__ == '__main__':
    # IMPORTANTE: Coloque aqui o nome exato do seu arquivo de captura
    nome_arquivo_debug = "debug_captura_132706.png" # <<< MUDE ESTE NOME

    if not os.path.exists(nome_arquivo_debug):
        print(f"ERRO: Arquivo de debug '{nome_arquivo_debug}' não encontrado na pasta.")
        print("Verifique se o nome está correto e se o arquivo existe.")
    else:
        # Carrega a imagem salva pelo seu sistema
        imagem_capturada = cv2.imread(nome_arquivo_debug)

        # Chama a função de debug
        debug_deteccao_cartas(imagem_capturada)

        # Espera uma tecla ser pressionada para fechar as janelas
        print("\n>>> Pressione qualquer tecla nas janelas de imagem para fechar o debug. <<<")
        cv2.waitKey(0)
        cv2.destroyAllWindows()