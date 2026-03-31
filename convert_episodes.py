import pandas as pd

base_dir = "datasets/airoa-org/airoa-moma/meta"

print("--- Converting episodes.parquet ---")
parquet_path = f"{base_dir}/episodes/chunk-000/file-000.parquet"
jsonl_path = f"{base_dir}/episodes.jsonl"

# Parquetを読み込んでJSONLとして保存
df_ep = pd.read_parquet(parquet_path)
df_ep.to_json(jsonl_path, orient="records", lines=True)

print("✅ episodes.jsonl の変換が完了しました！")
