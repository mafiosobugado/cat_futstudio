#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SISTEMA FINAL OTIMIZADO - FOOTBALL STUDIO
Sistema eficaz para capturar todas as cartas sem perder nenhuma
"""

import cv2
import numpy as np
import pytesseract
import pyautogui
import json
import time
from datetime import datetime
from collections import Counter

class FootballStudioDetector:
    def __init__(self):
        self.cartas_validas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.valores_cartas = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
        self.historico = []
        self.ultima_deteccao = None
        
    def capturar_tela(self):
        """Captura a tela completa"""
        try:
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return img
        except Exception as e:
            print(f"❌ Erro ao capturar tela: {e}")
            return None
    
    def extrair_regioes(self, img):
        """Extrai as regiões das cartas com coordenadas otimizadas"""
        altura, largura = img.shape[:2]
        
        # Coordenadas baseadas na análise da sua imagem
        # CASA (lado esquerdo)
        casa_x = int(largura * 0.10)   # 10% da largura
        casa_y = int(altura * 0.40)    # 40% da altura
        casa_w = int(largura * 0.30)   # 30% da largura
        casa_h = int(altura * 0.50)    # 50% da altura
        
        # VISITANTE (lado direito)
        visit_x = int(largura * 0.60)   # 60% da largura
        visit_y = int(altura * 0.40)    # 40% da altura
        visit_w = int(largura * 0.30)   # 30% da largura
        visit_h = int(altura * 0.50)    # 50% da altura
        
        regiao_casa = img[casa_y:casa_y+casa_h, casa_x:casa_x+casa_w]
        regiao_visitante = img[visit_y:visit_y+visit_h, visit_x:visit_x+visit_w]
        
        return regiao_casa, regiao_visitante
    
    def detectar_carta_ocr(self, img_regiao, lado):
        """Detecta carta usando OCR robusto"""
        try:
            if img_regiao is None or img_regiao.size == 0:
                return None
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(img_regiao, cv2.COLOR_BGR2GRAY)
            
            # Redimensionar se muito pequena
            h, w = gray.shape
            if h < 80 or w < 60:
                scale = max(80/h, 60/w, 3.0)
                new_h, new_w = int(h * scale), int(w * scale)
                gray = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            
            # Múltiplas técnicas de preprocessing
            preprocessamentos = []
            
            # 1. OTSU
            _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            preprocessamentos.append(otsu)
            
            # 2. Adaptativo
            adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            preprocessamentos.append(adaptive)
            
            # 3. Threshold simples
            _, simple = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            preprocessamentos.append(simple)
            
            # 4. Threshold invertido
            _, invertido = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
            preprocessamentos.append(invertido)
            
            # 5. Blur + OTSU
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            _, blur_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            preprocessamentos.append(blur_otsu)
            
            resultados = []
            
            # Testar cada preprocessamento
            for processed in preprocessamentos:
                try:
                    # Múltiplas configurações de OCR
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
                        
                        if texto_limpo in self.cartas_validas:
                            resultados.append(texto_limpo)
                            
                except Exception:
                    continue
            
            # Escolher resultado mais comum
            if resultados:
                contador = Counter(resultados)
                carta_final = contador.most_common(1)[0][0]
                confianca = contador[carta_final]
                print(f"   {lado}: {carta_final} (confiança: {confianca}/{len(resultados)})")
                return carta_final
            else:
                print(f"   {lado}: ❌ Não detectado")
                return None
                
        except Exception as e:
            print(f"❌ Erro OCR {lado}: {e}")
            return None
    
    def detectar_cartas(self, img):
        """Detecta ambas as cartas na imagem"""
        try:
            regiao_casa, regiao_visitante = self.extrair_regioes(img)
            
            # Salvar regiões para debug
            timestamp = datetime.now().strftime("%H%M%S")
            cv2.imwrite(f"debug_casa_{timestamp}.png", regiao_casa)
            cv2.imwrite(f"debug_visitante_{timestamp}.png", regiao_visitante)
            
            carta_casa = self.detectar_carta_ocr(regiao_casa, "CASA")
            carta_visitante = self.detectar_carta_ocr(regiao_visitante, "VISITANTE")
            
            return carta_casa, carta_visitante
            
        except Exception as e:
            print(f"❌ Erro na detecção: {e}")
            return None, None
    
    def determinar_vencedor(self, carta_casa, carta_visitante):
        """Determina o vencedor da rodada"""
        valor_casa = self.valores_cartas.get(carta_casa, 0)
        valor_visitante = self.valores_cartas.get(carta_visitante, 0)
        
        if valor_casa > valor_visitante:
            return "CASA"
        elif valor_visitante > valor_casa:
            return "VISITANTE"
        else:
            return "EMPATE"
    
    def salvar_historico(self):
        """Salva o histórico de jogadas"""
        try:
            with open("historico_final.json", "w", encoding='utf-8') as f:
                json.dump(self.historico, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erro ao salvar histórico: {e}")
    
    def monitorar(self):
        """Monitora o jogo em tempo real"""
        print("🚀 INICIANDO MONITOR FINAL OTIMIZADO")
        print("=" * 50)
        print("🎯 Sistema configurado para máxima eficácia")
        print("📸 Captura a cada 3 segundos")
        print("🔬 OCR com múltiplas técnicas")
        print("💾 Histórico salvo automaticamente")
        print("\n🎮 Pressione Ctrl+C para parar")
        print("=" * 50)
        
        tentativas = 0
        sucessos = 0
        
        try:
            while True:
                tentativas += 1
                print(f"\n🔄 Tentativa {tentativas}")
                
                # Capturar tela
                img = self.capturar_tela()
                if img is None:
                    continue
                
                print(f"📏 Tela: {img.shape[1]}x{img.shape[0]}")
                
                # Detectar cartas
                carta_casa, carta_visitante = self.detectar_cartas(img)
                
                if carta_casa and carta_visitante:
                    sucessos += 1
                    deteccao_atual = f"{carta_casa}-{carta_visitante}"
                    
                    # Verificar se é nova rodada
                    if deteccao_atual != self.ultima_deteccao:
                        vencedor = self.determinar_vencedor(carta_casa, carta_visitante)
                        
                        # Adicionar ao histórico
                        entrada = {
                            'timestamp': datetime.now().isoformat(),
                            'casa': carta_casa,
                            'visitante': carta_visitante,
                            'vencedor': vencedor,
                            'tentativa': tentativas
                        }
                        
                        self.historico.append(entrada)
                        self.salvar_historico()
                        
                        print("✅ NOVA RODADA DETECTADA!")
                        print(f"   🏠 CASA: {carta_casa}")
                        print(f"   ✈️ VISITANTE: {carta_visitante}")
                        print(f"   🏆 VENCEDOR: {vencedor}")
                        print(f"   📊 Total: {len(self.historico)} rodadas")
                        print(f"   📈 Taxa: {sucessos}/{tentativas} ({(sucessos/tentativas)*100:.1f}%)")
                        
                        self.ultima_deteccao = deteccao_atual
                    else:
                        print(f"🔄 Rodada repetida: {deteccao_atual}")
                else:
                    print("❌ Detecção falhou")
                    
                # Taxa de sucesso a cada 10 tentativas
                if tentativas % 10 == 0:
                    taxa = (sucessos/tentativas)*100
                    print(f"\n📊 ESTATÍSTICAS: {sucessos}/{tentativas} sucessos ({taxa:.1f}%)")
                    
                # Aguardar próxima captura
                time.sleep(3)
                
        except KeyboardInterrupt:
            print("\n⏹️ Monitoramento interrompido")
            
        finally:
            taxa_final = (sucessos/tentativas)*100 if tentativas > 0 else 0
            print(f"\n🏁 ESTATÍSTICAS FINAIS:")
            print(f"   🎯 Tentativas: {tentativas}")
            print(f"   ✅ Sucessos: {sucessos}")
            print(f"   📈 Taxa: {taxa_final:.1f}%")
            print(f"   🎮 Rodadas: {len(self.historico)}")
            print(f"\n📁 Histórico salvo em 'historico_final.json'")

if __name__ == "__main__":
    print("🎯 FOOTBALL STUDIO - DETECTOR FINAL")
    print("=" * 50)
    print("🎮 Abra o Football Studio no navegador")
    print("📱 Deixe o jogo visível na tela")
    print("⏰ Aguarde 5 segundos e pressione Enter...")
    
    input()
    
    detector = FootballStudioDetector()
    detector.monitorar()
