# main.py
from datetime import datetime
from database import criar_tabela, inserir_leitura, limpar_dados_antigos
from weather_api import coletar_todas_cidades, listar_cidades_disponiveis

def coletar_dados():
    """Coleta dados climáticos uma única vez"""
    
    criar_tabela()
    limpar_dados_antigos()
    
    cidades = listar_cidades_disponiveis()
    
    print("="*50)
    print("🌤️ COLETOR DE DADOS CLIMÁTICOS")
    print("="*50)
    print(f"📊 Monitorando {len(cidades)} cidades:")
    for cidade in cidades:
        print(f"   - {cidade}")
    
    print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Coletando dados...\n")
    
    dados_coletados = coletar_todas_cidades()
    
    if dados_coletados:
        for dados in dados_coletados:
            inserir_leitura(
                dados["cidade"],
                dados["temperatura"],
                dados["umidade"],
                dados["fonte"]
            )
        
        print(f"\n✅ Coleta concluída!")
        print(f"📊 {len(dados_coletados)} leituras salvas no banco")
    else:
        print("\n⚠️ Nenhum dado foi coletado!")
    
    print("\n🛑 Encerrando execução...")

if __name__ == "__main__":
    coletar_dados() 