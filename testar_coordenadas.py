"""
Script para encontrar as coordenadas corretas das cartas do Football Studio
Execute este script enquanto o jogo estiver aberto
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
import os

def capturar_tela_completa():
    """Captura a tela completa para análise"""
    print("📸 Capturando tela completa em 3 segundos...")
    time.sleep(3)
    
    screenshot = pyautogui.screenshot()
    img_np = np.array(screenshot)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    # Salvar imagem
    cv2.imwrite("captura_completa.png", img_bgr)
    print("✅ Tela capturada e salva como 'captura_completa.png'")
    
    return img_bgr

def testar_diferentes_regioes():
    """Testa diferentes regiões da tela para encontrar as cartas"""
    print("🔍 Testando diferentes regiões...")
    
    # Região 1: Área inferior (onde geralmente ficam as cartas)
    regioes_teste = [
        {"nome": "Inferior_Completa", "x": 0, "y": 600, "w": 1920, "h": 300},
        {"nome": "Cartas_Centro", "x": 200, "y": 650, "w": 800, "h": 150},
        {"nome": "Casa_Esquerda", "x": 50, "y": 600, "w": 400, "h": 200},
        {"nome": "Visitante_Direita", "x": 500, "y": 600, "w": 400, "h": 200},
        {"nome": "Area_Amarela", "x": 40, "y": 600, "w": 460, "h": 200},
        {"nome": "Area_Azul", "x": 500, "y": 600, "w": 460, "h": 200},
    ]
    
    for i, regiao in enumerate(regioes_teste):
        try:
            print(f"📷 Testando região {i+1}: {regiao['nome']}")
            
            screenshot = pyautogui.screenshot(region=(regiao['x'], regiao['y'], regiao['w'], regiao['h']))
            img_np = np.array(screenshot)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            
            # Salvar região
            nome_arquivo = f"regiao_{i+1}_{regiao['nome']}.png"
            cv2.imwrite(nome_arquivo, img_bgr)
            print(f"  ✅ Salvo como '{nome_arquivo}'")
            
            time.sleep(1)  # Pausa entre capturas
            
        except Exception as e:
            print(f"  ❌ Erro na região {regiao['nome']}: {e}")

def detectar_cores_cartas(img_path):
    """Analisa as cores presentes na imagem para encontrar padrões"""
    try:
        img = cv2.imread(img_path)
        if img is None:
            print(f"❌ Não foi possível carregar {img_path}")
            return
        
        print(f"🎨 Analisando cores em {img_path}...")
        
        # Converter para HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Definir ranges de cores
        cores = {
            "Amarelo/Dourado": ([20, 100, 100], [30, 255, 255]),
            "Azul": ([100, 50, 50], [130, 255, 255]),
            "Vermelho": ([0, 50, 50], [10, 255, 255]),
            "Branco": ([0, 0, 200], [180, 30, 255]),
            "Preto": ([0, 0, 0], [180, 255, 50])
        }
        
        for nome_cor, (lower, upper) in cores.items():
            lower = np.array(lower)
            upper = np.array(upper)
            
            mask = cv2.inRange(hsv, lower, upper)
            pixels = cv2.countNonZero(mask)
            
            if pixels > 100:  # Se encontrou pixels suficientes
                print(f"  🎯 {nome_cor}: {pixels} pixels")
                
                # Salvar máscara
                nome_mask = f"mask_{nome_cor.lower()}_{os.path.basename(img_path)}"
                cv2.imwrite(nome_mask, mask)
        
    except Exception as e:
        print(f"❌ Erro ao analisar cores: {e}")

def encontrar_posicao_mouse():
    """Mostra a posição do mouse em tempo real"""
    print("🖱️ Posição do mouse (pressione Ctrl+C para parar):")
    print("Posicione o mouse sobre as cartas para ver as coordenadas")
    
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\rPosição: x={x}, y={y}   ", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n✅ Monitoramento da posição do mouse finalizado")

def main():
    """Função principal"""
    print("="*60)
    print("🎮 TESTE DE COORDENADAS - FOOTBALL STUDIO")
    print("="*60)
    
    while True:
        print("\nEscolha uma opção:")
        print("1 - Capturar tela completa")
        print("2 - Testar diferentes regiões")
        print("3 - Analisar cores em imagem existente")
        print("4 - Mostrar posição do mouse")
        print("5 - Sair")
        
        opcao = input("\nDigite sua opção: ").strip()
        
        if opcao == "1":
            capturar_tela_completa()
            
        elif opcao == "2":
            testar_diferentes_regioes()
            
        elif opcao == "3":
            arquivo = input("Digite o nome do arquivo de imagem: ").strip()
            if os.path.exists(arquivo):
                detectar_cores_cartas(arquivo)
            else:
                print(f"❌ Arquivo '{arquivo}' não encontrado")
                
        elif opcao == "4":
            encontrar_posicao_mouse()
            
        elif opcao == "5":
            print("👋 Saindo...")
            break
            
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    main()
