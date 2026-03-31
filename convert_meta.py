import pandas as pd
import json

base_dir = "datasets/airoa-org/airoa-moma/meta"

print("--- 1. Converting tasks.parquet ---")
df_tasks = pd.read_parquet(f"{base_dir}/tasks.parquet")
print(f"🔍 Found columns: {df_tasks.columns.tolist()}")

valid_tasks = []
for idx, row in df_tasks.iterrows():
    # task_indexを取得（存在しなければ行番号）
    t_idx = row['task_index'] if 'task_index' in df_tasks.columns else idx
    
    # task（言語指示のテキスト）を取得
    t_text = "Unknown Task"
    for col in df_tasks.columns:
        if col != 'task_index':
            val = row[col]
            # NumPy配列やリストの中に入っている場合は最初の要素を取り出す
            if isinstance(val, (list, tuple)) and len(val) > 0:
                t_text = str(val[0])
            else:
                t_text = str(val)
            break # task_index以外の最初の列をタスク名として採用
            
    # LeRobotが求める完璧な辞書型を作成
    valid_tasks.append({"task_index": int(t_idx), "task": t_text})

# 手動で綺麗なJSONLとして書き込み
with open(f"{base_dir}/tasks.jsonl", "w", encoding="utf-8") as f:
    for t in valid_tasks:
        f.write(json.dumps(t) + "\n")
        
print(f"✅ Created clean tasks.jsonl. Example of first line: {valid_tasks[0]}")

print("\n--- 2. Converting episodes.parquet ---")
df_ep = pd.read_parquet(f"{base_dir}/episodes/chunk-000/file-000.parquet")
df_ep.to_json(f"{base_dir}/episodes.jsonl", orient="records", lines=True)

print("✅ 究極版の変換が完了しました！")
