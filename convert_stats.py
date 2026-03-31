import pandas as pd
import json
import numpy as np

def make_serializable(val):
    if isinstance(val, np.ndarray):
        return make_serializable(val.tolist())
    elif isinstance(val, (list, tuple)):
        return [make_serializable(v) for v in val]
    elif isinstance(val, dict):
        return {k: make_serializable(v) for k, v in val.items()}
    elif isinstance(val, np.generic):
        return val.item()
    return val

base_dir = "datasets/airoa-org/airoa-moma/meta"
df = pd.read_parquet(f"{base_dir}/episodes/chunk-000/file-000.parquet")

print("--- Converting episodes_stats.jsonl ---")
with open(f"{base_dir}/episodes_stats.jsonl", "w", encoding="utf-8") as f:
    for idx, row in df.iterrows():
        # episode_indexの取得
        ep_idx = row["episode_index"]
        if isinstance(ep_idx, (list, tuple, np.ndarray)):
            ep_idx = ep_idx[0]
            
        stats_dict = {}
        for col in df.columns:
            if col.startswith("stats/"):
                parts = col.split("/")
                if len(parts) == 3:
                    _, feature, stat_name = parts
                    if feature not in stats_dict:
                        stats_dict[feature] = {}
                    
                    val = row[col]
                    stats_dict[feature][stat_name] = make_serializable(val)
                    
        item = {"episode_index": int(make_serializable(ep_idx)), "stats": stats_dict}
        f.write(json.dumps(item) + "\n")

print("✅ episodes_stats.jsonl の階層化変換が完了しました！")
