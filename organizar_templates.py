#!/usr/bin/env python3
"""
Script para organizar templates existentes na nova estrutura de pastas
"""
import pickle
import cv2
import os
import shutil
from datetime import datetime

def organizar_templates():
    """Organiza templates do arquivo pickle na nova estrutura de pastas"""
    
    print("📁 ORGANIZADOR DE TEMPLATES")
    print("=" * 50)
    
    # Carregar templates existentes
    try:
        with open('templates_cartas.pkl', 'rb') as f:
            templates = pickle.load(f)
        print(f"✅ Templates carregados: {len(templates)} tipos")
    except FileNotFoundError:
        print("❌ Arquivo templates_cartas.pkl não encontrado!")
        return
    
    # Criar timestamp para backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Contador de arquivos organizados
    contador = 0
    
    for template_key, variaciones in templates.items():
        print(f"\n🔍 Processando: {template_key}")
        
        # Extrair informações do template_key
        if '_CASA' in template_key:
            naipe_pasta = 'casa_ouro'
            valor = template_key.replace('_CASA', '')
            naipe_nome = 'Casa (♦)'
        elif '_VISITANTE' in template_key:
            naipe_pasta = 'visitante_espada'
            valor = template_key.replace('_VISITANTE', '')
            naipe_nome = 'Visitante (♠)'
        else:
            print(f"   ⚠️ Formato não reconhecido: {template_key}")
            continue
        
        # Pasta de destino
        pasta_destino = f"templates_organizados/{naipe_pasta}/{valor}"
        
        print(f"   📂 Destino: {pasta_destino}")
        print(f"   🃏 {naipe_nome} - {valor}")
        print(f"   📊 Variações: {len(variaciones)}")
        
        # Salvar cada variação
        for i, (template_img, caracteristicas) in enumerate(variaciones, 1):
            nome_arquivo = f"{valor}_{naipe_pasta}_{timestamp}_v{i:02d}.png"
            caminho_completo = os.path.join(pasta_destino, nome_arquivo)
            
            try:
                # Salvar imagem
                cv2.imwrite(caminho_completo, template_img)
                
                # Salvar características em arquivo texto
                txt_arquivo = caminho_completo.replace('.png', '_caracteristicas.txt')
                with open(txt_arquivo, 'w') as f:
                    f.write(f"Template: {template_key}\n")
                    f.write(f"Variação: {i}\n")
                    f.write(f"Valor: {valor}\n")
                    f.write(f"Naipe: {naipe_nome}\n")
                    f.write(f"Características: {caracteristicas.tolist()}\n")
                    f.write(f"Data: {timestamp}\n")
                
                print(f"   ✅ Salvo: {nome_arquivo}")
                contador += 1
                
            except Exception as e:
                print(f"   ❌ Erro ao salvar {nome_arquivo}: {e}")
    
    print(f"\n📊 RESUMO:")
    print(f"✅ Templates organizados: {contador}")
    print(f"📁 Estrutura criada em: templates_organizados/")
    print(f"🗓️ Timestamp: {timestamp}")
    
    # Criar backup do arquivo original
    backup_nome = f"templates_cartas_backup_{timestamp}.pkl"
    try:
        shutil.copy2('templates_cartas.pkl', backup_nome)
        print(f"💾 Backup criado: {backup_nome}")
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")

def listar_templates_organizados():
    """Lista templates organizados por pasta"""
    
    print("\n📋 TEMPLATES ORGANIZADOS:")
    print("=" * 50)
    
    base_path = "templates_organizados"
    
    naipes = {
        'casa_ouro': "🔶 CASA (♦)",
        'visitante_espada': "🔷 VISITANTE (♠)", 
        'copas': "❤️ COPAS (♥)",
        'paus': "♣️ PAUS (♣)"
    }
    
    for naipe, naipe_nome in naipes.items():
        print(f"\n{naipe_nome}")
        
        naipe_path = os.path.join(base_path, naipe)
        if not os.path.exists(naipe_path):
            print("   ❌ Pasta não encontrada")
            continue
            
        # Listar cartas
        cartas = sorted(os.listdir(naipe_path))
        total_templates = 0
        for carta in cartas:
            carta_path = os.path.join(naipe_path, carta)
            if os.path.isdir(carta_path):
                arquivos = [f for f in os.listdir(carta_path) if f.endswith('.png')]
                total_templates += len(arquivos)
                print(f"   🃏 {carta}: {len(arquivos)} templates")
        
        print(f"   📊 Total {naipe}: {total_templates} templates")

if __name__ == "__main__":
    print("🗂️ ORGANIZADOR DE TEMPLATES DE CARTAS")
    print("=" * 60)
    print("1 - Organizar templates existentes")
    print("2 - Listar templates organizados")
    print("3 - Sair")
    
    opcao = input("\n🎮 Escolha uma opção (1-3): ").strip()
    
    if opcao == '1':
        organizar_templates()
    elif opcao == '2':
        listar_templates_organizados()
    elif opcao == '3':
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida!")
