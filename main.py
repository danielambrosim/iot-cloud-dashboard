# main.py (versão completa com suporte a GitHub Actions)

import time
import argparse
from datetime import datetime
from database import criar_tabela, inserir_leitura, limpar_dados_antigos
from weather_api import WeatherAPISensor, escolher_cidade

class AnalisadorClima:
    def __init__(self, cidade):
        self.historico = []
        self.cidade = cidade
    
    def processar_dados(self, temperatura, umidade):
        # Verifica alertas
        if temperatura > 35:
            print(f"🚨 ALERTA: Temperatura extremamente alta em {self.cidade}! {temperatura}°C")
        elif temperatura > 30:
            print(f"⚠️ ALERTA: Temperatura alta em {self.cidade}! {temperatura}°C")
        elif temperatura < 15:
            print(f"❄️ ALERTA: Temperatura baixa em {self.cidade}! {temperatura}°C")
        
        if umidade and umidade < 30:
            print(f"🌵 ALERTA: Umidade muito baixa! {umidade}% - Risco de incêndio")
        elif umidade and umidade > 80:
            print(f"💧 ALERTA: Umidade muito alta! {umidade}%")
        
        # Armazena histórico
        self.historico.append((temperatura, umidade, datetime.now()))
        
        if len(self.historico) > 100:
            self.historico.pop(0)
        
        # Calcula média das últimas 5 leituras
        if len(self.historico) >= 5:
            ultimas_temp = [item[0] for item in self.historico[-5:] if item[0] is not None]
            if ultimas_temp:
                media = sum(ultimas_temp) / len(ultimas_temp)
                return media
        return None
    
    def gerar_relatorio(self):
        print(f"\n📊 RELATÓRIO DA SESSÃO - {self.cidade}")
        print(f"Total de leituras na sessão: {len(self.historico)}")
        
        if self.historico:
            temperaturas = [item[0] for item in self.historico if item[0] is not None]
            if temperaturas:
                print(f"Temperatura máxima: {max(temperaturas)}°C")
                print(f"Temperatura mínima: {min(temperaturas)}°C")
                print(f"Temperatura média: {sum(temperaturas)/len(temperaturas):.1f}°C")

def simular_sistema(cidade_automatica=None, interactive=True):
    # Criar tabela
    criar_tabela()
    
    # Limpar dados antigos
    removidos = limpar_dados_antigos()
    print(f"🗑️ Removidas {removidos} leituras antigas (>30 dias)")
    
    # Escolher cidade (modo interativo ou automático)
    if interactive:
        cidade, latitude, longitude = escolher_cidade(interactive=True)
    else:
        cidade, latitude, longitude = escolher_cidade(interactive=False, cidade_automatica=cidade_automatica)
    
    # Criar sensor com API real
    sensor = WeatherAPISensor(cidade, latitude, longitude)
    analisador = AnalisadorClima(cidade)
    
    print("\n" + "="*50)
    print("🌤️ SISTEMA DE MONITORAMENTO CLIMÁTICO - IoT na Nuvem")
    print("="*50)
    print(f"📍 Cidade monitorada: {cidade}")
    print(f"🗺️ Coordenadas: {latitude}, {longitude}")
    print(f"🔗 Fonte: Open-Meteo API (dados climáticos reais)")
    
    if interactive:
        print(f"⏱️  Intervalo: 60 segundos entre consultas")
        print("💡 Dica: A API tem limites, não consultamos com muita frequência")
        print("\n⏹️ Pressione Ctrl+C para parar\n")
    else:
        print(f"🤖 Modo automático (GitHub Actions) - Executando uma consulta")
    
    contador = 0
    
    try:
        # Em modo automático, faz apenas 1 consulta
        if not interactive:
            dados = sensor.buscar_temperatura_umidade()
            
            if dados and dados["temperatura"] is not None:
                temperatura = dados["temperatura"]
                umidade = dados["umidade"]
                
                # Salvar no banco
                inserir_leitura(cidade, temperatura, umidade, dados["fonte"])
                
                # Processar análise
                media = analisador.processar_dados(temperatura, umidade)
                
                if media:
                    print(f"📈 Média últimas 5 leituras: {media:.1f}°C")
                
                contador += 1
                print(f"✅ Coleta concluída! Total de consultas: {contador}")
            else:
                print("⚠️ Falha ao obter dados da API.")
            
            analisador.gerar_relatorio()
            return
        
        # Modo interativo - loop contínuo
        while True:
            dados = sensor.buscar_temperatura_umidade()
            
            if dados and dados["temperatura"] is not None:
                temperatura = dados["temperatura"]
                umidade = dados["umidade"]
                
                # Salvar no banco
                inserir_leitura(cidade, temperatura, umidade, dados["fonte"])
                
                # Processar análise
                media = analisador.processar_dados(temperatura, umidade)
                
                if media:
                    print(f"📈 Média últimas 5 leituras: {media:.1f}°C")
                
                contador += 1
                
                if contador % 5 == 0:
                    print(f"\n📊 Status: {contador} consultas realizadas\n")
            else:
                print("⚠️ Falha ao obter dados da API. Tentando novamente...")
            
            time.sleep(60)
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*50}")
        print("🛑 SISTEMA FINALIZADO")
        print(f"{'='*50}")
        print(f"📊 Total de consultas nesta sessão: {contador}")
        analisador.gerar_relatorio()
        print(f"\n📍 Dados salvos para cidade: {cidade}")
        print("💾 Os dados permanecem no banco para consulta na dashboard")

def main():
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Coletor de dados climáticos IoT')
    parser.add_argument('--non-interactive', action='store_true', 
                        help='Executa em modo não interativo (para GitHub Actions)')
    parser.add_argument('--cidade', type=str, default="São Paulo",
                        help='Cidade para monitorar (ex: "São Paulo")')
    
    args = parser.parse_args()
    
    # Executar o sistema
    simular_sistema(
        cidade_automatica=args.cidade,
        interactive=not args.non_interactive
    )

if __name__ == "__main__":
    main()