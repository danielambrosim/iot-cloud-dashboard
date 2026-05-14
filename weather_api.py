# weather_api.py
import requests
from datetime import datetime
import time

class WeatherAPISensor:
    def __init__(self, cidade, latitude, longitude):
        self.cidade = cidade
        self.latitude = latitude
        self.longitude = longitude
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def buscar_temperatura_umidade(self):
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current_weather": "true",
            "hourly": "temperature_2m,relativehumidity_2m",
            "timezone": "auto",
            "forecast_days": 1
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            dados = response.json()
            temperatura = dados.get("current_weather", {}).get("temperature")
            
            hourly_umidade = dados.get("hourly", {}).get("relativehumidity_2m", [])
            umidade = hourly_umidade[-1] if hourly_umidade else None
            
            return {
                "temperatura": temperatura,
                "umidade": umidade,
                "timestamp": datetime.now().isoformat(),
                "cidade": self.cidade,
                "fonte": "Open-Meteo API"
            }
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None

# Lista de cidades para monitoramento
CIDADES_MONITORADAS = {
    "São Paulo": {"lat": -23.5505, "lon": -46.6333},
    "Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729},
    "Belo Horizonte": {"lat": -19.9167, "lon": -43.9346},
    "Curitiba": {"lat": -25.4284, "lon": -49.2733},
    "Porto Alegre": {"lat": -30.0346, "lon": -51.2177}
}

def coletar_todas_cidades():
    """Coleta dados de todas as cidades monitoradas"""
    resultados = []
    for cidade, coords in CIDADES_MONITORADAS.items():
        sensor = WeatherAPISensor(cidade, coords["lat"], coords["lon"])
        dados = sensor.buscar_temperatura_umidade()
        if dados:
            resultados.append(dados)
            print(f"✅ {cidade}: {dados['temperatura']}°C, {dados['umidade']}%")
        else:
            print(f"❌ Falha ao coletar {cidade}")
        time.sleep(1)
    return resultados

def listar_cidades_disponiveis():
    return list(CIDADES_MONITORADAS.keys())