import sqlite3
from datetime import datetime, timedelta
import random

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

def adicionar_dados_exemplo():
    """Adiciona dados de exemplo para demonstração"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Verificar se já existem dados
    cursor.execute("SELECT COUNT(*) FROM leituras")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"📊 Banco já possui {count} registros. Pulando dados de exemplo.")
        conn.close()
        return
    
    print("📝 Adicionando dados de exemplo...")
    
    cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre"]
    
    for i in range(30):  # 30 dias de dados
        data = (datetime.now() - timedelta(days=i)).isoformat()
        for cidade in cidades:
            # Variação realista de temperatura por cidade
            if cidade == "São Paulo":
                temp_base = 22
            elif cidade == "Rio de Janeiro":
                temp_base = 26
            elif cidade == "Belo Horizonte":
                temp_base = 24
            elif cidade == "Curitiba":
                temp_base = 18
            else:  # Porto Alegre
                temp_base = 23
            
            # Adiciona variação diária
            temp = round(temp_base + random.uniform(-3, 5) + (i % 10) / 5, 1)
            umidade = random.randint(50, 85)
            
            cursor.execute('''
                INSERT INTO leituras (timestamp, localizacao, temperatura, umidade, fonte)
                VALUES (?, ?, ?, ?, ?)
            ''', (data, cidade, temp, umidade, "Dados de Exemplo"))
    
    conn.commit()
    conn.close()
    print("✅ Dados de exemplo adicionados com sucesso!")

def listar_locais():
    """Retorna lista de todas as localizações distintas no banco"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT DISTINCT localizacao FROM leituras
        ''')
        
        locais = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Se não houver dados, adiciona dados de exemplo
        if not locais:
            adicionar_dados_exemplo()
            return listar_locais()  # Recursão para pegar os novos dados
        
        return locais
        
    except sqlite3.OperationalError as e:
        # Tabela não existe - criar e adicionar dados
        conn.close()
        criar_tabela()
        adicionar_dados_exemplo()
        return listar_locais()

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

def get_estatisticas():
    """Retorna estatísticas do banco"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            MIN(temperatura) as min_temp,
            MAX(temperatura) as max_temp,
            AVG(temperatura) as avg_temp,
            COUNT(DISTINCT localizacao) as total_locais
        FROM leituras
    ''')
    
    stats = cursor.fetchone()
    conn.close()
    
    return {
        'total': stats[0],
        'min_temp': round(stats[1], 1) if stats[1] else 0,
        'max_temp': round(stats[2], 1) if stats[2] else 0,
        'avg_temp': round(stats[3], 1) if stats[3] else 0,
        'total_locais': stats[4]
    }

if __name__ == "__main__":
    criar_tabela()
    adicionar_dados_exemplo()
    limpar_dados_antigos()
    print(f"\n📊 Estatísticas:")
    stats = get_estatisticas()
    print(f"   Total de registros: {stats['total']}")
    print(f"   Locais monitorados: {stats['total_locais']}")
    print(f"   Temperatura média: {stats['avg_temp']}°C")
    print(f"   Locais: {listar_locais()}")