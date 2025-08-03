import pyautogui
import time

print("=== Ferramenta de Captura de Coordenadas ===")
print("Posicione o mouse sobre a tela e veja as coordenadas em tempo real.")
print("1. Leve o mouse para o CANTO SUPERIOR ESQUERDO da área que deseja capturar e anote os valores de X e Y.")
print("2. Leve o mouse para o CANTO INFERIOR DIREITO e anote os novos valores de X e Y.")
print("Pressione Ctrl+C no terminal para parar.")

try:
    while True:
        x, y = pyautogui.position()
        posicao_str = f"X: {x:4d} Y: {y:4d}"
        print(posicao_str, end='\r') # O '\r' faz a linha se atualizar em vez de criar novas
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nScript finalizado.")