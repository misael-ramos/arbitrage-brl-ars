# 💱 arbitrage-brl-ars

Dashboard de **arbitragem cambial em tempo real** entre Real Brasileiro (BRL) e Peso Argentino (ARS) via criptomoedas. Compara três rotas de conversão e indica qual oferece o melhor resultado para o usuário, com histórico horário armazenado em AWS S3.

---

## 🎯 Objetivo de negócio

O mercado cambial argentino opera com múltiplos câmbios simultâneos (oficial, blue, MEP, CCL). Brasileiros e argentinos que precisam converter BRL → ARS frequentemente obtêm resultados muito melhores passando por criptomoedas (USDT ou BTC) do que usando o câmbio oficial.

Este dashboard calcula as três rotas em tempo real e responde: **qual é a melhor forma de converter seus reais em pesos agora?**

| Rota | Fluxo | Característica |
|---|---|---|
| Via USDT | BRL → USDT → ARS (blue) | Mais líquida, spread menor |
| Via BTC | BRL → BTC → ARS (blue) | Varia com volatilidade do BTC |
| Câmbio direto | BRL → ARS (oficial) | Referência base — geralmente a pior |

---

## 💡 Decisões técnicas

| Decisão | Alternativa considerada | Justificativa |
|---|---|---|
| Flask em vez de FastAPI | FastAPI | Flask é suficiente para o volume; FastAPI adicionaria complexidade sem ganho real |
| Cache de 5 min em memória | Chamar API a cada request | APIs gratuitas têm rate limit — cache evita bloqueio por excesso de requisições |
| S3 para histórico horário | Banco de dados relacional | S3 + JSON é serverless e gratuito no free tier; não precisa de instância RDS |
| Cron local em vez de Lambda | AWS Lambda + EventBridge | Para uso pessoal, cron é suficiente; Lambda seria over-engineering no escopo atual |
| Bluelytics para dólar blue | Scraping de sites | Bluelytics é uma API pública gratuita com dados do mercado paralelo argentino |
| CoinGecko em vez de Binance | Binance API | Binance bloqueia IPs de servidores em nuvem (erro 451); CoinGecko não tem restrição geográfica |

---

## 🏗️ Arquitetura

```
CoinGecko API (USDT/BRL, BTC/BRL)
Bluelytics API (dólar blue ARS)    →  Python (calcula 3 rotas)  →  S3 (histórico horário JSON)
ExchangeRate API (BRL/ARS oficial)                               →  Flask (dashboard web)
                                                                 →  Cron (salva snapshot/hora)
```

**Fluxo de dados:**
1. `fetch_rates.py` — coleta cotações das 3 APIs
2. `arbitrage.py` — calcula resultado das 3 rotas para qualquer valor em BRL
3. `save_history.py` — persiste snapshot JSON no S3 particionado por data/hora
4. `app.py` — serve o dashboard Flask com cache de 5 minutos
5. `save_hourly.py` — chamado pelo cron a cada hora para salvar histórico

---

## 📊 Exemplo de resultado

Para **R$ 100,00** convertidos (dados reais):

```
Via USDT   →  31.240 ARS  (+4.2% vs câmbio direto)  ✅ MELHOR
Via BTC    →  30.890 ARS  (+2.8% vs câmbio direto)
Câmbio direto → 29.980 ARS  (referência)
```

O dashboard também exibe:
- Calculadora interativa para qualquer valor em BRL
- Gráfico de evolução das 3 rotas ao longo do dia
- Tabela com histórico horário e o vencedor de cada hora

---

## 🛠️ Stack

- **Python 3.11+** + **Flask** — backend e servidor web
- **boto3** — integração com AWS S3
- **Amazon S3** — armazenamento do histórico horário (JSON particionado)
- **CoinGecko API** — cotações USDT/BRL e BTC/BRL em tempo real
- **Bluelytics API** — cotação do dólar blue argentino
- **ExchangeRate API** — câmbio oficial BRL/ARS

---

## 🚀 Como executar

```bash
git clone https://github.com/misael-ramos/arbitrage-brl-ars.git
cd arbitrage-brl-ars
python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt
cp .env.example .env
# edite o .env com seu bucket S3
python3 run.py
# acesse http://localhost:5000
```

## ⏰ Salvar histórico automaticamente

```bash
# adiciona ao cron — salva snapshot no S3 a cada hora
(crontab -l 2>/dev/null; echo "0 * * * * cd /caminho/arbitrage-brl-ars && source venv/bin/activate && python3 save_hourly.py") | crontab -
```

---

## 📁 Estrutura

```
arbitrage-brl-ars/
├── config/
│   └── settings.py          # configurações centralizadas
├── src/
│   ├── collector/
│   │   └── fetch_rates.py   # coleta cotações das 3 APIs
│   ├── calculator/
│   │   └── arbitrage.py     # calcula as 3 rotas de conversão
│   ├── storage/
│   │   └── save_history.py  # lê e escreve histórico no S3
│   └── web/
│       ├── app.py           # servidor Flask com cache
│       └── templates/
│           └── index.html   # dashboard interativo
├── run.py                   # entry point do servidor web
└── save_hourly.py           # script chamado pelo cron
```

---

## 🔗 Projetos relacionados

- [crypto-pipeline](https://github.com/misael-ramos/crypto-pipeline) — ETL de preços de criptomoedas
- [crypto-dw](https://github.com/misael-ramos/crypto-dw) — Data Warehouse com Star Schema
- [crypto-seasonality-spark](https://github.com/misael-ramos/crypto-seasonality-spark) — análise histórica com PySpark
- [crypto-news-streaming](https://github.com/misael-ramos/crypto-news-streaming) — streaming de sentimento com Kafka
