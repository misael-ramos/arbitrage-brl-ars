import os
from dotenv import load_dotenv

load_dotenv()

AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION      = os.getenv("AWS_REGION", "us-east-1")

S3_HISTORY_PREFIX = "history"

#BINANCE_URL      = "https://api.binance.com/api/v3/ticker/price"
BLUELYTICS_URL   = "https://api.bluelytics.com.ar/v2/latest"
EXCHANGERATE_URL = "https://api.exchangerate-api.com/v4/latest/BRL"