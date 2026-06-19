# Arbitragem BRL → ARS

Pipeline de arbitragem cambial em tempo real entre Real Brasileiro e Peso Argentino via criptomoedas.

## 🏗️ Arquitetura

```
Binance API (USDT/BRL, BTC/BRL)
Bluelytics API (Dólar blue ARS)     →  Python (calcula 3 rotas)  →  S3 (histórico horário)
ExchangeRate API (BRL/ARS oficial)                                →  Flask (dashboard web)
```

## 🛠️ Stack

- **Python 3.11+** + **Flask** — backend e servidor web
- **boto3** — integração com AWS S3
- **Amazon S3** — armazenamento do histórico horário
- **Binance API** — cotações USDT/BRL e BTC/BRL em tempo real
- **Bluelytics API** — cotação do dólar blue argentino
- **ExchangeRate API** — câmbio oficial BRL/ARS

## 🚀 Como executar

```bash
git clone https://github.com/seu-usuario/arbitrage-brl-ars.git
cd arbitrage-brl-ars
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha com seu bucket S3
python run.py          # acesse http://localhost:5000
```

## ⏰ Salvar histórico automaticamente (cron)

```bash
# salva snapshot no S3 a cada hora
0 * * * * cd /caminho/arbitrage-brl-ars && source venv/bin/activate && python save_hourly.py
```

## 📊 Rotas calculadas

| Rota | Fluxo | Vantagem |
|------|-------|----------|
| Via USDT | BRL → USDT → ARS (blue) | Spread menor, mais líquido |
| Via BTC | BRL → BTC → ARS (blue) | Varia com volatilidade do BTC |
| Câmbio direto | BRL → ARS (oficial) | Referência base |
