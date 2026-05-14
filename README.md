# Atividade 2: Dashboard IoT com Dados Reais e Deploy na Nuvem

## Sobre a Atividade

Agora que você já corrigiu o código da atividade anterior, é hora de **evoluir** o sistema!

Nesta atividade, você irá:

- 🌐 **Integrar com uma API real** de clima (Open-Meteo) - dados de temperatura e umidade **reais**
- 📊 **Criar uma dashboard interativa** usando Streamlit
- 🗄️ **Armazenar dados** em banco de dados SQLite
- ☁️ **Fazer deploy** da dashboard na nuvem (Streamlit Cloud)

O sistema deixará de ser uma simulação e se tornará um **monitoramento climático real**!

## Arquivos do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Código principal que busca dados da API e salva no banco |
| `weather_api.py` | Cliente para acessar a Open-Meteo API |
| `database.py` | Funções para gerenciar o banco SQLite |
| `dashboard.py` | Dashboard Streamlit com gráficos interativos |
| `requirements.txt` | Bibliotecas necessárias |

## Como executar localmente

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```
### 2. Executar o coletor de dados

```bash
python main.py
```
Este programa irá:

- Perguntar qual cidade você quer monitorar
- Buscar dados climáticos reais da API a cada 60 segundos
- Salvar os dados no banco SQLite
- Remover automaticamente dados com mais de 30 dias

### 3. Executar a dashboard (em outro terminal)

```bash
streamlit run dashboard.py
```
A dashboard abrirá no seu navegador em http://localhost:8501

## O que fazer

### Parte 1: Configurar e executar localmente

1. Clone o repositório com os arquivos fornecidos
2. Instale as dependências do `requirements.txt`
3. Execute o `main.py` e escolha uma cidade para monitorar
4. Execute o `dashboard.py` e explore os gráficos

### Parte 2: Fazer deploy na nuvem

1. Crie um repositório no GitHub
2. Envie todos os arquivos do projeto
3. Acesse [share.streamlit.io](https://share.streamlit.io)
4. Faça login com sua conta do GitHub
5. Clique em "New app" e selecione seu repositório
6. Configure:
   - **Branch:** `main`
   - **Main file path:** `dashboard.py`
7. Clique em "Deploy"

### Parte 3: Responder as questões

Após finalizar, responda:

1. O que mudou do código anterior (simulado) para este (com API real)?
2. Qual a função da função `limpar_dados_antigos()` e por que ela é importante?
3. O que acontece com os dados quando você faz deploy no Streamlit Cloud?
4. Como você poderia manter os dados mesmo após o deploy?

## Entrega

Envie no Google Classroom:

- Link do repositório GitHub com todos os arquivos
- Link da dashboard funcionando no Streamlit Cloud
- Respostas das questões em um arquivo `respostas.txt`

## Referências

- [Streamlit - Criando dashboards](https://docs.streamlit.io/)
- [Plotly - Gráficos interativos](https://plotly.com/python/)
- [Open-Meteo API - Dados climáticos gratuitos](https://open-meteo.com/)
- [SQLite com Python](https://docs.python.org/3/library/sqlite3.html)
- [Deploy no Streamlit Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)

## Dicas

> 💡 A API Open-Meteo é gratuita e não precisa de chave de acesso. Use-a com responsabilidade!

> 💡 O Streamlit Cloud tem armazenamento temporário. Seu banco SQLite será resetado quando o servidor reiniciar. Isso é normal para esta atividade.

> 💡 Execute `python database.py` sozinho para testar se o banco de dados está funcionando.

> 💡 Se aparecer erro de tabela, apague o arquivo `iot_data.db` e execute `python database.py` novamente.

## Desafio extra (opcional)

Implemente **uma das seguintes melhorias** na dashboard:

- Botão para **exportar** os dados para CSV
- **Alerta visual** quando temperatura > 30°C ou < 15°C
- **Seletor de período** (últimas 24h, 7 dias, 30 dias)
- **Previsão do tempo** para os próximos dias
