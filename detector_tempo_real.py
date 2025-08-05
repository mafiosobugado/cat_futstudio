#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 DETECTOR TEMPO REAL - FOOTBALL STUDIO
Sistema simplificado e eficaz para captura em tempo real
"""

import cv2
import numpy as np
import pytesseract
import pyautogui
import json
import time
import threading
from datetime import datetime

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class DetectorTempoReal:
    def __init__(self):
        self.ativo = False
        self.historico = []
        self.ultima_deteccao = None
        self.cartas_validas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
    def capturar_e_detectar(self):
        """Captura tela e detecta cartas rapidamente"""
        try:
            # Capturar tela completa
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            altura, largura = img.shape[:2]
            
            print(f"📸 Tela: {largura}x{altura}")
            
            # Coordenadas SIMPLES e EFICAZES (baseadas na sua imagem)
            # CASA (lado esquerdo)
            casa_x = int(largura * 0.05)   # 5% da largura
            casa_y = int(altura * 0.6)     # 60% da altura
            casa_w = int(largura * 0.35)   # 35% da largura
            casa_h = int(altura * 0.35)    # 35% da altura
            
            # VISITANTE (lado direito)
            visit_x = int(largura * 0.6)    # 60% da largura
            visit_y = int(altura * 0.6)     # 60% da altura
            visit_w = int(largura * 0.35)   # 35% da largura
            visit_h = int(altura * 0.35)    # 35% da altura
            
            # Extrair regiões
            regiao_casa = img[casa_y:casa_y+casa_h, casa_x:casa_x+casa_w]
            regiao_visitante = img[visit_y:visit_y+visit_h, visit_x:visit_x+visit_w]
            
            # Detectar cartas RAPIDAMENTE
            carta_casa = self.detectar_carta_rapida(regiao_casa, "CASA")
            carta_visitante = self.detectar_carta_rapida(regiao_visitante, "VISITANTE")
            
            return carta_casa, carta_visitante
            
        except Exception as e:
            print(f"❌ Erro na captura: {e}")
            return None, None
    
    def detectar_carta_rapida(self, img_regiao, lado):
        """Detecção rápida e eficaz de carta"""
        try:
            if img_regiao is None or img_regiao.size == 0:
                return None
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(img_regiao, cv2.COLOR_BGR2GRAY)
            
            # Redimensionar se muito pequena
            h, w = gray.shape
            if h < 100 or w < 80:
                scale = max(100/h, 80/w, 2.0)
                new_h, new_w = int(h * scale), int(w * scale)
                gray = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            
            # Múltiplas tentativas RÁPIDAS
            metodos = [
                # OTSU
                cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
                # Adaptativo
                cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),
                # Simples
                cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1],
                # Invertido
                cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]
            ]
            
            for processed in metodos:
                try:
                    # OCR rápido
                    texto = pytesseract.image_to_string(processed, config='--psm 8 -c tessedit_char_whitelist=A23456789JQK10')
                    texto_limpo = self.limpar_texto(texto)
                    
                    if texto_limpo in self.cartas_validas:
                        print(f"   ✅ {lado}: {texto_limpo}")
                        return texto_limpo
                except:
                    continue
            
            print(f"   ❌ {lado}: Não detectado")
            return None
            
        except Exception as e:
            print(f"❌ Erro {lado}: {e}")
            return None
    
    def limpar_texto(self, texto):
        """Limpa texto OCR rapidamente"""
        if not texto:
            return ""
        
        # Limpar
        texto = texto.strip().upper().replace(' ', '').replace('\n', '')
        
        # Correções rápidas
        texto = texto.replace('O', '0').replace('I', '1').replace('L', '1')
        texto = texto.replace('S', '5').replace('Z', '2').replace('G', '6')
        
        # Verificar se é carta válida diretamente
        if texto in self.cartas_validas:
            return texto
        
        # Verificar '10'
        if '10' in texto:
            return '10'
        
        # Primeiro caractere válido
        for char in texto:
            if char in self.cartas_validas:
                return char
        
        return ""
    
    def determinar_vencedor(self, carta_casa, carta_visitante):
        """Determina vencedor rapidamente"""
        valores = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
        
        valor_casa = valores.get(carta_casa, 0)
        valor_visitante = valores.get(carta_visitante, 0)
        
        if valor_casa > valor_visitante:
            return "CASA GANHOU"
        elif valor_visitante > valor_casa:
            return "VISITANTE GANHOU"
        else:
            return "EMPATE"
    
    def salvar_resultado(self, carta_casa, carta_visitante, vencedor):
        """Salva resultado rapidamente"""
        entrada = {
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'casa': carta_casa,
            'visitante': carta_visitante,
            'vencedor': vencedor
        }
        
        self.historico.append(entrada)
        
        # Manter apenas últimas 50
        if len(self.historico) > 50:
            self.historico = self.historico[-50:]
        
        # Salvar arquivo
        try:
            with open("historico_tempo_real.json", "w", encoding='utf-8') as f:
                json.dump(self.historico, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def monitorar_tempo_real(self):
        """Monitor principal em tempo real"""
        print("🚀 INICIANDO MONITOR TEMPO REAL")
        print("=" * 50)
        print("⚡ Captura a cada 1 segundo")
        print("🎯 Detecção simplificada e rápida")
        print("📊 Histórico automático")
        print("\n⏹️ Pressione Ctrl+C para parar")
        print("=" * 50)
        
        tentativas = 0
        sucessos = 0
        
        try:
            while self.ativo:
                tentativas += 1
                print(f"\n🔄 [{tentativas}] Capturando...")
                
                # Capturar e detectar
                carta_casa, carta_visitante = self.capturar_e_detectar()
                
                if carta_casa and carta_visitante:
                    sucessos += 1
                    deteccao_atual = f"{carta_casa}-{carta_visitante}"
                    
                    # Verificar se é nova
                    if deteccao_atual != self.ultima_deteccao:
                        vencedor = self.determinar_vencedor(carta_casa, carta_visitante)
                        
                        # Salvar
                        self.salvar_resultado(carta_casa, carta_visitante, vencedor)
                        
                        print("🎉 NOVA RODADA!")
                        print(f"   🏠 CASA: {carta_casa}")
                        print(f"   ✈️ VISITANTE: {carta_visitante}")
                        print(f"   🏆 {vencedor}")
                        print(f"   📊 Total: {len(self.historico)}")
                        print(f"   📈 Taxa: {sucessos}/{tentativas} ({(sucessos/tentativas)*100:.1f}%)")
                        
                        self.ultima_deteccao = deteccao_atual
                    else:
                        print(f"🔄 Mesma rodada: {deteccao_atual}")
                else:
                    print("❌ Não detectado")
                
                # Taxa de sucesso
                if tentativas % 20 == 0:
                    taxa = (sucessos/tentativas)*100
                    print(f"\n📊 ESTATÍSTICA: {sucessos}/{tentativas} ({taxa:.1f}%)")
                
                # Aguardar 1 segundo
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️ Parando...")
        
        finally:
            self.ativo = False
            taxa_final = (sucessos/tentativas)*100 if tentativas > 0 else 0
            print(f"\n🏁 FINAL: {sucessos}/{tentativas} ({taxa_final:.1f}%)")
            print(f"📁 Histórico salvo: {len(self.historico)} rodadas")
    
    def iniciar(self):
        """Inicia o monitor"""
        if not self.ativo:
            self.ativo = True
            thread = threading.Thread(target=self.monitorar_tempo_real)
            thread.daemon = True
            thread.start()
            return thread
        return None
    
    def parar(self):
        """Para o monitor"""
        self.ativo = False

def testar_uma_captura():
    """Testa uma captura para ver se funciona"""
    print("🧪 TESTE RÁPIDO DE CAPTURA")
    print("-" * 30)
    
    detector = DetectorTempoReal()
    carta_casa, carta_visitante = detector.capturar_e_detectar()
    
    if carta_casa and carta_visitante:
        vencedor = detector.determinar_vencedor(carta_casa, carta_visitante)
        print(f"✅ SUCESSO!")
        print(f"   🏠 CASA: {carta_casa}")
        print(f"   ✈️ VISITANTE: {carta_visitante}")
        print(f"   🏆 {vencedor}")
        return True
    else:
        print(f"❌ FALHA: CASA={carta_casa}, VISITANTE={carta_visitante}")
        return False

if __name__ == "__main__":
    print("🎯 FOOTBALL STUDIO - DETECTOR TEMPO REAL")
    print("=" * 50)
    
    opcao = input("Escolha:\n1 - Teste rápido\n2 - Monitor contínuo\nOpção: ")
    
    if opcao == "1":
        print("\n🎮 Abra o Football Studio e pressione Enter...")
        input()
        testar_uma_captura()
    
    elif opcao == "2":
        print("\n🎮 Abra o Football Studio e pressione Enter...")
        input()
        
        detector = DetectorTempoReal()
        thread = detector.iniciar()
        
        if thread:
            try:
                thread.join()
            except KeyboardInterrupt:
                detector.parar()
                print("\n👋 Finalizando...")
    
    else:
        print("❌ Opção inválida")
