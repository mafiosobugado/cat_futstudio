# Configurações do Football Studio
# ==================================

# URL do Football Studio na LuckBet (português brasileiro)
FOOTBALL_STUDIO_URL = "https://luck.bet.br/live-casino/game/1170048?provider=Evolution&from=%2Flive-casino&locale=pt-BR&lang=pt"

# URLs relacionadas
LUCKBET_BASE_URL = "https://luck.bet.br"
LIVE_CASINO_URL = "https://luck.bet.br/live-casino"

# Configurações do jogo
GAME_ID = "1170048"
PROVIDER = "Evolution"
FROM_PAGE = "/live-casino"

# Configurações de captura
DEFAULT_CAPTURE_DELAY = 2  # segundos entre capturas
DEFAULT_SIMILARITY_THRESHOLD = 0.7  # limite de similaridade para templates

# Coordenadas padrão (percentuais da tela)
DEFAULT_CASA_COORDS = {
    'x': 0.30,  # 30% da largura
    'y': 0.60,  # 60% da altura
    'w': 0.20,  # 20% da largura
    'h': 0.35   # 35% da altura
}

DEFAULT_VISITANTE_COORDS = {
    'x': 0.50,  # 50% da largura
    'y': 0.60,  # 60% da altura
    'w': 0.20,  # 20% da largura
    'h': 0.35   # 35% da altura
}

# Configurações de interface
LOCAL_SERVER_URL = "http://localhost:5000"
DEBUG_MODE = True

# Arquivos de dados
TEMPLATES_FILE = "templates_cartas.pkl"
HISTORICO_FILE = "historico_cartas.json"
TEMPLATES_FOLDER = "templates_organizados"
