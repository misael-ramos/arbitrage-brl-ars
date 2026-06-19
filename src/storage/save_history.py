import json
import boto3
from datetime import datetime, timezone
from config.settings import AWS_BUCKET_NAME, AWS_REGION, S3_HISTORY_PREFIX


def save_to_s3(data: dict) -> bool:
    """Salva o snapshot de arbitragem no S3 particionado por data e hora."""
    try:
        s3 = boto3.client("s3", region_name=AWS_REGION)
        now = datetime.now(timezone.utc)

        date_str = now.strftime("%Y-%m-%d")
        hour_str = now.strftime("%H")
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")

        s3_key = f"{S3_HISTORY_PREFIX}/date={date_str}/hour={hour_str}/{timestamp_str}.json"

        s3.put_object(
            Bucket=AWS_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(data, ensure_ascii=False).encode("utf-8"),
            ContentType="application/json",
        )
        print(f"Histórico salvo em: s3://{AWS_BUCKET_NAME}/{s3_key}")
        return True
    except Exception as e:
        print(f"Erro ao salvar no S3: {e}")
        return False


def load_today_history() -> list[dict]:
    """Carrega todos os snapshots do dia atual do S3."""
    try:
        s3 = boto3.client("s3", region_name=AWS_REGION)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        prefix = f"{S3_HISTORY_PREFIX}/date={today}/"

        response = s3.list_objects_v2(Bucket=AWS_BUCKET_NAME, Prefix=prefix)
        objects = response.get("Contents", [])

        history = []
        for obj in sorted(objects, key=lambda x: x["Key"]):
            body = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=obj["Key"])
            record = json.loads(body["Body"].read().decode("utf-8"))
            history.append(record)

        return history
    except Exception as e:
        print(f"Erro ao carregar histórico: {e}")
        return []
