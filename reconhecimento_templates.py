#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SISTEMA DE RECONHECIMENTO DE CARTAS POR TEMPLATES
Sistema similar ao reconhecimento facial - cria modelos das cartas e compara
"""

import cv2
import numpy as np
import pyautogui
import json
import os
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class TemplateCardRecognizer:
    """Sistema de reconhecimento de cartas por templates"""
    
    def __init__(self):
        self.templates = {}  # Dicionário para armazenar templates das cartas
        self.templates_file = "templates_cartas.pkl"
        self.cartas_validas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.threshold_similaridade = 0.7  # Threshold para aceitar reconhecimento
        self.carregar_templates()
    
    def extrair_caracteristicas(self, img_carta):
        """Extrai características da imagem da carta para comparação"""
        try:
            if img_carta is None or img_carta.size == 0:
                return None
            
            # Redimensionar para tamanho padrão
            img_redimensionada = cv2.resize(img_carta, (100, 140), interpolation=cv2.INTER_AREA)
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(img_redimensionada, cv2.COLOR_BGR2GRAY)
            
            # Normalizar a imagem
            gray = cv2.equalizeHist(gray)
            
            # Aplicar filtro Gaussiano para reduzir ruído
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            
            # Extrair bordas usando Canny
            edges = cv2.Canny(gray, 50, 150)
            
            # Combinar informações: imagem original + bordas
            # Redimensionar para vetor de características
            gray_flat = gray.flatten()
            edges_flat = edges.flatten()
            
            # Combinar características
            caracteristicas = np.concatenate([gray_flat, edges_flat])
            
            # Normalizar características
            if np.linalg.norm(caracteristicas) > 0:
                caracteristicas = caracteristicas / np.linalg.norm(caracteristicas)
            
            return caracteristicas
            
        except Exception as e:
            print(f"❌ Erro ao extrair características: {e}")
            return None
    
    def salvar_template(self, img_carta, valor_carta, lado="GERAL"):
        """Salva um template de carta para reconhecimento posterior"""
        try:
            caracteristicas = self.extrair_caracteristicas(img_carta)
            if caracteristicas is None:
                return False
            
            # Criar chave única para o template
            chave = f"{valor_carta}_{lado}"
            
            # Se já existe template desta carta, criar lista de variações
            if chave not in self.templates:
                self.templates[chave] = []
            
            # Adicionar template
            template_info = {
                'caracteristicas': caracteristicas,
                'valor': valor_carta,
                'lado': lado,
                'timestamp': datetime.now().isoformat(),
                'tamanho_original': img_carta.shape
            }
            
            self.templates[chave].append(template_info)
            
            # Manter apenas os 5 melhores templates por carta
            if len(self.templates[chave]) > 5:
                self.templates[chave] = self.templates[chave][-5:]
            
            print(f"✅ Template salvo: {valor_carta} ({lado}) - Total de variações: {len(self.templates[chave])}")
            
            # Salvar templates no arquivo
            self.salvar_templates_arquivo()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar template: {e}")
            return False
    
    def reconhecer_carta(self, img_carta):
        """Reconhece uma carta comparando com templates salvos"""
        try:
            if not self.templates:
                print("⚠️ Nenhum template disponível para comparação")
                return None, 0.0
            
            # Extrair características da carta atual
            caracteristicas_carta = self.extrair_caracteristicas(img_carta)
            if caracteristicas_carta is None:
                return None, 0.0
            
            melhor_match = None
            melhor_similaridade = 0.0
            
            # Comparar com todos os templates
            for chave, templates_lista in self.templates.items():
                for template in templates_lista:
                    # Calcular similaridade coseno
                    caracteristicas_template = template['caracteristicas']
                    
                    # Redimensionar se necessário para ter mesmo tamanho
                    tamanho_min = min(len(caracteristicas_carta), len(caracteristicas_template))
                    carac_carta = caracteristicas_carta[:tamanho_min].reshape(1, -1)
                    carac_template = caracteristicas_template[:tamanho_min].reshape(1, -1)
                    
                    similaridade = cosine_similarity(carac_carta, carac_template)[0][0]
                    
                    if similaridade > melhor_similaridade:
                        melhor_similaridade = similaridade
                        melhor_match = template['valor']
            
            # Verificar se a similaridade é suficiente
            if melhor_similaridade >= self.threshold_similaridade:
                print(f"✅ Carta reconhecida: {melhor_match} (similaridade: {melhor_similaridade:.3f})")
                return melhor_match, melhor_similaridade
            else:
                print(f"❌ Baixa similaridade: {melhor_similaridade:.3f} (threshold: {self.threshold_similaridade})")
                return None, melhor_similaridade
            
        except Exception as e:
            print(f"❌ Erro no reconhecimento: {e}")
            return None, 0.0
    
    def salvar_templates_arquivo(self):
        """Salva templates em arquivo"""
        try:
            with open(self.templates_file, 'wb') as f:
                pickle.dump(self.templates, f)
            print(f"💾 Templates salvos em {self.templates_file}")
        except Exception as e:
            print(f"❌ Erro ao salvar templates: {e}")
    
    def carregar_templates(self):
        """Carrega templates do arquivo"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'rb') as f:
                    self.templates = pickle.load(f)
                print(f"📁 Templates carregados: {len(self.templates)} tipos de cartas")
                
                # Mostrar estatísticas
                for chave, templates_lista in self.templates.items():
                    print(f"   📋 {chave}: {len(templates_lista)} variações")
            else:
                print("📝 Nenhum template encontrado. Será necessário criar templates primeiro.")
        except Exception as e:
            print(f"❌ Erro ao carregar templates: {e}")
            self.templates = {}
    
    def limpar_templates(self):
        """Limpa todos os templates"""
        self.templates = {}
        if os.path.exists(self.templates_file):
            os.remove(self.templates_file)
        print("🗑️ Templates limpos")

def capturar_blocos_para_templates():
    """Captura blocos das cartas para criar templates"""
    try:
        print("📸 Capturando blocos das cartas para criar templates...")
        
        # Capturar tela completa
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        altura, largura = img.shape[:2]
        
        # Coordenadas dos blocos (ÁREA AUMENTADA PARA MELHOR CAPTURA)
        casa_x = int(largura * 0.30)    # 30% da largura (aumentado)
        casa_y = int(altura * 0.60)     # 60% da altura (aumentado)
        casa_w = int(largura * 0.20)    # 20% da largura (aumentado)
        casa_h = int(altura * 0.35)     # 35% da altura (aumentado)
        
        visit_x = int(largura * 0.50)   # 50% da largura (aumentado)
        visit_y = int(altura * 0.60)    # 60% da altura (aumentado)
        visit_w = int(largura * 0.20)   # 20% da largura (aumentado)
        visit_h = int(altura * 0.35)    # 35% da altura (aumentado)
        
        # Extrair blocos
        bloco_casa = img[casa_y:casa_y+casa_h, casa_x:casa_x+casa_w]
        bloco_visitante = img[visit_y:visit_y+visit_h, visit_x:visit_x+visit_w]
        
        return bloco_casa, bloco_visitante
        
    except Exception as e:
        print(f"❌ Erro ao capturar blocos: {e}")
        return None, None

def criar_templates_interativo():
    """Sistema interativo para criar templates das cartas"""
    print("🎯 SISTEMA DE CRIAÇÃO DE TEMPLATES")
    print("=" * 50)
    print("📋 Instruções:")
    print("   1. Abra o Football Studio")
    print("   2. Aguarde aparecer cartas na tela")
    print("   3. Digite o valor da carta que está vendo")
    print("   4. O sistema capturará o template")
    print("   5. Repita para todas as cartas (A, 2-9, 10, J, Q, K)")
    print("\n⌨️ Comandos especiais:")
    print("   'sair' - Finalizar criação de templates")
    print("   'ver' - Ver templates já criados")
    print("   'limpar' - Limpar todos os templates")
    
    recognizer = TemplateCardRecognizer()
    
    while True:
        try:
            print("\n" + "="*50)
            comando = input("🎮 Digite o valor da carta visível (ou comando): ").strip().upper()
            
            if comando == 'SAIR':
                print("👋 Finalizando criação de templates...")
                break
            elif comando == 'VER':
                print("\n📋 Templates criados:")
                if recognizer.templates:
                    for chave, templates_lista in recognizer.templates.items():
                        print(f"   🃏 {chave}: {len(templates_lista)} variações")
                else:
                    print("   📝 Nenhum template criado ainda")
                continue
            elif comando == 'LIMPAR':
                recognizer.limpar_templates()
                continue
            elif comando not in recognizer.cartas_validas:
                print(f"❌ Valor inválido. Use: {', '.join(recognizer.cartas_validas)}")
                continue
            
            # Capturar blocos atuais
            print(f"📸 Capturando templates para carta: {comando}")
            bloco_casa, bloco_visitante = capturar_blocos_para_templates()
            
            if bloco_casa is None or bloco_visitante is None:
                print("❌ Falha na captura dos blocos")
                continue
            
            # Salvar ambos os blocos como templates
            print("💾 Salvando templates...")
            
            # Template do bloco CASA
            sucesso_casa = recognizer.salvar_template(bloco_casa, comando, "CASA")
            
            # Template do bloco VISITANTE  
            sucesso_visitante = recognizer.salvar_template(bloco_visitante, comando, "VISITANTE")
            
            if sucesso_casa or sucesso_visitante:
                print(f"✅ Templates da carta {comando} salvos com sucesso!")
                
                # Salvar imagens para debug
                timestamp = datetime.now().strftime("%H%M%S")
                cv2.imwrite(f"template_{comando}_casa_{timestamp}.png", bloco_casa)
                cv2.imwrite(f"template_{comando}_visitante_{timestamp}.png", bloco_visitante)
                print(f"💾 Imagens salvas: template_{comando}_*_{timestamp}.png")
            else:
                print(f"❌ Erro ao salvar templates da carta {comando}")
            
        except KeyboardInterrupt:
            print("\n⏹️ Interrompido pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print(f"\n🎉 Criação de templates finalizada!")
    print(f"📊 Total de templates criados: {len(recognizer.templates)}")

def testar_reconhecimento():
    """Testa o sistema de reconhecimento com captura em tempo real"""
    print("🧪 TESTE DO SISTEMA DE RECONHECIMENTO")
    print("=" * 50)
    
    recognizer = TemplateCardRecognizer()
    
    if not recognizer.templates:
        print("❌ Nenhum template encontrado!")
        print("💡 Execute primeiro a criação de templates")
        return
    
    print(f"📋 Templates disponíveis: {len(recognizer.templates)}")
    print("🔄 Iniciando teste em tempo real...")
    print("⌨️ Pressione Ctrl+C para parar")
    
    contador = 0
    try:
        while True:
            contador += 1
            print(f"\n🔍 Teste {contador}")
            
            # Capturar blocos atuais
            bloco_casa, bloco_visitante = capturar_blocos_para_templates()
            
            if bloco_casa is None or bloco_visitante is None:
                print("❌ Falha na captura")
                continue
            
            # Tentar reconhecer ambas as cartas
            print("🎯 Reconhecendo CASA...")
            carta_casa, sim_casa = recognizer.reconhecer_carta(bloco_casa)
            
            print("🎯 Reconhecendo VISITANTE...")
            carta_visitante, sim_visitante = recognizer.reconhecer_carta(bloco_visitante)
            
            # Mostrar resultados
            print("📊 RESULTADOS:")
            if carta_casa:
                print(f"   🔶 CASA: {carta_casa} (similaridade: {sim_casa:.3f})")
            else:
                print(f"   🔶 CASA: ❌ Não reconhecida (max sim: {sim_casa:.3f})")
            
            if carta_visitante:
                print(f"   🔷 VISITANTE: {carta_visitante} (similaridade: {sim_visitante:.3f})")
            else:
                print(f"   🔷 VISITANTE: ❌ Não reconhecida (max sim: {sim_visitante:.3f})")
            
            # Se ambas foram reconhecidas, determinar vencedor
            if carta_casa and carta_visitante:
                print("\n🎉 AMBAS AS CARTAS RECONHECIDAS!")
                
                # Determinar vencedor
                valores = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
                          '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
                
                valor_casa = valores.get(carta_casa, 0)
                valor_visitante = valores.get(carta_visitante, 0)
                
                if valor_casa > valor_visitante:
                    vencedor = "CASA GANHOU"
                elif valor_visitante > valor_casa:
                    vencedor = "VISITANTE GANHOU"
                else:
                    vencedor = "EMPATE"
                
                print(f"🏆 {vencedor}")
            
            # Aguardar antes do próximo teste
            import time
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido")
    
    print("🏁 Teste finalizado")

if __name__ == "__main__":
    print("🎯 SISTEMA DE RECONHECIMENTO DE CARTAS POR TEMPLATES")
    print("=" * 60)
    print("📋 Escolha uma opção:")
    print("   1 - Criar templates das cartas")
    print("   2 - Testar reconhecimento")
    print("   3 - Ver templates existentes")
    print("   4 - Limpar templates")
    
    try:
        opcao = input("\n🎮 Digite sua opção (1-4): ").strip()
        
        if opcao == "1":
            criar_templates_interativo()
        elif opcao == "2":
            testar_reconhecimento()
        elif opcao == "3":
            recognizer = TemplateCardRecognizer()
            print(f"\n📊 Templates existentes: {len(recognizer.templates)}")
            for chave, templates_lista in recognizer.templates.items():
                print(f"   🃏 {chave}: {len(templates_lista)} variações")
        elif opcao == "4":
            recognizer = TemplateCardRecognizer()
            recognizer.limpar_templates()
        else:
            print("❌ Opção inválida")
            
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido")
    except Exception as e:
        print(f"❌ Erro: {e}")
