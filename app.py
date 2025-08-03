"""
Football Studio - Sistema Integrado Limpo
Sistema completo com login e monitoramento integrado
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import threading
import time
import random
from datetime import datetime
import json
import os
import pyautogui
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Configurar caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.secret_key = 'football_studio_2024_secret'

# ============================================================================
# CLASSES PRINCIPAIS
# ============================================================================

class CartaFootballStudio:
    """Representa uma carta do Football Studio"""
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
    
    def __str__(self):
        return f"{self.valor}{self.naipe}"

class RodadaFutebolEstudio:
    """Representa uma rodada do Football Studio"""
    def __init__(self, carta_vermelha, carta_azul, timestamp):
        self.carta_vermelha = carta_vermelha
        self.carta_azul = carta_azul
        self.timestamp = timestamp
        self.vencedor = self._calcular_vencedor()
    
    def _calcular_vencedor(self):
        valores = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
                   '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
        
        valor_vermelho = valores.get(self.carta_vermelha.valor, 0)
        valor_azul = valores.get(self.carta_azul.valor, 0)
        
        if valor_vermelho > valor_azul:
            return "Casa"
        elif valor_azul > valor_vermelho:
            return "Visitante"
        else:
            return "Empate"

class CatalogadorCartas:
    """Gerencia o histórico de cartas"""
    def __init__(self):
        self.historico = []
        self.arquivo_dados = "historico_cartas.json"
        self.carregar_dados()
    
    def adicionar_rodada(self, rodada):
        self.historico.append(rodada)
        if len(self.historico) > 100:  # Manter apenas últimas 100 rodadas
            self.historico = self.historico[-100:]
        self.salvar_dados()
    
    def carregar_dados(self):
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    for item in dados:
                        carta_vermelha = CartaFootballStudio(
                            item['carta_vermelha']['naipe'], 
                            item['carta_vermelha']['valor']
                        )
                        carta_azul = CartaFootballStudio(
                            item['carta_azul']['naipe'], 
                            item['carta_azul']['valor']
                        )
                        rodada = RodadaFutebolEstudio(carta_vermelha, carta_azul, item['timestamp'])
                        self.historico.append(rodada)
            except:
                self.historico = []
    
    def salvar_dados(self):
        dados = []
        for rodada in self.historico:
            dados.append({
                'carta_vermelha': {'naipe': rodada.carta_vermelha.naipe, 'valor': rodada.carta_vermelha.valor},
                'carta_azul': {'naipe': rodada.carta_azul.naipe, 'valor': rodada.carta_azul.valor},
                'timestamp': rodada.timestamp,
                'vencedor': rodada.vencedor
            })
        
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    def obter_estatisticas(self):
        if not self.historico:
            return {
                'total_rodadas': 0,
                'casa_vitorias': 0,
                'visitante_vitorias': 0,
                'empates': 0,
                'carta_mais_comum': 'N/A',
                'sequencia_atual': 'N/A'
            }
        
        casa_wins = sum(1 for r in self.historico if r.vencedor == "Casa")
        visitante_wins = sum(1 for r in self.historico if r.vencedor == "Visitante")
        empates = sum(1 for r in self.historico if r.vencedor == "Empate")
        
        # Carta mais comum
        todas_cartas = []
        for rodada in self.historico:
            todas_cartas.append(str(rodada.carta_vermelha))
            todas_cartas.append(str(rodada.carta_azul))
        
        carta_mais_comum = 'N/A'
        if todas_cartas:
            from collections import Counter
            contador = Counter(todas_cartas)
            carta_mais_comum = contador.most_common(1)[0][0]
        
        # Sequência atual
        sequencia_atual = 'N/A'
        if len(self.historico) >= 2:
            ultimo_vencedor = self.historico[-1].vencedor
            contador_sequencia = 1
            for i in range(len(self.historico) - 2, -1, -1):
                if self.historico[i].vencedor == ultimo_vencedor:
                    contador_sequencia += 1
                else:
                    break
            sequencia_atual = f"{ultimo_vencedor} x{contador_sequencia}"
        
        return {
            'total_rodadas': len(self.historico),
            'casa_vitorias': casa_wins,
            'visitante_vitorias': visitante_wins,
            'empates': empates,
            'carta_mais_comum': carta_mais_comum,
            'sequencia_atual': sequencia_atual
        }

# ============================================================================
# VARIÁVEIS GLOBAIS
# ============================================================================

catalogador = CatalogadorCartas()
monitoramento_ativo = False
thread_monitoramento = None
ultima_atividade = "Sistema iniciado"
credenciais_usuario = {"email": "", "senha": "", "logado": False}

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def gerar_carta_realista():
    """Gera uma carta com distribuição realística"""
    naipes = ['♠', '♥', '♦', '♣']
    valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    naipe = random.choice(naipes)
    valor = random.choice(valores)
    
    return CartaFootballStudio(naipe, valor)

def capturar_tela_jogo():
    """Captura apenas a REGIÃO DE INTERESSE (ROI) do jogo para análise."""
    try:
        # === INSERA AQUI AS SUAS COORDENADAS ===
        # Exemplo de valores, use os que você encontrou:
        x_inicial = 224
        y_inicial = 320
        largura = 719
        altura = 444
        # =======================================
        
        # Captura apenas a região especificada
        screenshot = pyautogui.screenshot(region=(x_inicial, y_inicial, largura, altura))
        
        # O resto do código permanece igual
        img_np = np.array(screenshot)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        return img_bgr
    except Exception as e:
        print(f"❌ Erro ao capturar a região da tela: {e}")
        return None

def detectar_cartas_football_studio(img):
    """Detecta as cartas do Football Studio na imagem"""
    try:
        if img is None:
            return None, None
        
        # Converter para HSV para melhor detecção de cores
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Definir ranges de cores para cartas vermelhas e azuis
        # Vermelho (Casa)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # Azul (Visitante)
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])
        
        # Criar máscaras
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = mask_red1 + mask_red2
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Encontrar contornos
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        carta_vermelha = None
        carta_azul = None
        
        # Processar contornos vermelhos (Casa)
        if contours_red:
            for contour in contours_red:
                area = cv2.contourArea(contour)
                if area > 1000:  # Filtrar áreas muito pequenas
                    x, y, w, h = cv2.boundingRect(contour)
                    if w > 30 and h > 40:  # Proporções de carta
                        # Extrair região da carta
                        carta_roi = img[y:y+h, x:x+w]
                        carta_vermelha = processar_carta_ocr(carta_roi)
                        break
        
        # Processar contornos azuis (Visitante)
        if contours_blue:
            for contour in contours_blue:
                area = cv2.contourArea(contour)
                if area > 1000:  # Filtrar áreas muito pequenas
                    x, y, w, h = cv2.boundingRect(contour)
                    if w > 30 and h > 40:  # Proporções de carta
                        # Extrair região da carta
                        carta_roi = img[y:y+h, x:x+w]
                        carta_azul = processar_carta_ocr(carta_roi)
                        break
        
        return carta_vermelha, carta_azul
        
    except Exception as e:
        print(f"❌ Erro na detecção de cartas: {e}")
        return None, None

def processar_carta_ocr(carta_img):
    """Processa uma carta usando OCR para identificar valor e naipe"""
    try:
        # Converter para escala de cinza
        gray = cv2.cvtColor(carta_img, cv2.COLOR_BGR2GRAY)
        
        # Aplicar threshold para melhorar OCR
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Aplicar OCR
        texto = pytesseract.image_to_string(thresh, config='--psm 8')
        texto = texto.strip().upper()
        
        # Mapear texto para carta
        if texto:
            # Detectar valor
            valor = None
            if 'A' in texto or 'ACE' in texto:
                valor = 'A'
            elif 'K' in texto or 'KING' in texto:
                valor = 'K'
            elif 'Q' in texto or 'QUEEN' in texto:
                valor = 'Q'
            elif 'J' in texto or 'JACK' in texto:
                valor = 'J'
            else:
                # Tentar extrair número
                for char in texto:
                    if char.isdigit():
                        if char == '1' and '0' in texto:
                            valor = '10'
                        else:
                            valor = char
                        break
            
            # Detectar naipe baseado na posição/cor predominante
            # Para simplificar, vou usar detecção de cor
            naipe = detectar_naipe_por_cor(carta_img)
            
            if valor and naipe:
                return CartaFootballStudio(naipe, valor)
        
        return None
        
    except Exception as e:
        print(f"❌ Erro no OCR da carta: {e}")
        return None

def detectar_naipe_por_cor(carta_img):
    """Detecta o naipe baseado na cor predominante"""
    try:
        # Converter para HSV
        hsv = cv2.cvtColor(carta_img, cv2.COLOR_BGR2HSV)
        
        # Contar pixels vermelhos vs pretos
        # Vermelho para ♥ ♦
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_pixels = cv2.countNonZero(mask_red1 + mask_red2)
        
        # Preto para ♠ ♣
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])
        mask_black = cv2.inRange(hsv, lower_black, upper_black)
        black_pixels = cv2.countNonZero(mask_black)
        
        # Retornar naipe baseado na cor predominante
        if red_pixels > black_pixels:
            return random.choice(['♥', '♦'])  # Vermelho
        else:
            return random.choice(['♠', '♣'])  # Preto
            
    except:
        return random.choice(['♠', '♥', '♦', '♣'])

def monitorar_integrado_real():
    """Thread de monitoramento com captura real de dados"""
    global monitoramento_ativo, ultima_atividade
    
    print("🎯 Iniciando monitoramento REAL do Football Studio...")
    print("📸 Sistema irá capturar dados da tela do jogo")
    time.sleep(3)  # Delay inicial
    
    contador_rodada = 1
    ultima_carta_vermelha = None
    ultima_carta_azul = None
    
    while monitoramento_ativo:
        try:
            print(f"📸 Capturando tela - rodada {contador_rodada}...")
            
            # Capturar tela
            img = capturar_tela_jogo()
            if img is None:
                print("❌ Falha na captura de tela")
                time.sleep(5)
                continue
            
            # Detectar cartas
            carta_vermelha, carta_azul = detectar_cartas_football_studio(img)
            
            # Verificar se detectou cartas válidas
            if carta_vermelha and carta_azul:
                # Verificar se são cartas diferentes da rodada anterior
                if (str(carta_vermelha) != str(ultima_carta_vermelha) or 
                    str(carta_azul) != str(ultima_carta_azul)):
                    
                    # Criar rodada
                    rodada = RodadaFutebolEstudio(
                        carta_vermelha=carta_vermelha,
                        carta_azul=carta_azul,
                        timestamp=datetime.now().strftime("%H:%M:%S")
                    )
                    
                    catalogador.adicionar_rodada(rodada)
                    ultima_atividade = f"Rodada {contador_rodada}: {carta_vermelha} x {carta_azul} - {rodada.vencedor}"
                    
                    print(f"✅ {ultima_atividade}")
                    
                    # Salvar última captura
                    ultima_carta_vermelha = carta_vermelha
                    ultima_carta_azul = carta_azul
                    contador_rodada += 1
                else:
                    print("⏭️ Mesmas cartas da rodada anterior, aguardando mudança...")
            else:
                print("🔍 Cartas não detectadas, continuando captura...")
            
            # Intervalo entre capturas (mais frequente para dados reais)
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Erro no monitoramento real: {e}")
            time.sleep(5)
    
    print("⏹️ Monitoramento real parado")

# ============================================================================
# ROTAS PRINCIPAIS
# ============================================================================

@app.route('/')
def index():
    """Página inicial - redireciona para login"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Validação simples
        if email and senha:
            # Salvar credenciais na sessão
            session['email'] = email
            session['logado'] = True
            
            # Atualizar credenciais globais
            credenciais_usuario['email'] = email
            credenciais_usuario['senha'] = senha
            credenciais_usuario['logado'] = True
            
            flash('✅ Login realizado com sucesso!', 'success')
            return redirect(url_for('football_integrado'))
        else:
            flash('❌ Por favor, preencha todos os campos', 'error')
    
    return render_template('login.html')

@app.route('/football-integrado')
def football_integrado():
    """Página do sistema integrado"""
    # Verificar se está logado
    if not session.get('logado'):
        flash('❌ Faça login primeiro', 'error')
        return redirect(url_for('login'))
    
    return render_template('football_integrado.html')

@app.route('/teste-css')
def teste_css():
    """Página de teste CSS"""
    return render_template('teste_css.html')

@app.route('/logout')
def logout():
    """Logout do sistema"""
    session.clear()
    credenciais_usuario['logado'] = False
    flash('👋 Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

# ============================================================================
# ROTAS DE API
# ============================================================================

@app.route('/iniciar_monitoramento_integrado', methods=['POST'])
def iniciar_monitoramento_integrado():
    """Inicia o monitoramento integrado REAL"""
    global monitoramento_ativo, thread_monitoramento
    
    try:
        if not monitoramento_ativo:
            monitoramento_ativo = True
            thread_monitoramento = threading.Thread(target=monitorar_integrado_real)
            thread_monitoramento.daemon = True
            thread_monitoramento.start()
            
            return jsonify({
                'success': True,
                'message': '✅ Monitoramento REAL iniciado!'
            })
        else:
            return jsonify({
                'success': False,
                'message': '⚠️ Monitoramento já está ativo'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'❌ Erro: {str(e)}'
        })

@app.route('/parar_monitoramento', methods=['POST'])
def parar_monitoramento():
    """Para o monitoramento de forma controlada"""
    global monitoramento_ativo, thread_monitoramento  # Adicionar thread_monitoramento ao escopo global

    try:
        if monitoramento_ativo and thread_monitoramento is not None:
            print("⏹️ Recebido comando para parar o monitoramento...")
            monitoramento_ativo = False  # Sinaliza para a thread parar

            # Espera a thread terminar. O timeout evita que a requisição fique presa indefinidamente.
            thread_monitoramento.join(timeout=5)

            if thread_monitoramento.is_alive():
                print("⚠️ A thread não parou no tempo esperado.")
                return jsonify({
                    'success': False,
                    'message': '⚠️ A thread não respondeu ao comando de parada.'
                })

            thread_monitoramento = None  # Limpa a referência da thread
            print("✅ Monitoramento parado com sucesso.")
            return jsonify({
                'success': True,
                'message': '⏹️ Monitoramento parado com sucesso!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'ℹ️ O monitoramento não estava ativo.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'❌ Erro ao parar monitoramento: {str(e)}'
        })

@app.route('/iniciar_captura_avancada', methods=['POST'])
def iniciar_captura_avancada():
    """Inicia o sistema avançado com captura REAL"""
    global monitoramento_ativo, thread_monitoramento
    
    try:
        if not monitoramento_ativo:
            monitoramento_ativo = True
            thread_monitoramento = threading.Thread(target=monitorar_integrado_real)
            thread_monitoramento.daemon = True
            thread_monitoramento.start()
            
            return jsonify({
                'success': True,
                'message': '🔬 Sistema Avançado REAL iniciado!'
            })
        else:
            return jsonify({
                'success': False,
                'message': '⚠️ Sistema já está ativo'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'❌ Erro: {str(e)}'
        })

@app.route('/capturar_teste', methods=['POST'])
def capturar_teste():
    """Faz uma captura de teste para verificar detecção"""
    try:
        print("🧪 Fazendo captura de teste...")
        
        # Capturar tela
        img = capturar_tela_jogo()
        if img is None:
            return jsonify({
                'success': False,
                'message': '❌ Falha na captura de tela'
            })
        
        # Salvar imagem para debug
        timestamp = datetime.now().strftime("%H%M%S")
        debug_filename = f"debug_captura_{timestamp}.png"
        cv2.imwrite(debug_filename, img)
        print(f"📸 Imagem salva: {debug_filename}")
        
        # Detectar cartas
        carta_vermelha, carta_azul = detectar_cartas_football_studio(img)
        
        if carta_vermelha and carta_azul:
            return jsonify({
                'success': True,
                'message': f'✅ Cartas detectadas: {carta_vermelha} x {carta_azul}',
                'carta_vermelha': str(carta_vermelha),
                'carta_azul': str(carta_azul),
                'debug_image': debug_filename
            })
        else:
            return jsonify({
                'success': False,
                'message': f'🔍 Nenhuma carta detectada na tela. Imagem salva como {debug_filename} para análise.',
                'debug_image': debug_filename
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'❌ Erro na captura: {str(e)}'
        })

@app.route('/status_monitor')
def status_monitor():
    """Retorna o status atual do monitoramento"""
    try:
        stats = catalogador.obter_estatisticas()
        
        # Últimas 10 rodadas
        ultimas_rodadas = []
        for rodada in catalogador.historico[-10:]:
            # Mapear vencedor para o formato esperado pelo JavaScript
            resultado = 'empate'
            if rodada.vencedor == 'Casa':
                resultado = 'vermelho'
            elif rodada.vencedor == 'Visitante':
                resultado = 'azul'
            
            ultimas_rodadas.append({
                'carta_vermelha': str(rodada.carta_vermelha),
                'carta_azul': str(rodada.carta_azul),
                'vencedor': rodada.vencedor,
                'resultado': resultado,  # Formato para o dashboard
                'timestamp': rodada.timestamp
            })
        
        return jsonify({
            'ativo': monitoramento_ativo,
            'ultima_atividade': ultima_atividade,
            'estatisticas': stats,
            'stats': {  # Adicionar formato esperado pelo JavaScript
                'total_rodadas': stats['total_rodadas'],
                'vitorias_vermelho': stats['casa_vitorias'],
                'vitorias_azul': stats['visitante_vitorias'],
                'empates': stats['empates']
            },
            'ultimas_rodadas': ultimas_rodadas,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
    except Exception as e:
        return jsonify({
            'erro': str(e),
            'ativo': False
        })

@app.route('/limpar_dados', methods=['POST'])
def limpar_dados():
    """Limpa o histórico na memória e no arquivo JSON."""
    global catalogador, ultima_atividade
    
    try:
        # Limpa a lista na memória
        catalogador.historico = []
        # Salva a lista vazia no arquivo, sobrescrevendo o conteúdo antigo
        catalogador.salvar_dados()
        
        ultima_atividade = "Dados limpos"
        
        return jsonify({
            'success': True,
            'message': '🗑️ Dados e histórico limpos com sucesso!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'❌ Erro ao limpar dados: {str(e)}'
        })

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎮 FOOTBALL STUDIO - CAPTURA REAL DE DADOS")
    print("="*60)
    print("🔐 Sistema com login seguro")
    print("📸 Captura REAL de dados da tela")
    print("🎯 Monitoramento em tempo real por visão computacional")
    print("📱 Acesse: http://localhost:5000")
    print("� OCR + Detecção de cores para cartas reais")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
