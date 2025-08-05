"""
Sistema Avançado de Calibração para Football Studio
Ferramenta para encontrar as coordenadas exatas e calibrar a detecção
"""

import cv2
import numpy as np
import pyautogui
import time
import os
import json
from datetime import datetime
import pytesseract

# Configurar caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class CalibradorDeteccao:
    def __init__(self):
        self.coordenadas_casa = None
        self.coordenadas_visitante = None
        self.config_arquivo = "coordenadas_calibradas.json"
        self.carregar_coordenadas()
    
    def carregar_coordenadas(self):
        """Carrega coordenadas salvas anteriormente"""
        if os.path.exists(self.config_arquivo):
            try:
                with open(self.config_arquivo, 'r') as f:
                    dados = json.load(f)
                    self.coordenadas_casa = dados.get('casa')
                    self.coordenadas_visitante = dados.get('visitante')
                    print(f"✅ Coordenadas carregadas: {self.config_arquivo}")
            except:
                print("⚠️ Erro ao carregar coordenadas, usando padrão")
    
    def salvar_coordenadas(self):
        """Salva as coordenadas calibradas"""
        dados = {
            'casa': self.coordenadas_casa,
            'visitante': self.coordenadas_visitante,
            'timestamp': datetime.now().isoformat()
        }
        with open(self.config_arquivo, 'w') as f:
            json.dump(dados, f, indent=2)
        print(f"💾 Coordenadas salvas em: {self.config_arquivo}")
    
    def capturar_coordenadas_mouse(self):
        """Captura coordenadas interativamente"""
        print("\n" + "="*60)
        print("🎯 CALIBRAÇÃO INTERATIVA DE COORDENADAS")
        print("="*60)
        print("Instruções:")
        print("1. Posicione o mouse no CANTO SUPERIOR ESQUERDO da carta CASA")
        print("2. Pressione ENTER")
        print("3. Posicione o mouse no CANTO INFERIOR DIREITO da carta CASA")
        print("4. Pressione ENTER")
        print("5. Repita para a carta VISITANTE")
        print("="*60)
        
        # Capturar CASA
        input("Posicione o mouse no canto SUPERIOR ESQUERDO da carta CASA e pressione ENTER...")
        casa_x1, casa_y1 = pyautogui.position()
        print(f"📍 CASA - Canto superior esquerdo: ({casa_x1}, {casa_y1})")
        
        input("Posicione o mouse no canto INFERIOR DIREITO da carta CASA e pressione ENTER...")
        casa_x2, casa_y2 = pyautogui.position()
        print(f"📍 CASA - Canto inferior direito: ({casa_x2}, {casa_y2})")
        
        # Capturar VISITANTE
        input("Posicione o mouse no canto SUPERIOR ESQUERDO da carta VISITANTE e pressione ENTER...")
        visit_x1, visit_y1 = pyautogui.position()
        print(f"📍 VISITANTE - Canto superior esquerdo: ({visit_x1}, {visit_y1})")
        
        input("Posicione o mouse no canto INFERIOR DIREITO da carta VISITANTE e pressione ENTER...")
        visit_x2, visit_y2 = pyautogui.position()
        print(f"📍 VISITANTE - Canto inferior direito: ({visit_x2}, {visit_y2})")
        
        # Calcular regiões
        self.coordenadas_casa = {
            'x': min(casa_x1, casa_x2),
            'y': min(casa_y1, casa_y2),
            'w': abs(casa_x2 - casa_x1),
            'h': abs(casa_y2 - casa_y1)
        }
        
        self.coordenadas_visitante = {
            'x': min(visit_x1, visit_y1),
            'y': min(visit_y1, visit_y2),
            'w': abs(visit_x2 - visit_x1),
            'h': abs(visit_y2 - visit_y1)
        }
        
        print("\n✅ Coordenadas capturadas:")
        print(f"   CASA: {self.coordenadas_casa}")
        print(f"   VISITANTE: {self.coordenadas_visitante}")
        
        self.salvar_coordenadas()
    
    def testar_captura_atual(self):
        """Testa a captura com as coordenadas atuais"""
        if not self.coordenadas_casa or not self.coordenadas_visitante:
            print("❌ Coordenadas não configuradas. Execute calibração primeiro.")
            return
        
        print("\n🧪 Testando captura com coordenadas calibradas...")
        print("Capturando em 3 segundos...")
        time.sleep(3)
        
        timestamp = datetime.now().strftime("%H%M%S")
        
        # Capturar região CASA
        casa = self.coordenadas_casa
        screenshot_casa = pyautogui.screenshot(region=(casa['x'], casa['y'], casa['w'], casa['h']))
        img_casa = cv2.cvtColor(np.array(screenshot_casa), cv2.COLOR_RGB2BGR)
        cv2.imwrite(f"teste_casa_{timestamp}.png", img_casa)
        
        # Capturar região VISITANTE
        visit = self.coordenadas_visitante
        screenshot_visit = pyautogui.screenshot(region=(visit['x'], visit['y'], visit['w'], visit['h']))
        img_visit = cv2.cvtColor(np.array(screenshot_visit), cv2.COLOR_RGB2BGR)
        cv2.imwrite(f"teste_visitante_{timestamp}.png", img_visit)
        
        print(f"✅ Imagens salvas:")
        print(f"   📁 teste_casa_{timestamp}.png")
        print(f"   📁 teste_visitante_{timestamp}.png")
        
        # Tentar OCR nas imagens capturadas
        carta_casa = self.detectar_carta_avancada(img_casa, "CASA")
        carta_visit = self.detectar_carta_avancada(img_visit, "VISITANTE")
        
        print(f"\n🔤 Resultado da detecção:")
        print(f"   CASA: {carta_casa if carta_casa else 'Não detectada'}")
        print(f"   VISITANTE: {carta_visit if carta_visit else 'Não detectada'}")
    
    def detectar_carta_avancada(self, img, tipo_carta):
        """Detecção avançada de carta com múltiplos métodos"""
        if img is None or img.size == 0:
            return None
        
        print(f"\n🔍 Analisando {tipo_carta}...")
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Múltiplos preprocessamentos
        preprocessamentos = {
            'original': gray,
            'otsu': cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            'adaptativo': cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),
            'media': cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2),
            'simples': cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1],
            'invertido': cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]
        }
        
        # Salvar preprocessamentos para análise
        timestamp = datetime.now().strftime("%H%M%S")
        for nome, proc_img in preprocessamentos.items():
            cv2.imwrite(f"debug_{tipo_carta.lower()}_{nome}_{timestamp}.png", proc_img)
        
        # Configurações de OCR
        configs_ocr = [
            '--psm 8 -c tessedit_char_whitelist=A23456789JQK10',
            '--psm 7 -c tessedit_char_whitelist=A23456789JQK10',  
            '--psm 6 -c tessedit_char_whitelist=A23456789JQK10',
            '--psm 10 -c tessedit_char_whitelist=A23456789JQK10',
            '--psm 13 -c tessedit_char_whitelist=A23456789JQK10',
            '--psm 8',
            '--psm 7',
            '--psm 6'
        ]
        
        # Tentar todas as combinações
        resultados = []
        for nome_proc, proc_img in preprocessamentos.items():
            for i, config in enumerate(configs_ocr):
                try:
                    texto = pytesseract.image_to_string(proc_img, config=config)
                    texto_limpo = self.limpar_texto_ocr(texto)
                    if texto_limpo:
                        valor_carta = self.validar_valor_carta(texto_limpo)
                        if valor_carta:
                            resultado = {
                                'preprocessamento': nome_proc,
                                'config': i,
                                'texto_bruto': texto,
                                'texto_limpo': texto_limpo,
                                'valor_carta': valor_carta,
                                'confianca': self.calcular_confianca(texto_limpo, valor_carta)
                            }
                            resultados.append(resultado)
                            print(f"   🔤 {nome_proc}[{i}]: '{texto}' -> '{texto_limpo}' -> '{valor_carta}'")
                except Exception as e:
                    continue
        
        # Escolher melhor resultado
        if resultados:
            melhor = max(resultados, key=lambda x: x['confianca'])
            print(f"   ✅ Melhor resultado: {melhor['valor_carta']} (confiança: {melhor['confianca']})")
            return melhor['valor_carta']
        
        print(f"   ❌ Nenhuma carta detectada em {tipo_carta}")
        return None
    
    def limpar_texto_ocr(self, texto):
        """Limpeza rigorosa do texto OCR"""
        if not texto:
            return ""
        
        # Converter e limpar
        texto = texto.strip().upper().replace(' ', '').replace('\n', '').replace('\t', '')
        
        # Correções comuns de OCR
        correções = {
            'O': '0', 'I': '1', 'L': '1', 'S': '5', 'Z': '2', 
            'G': '6', 'B': '8', 'T': '7', 'D': '0', 'U': '0'
        }
        
        for erro, correto in correções.items():
            texto = texto.replace(erro, correto)
        
        # Manter apenas caracteres válidos
        caracteres_validos = set('A23456789JQK10')
        texto_filtrado = ''.join(c for c in texto if c in caracteres_validos)
        
        return texto_filtrado
    
    def validar_valor_carta(self, texto):
        """Valida e extrai valor de carta válido"""
        valores_validos = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        # Verificação direta
        if texto in valores_validos:
            return texto
        
        # Verificar se contém '10'
        if '10' in texto:
            return '10'
        
        # Verificar primeiro caractere válido
        for char in texto:
            if char in valores_validos:
                return char
        
        return None
    
    def calcular_confianca(self, texto_limpo, valor_carta):
        """Calcula nível de confiança do resultado"""
        if not texto_limpo or not valor_carta:
            return 0
        
        confianca = 50  # Base
        
        # Bônus por correspondência exata
        if texto_limpo == valor_carta:
            confianca += 40
        
        # Bônus por tamanho correto
        if len(texto_limpo) <= 2:
            confianca += 10
        
        # Penalidade por caracteres extras
        if len(texto_limpo) > len(valor_carta):
            confianca -= (len(texto_limpo) - len(valor_carta)) * 5
        
        return max(0, min(100, confianca))
    
    def analise_completa_tela(self):
        """Análise completa da tela para detectar padrões"""
        print("\n🔬 ANÁLISE COMPLETA DA TELA")
        print("Capturando tela completa em 3 segundos...")
        time.sleep(3)
        
        # Capturar tela completa
        screenshot = pyautogui.screenshot()
        img_completa = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        timestamp = datetime.now().strftime("%H%M%S")
        cv2.imwrite(f"tela_completa_{timestamp}.png", img_completa)
        
        # Converter para HSV para análise de cores
        hsv = cv2.cvtColor(img_completa, cv2.COLOR_BGR2HSV)
        
        # Definir ranges de cores para cartas
        cores_procurar = {
            'vermelho1': ([0, 50, 50], [10, 255, 255]),
            'vermelho2': ([170, 50, 50], [180, 255, 255]),
            'azul': ([100, 50, 50], [130, 255, 255]),
            'amarelo': ([20, 100, 100], [30, 255, 255]),
            'branco': ([0, 0, 200], [180, 30, 255])
        }
        
        print(f"📊 Análise de cores na tela:")
        regioes_interesse = []
        
        for nome_cor, (lower, upper) in cores_procurar.items():
            lower = np.array(lower)
            upper = np.array(upper)
            
            mask = cv2.inRange(hsv, lower, upper)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            areas_significativas = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Área mínima para ser relevante
                    x, y, w, h = cv2.boundingRect(contour)
                    areas_significativas.append({
                        'x': x, 'y': y, 'w': w, 'h': h, 'area': area
                    })
            
            if areas_significativas:
                print(f"   🎯 {nome_cor}: {len(areas_significativas)} regiões encontradas")
                regioes_interesse.extend(areas_significativas)
                
                # Salvar máscara
                cv2.imwrite(f"mask_{nome_cor}_{timestamp}.png", mask)
        
        # Salvar análise de regiões
        if regioes_interesse:
            with open(f"regioes_interesse_{timestamp}.json", 'w') as f:
                json.dump(regioes_interesse, f, indent=2)
            
            print(f"💾 {len(regioes_interesse)} regiões de interesse salvas")
        
        print(f"✅ Análise completa salva com timestamp: {timestamp}")

def main():
    """Função principal"""
    calibrador = CalibradorDeteccao()
    
    while True:
        print("\n" + "="*60)
        print("🎯 SISTEMA AVANÇADO DE CALIBRAÇÃO - FOOTBALL STUDIO")
        print("="*60)
        print("Escolha uma opção:")
        print("1 - 📍 Calibrar coordenadas das cartas (interativo)")
        print("2 - 🧪 Testar captura com coordenadas atuais")
        print("3 - 🔬 Análise completa da tela (detectar padrões)")
        print("4 - 📊 Ver coordenadas salvas")
        print("5 - 🔄 Recarregar coordenadas")
        print("6 - ❌ Sair")
        print("="*60)
        
        opcao = input("Digite sua opção: ").strip()
        
        if opcao == "1":
            calibrador.capturar_coordenadas_mouse()
        
        elif opcao == "2":
            calibrador.testar_captura_atual()
        
        elif opcao == "3":
            calibrador.analise_completa_tela()
        
        elif opcao == "4":
            print(f"\n📊 Coordenadas atuais:")
            print(f"   CASA: {calibrador.coordenadas_casa}")
            print(f"   VISITANTE: {calibrador.coordenadas_visitante}")
        
        elif opcao == "5":
            calibrador.carregar_coordenadas()
            print("🔄 Coordenadas recarregadas")
        
        elif opcao == "6":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    main()
