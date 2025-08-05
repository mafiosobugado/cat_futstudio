#!/usr/bin/env python3
"""
Script para testar o sistema de reconhecimento por templates
"""
import cv2
import numpy as np
import pyautogui
from reconhecimento_templates import TemplateCardRecognizer

def main():
    print("🧪 TESTE DO SISTEMA DE TEMPLATES")
    print("=" * 50)
    
    # Inicializar o reconhecedor
    recognizer = TemplateCardRecognizer()
    
    # Mostrar templates carregados
    print(f"📦 Templates carregados: {len(recognizer.templates)}")
    if recognizer.templates:
        print("   Valores disponíveis:", list(recognizer.templates.keys()))
    else:
        print("❌ Nenhum template encontrado!")
        print("💡 Execute 'python reconhecimento_templates.py' primeiro")
        return
    
    print("\n🎯 Fazendo captura de tela...")
    
    # Capturar tela
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    altura, largura = img.shape[:2]
    
    print(f"📏 Imagem capturada: {largura}x{altura}")
    
    # COORDENADAS DOS BLOCOS DAS CARTAS (ÁREA AUMENTADA)
    casa_x = int(largura * 0.30)    # 30% da largura (aumentado)
    casa_y = int(altura * 0.60)     # 60% da altura (aumentado)
    casa_w = int(largura * 0.20)    # 20% da largura (aumentado)
    casa_h = int(altura * 0.35)     # 35% da altura (aumentado)
    
    visit_x = int(largura * 0.50)   # 50% da largura (aumentado)
    visit_y = int(altura * 0.60)    # 60% da altura (aumentado)
    visit_w = int(largura * 0.20)   # 20% da largura (aumentado)
    visit_h = int(altura * 0.35)    # 35% da altura (aumentado)
    
    print(f"🔶 BLOCO CASA: x={casa_x}, y={casa_y}, w={casa_w}, h={casa_h}")
    print(f"🔷 BLOCO VISITANTE: x={visit_x}, y={visit_y}, w={visit_w}, h={visit_h}")
    
    # Extrair blocos
    bloco_casa = img[casa_y:casa_y+casa_h, casa_x:casa_x+casa_w]
    bloco_visitante = img[visit_y:visit_y+visit_h, visit_x:visit_x+visit_w]
    
    # Salvar blocos para análise
    cv2.imwrite("teste_bloco_casa.png", bloco_casa)
    cv2.imwrite("teste_bloco_visitante.png", bloco_visitante)
    print("💾 Blocos salvos: teste_bloco_casa.png e teste_bloco_visitante.png")
    
    # Testar reconhecimento
    print("\n🔍 TESTE DE RECONHECIMENTO:")
    
    print("  🏠 CASA:", end=" ")
    valor_casa, sim_casa = recognizer.reconhecer_carta(bloco_casa)
    if valor_casa:
        print(f"✅ {valor_casa} (similaridade: {sim_casa:.3f})")
    else:
        print(f"❌ Não reconhecida (max: {sim_casa:.3f})")
    
    print("  ✈️ VISITANTE:", end=" ")
    valor_visitante, sim_visitante = recognizer.reconhecer_carta(bloco_visitante)
    if valor_visitante:
        print(f"✅ {valor_visitante} (similaridade: {sim_visitante:.3f})")
    else:
        print(f"❌ Não reconhecida (max: {sim_visitante:.3f})")
    
    print("\n📊 RESULTADO:")
    if valor_casa and valor_visitante:
        print(f"🎉 AMBAS DETECTADAS: {valor_casa} x {valor_visitante}")
        # Simular determinação de vencedor
        if valor_casa == valor_visitante:
            print("🏆 EMPATE")
        elif valor_casa in ['A'] or (valor_casa.isdigit() and int(valor_casa) == 1):
            casa_val = 1
        elif valor_casa in ['J', 'Q', 'K']:
            casa_val = 10
        else:
            casa_val = int(valor_casa) if valor_casa.isdigit() else 0
            
        if valor_visitante in ['A'] or (valor_visitante.isdigit() and int(valor_visitante) == 1):
            visit_val = 1
        elif valor_visitante in ['J', 'Q', 'K']:
            visit_val = 10
        else:
            visit_val = int(valor_visitante) if valor_visitante.isdigit() else 0
            
        if casa_val > visit_val:
            print("🏆 CASA VENCE")
        elif visit_val > casa_val:
            print("🏆 VISITANTE VENCE")
        else:
            print("🏆 EMPATE")
    else:
        print("❌ Falha na detecção")
        if len(recognizer.templates) < 10:
            print("💡 Crie mais templates executando 'python reconhecimento_templates.py'")

if __name__ == "__main__":
    main()
