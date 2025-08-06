import cv2
import numpy as np
import mss
from datetime import datetime

def definir_area_de_captura():
    """
    Abre uma visualização da tela, permite que o usuário selecione uma ROI
    e imprime as coordenadas detalhadas no terminal.
    Retorna as coordenadas da ROI como um dicionário.
    """
    print("Posicione a janela do jogo na tela principal.")
    print("Pressione 'Enter' ou 'Espaço' após selecionar a área.")
    print("Pressione 'c' para cancelar a seleção.")

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        frame = np.array(sct.grab(monitor))
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        cv2.imshow("Selecione a Area de Captura", frame_bgr)
        roi = cv2.selectROI("Selecione a Area de Captura", frame_bgr, fromCenter=False)
        cv2.destroyWindow("Selecione a Area de Captura") # Fecha a janela de seleção imediatamente

        if roi[2] > 0 and roi[3] > 0:
            # --- NOVA SEÇÃO DE IMPRESSÃO DAS COORDENADAS ---
            print("\n✅ Área de captura definida com sucesso!")
            print("-----------------------------------------")
            print(f"  Coordenadas (x, y, largura, altura): {roi}")
            print(f"  Ponto X inicial: {roi[0]}")
            print(f"  Ponto Y inicial: {roi[1]}")
            print(f"  Largura da área: {roi[2]} pixels")
            print(f"  Altura da área:  {roi[3]} pixels")
            print("-----------------------------------------")
            # --- FIM DA NOVA SEÇÃO ---

            return {
                "top": int(roi[1]),
                "left": int(roi[0]),
                "width": int(roi[2]),
                "height": int(roi[3])
            }
        else:
            print("\n❌ Nenhuma área selecionada. O programa será encerrado.")
            return None

if __name__ == "__main__":
    area_captura = definir_area_de_captura()

    if area_captura:
        print("\n--- Pré-visualização iniciada ---")
        print("Foque a janela 'Area Capturada'.")
        print("Pressione 'p' para salvar a imagem atual.")
        print("Pressione 'q' para sair.")
        
        with mss.mss() as sct:
            while True:
                frame_capturado = np.array(sct.grab(area_captura))
                
                cv2.imshow('Area Capturada', frame_capturado)

                key = cv2.waitKey(1) & 0xFF

                if key == ord('p'):
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
                    nome_arquivo = f"captura_{timestamp}.png"
                    
                    cv2.imwrite(nome_arquivo, frame_capturado)
                    print(f"Imagem capturada e salva como: {nome_arquivo}")

                elif key == ord('q'):
                    print("Encerrando o programa.")
                    break
        
        cv2.destroyAllWindows()