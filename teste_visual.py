# Salve este arquivo como: teste_visual.py
import cv2
import numpy as np
import mss
import time
import os

# --- CONFIGURAÇÃO ---
# ==============================================================================
# ATENÇÃO: EDITE AS LINHAS ABAIXO COM AS COORDENADAS QUE VOCÊ ANOTOU NO PASSO 1
# ==============================================================================
# Coordenadas da área geral que contém as duas cartas.
# (top, left) são as coordenadas do canto superior esquerdo.
# (width, height) são a largura e altura da área.
MONITOR_AREA = {'top': 460, 'left': 492, 'width': 364, 'height': 70}

# ATENÇÃO: Você ainda precisa ajustar as coordenadas abaixo!
# Elas são RELATIVAS à MONITOR_AREA. O ponto (0,0) é o canto superior esquerdo
# da área que você definiu acima.
ROI_BLUE_CARD = (10, 10, 90, 130) # Exemplo: (x, y, largura, altura)
ROI_RED_CARD = (260, 10, 90, 130) # Exemplo: (x, y, largura, altura)
# ==============================================================================


def load_templates_from_architecture(base_folder='templates/'):
    """Carrega todos os modelos da sua estrutura de pastas."""
    templates = {}
    print("Iniciando carregamento dos modelos...")
    for suit_folder in os.listdir(base_folder):
        suit_path = os.path.join(base_folder, suit_folder)
        if os.path.isdir(suit_path):
            for rank_folder in os.listdir(suit_path):
                rank_path = os.path.join(suit_path, rank_folder)
                if os.path.isdir(rank_path):
                    card_name = rank_folder.replace('template_', '')
                    if card_name not in templates:
                        templates[card_name] = []
                    for template_file in os.listdir(rank_path):
                        if template_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            img_path = os.path.join(rank_path, template_file)
                            template_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                            if template_img is not None:
                                templates[card_name].append(template_img)
    print("Modelos carregados com sucesso!")
    for card, imgs in templates.items():
        print(f" - Carta '{card}': {len(imgs)} variações.")
    return templates

def recognize_card_with_multiple_templates(image_roi, templates):
    """Compara a imagem com todos os modelos e retorna o melhor resultado."""
    best_overall_score = 0.7  # Limite de confiança. Diminua se não reconhecer nada.
    best_overall_card = "Nenhum"
    
    # Converte a imagem para escala de cinza para a comparação
    gray_roi = cv2.cvtColor(image_roi, cv2.COLOR_BGR2GRAY)

    for card_name, template_variations in templates.items():
        for template_img in template_variations:
            # Pula a comparação se o modelo for maior que a imagem capturada
            if gray_roi.shape[0] < template_img.shape[0] or gray_roi.shape[1] < template_img.shape[1]:
                continue

            res = cv2.matchTemplate(gray_roi, template_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            
            if max_val > best_overall_score:
                best_overall_score = max_val
                best_overall_card = card_name
                
    return best_overall_card, best_overall_score

# --- INÍCIO DO PROGRAMA DE TESTE ---
templates = load_templates_from_architecture('templates/')
sct = mss.mss()

print("\n--- INICIANDO TESTE VISUAL ---")
print("Pressione a tecla 'q' em uma das janelas para sair.")

while True:
    # Captura a área principal da tela
    screen_grab = np.array(sct.grab(MONITOR_AREA))
    
    # Extrai as ROIs (Regiões de Interesse) das cartas
    x_blue, y_blue, w_blue, h_blue = ROI_BLUE_CARD
    blue_card_roi = screen_grab[y_blue:y_blue+h_blue, x_blue:x_blue+w_blue]
    
    x_red, y_red, w_red, h_red = ROI_RED_CARD
    red_card_roi = screen_grab[y_red:y_red+h_red, x_red:x_red+w_red]

    # Tenta reconhecer as cartas
    blue_rank, blue_score = recognize_card_with_multiple_templates(blue_card_roi, templates)
    red_rank, red_score = recognize_card_with_multiple_templates(red_card_roi, templates)

    # --- FEEDBACK VISUAL ---
    # Desenha retângulos na imagem principal para você ver onde o programa está "olhando"
    cv2.rectangle(screen_grab, (x_blue, y_blue), (x_blue + w_blue, y_blue + h_blue), (255, 170, 0), 2) # Azul
    cv2.rectangle(screen_grab, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 0, 255), 2) # Vermelho
    
    # Mostra a janela com a captura principal e os retângulos
    cv2.imshow('Visualizador - Principal', screen_grab)

    # Mostra as janelas das ROIs individuais para análise
    cv2.imshow('ROI - Carta Azul', blue_card_roi)
    cv2.imshow('ROI - Carta Vermelha', red_card_roi)

    # Imprime o resultado no terminal para acompanhamento
    print(f"Resultado -> Azul: {blue_rank} (Confiança: {blue_score:.2f}) | Vermelho: {red_rank} (Confiança: {red_score:.2f})")

    # Espera por uma tecla. Se for 'q', o programa fecha.
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    
    # Pausa entre as capturas para não sobrecarregar o PC
    time.sleep(1)
