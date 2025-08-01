# Configurações de Captura do Football Studio

# Configurações de OCR
TESSERACT_CONFIG = '--psm 8 -c tessedit_char_whitelist=0123456789AKQJ'

# Configurações de detecção de cor
COR_VERMELHA = {
    'lower_hsv1': [0, 50, 50],
    'upper_hsv1': [10, 255, 255],
    'lower_hsv2': [170, 50, 50],
    'upper_hsv2': [180, 255, 255]
}

COR_AZUL = {
    'lower_hsv': [100, 50, 50],
    'upper_hsv': [130, 255, 255]
}

# Configurações de área mínima para cartas
AREA_MINIMA_CARTA = 1000
LARGURA_MINIMA_CARTA = 30
ALTURA_MINIMA_CARTA = 40

# Intervalo entre capturas (segundos)
INTERVALO_CAPTURA = 3

# Região da tela para capturar (deixe None para tela inteira)
# Format: (x, y, width, height)
REGIAO_CAPTURA = None  # ou ex: (100, 100, 800, 600)

# Debug - salvar imagens capturadas
SALVAR_DEBUG_IMAGENS = False
PASTA_DEBUG = "debug_capturas"
