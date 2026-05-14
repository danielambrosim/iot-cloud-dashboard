# main.py
import argparse
from datetime import datetime
from database import criar_tabela, inserir_leitura, limpar_dados_antigos
from weather_api import coletar_todas_cidades, listar_cidades_disponiveis

def simular_sistema(interactive=True):
    """Coleta dados de todas as cidades monitoradas"""
    
    # Criar tabela do banco de dados
    criar_tabela()
    
    # Limpar dados antigos
    removidos = limpar_dados_antigos()
    print(f"🗑️ Removidas {removidos} leituras antigas (>30 dias)")
    
    cidades = listar_cidades_disponiveis()
    
    print("\n" + "="*50)
    print("🌤️ COLETOR AUTOMÁTICO DE DADOS CLIMÁTICOS")
    print("="*50)
    print(f"📊 Monitorando {len(cidades)} cidades:")
    for cidade in cidades:
        print(f"   - {cidade}")
    print(f"🔗 Fonte: Open-Meteo API")
    
    if interactive:
        print("⏱️  Intervalo: 60 segundos entre coletas")
        print("⏹️ Pressione Ctrl+C para parar\n")
    else:
        print("🤖 Modo automático (GitHub Actions) - Executando uma coleta")
    
    contador = 0
    
    try:
        while True:
            print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Coletando dados...")
            
            # Coleta dados de todas as cidades
            dados_coletados = coletar_todas_cidades()
            
            # Salvar cada leitura no banco
            for dados in dados_coletados:
                inserir_leitura(
                    dados["cidade"], 
                    dados["temperatura"], 
                    dados["umidade"], 
                    dados["fonte"]
                )
            
            contador += len(dados_coletados)
            print(f"📊 Total de leituras salvas: {contador}")
            
            if not interactive:
                # Modo automático: faz uma coleta e para
                break
            
            # Aguardar 60 segundos para a próxima coleta
            time.sleep(60)
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*50}")
        print("🛑 COLETOR FINALIZADO")
        print(f"{'='*50}")
        print(f"📊 Total de leituras na sessão: {contador}")

def main():
    parser = argparse.ArgumentParser(description='Coletor de dados climáticos IoT')
    parser.add_argument('--non-interactive', action='store_true', 
                        help='Executa em modo não interativo (para GitHub Actions)')
    
    args = parser.parse_args()
    simular_sistema(interactive=not args.non_interactive)

if __name__ == "__main__":
    import time  # Adicionado para o loop
    main()