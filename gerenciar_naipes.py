#!/usr/bin/env python3
"""
Gerenciador de Templates por Naipe
Permite organizar templates específicos para cada naipe de cartas
"""
import os
import shutil
from datetime import datetime

def criar_template_naipe():
    """Cria template para um naipe específico"""
    print("🃏 CRIADOR DE TEMPLATE POR NAIPE")
    print("=" * 40)
    
    naipes = {
        '1': ('casa_ouro', 'Casa (♦)', '🔶'),
        '2': ('visitante_espada', 'Visitante (♠)', '🔷'),
        '3': ('copas', 'Copas (♥)', '❤️'),
        '4': ('paus', 'Paus (♣)', '♣️')
    }
    
    print("Escolha o naipe:")
    for key, (folder, nome, emoji) in naipes.items():
        print(f"   {key} - {emoji} {nome}")
    
    escolha = input("\n🎮 Digite o número do naipe (1-4): ").strip()
    
    if escolha not in naipes:
        print("❌ Opção inválida!")
        return
    
    pasta_naipe, nome_naipe, emoji = naipes[escolha]
    
    cartas_validas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    print(f"\n{emoji} Criando template para {nome_naipe}")
    print("Cartas disponíveis:", ', '.join(cartas_validas))
    
    carta = input("🃏 Digite o valor da carta: ").strip().upper()
    
    if carta not in cartas_validas:
        print(f"❌ Carta inválida! Use: {', '.join(cartas_validas)}")
        return
    
    pasta_carta = f"templates_organizados/{pasta_naipe}/{carta}"
    
    if not os.path.exists(pasta_carta):
        print(f"❌ Pasta não encontrada: {pasta_carta}")
        return
    
    print(f"\n📁 Pasta de destino: {pasta_carta}")
    print("💡 Coloque a imagem da carta na área de captura")
    input("⏳ Pressione ENTER quando estiver pronto para capturar...")
    
    # Aqui você pode integrar com o sistema de captura
    print("📸 Captura simulada...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{carta}_{pasta_naipe}_{timestamp}.png"
    
    print(f"✅ Template {nome_arquivo} seria salvo em {pasta_carta}")
    print(f"🎯 {emoji} {nome_naipe} - {carta} adicionado!")

def listar_templates_por_naipe():
    """Lista templates organizados por naipe"""
    print("📋 TEMPLATES POR NAIPE")
    print("=" * 40)
    
    naipes = {
        'casa_ouro': ('🔶', 'Casa (♦)'),
        'visitante_espada': ('🔷', 'Visitante (♠)'),
        'copas': ('❤️', 'Copas (♥)'),
        'paus': ('♣️', 'Paus (♣)')
    }
    
    base_path = "templates_organizados"
    
    for pasta_naipe, (emoji, nome) in naipes.items():
        print(f"\n{emoji} {nome}")
        
        naipe_path = os.path.join(base_path, pasta_naipe)
        if not os.path.exists(naipe_path):
            print("   ❌ Pasta não encontrada")
            continue
        
        cartas = sorted(os.listdir(naipe_path))
        total_templates = 0
        cartas_com_templates = 0
        
        for carta in cartas:
            carta_path = os.path.join(naipe_path, carta)
            if os.path.isdir(carta_path):
                arquivos = [f for f in os.listdir(carta_path) if f.endswith('.png')]
                if arquivos:
                    total_templates += len(arquivos)
                    cartas_com_templates += 1
                    print(f"   🃏 {carta}: {len(arquivos)} templates")
        
        if total_templates == 0:
            print("   📭 Nenhum template encontrado")
        else:
            print(f"   📊 Total: {total_templates} templates em {cartas_com_templates}/13 cartas")

def copiar_templates_entre_naipes():
    """Copia templates entre naipes diferentes"""
    print("🔄 COPIAR TEMPLATES ENTRE NAIPES")
    print("=" * 40)
    
    naipes = ['casa_ouro', 'visitante_espada', 'copas', 'paus']
    
    print("Naipes disponíveis:")
    for i, naipe in enumerate(naipes, 1):
        print(f"   {i} - {naipe}")
    
    origem = input("\n📥 Naipe de origem (1-4): ").strip()
    destino = input("📤 Naipe de destino (1-4): ").strip()
    
    try:
        origem_idx = int(origem) - 1
        destino_idx = int(destino) - 1
        
        if not (0 <= origem_idx < 4) or not (0 <= destino_idx < 4):
            print("❌ Opções inválidas!")
            return
        
        naipe_origem = naipes[origem_idx]
        naipe_destino = naipes[destino_idx]
        
        print(f"🔄 Copiando de {naipe_origem} para {naipe_destino}")
        
        # Simular cópia
        print("✅ Cópia simulada realizada!")
        
    except ValueError:
        print("❌ Digite apenas números!")

def estatisticas_completas():
    """Mostra estatísticas completas de todos os naipes"""
    print("📊 ESTATÍSTICAS COMPLETAS")
    print("=" * 40)
    
    naipes = {
        'casa_ouro': ('🔶', 'Casa (♦)'),
        'visitante_espada': ('🔷', 'Visitante (♠)'),
        'copas': ('❤️', 'Copas (♥)'),
        'paus': ('♣️', 'Paus (♣)')
    }
    
    base_path = "templates_organizados"
    total_geral = 0
    cartas_geral = 0
    
    for pasta_naipe, (emoji, nome) in naipes.items():
        naipe_path = os.path.join(base_path, pasta_naipe)
        if os.path.exists(naipe_path):
            cartas = [c for c in os.listdir(naipe_path) if os.path.isdir(os.path.join(naipe_path, c))]
            templates_naipe = 0
            cartas_naipe = 0
            
            for carta in cartas:
                carta_path = os.path.join(naipe_path, carta)
                arquivos = [f for f in os.listdir(carta_path) if f.endswith('.png')]
                if arquivos:
                    templates_naipe += len(arquivos)
                    cartas_naipe += 1
            
            print(f"{emoji} {nome}: {templates_naipe} templates em {cartas_naipe}/13 cartas")
            total_geral += templates_naipe
            cartas_geral += cartas_naipe
    
    print(f"\n📈 TOTAL GERAL:")
    print(f"   🃏 {total_geral} templates")
    print(f"   📊 {cartas_geral}/52 cartas com templates")
    print(f"   📋 {len(naipes)} naipes organizados")

if __name__ == "__main__":
    print("🃏 GERENCIADOR DE TEMPLATES POR NAIPE")
    print("=" * 50)
    print("1 - Criar template por naipe")
    print("2 - Listar templates por naipe")
    print("3 - Copiar templates entre naipes")
    print("4 - Estatísticas completas")
    print("5 - Sair")
    
    opcao = input("\n🎮 Escolha uma opção (1-5): ").strip()
    
    if opcao == '1':
        criar_template_naipe()
    elif opcao == '2':
        listar_templates_por_naipe()
    elif opcao == '3':
        copiar_templates_entre_naipes()
    elif opcao == '4':
        estatisticas_completas()
    elif opcao == '5':
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida!")
