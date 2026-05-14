# database.py
import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'iot_data.db'

def criar_tabela():
    """Cria a tabela de leituras se não existir"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            localizacao TEXT,
            temperatura REAL,
            umidade INTEGER,
            fonte TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Tabela criada/verificada com sucesso!")

def inserir_leitura(localizacao, temperatura, umidade, fonte="API"):
    """Insere uma nova leitura no banco"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute('''
        INSERT INTO leituras (timestamp, localizacao, temperatura, umidade, fonte)
        VALUES (?, ?, ?, ?, ?)
    ''', (now, localizacao, temperatura, umidade, fonte))
    
    conn.commit()
    conn.close()
    print(f"✅ Leitura inserida: {localizacao} -> {temperatura}°C, {umidade}%")

def limpar_dados_antigos():
    """Remove dados com mais de 30 dias"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    data_limite = (datetime.now() - timedelta(days=30)).isoformat()
    
    cursor.execute('''
        DELETE FROM leituras 
        WHERE timestamp < ?
    ''', (data_limite,))
    
    quantidade = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"🗑️ Removidas {quantidade} leituras antigas (>30 dias)")
    return quantidade

def buscar_todas_leituras():
    """Retorna todas as leituras do banco"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, localizacao, temperatura, umidade, fonte 
        FROM leituras 
        ORDER BY timestamp DESC
    ''')
    
    dados = cursor.fetchall()
    conn.close()
    return dados

def listar_locais():
    """Retorna lista de todas as localizações distintas no banco"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT localizacao FROM leituras
    ''')
    
    locais = [row[0] for row in cursor.fetchall()]
    conn.close()
    return locais

def buscar_leituras_por_local(localizacao, limite=100):
    """Retorna leituras filtradas por localização"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, localizacao, temperatura, umidade, fonte 
        FROM leituras 
        WHERE localizacao = ?
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (localizacao, limite))
    
    dados = cursor.fetchall()
    conn.close()
    return dados

if __name__ == "__main__":
    criar_tabela()
    limpar_dados_antigos()
    print("✅ Database module ready!")
    print(f"📊 Locais encontrados: {listar_locais()}")