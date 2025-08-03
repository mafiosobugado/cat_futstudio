import cv2
import numpy as np
import os

# Função vazia necessária para a criação das trackbars
def nada(x):
    pass

# --- SCRIPT PRINCIPAL DE CALIBRAGEM ---
if __name__ == '__main__':
    # IMPORTANTE: Coloque aqui o nome exato do seu arquivo de captura
    nome_arquivo_debug = "debug_captura_134234.png" # <<< MUDE ESTE NOME PARA O SEU ARQUIVO

    if not os.path.exists(nome_arquivo_debug):
        print(f"ERRO: Arquivo de debug '{nome_arquivo_debug}' não encontrado na pasta.")
    else:
        # Carrega a imagem que vamos analisar
        img = cv2.imread(nome_arquivo_debug)
        # Redimensiona a imagem para caber melhor na tela, se for muito grande
        # Mantém a proporção original
        scale_percent = 50 # percentual do tamanho original
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img_resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        # Converte a imagem para o espaço de cores HSV
        hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)

        # Cria uma janela para os controles (trackbars)
        cv2.namedWindow("Controles")
        cv2.resizeWindow("Controles", 600, 300)

        # Cria as trackbars para os valores de HUE, SATURATION e VALUE
        # HUE: 0-179 (no OpenCV)
        # SATURATION: 0-255
        # VALUE: 0-255
        cv2.createTrackbar("HUE Min", "Controles", 0, 179, nada)
        cv2.createTrackbar("HUE Max", "Controles", 179, 179, nada)
        cv2.createTrackbar("SAT Min", "Controles", 0, 255, nada)
        cv2.createTrackbar("SAT Max", "Controles", 255, 255, nada)
        cv2.createTrackbar("VAL Min", "Controles", 0, 255, nada)
        cv2.createTrackbar("VAL Max", "Controles", 255, 255, nada)

        print("\n=== Calibrador de Cores HSV ===")
        print("Ajuste os controles deslizantes para isolar a cor desejada na janela 'Mascara Resultante'.")
        print("Quando estiver satisfeito, anote os valores de LOWER e UPPER exibidos no terminal.")
        print("Pressione 'q' na janela de imagem para sair.")

        while True:
            # Lê os valores atuais das trackbars
            h_min = cv2.getTrackbarPos("HUE Min", "Controles")
            h_max = cv2.getTrackbarPos("HUE Max", "Controles")
            s_min = cv2.getTrackbarPos("SAT Min", "Controles")
            s_max = cv2.getTrackbarPos("SAT Max", "Controles")
            v_min = cv2.getTrackbarPos("VAL Min", "Controles")
            v_max = cv2.getTrackbarPos("VAL Max", "Controles")

            # Cria os arrays numpy com os limites inferior e superior
            lower_bound = np.array([h_min, s_min, v_min])
            upper_bound = np.array([h_max, s_max, v_max])

            # Cria a máscara usando os valores atuais
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            
            # Mostra a imagem original e a máscara resultante
            cv2.imshow("Original Redimensionada", img_resized)
            cv2.imshow("Mascara Resultante", mask)
            
            # Imprime os valores no terminal para fácil cópia
            print(f"\rLOWER: [{h_min:3d}, {s_min:3d}, {v_min:3d}] | UPPER: [{h_max:3d}, {s_max:3d}, {v_max:3d}]", end="")

            # Espera por uma tecla, se for 'q', sai do loop
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                break
        
        print("\n\nCalibragem finalizada.")
        cv2.destroyAllWindows()