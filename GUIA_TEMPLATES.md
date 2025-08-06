🎯 GUIA RÁPIDO - SISTEMA DE TEMPLATES
=====================================

## Como Usar o Sistema de Reconhecimento por Templates

### 1. 🎮 Abrir o Football Studio
- Abra seu navegador
- Acesse: https://luck.bet.br/live-casino/game/1170048?provider=Evolution&from=%2Flive-casino&locale=pt-BR&lang=pt
- Entre no Football Studio (versão em português)
- Aguarde aparecer cartas na tela

### 2. 📦 Criar Templates das Cartas
```bash
python reconhecimento_templates.py
```
- Escolha opção **1** (Criar templates)
- Para cada carta visível na tela:
  - Digite o valor: **A**, **2**, **3**... **10**, **J**, **Q**, **K**
  - Sistema captura automaticamente o template
- Digite **sair** quando terminar

### 3. 🧪 Testar o Sistema
```bash
python testar_templates.py
```
- Mostra se os templates estão funcionando
- Testa reconhecimento em tempo real

### 4. 🚀 Usar no Monitoramento
- Abra a interface web: `python app.py`
- Clique em **"Iniciar Monitoramento"**
- Agora usa templates em vez de OCR!

## 📊 Comandos Úteis

### Ver Templates Criados:
```bash
python reconhecimento_templates.py
# Escolher opção 3
```

### Limpar Templates:
```bash
python reconhecimento_templates.py  
# Escolher opção 4
```

### Testar Detecção:
```bash
python testar_templates.py
```

## 🎯 Dicas Importantes

- ✅ **Crie templates para TODAS as cartas** (A, 2-9, 10, J, Q, K)
- ✅ **Cartas devem estar visíveis** ao criar templates
- ✅ **Sistema funciona melhor** com templates de boa qualidade
- ✅ **Quanto mais templates**, melhor a precisão

## 📈 Vantagens do Sistema de Templates

- 🎯 **Mais preciso** que OCR
- ⚡ **Reconhece padrões visuais** em vez de texto
- 📦 **Aprende as cartas** do seu jogo específico
- 🔄 **Funciona com diferentes iluminações**

---
🚀 **APENAS DADOS REAIS NO CATÁLOGO** - Sistema usa cartas reais do seu jogo!
