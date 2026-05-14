import argparse
import time
from datetime import datetime
from database import criar_tabela, inserir_leitura, limpar_dados_antigos
from weather_api import coletar_todas_cidades, listar_cidades_disponiveis

def simular_sistema(interactive=True):
    """Coleta dados de todas as cidades monitoradas"""
    
    criar_tabela()
    limpar_dados_antigos()
    
    cidades = listar_cidades_disponiveis()
    
    print("\n" + "="*50)
    print("🌤️ COLETOR AUTOMÁTICO DE DADOS CLIMÁTICOS")
    print("="*50)
    print(f"📊 Monitorando {len(cidades)} cidades:")
    for cidade in cidades:
        print(f"   - {cidade}")
    
    if interactive:
        print("\n⏱️  Intervalo: 60 segundos entre coletas")
        print("⏹️ Pressione Ctrl+C para parar\n")
    else:
        print("\n🤖 Modo automático (GitHub Actions) - Executando uma coleta\n")
    
    contador = 0
    
    try:
        while True:
            print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Coletando dados...")
            
            dados_coletados = coletar_todas_cidades()
            
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
                print("\n✅ Coleta concluída com sucesso!")
                break
            
            time.sleep(60)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Coletor finalizado. Total: {contador} leituras")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--non-interactive', action='store_true')
    args = parser.parse_args()
    
    simular_sistema(interactive=not args.non_interactive)

if __name__ == "__main__":
    main()