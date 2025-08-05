#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 TESTE ESPECÍFICO DOS BLOCOS DAS CARTAS
Teste focado apenas nos blocos onde aparecem as cartas no Football Studio
"""

import cv2
import numpy as np
import pytesseract
import pyautogui
from datetime import datetime
import os

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def testar_blocos_cartas():
    """Teste específico dos blocos das cartas"""
    print("🎯 TESTE DOS BLOCOS DAS CARTAS - FOOTBALL STUDIO")
    print("=" * 60)
    
    try:
        # Capturar tela completa
        print("📸 Capturando tela completa...")
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        altura, largura = img.shape[:2]
        
        print(f"📏 Tela: {largura}x{altura}")
        
        # COORDENADAS EXATAS DOS BLOCOS (baseadas na sua imagem)
        print("\n🎯 Definindo coordenadas dos blocos...")
        
        # Bloco CASA (lado esquerdo laranja)
        casa_x = int(largura * 0.355)   # 35.5% da largura 
        casa_y = int(altura * 0.72)     # 72% da altura
        casa_w = int(largura * 0.14)    # 14% da largura
        casa_h = int(altura * 0.25)     # 25% da altura
        
        # Bloco VISITANTE (lado direito azul)
        visit_x = int(largura * 0.495)  # 49.5% da largura
        visit_y = int(altura * 0.72)    # 72% da altura  
        visit_w = int(largura * 0.14)   # 14% da largura
        visit_h = int(altura * 0.25)    # 25% da altura
        
        print(f"🔶 CASA: x={casa_x}, y={casa_y}, w={casa_w}, h={casa_h}")
        print(f"🔷 VISITANTE: x={visit_x}, y={visit_y}, w={visit_w}, h={visit_h}")
        
        # Extrair blocos
        print("\n📦 Extraindo blocos...")
        bloco_casa = img[casa_y:casa_y+casa_h, casa_x:casa_x+casa_w]
        bloco_visitante = img[visit_y:visit_y+visit_h, visit_x:visit_x+visit_w]
        
        # Verificar se blocos foram extraídos
        if bloco_casa.size == 0:
            print("❌ Bloco CASA vazio!")
            return False
        if bloco_visitante.size == 0:
            print("❌ Bloco VISITANTE vazio!")
            return False
        
        print(f"✅ Bloco CASA: {bloco_casa.shape}")
        print(f"✅ Bloco VISITANTE: {bloco_visitante.shape}")
        
        # Salvar blocos para análise
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_casa = f"teste_bloco_casa_{timestamp}.png"
        nome_visitante = f"teste_bloco_visitante_{timestamp}.png"
        
        cv2.imwrite(nome_casa, bloco_casa)
        cv2.imwrite(nome_visitante, bloco_visitante)
        
        print(f"\n💾 Blocos salvos:")
        print(f"   📁 {nome_casa}")
        print(f"   📁 {nome_visitante}")
        
        # Analisar blocos com OCR
        print("\n🔍 Analisando blocos com OCR...")
        
        carta_casa = analisar_bloco_ocr(bloco_casa, "CASA")
        carta_visitante = analisar_bloco_ocr(bloco_visitante, "VISITANTE")
        
        # Resultado final
        print("\n" + "="*60)
        print("📊 RESULTADO DO TESTE:")
        if carta_casa:
            print(f"   🔶 CASA: {carta_casa}")
        else:
            print("   🔶 CASA: ❌ Não detectada")
            
        if carta_visitante:
            print(f"   🔷 VISITANTE: {carta_visitante}")
        else:
            print("   🔷 VISITANTE: ❌ Não detectada")
        
        if carta_casa and carta_visitante:
            print("\n🎉 SUCESSO! Ambas as cartas foram detectadas nos blocos!")
            
            # Determinar vencedor
            valores = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
                      '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
            
            valor_casa = valores.get(carta_casa, 0)
            valor_visitante = valores.get(carta_visitante, 0)
            
            if valor_casa > valor_visitante:
                vencedor = "CASA"
            elif valor_visitante > valor_casa:
                vencedor = "VISITANTE"
            else:
                vencedor = "EMPATE"
                
            print(f"🏆 VENCEDOR: {vencedor}")
            return True
        else:
            print("\n⚠️ Falha na detecção. Verifique:")
            print("   - Se o Football Studio está aberto e visível")
            print("   - Se as cartas estão sendo exibidas na tela")
            print("   - Se a resolução da tela mudou")
            return False
        
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        return False

def analisar_bloco_ocr(bloco_img, tipo):
    """Analisa um bloco específico com OCR"""
    try:
        print(f"\n🔬 Analisando bloco {tipo}...")
        
        # Redimensionar para melhorar OCR
        h, w = bloco_img.shape[:2]
        if h < 120 or w < 80:
            escala = max(120/h, 80/w, 4.0)
            novo_h, novo_w = int(h * escala), int(w * escala)
            bloco_img = cv2.resize(bloco_img, (novo_w, novo_h), interpolation=cv2.INTER_CUBIC)
            print(f"   📈 Redimensionado: {w}x{h} -> {novo_w}x{novo_h}")
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(bloco_img, cv2.COLOR_BGR2GRAY)
        
        # Múltiplos preprocessamentos
        preprocessamentos = [
            ("Original", gray),
            ("OTSU", cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
            ("OTSU_INV", cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]),
            ("Adaptativo", cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)),
            ("Médio", cv2.threshold(gray, int(gray.mean()), 255, cv2.THRESH_BINARY)[1]),
            ("Médio_INV", cv2.threshold(gray, int(gray.mean()), 255, cv2.THRESH_BINARY_INV)[1])
        ]
        
        # Configurações OCR
        configs = [
            '--psm 8 -c tessedit_char_whitelist=A23456789JQK10',
            '--psm 10 -c tessedit_char_whitelist=A23456789JQK10',
            '--psm 7 -c tessedit_char_whitelist=A23456789JQK10',
            '--psm 8',
            '--psm 10'
        ]
        
        # Tentar todas as combinações
        resultados = []
        for nome_prep, processed in preprocessamentos:
            for i, config in enumerate(configs):
                try:
                    texto = pytesseract.image_to_string(processed, config=config)
                    texto_limpo = limpar_texto_teste(texto)
                    
                    if texto_limpo:
                        valor = validar_carta_teste(texto_limpo)
                        if valor:
                            resultados.append(valor)
                            print(f"   🔤 {nome_prep}[{i}]: '{texto.strip()}' -> '{texto_limpo}' -> '{valor}'")
                            
                            # Salvar preprocessamento que deu resultado
                            timestamp = datetime.now().strftime("%H%M%S")
                            cv2.imwrite(f"debug_{tipo}_{nome_prep}_{timestamp}.png", processed)
                except:
                    continue
        
        # Escolher resultado mais comum
        if resultados:
            from collections import Counter
            contador = Counter(resultados)
            carta_final = contador.most_common(1)[0][0]
            frequencia = contador[carta_final]
            
            print(f"   ✅ Resultado {tipo}: {carta_final} (freq: {frequencia}/{len(resultados)})")
            return carta_final
        else:
            print(f"   ❌ Nenhuma carta detectada para {tipo}")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro no OCR {tipo}: {e}")
        return None

def limpar_texto_teste(texto):
    """Limpeza de texto para teste"""
    if not texto:
        return ""
    
    texto = texto.strip().upper().replace(' ', '').replace('\n', '').replace('\t', '')
    
    # Correções básicas
    correções = {
        'O': '0', 'I': '1', 'L': '1', 'S': '5', 'Z': '2', 'G': '6', 'B': '8', 'T': '7'
    }
    
    for erro, correto in correções.items():
        texto = texto.replace(erro, correto)
    
    # Manter apenas caracteres válidos
    validos = set('A23456789JQK10')
    return ''.join(c for c in texto if c in validos)

def validar_carta_teste(texto):
    """Validação de carta para teste"""
    valores_validos = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    if texto in valores_validos:
        return texto
    
    if '10' in texto:
        return '10'
    
    for char in texto:
        if char in valores_validos:
            return char
    
    return None

if __name__ == "__main__":
    print("🎯 TESTE ESPECÍFICO DOS BLOCOS DAS CARTAS")
    print("📱 Abra o Football Studio e deixe as cartas visíveis")
    print("⏰ Pressione Enter quando estiver pronto...")
    input()
    
    sucesso = testar_blocos_cartas()
    
    if sucesso:
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("📁 Verifique as imagens salvas para análise")
    else:
        print("\n⚠️ TESTE FALHOU")
        print("🔧 Ajuste as coordenadas se necessário")
    
    print("\n📋 Arquivos gerados:")
    for arquivo in os.listdir('.'):
        if arquivo.startswith('teste_bloco_') or arquivo.startswith('debug_'):
            print(f"   📁 {arquivo}")
