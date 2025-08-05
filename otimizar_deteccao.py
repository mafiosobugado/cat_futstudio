#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 OTIMIZADOR DE DETECÇÃO - FOOTBALL STUDIO
Sistema para otimizar coordenadas e melhorar precisão
"""

import cv2
import numpy as np
import pytesseract
import pyautogui
import json
import os
from datetime import datetime

def capturar_tela_completa():
    """Captura a tela completa"""
    try:
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        print(f"📏 Tela capturada: {img.shape[1]}x{img.shape[0]}")
        return img
    except Exception as e:
        print(f"❌ Erro ao capturar tela: {e}")
        return None

def detectar_com_coordenadas_otimizadas(img):
    """Detecta cartas com coordenadas otimizadas baseadas na sua imagem"""
    try:
        altura, largura = img.shape[:2]
        print(f"📐 Analisando imagem: {largura}x{altura}")
        
        # Coordenadas OTIMIZADAS baseadas na sua imagem do Football Studio
        # Ajustadas para pegar exatamente as cartas
        
        # CASA (lado esquerdo vermelho)
        casa_x = int(largura * 0.12)   # 12% da largura
        casa_y = int(altura * 0.45)    # 45% da altura  
        casa_w = int(largura * 0.28)   # 28% da largura
        casa_h = int(altura * 0.45)    # 45% da altura
        
        # VISITANTE (lado direito azul)
        visit_x = int(largura * 0.6)    # 60% da largura
        visit_y = int(altura * 0.45)    # 45% da altura
        visit_w = int(largura * 0.28)   # 28% da largura  
        visit_h = int(altura * 0.45)    # 45% da altura
        
        print(f"🎯 CASA: x={casa_x}, y={casa_y}, w={casa_w}, h={casa_h}")
        print(f"🎯 VISITANTE: x={visit_x}, y={visit_y}, w={visit_w}, h={visit_h}")
        
        # Extrair regiões
        regiao_casa = img[casa_y:casa_y+casa_h, casa_x:casa_x+casa_w]
        regiao_visitante = img[visit_y:visit_y+visit_h, visit_x:visit_x+visit_w]
        
        # Salvar regiões para debug
        timestamp = datetime.now().strftime("%H%M%S")
        cv2.imwrite(f"debug_otimizado_casa_{timestamp}.png", regiao_casa)
        cv2.imwrite(f"debug_otimizado_visitante_{timestamp}.png", regiao_visitante)
        
        # Detectar cartas
        carta_casa = detectar_carta_ocr_robusto(regiao_casa, "CASA")
        carta_visitante = detectar_carta_ocr_robusto(regiao_visitante, "VISITANTE")
        
        return carta_casa, carta_visitante, {
            'casa': {'x': casa_x, 'y': casa_y, 'w': casa_w, 'h': casa_h},
            'visitante': {'x': visit_x, 'y': visit_y, 'w': visit_w, 'h': visit_h}
        }
        
    except Exception as e:
        print(f"❌ Erro na detecção: {e}")
        return None, None, None

def detectar_carta_ocr_robusto(img_regiao, lado):
    """OCR robusto para detectar cartas"""
    try:
        if img_regiao is None or img_regiao.size == 0:
            return None
            
        print(f"🔬 Analisando {lado}...")
        
        # Cartas válidas
        cartas_validas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(img_regiao, cv2.COLOR_BGR2GRAY)
        
        # Múltiplas técnicas de preprocessing
        metodos = []
        
        # 1. OTSU
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        metodos.append(('OTSU', otsu))
        
        # 2. Adaptativo
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        metodos.append(('ADAPTATIVO', adaptive))
        
        # 3. Threshold simples
        _, simple = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        metodos.append(('SIMPLES', simple))
        
        # 4. Threshold invertido
        _, invertido = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        metodos.append(('INVERTIDO', invertido))
        
        # 5. Blur + OTSU
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        _, blur_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        metodos.append(('BLUR_OTSU', blur_otsu))
        
        resultados = []
        
        for nome, processed in metodos:
            try:
                # Redimensionar para melhorar OCR
                h, w = processed.shape
                if h < 60 or w < 40:
                    scale = max(60/h, 40/w, 2.0)
                    new_h, new_w = int(h * scale), int(w * scale)
                    processed = cv2.resize(processed, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
                
                # OCR com configurações específicas
                configs = [
                    '--psm 8 -c tessedit_char_whitelist=A23456789JQK10',
                    '--psm 7 -c tessedit_char_whitelist=A23456789JQK10',
                    '--psm 6 -c tessedit_char_whitelist=A23456789JQK10',
                    '--psm 10 -c tessedit_char_whitelist=A23456789JQK10'
                ]
                
                for config in configs:
                    texto = pytesseract.image_to_string(processed, config=config).strip()
                    # Limpar texto
                    texto_limpo = ''.join(c for c in texto if c.isalnum())
                    
                    if texto_limpo in cartas_validas:
                        resultados.append(texto_limpo)
                        print(f"   ✅ {nome}: {texto_limpo}")
                        
            except Exception as e:
                continue
        
        # Escolher resultado mais comum
        if resultados:
            from collections import Counter
            contador = Counter(resultados)
            carta_final = contador.most_common(1)[0][0]
            confianca = contador[carta_final]
            print(f"🎯 {lado}: {carta_final} (confiança: {confianca}/{len(resultados)})")
            return carta_final
        else:
            print(f"❌ {lado}: Nenhuma carta detectada")
            return None
            
    except Exception as e:
        print(f"❌ Erro OCR {lado}: {e}")
        return None

def salvar_coordenadas_otimizadas(coordenadas):
    """Salva coordenadas otimizadas"""
    try:
        with open("coordenadas_otimizadas.json", "w") as f:
            json.dump(coordenadas, f, indent=2)
        print("✅ Coordenadas otimizadas salvas!")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

def testar_deteccao_otimizada():
    """Testa a detecção com coordenadas otimizadas"""
    print("🚀 TESTANDO DETECÇÃO OTIMIZADA")
    print("=" * 50)
    
    for tentativa in range(3):
        print(f"\n🔄 Tentativa {tentativa + 1}/3")
        
        # Capturar tela
        img = capturar_tela_completa()
        if img is None:
            continue
            
        # Detectar com coordenadas otimizadas
        carta_casa, carta_visitante, coordenadas = detectar_com_coordenadas_otimizadas(img)
        
        if carta_casa and carta_visitante:
            print(f"✅ SUCESSO:")
            print(f"   🏠 CASA: {carta_casa}")
            print(f"   ✈️ VISITANTE: {carta_visitante}")
            
            # Determinar vencedor
            valores_cartas = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
            
            valor_casa = valores_cartas.get(carta_casa, 0)
            valor_visitante = valores_cartas.get(carta_visitante, 0)
            
            if valor_casa > valor_visitante:
                vencedor = "CASA"
            elif valor_visitante > valor_casa:
                vencedor = "VISITANTE"
            else:
                vencedor = "EMPATE"
                
            print(f"   🏆 VENCEDOR: {vencedor}")
            
            # Salvar coordenadas
            if coordenadas:
                salvar_coordenadas_otimizadas(coordenadas)
                
            return True
        else:
            print(f"❌ FALHA: CASA={carta_casa}, VISITANTE={carta_visitante}")
            
        print("⏳ Aguardando 5 segundos...")
        import time
        time.sleep(5)
    
    print("\n❌ Todas as tentativas falharam")
    return False

if __name__ == "__main__":
    print("🎯 OTIMIZADOR DE DETECÇÃO - FOOTBALL STUDIO")
    print("=" * 50)
    print("📋 Este script irá:")
    print("   1. Capturar a tela do Football Studio")
    print("   2. Usar coordenadas otimizadas")
    print("   3. Testar detecção de cartas")
    print("   4. Salvar coordenadas que funcionam")
    print("\n🎮 Abra o Football Studio e pressione Enter...")
    input()
    
    sucesso = testar_deteccao_otimizada()
    
    if sucesso:
        print("\n🎉 OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("📁 Coordenadas salvas em 'coordenadas_otimizadas.json'")
        print("💡 Agora execute o sistema principal:")
        print("   python app.py")
    else:
        print("\n⚠️ Otimização não obteve sucesso completo")
        print("📝 Verifique se o Football Studio está visível na tela")
        print("🔧 Pode ser necessário ajustar coordenadas manualmente")
