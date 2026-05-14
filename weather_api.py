# weather_api.py
import requests
from datetime import datetime, timedelta
import time

class WeatherAPISensor:
    """Sensor que busca dados climáticos reais da API Open-Meteo"""
    
    def __init__(self, cidade, latitude, longitude):
        self.cidade = cidade
        self.latitude = latitude
        self.longitude = longitude
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        print(f"✅ Sensor configurado para: {cidade} ({latitude}, {longitude})")
    
    def buscar_temperatura_umidade(self):
        """Busca dados climáticos atuais da API"""
        
        # Parâmetros da requisição
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current_weather": "true",
            "hourly": "temperature_2m,relativehumidity_2m",
            "timezone": "auto",
            "forecast_days": 1
        }
        
        try:
            # Faz a requisição para a API
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Levanta erro se status não for 200
            
            dados = response.json()
            
            # Extrai os dados atuais
            temperatura = dados.get("current_weather", {}).get("temperature")
            
            # Para umidade, precisamos pegar do hourly
            hourly_times = dados.get("hourly", {}).get("time", [])
            hourly_umidade = dados.get("hourly", {}).get("relativehumidity_2m", [])
            
            # Encontra a leitura mais recente
            if hourly_times and hourly_umidade:
                umidade = hourly_umidade[-1]
            else:
                umidade = None
            
            return {
                "temperatura": temperatura,
                "umidade": umidade,
                "timestamp": datetime.now().isoformat(),
                "cidade": self.cidade,
                "fonte": "Open-Meteo API"
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao buscar dados da API: {e}")
            return None
        except KeyError as e:
            print(f"❌ Erro ao processar dados: {e}")
            return None

# Dicionário de cidades brasileiras com coordenadas
CIDADES_BRASIL = {
    "são paulo": {"lat": -23.5505, "lon": -46.6333},
    "rio de janeiro": {"lat": -22.9068, "lon": -43.1729},
    "belo horizonte": {"lat": -19.9167, "lon": -43.9346},
    "brasília": {"lat": -15.8267, "lon": -47.9218},
    "salvador": {"lat": -12.9714, "lon": -38.5014},
    "fortaleza": {"lat": -3.7319, "lon": -38.5267},
    "curitiba": {"lat": -25.4284, "lon": -49.2733},
    "manaus": {"lat": -3.1190, "lon": -60.0217},
    "recife": {"lat": -8.0476, "lon": -34.8770},
    "porto alegre": {"lat": -30.0346, "lon": -51.2177}
}

# weather_api.py (parte final - substitua as funções escolher_cidade e criar_cidade_personalizada)

def escolher_cidade(interactive=True, cidade_automatica=None):
    """Permite ao usuário escolher uma cidade ou usa modo automático"""
    
    if not interactive and cidade_automatica:
        # Modo automático (GitHub Actions)
        cidade = cidade_automatica.lower()
        if cidade in CIDADES_BRASIL:
            coords = CIDADES_BRASIL[cidade]
            print(f"🤖 Modo automático - Cidade selecionada: {cidade.title()}")
            return cidade.title(), coords["lat"], coords["lon"]
        else:
            # Cidade não encontrada, usar São Paulo como padrão
            print(f"⚠️ Cidade '{cidade_automatica}' não encontrada. Usando São Paulo como padrão.")
            return "São Paulo", CIDADES_BRASIL["são paulo"]["lat"], CIDADES_BRASIL["são paulo"]["lon"]
    
    # Modo interativo (quando roda no computador local)
    print("\n" + "="*50)
    print("📍 SELECIONE UMA CIDADE PARA MONITORAR O CLIMA")
    print("="*50)
    
    print("\nCidades disponíveis:")
    cidades_lista = list(CIDADES_BRASIL.keys())
    for i, cidade in enumerate(cidades_lista, 1):
        print(f"   {i}. {cidade.title()}")
    print(f"   {len(cidades_lista)+1}. Digitar outra cidade")
    
    try:
        opcao = int(input("\nEscolha uma opção (número): "))
        if 1 <= opcao <= len(cidades_lista):
            cidade = cidades_lista[opcao-1]
            coords = CIDADES_BRASIL[cidade]
            return cidade.title(), coords["lat"], coords["lon"]
        else:
            return criar_cidade_personalizada()
    except ValueError:
        return criar_cidade_personalizada()

def criar_cidade_personalizada():
    """Permite criar uma cidade personalizada (apenas modo interativo)"""
    print("\n🏙️ CIDADE PERSONALIZADA")
    cidade = input("Digite o nome da cidade: ").strip()
    if not cidade:
        cidade = "São Paulo"
        print(f"⚠️ Usando cidade padrão: {cidade}")
    
    print(f"📍 Buscando coordenadas para {cidade}...")
    lat = float(input("Digite a latitude (ex: -23.5505): "))
    lon = float(input("Digite a longitude (ex: -46.6333): "))
    
    return cidade.title(), lat, lon

if __name__ == "__main__":
    # Teste rápido
    cidade, lat, lon = escolher_cidade()
    sensor = WeatherAPISensor(cidade, lat, lon)
    dados = sensor.buscar_temperatura_umidade()
    
    if dados:
        print(f"\n🌡️ Temperatura atual: {dados['temperatura']}°C")
        print(f"💧 Umidade atual: {dados['umidade']}%")
        print(f"🕐 Atualizado: {dados['timestamp']}")
        print(f"📍 Cidade: {dados['cidade']}")
        print(f"🔗 Fonte: {dados['fonte']}")