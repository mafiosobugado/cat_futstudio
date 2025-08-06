import cv2
import numpy as np
import mss
import os
import time

def load_templates(base_folder='templates_cartas/'):
    """
    Carrega todos os modelos da estrutura de pastas, criando nomes únicos para cada carta.
    Ex: 'copas_2', 'ouros_as'.
    """
    templates = {}
    print("Iniciando carregamento dos modelos...")
    
    if not os.path.isdir(base_folder):
        print(f"ERRO: A pasta de modelos '{base_folder}' não foi encontrada.")
        return None

    for suit_folder in os.listdir(base_folder):
        suit_path = os.path.join(base_folder, suit_folder)
        if os.path.isdir(suit_path):
            for rank_folder in os.listdir(suit_path):
                rank_path = os.path.join(suit_path, rank_folder)
                if os.path.isdir(rank_path):
                    card_name = f"{suit_folder}_{rank_folder}"
                    
                    if card_name not in templates:
                        templates[card_name] = []
                        
                    for template_file in os.listdir(rank_path):
                        if template_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            img_path = os.path.join(rank_path, template_file)
                            template_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                            if template_img is not None:
                                templates[card_name].append(template_img)
    
    if not templates:
        print("Nenhum modelo foi carregado. Verifique a estrutura de pastas e os nomes.")
        return None

    print("\nModelos carregados com sucesso!")
    for card, imgs in templates.items():
        print(f" - Carta '{card}': {len(imgs)} variações.")
    return templates

def recognize_card(image_roi, templates):
    """
    Compara a imagem com todos os modelos e retorna o melhor resultado.
    """
    # Limite de confiança. Ajuste se necessário.
    # Valores mais altos = mais exigente. Valores mais baixos = mais flexível.
    best_overall_score = 0.50 
    best_overall_card = "Nenhuma"
    
    # Converte a imagem capturada para escala de cinza
    gray_roi = cv2.cvtColor(image_roi, cv2.COLOR_BGRA2GRAY)

    for card_name, template_variations in templates.items():
        for template_img in template_variations:
            # Pula se o modelo for maior que a imagem capturada
            if gray_roi.shape[0] < template_img.shape[0] or gray_roi.shape[1] < template_img.shape[1]:
                continue

            res = cv2.matchTemplate(gray_roi, template_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            
            if max_val > best_overall_score:
                best_overall_score = max_val
                best_overall_card = card_name
                
    return best_overall_card, best_overall_score

def configurar_rois_cartas():
    """
    Permite ao usuário selecionar as ROIs para duas cartas sequencialmente.
    """
    print("\n--- CONFIGURAÇÃO DAS ÁREAS DAS CARTAS ---")
    
    with mss.mss() as sct:
        frame_para_selecao = np.array(sct.grab(sct.monitors[1]))
        frame_para_selecao_bgr = cv2.cvtColor(frame_para_selecao, cv2.COLOR_BGRA2BGR)

    roi1_coords = cv2.selectROI("1. Selecione a PRIMEIRA CARTA e pressione Enter", frame_para_selecao_bgr, fromCenter=False)
    if roi1_coords[2] == 0: return None, None
    roi1 = {'top': int(roi1_coords[1]), 'left': int(roi1_coords[0]), 'width': int(roi1_coords[2]), 'height': int(roi1_coords[3])}
    print(f"-> Área da Carta 1 definida em: {roi1}")

    roi2_coords = cv2.selectROI("2. Selecione a SEGUNDA CARTA e pressione Enter", frame_para_selecao_bgr, fromCenter=False)
    if roi2_coords[2] == 0: return None, None
    roi2 = {'top': int(roi2_coords[1]), 'left': int(roi2_coords[0]), 'width': int(roi2_coords[2]), 'height': int(roi2_coords[3])}
    print(f"-> Área da Carta 2 definida em: {roi2}")
    
    cv2.destroyAllWindows()
    return roi1, roi2

# --- INÍCIO DO PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    # 1. Carregar os modelos de cartas
    templates = load_templates(base_folder='templates_cartas/')
    if not templates:
        exit() # Encerra o programa se nenhum modelo for carregado

    # 2. Configurar as áreas de captura das cartas
    roi_carta1, roi_carta2 = configurar_rois_cartas()
    if not roi_carta1 or not roi_carta2:
        exit() # Encerra se o usuário não selecionar as áreas

    # 3. Iniciar o loop de reconhecimento
    print("\n--- INICIANDO RECONHECIMENTO ---")
    print("Pressione a tecla 'q' na janela de visualização para sair.")
    
    with mss.mss() as sct:
        while True:
            # Captura as duas áreas de interesse definidas pelo usuário
            carta1_img = np.array(sct.grab(roi_carta1))
            carta2_img = np.array(sct.grab(roi_carta2))

            # Tenta reconhecer cada carta
            nome_carta1, score1 = recognize_card(carta1_img, templates)
            nome_carta2, score2 = recognize_card(carta2_img, templates)

            # Imprime o resultado no terminal
            print(f"Carta 1: {nome_carta1} ({score1:.2f}) | Carta 2: {nome_carta2} ({score2:.2f})")

            # --- Feedback Visual (Opcional, mas útil) ---
            # Mostra o que o programa está "vendo"
            cv2.imshow('Visao - Carta 1', carta1_img)
            cv2.imshow('Visao - Carta 2', carta2_img)
            
            # Pausa para não sobrecarregar o PC
            time.sleep(1)

            # Condição para sair do loop
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break