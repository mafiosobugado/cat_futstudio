# 🎮 Football Studio - Sistema Integrado

Sistema completo para monitoramento de cartas do Football Studio com interface integrada.

## 📋 Funcionalidades

- 🔐 **Login seguro** para acesso ao sistema
- 🎮 **Jogo integrado** - Football Studio direto na interface
- 📊 **Monitoramento em tempo real** das cartas
- 📈 **Estatísticas avançadas** e análise de padrões
- 🎯 **Interface limpa** e responsiva
- 💾 **Histórico persistente** das rodadas

## 🚀 Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o Sistema
```bash
python app.py
```

### 3. Acessar o Sistema
- Abra seu navegador em: `http://localhost:5000`
- Faça login com suas credenciais
- Acesse o sistema integrado
- O Football Studio será carregado automaticamente na URL: 
  `https://luck.bet.br/live-casino/game/1170048?provider=Evolution&from=%2Flive-casino`

## 📁 Estrutura do Projeto

```
magocatalogo/
├── app.py                     # Aplicação principal Flask
├── requirements.txt           # Dependências do projeto
├── historico_cartas.json     # Dados persistentes das rodadas
├── templates/
│   ├── login.html            # Página de login
│   └── football_integrado.html # Interface integrada
├── static/                   # Arquivos estáticos (CSS, JS, images)
├── abrir_chrome_debug.bat    # Script para abrir Chrome em modo debug
└── abrir_edge_debug.bat      # Script para abrir Edge em modo debug
```

## 🎯 Funcionalidades Principais

### Login e Autenticação
- Sistema de login com validação
- Sessões seguras
- Redirecionamento automático

### Sistema Integrado
- Jogo Football Studio em iframe
- Painel de monitoramento lateral
- Controles de início/parada
- Geração de dados de teste

### Monitoramento
- Captura simulada de cartas em tempo real
- Cálculo automático de vencedores
- Estatísticas dinâmicas
- Histórico das últimas rodadas

### Estatísticas
- Total de rodadas
- Vitórias por lado (Casa/Visitante)
- Empates
- Carta mais frequente
- Sequências de vitórias

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Dados**: JSON para persistência
- **Interface**: Design responsivo e moderno

## 📱 Interface

### Página de Login
- Design elegante com tema dourado
- Validação de campos
- Mensagens de feedback
- Informações sobre o sistema

### Sistema Integrado
- **Área do Jogo**: Iframe com Football Studio
- **Painel de Monitoramento**: 
  - Controles de sistema
  - Status em tempo real
  - Estatísticas ao vivo
  - Histórico de rodadas

## 🎮 Como Jogar

1. Faça login no sistema
2. Acesse a página integrada
3. Jogue Football Studio na área principal
4. Use o painel lateral para:
   - Iniciar monitoramento
   - Gerar dados de teste
   - Ver estatísticas
   - Acompanhar histórico

## 🔧 Configuração Avançada

### Scripts de Debug
- `abrir_chrome_debug.bat`: Abre Chrome com debug habilitado
- `abrir_edge_debug.bat`: Abre Edge com debug habilitado

### Persistência de Dados
- Dados são salvos automaticamente em `historico_cartas.json`
- Histórico mantém últimas 100 rodadas
- Backup automático a cada nova rodada

## 📊 Análise de Dados

O sistema fornece análises em tempo real:
- Padrões de cartas
- Frequência de resultados
- Sequências de vitórias
- Tendências estatísticas

## 🎯 Próximos Passos

- [ ] Integração com API real do jogo
- [ ] Análise preditiva avançada
- [ ] Exportação de dados
- [ ] Dashboard expandido
- [ ] Alertas personalizados

---

**Desenvolvido para análise educacional do Football Studio** 🎮
