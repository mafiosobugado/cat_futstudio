#!/usr/bin/env python3
"""
Script para abrir automaticamente o Football Studio no navegador
"""
import webbrowser
from config_football_studio import FOOTBALL_STUDIO_URL, LOCAL_SERVER_URL

def abrir_football_studio():
    """Abre o Football Studio no navegador padrão"""
    print("🎮 ABRINDO FOOTBALL STUDIO")
    print("=" * 40)
    print(f"🔗 URL: {FOOTBALL_STUDIO_URL}")
    print("🚀 Abrindo no navegador...")
    
    try:
        webbrowser.open(FOOTBALL_STUDIO_URL)
        print("✅ Football Studio aberto com sucesso!")
        print("🆔 Game ID: 1170048 (Versão em Português)")
    except Exception as e:
        print(f"❌ Erro ao abrir: {e}")
        print("💡 Copie e cole a URL manualmente:")
        print(f"   {FOOTBALL_STUDIO_URL}")

def abrir_interface_local():
    """Abre a interface local do sistema"""
    print("\n🖥️ ABRINDO INTERFACE LOCAL")
    print("=" * 40)
    print(f"🔗 URL: {LOCAL_SERVER_URL}")
    print("🚀 Abrindo no navegador...")
    
    try:
        webbrowser.open(LOCAL_SERVER_URL)
        print("✅ Interface local aberta com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao abrir: {e}")
        print("💡 Copie e cole a URL manualmente:")
        print(f"   {LOCAL_SERVER_URL}")

def mostrar_links():
    """Mostra todos os links importantes"""
    print("🔗 LINKS DO SISTEMA")
    print("=" * 40)
    print(f"🎮 Football Studio: {FOOTBALL_STUDIO_URL}")
    print(f"🖥️ Interface Local:  {LOCAL_SERVER_URL}")
    print(f"🏠 LuckBet Home:     https://luck.bet.br")
    print(f"🎰 Live Casino:      https://luck.bet.br/live-casino")

if __name__ == "__main__":
    print("🎯 FOOTBALL STUDIO - UTILITÁRIO DE LINKS")
    print("=" * 50)
    print("1 - Abrir Football Studio")
    print("2 - Abrir Interface Local")
    print("3 - Mostrar todos os links")
    print("4 - Sair")
    
    opcao = input("\n🎮 Escolha uma opção (1-4): ").strip()
    
    if opcao == '1':
        abrir_football_studio()
    elif opcao == '2':
        abrir_interface_local()
    elif opcao == '3':
        mostrar_links()
    elif opcao == '4':
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida!")
        mostrar_links()
