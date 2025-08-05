"""
Calibrador específico para Football Studio
Sistema para encontrar coordenadas exatas das cartas
"""

import cv2
import numpy as np
import pyautogui
from datetime import datetime
import json

def capturar_tela_completa():
    """Captura a tela completa para análise"""
    print("📸 Capturando tela completa...")
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"captura_calibracao_{timestamp}.png"
    cv2.imwrite(filename, img)
    print(f"💾 Tela salva como: {filename}")
    return img, filename

def detectar_regioes_cartas(img):
    """Detecta automaticamente as regiões das cartas no Football Studio"""
    print("🔍 Analisando imagem para encontrar cartas...")
    
    altura, largura = img.shape[:2]
    print(f"📏 Resolução: {largura}x{altura}")
    
    # Converter para HSV para melhor detecção de cores
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Definir ranges de cores para detectar as áreas das cartas
    # Amarelo/Dourado para CASA
    lower_yellow = np.array([15, 50, 50])
    upper_yellow = np.array([35, 255, 255])
    
    # Azul para VISITANTE  
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    # Criar máscaras
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Salvar máscaras para debug
    cv2.imwrite("debug_mask_yellow.png", mask_yellow)
    cv2.imwrite("debug_mask_blue.png", mask_blue)
    
    coordenadas = {}
    
    # Encontrar contornos para CASA (amarelo)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_yellow:
        # Pegar o maior contorno
        largest_yellow = max(contours_yellow, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_yellow)
        
        # Área específica onde geralmente aparece a carta
        # Ajustar para capturar apenas a região da carta
        carta_x = x + int(w * 0.1)  # 10% da margem esquerda
        carta_y = y + int(h * 0.3)  # 30% da margem superior
        carta_w = int(w * 0.3)      # 30% da largura total
        carta_h = int(h * 0.4)      # 40% da altura total
        
        coordenadas['casa'] = {
            'x': carta_x,
            'y': carta_y, 
            'w': carta_w,
            'h': carta_h
        }
        print(f"🟡 CASA detectada: x={carta_x}, y={carta_y}, w={carta_w}, h={carta_h}")
    
    # Encontrar contornos para VISITANTE (azul)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_blue:
        # Pegar o maior contorno
        largest_blue = max(contours_blue, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_blue)
        
        # Área específica onde geralmente aparece a carta
        carta_x = x + int(w * 0.6)  # 60% da margem esquerda (lado direito)
        carta_y = y + int(h * 0.3)  # 30% da margem superior
        carta_w = int(w * 0.3)      # 30% da largura total
        carta_h = int(h * 0.4)      # 40% da altura total
        
        coordenadas['visitante'] = {
            'x': carta_x,
            'y': carta_y,
            'w': carta_w, 
            'h': carta_h
        }
        print(f"🔵 VISITANTE detectado: x={carta_x}, y={carta_y}, w={carta_w}, h={carta_h}")
    
    return coordenadas

def criar_imagem_debug(img, coordenadas):
    """Cria imagem com as regiões marcadas"""
    debug_img = img.copy()
    
    if 'casa' in coordenadas:
        casa = coordenadas['casa']
        cv2.rectangle(debug_img, 
                     (casa['x'], casa['y']), 
                     (casa['x'] + casa['w'], casa['y'] + casa['h']), 
                     (0, 255, 255), 3)  # Amarelo
        cv2.putText(debug_img, 'CASA', (casa['x'], casa['y']-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    if 'visitante' in coordenadas:
        visit = coordenadas['visitante']
        cv2.rectangle(debug_img, 
                     (visit['x'], visit['y']), 
                     (visit['x'] + visit['w'], visit['y'] + visit['h']), 
                     (255, 0, 0), 3)  # Azul
        cv2.putText(debug_img, 'VISITANTE', (visit['x'], visit['y']-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_filename = f"debug_coordenadas_{timestamp}.png"
    cv2.imwrite(debug_filename, debug_img)
    print(f"🖼️ Debug salvo como: {debug_filename}")
    
    return debug_filename

def salvar_coordenadas(coordenadas):
    """Salva as coordenadas calibradas em arquivo JSON"""
    filename = "coordenadas_calibradas.json"
    with open(filename, 'w') as f:
        json.dump(coordenadas, f, indent=2)
    print(f"💾 Coordenadas salvas em: {filename}")

def calibrar_automatico():
    """Executa calibração automática completa"""
    print("🎯 INICIANDO CALIBRAÇÃO AUTOMÁTICA DO FOOTBALL STUDIO")
    print("="*60)
    
    # Capturar tela
    img, captura_filename = capturar_tela_completa()
    
    # Detectar regiões
    coordenadas = detectar_regioes_cartas(img)
    
    if len(coordenadas) >= 2:
        print("✅ Ambas as regiões detectadas!")
        
        # Criar debug visual
        debug_filename = criar_imagem_debug(img, coordenadas)
        
        # Salvar coordenadas
        salvar_coordenadas(coordenadas)
        
        print("\n📊 COORDENADAS CALIBRADAS:")
        for regiao, coords in coordenadas.items():
            print(f"   {regiao.upper()}: x={coords['x']}, y={coords['y']}, w={coords['w']}, h={coords['h']}")
        
        print(f"\n🔍 Verifique as imagens geradas:")
        print(f"   - {captura_filename} (captura original)")
        print(f"   - {debug_filename} (regiões marcadas)")
        print(f"   - debug_mask_yellow.png (máscara amarela)")
        print(f"   - debug_mask_blue.png (máscara azul)")
        
        return True
    else:
        print("❌ Não foi possível detectar ambas as regiões")
        print("💡 Certifique-se de que o jogo está visível na tela")
        return False

def teste_coordenadas():
    """Testa as coordenadas calibradas"""
    try:
        with open("coordenadas_calibradas.json", 'r') as f:
            coords = json.load(f)
        
        print("🧪 Testando coordenadas calibradas...")
        
        for regiao, coord in coords.items():
            x, y, w, h = coord['x'], coord['y'], coord['w'], coord['h']
            
            # Capturar região específica
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Salvar para verificação
            filename = f"teste_regiao_{regiao}.png"
            cv2.imwrite(filename, img)
            print(f"📸 Região {regiao} salva como: {filename}")
        
        print("✅ Teste concluído! Verifique as imagens geradas.")
        
    except FileNotFoundError:
        print("❌ Arquivo de coordenadas não encontrado")
        print("💡 Execute a calibração primeiro")

if __name__ == "__main__":
    print("CALIBRADOR FOOTBALL STUDIO")
    print("1. Calibração automática")
    print("2. Teste coordenadas existentes")
    
    opcao = input("\nEscolha uma opção (1-2): ").strip()
    
    if opcao == "1":
        calibrar_automatico()
    elif opcao == "2":
        teste_coordenadas()
    else:
        print("❌ Opção inválida")
