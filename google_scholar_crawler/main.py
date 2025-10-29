from scholarly import scholarly
import json
from datetime import datetime
import os
import time

MAX_RETRIES = 3        # 最多重试 3 次
RETRY_DELAY = 180      # 每次失败后等待 3 分钟（180 秒）

def fetch_author_data():
    """尝试抓取 Google Scholar 作者数据"""
    author = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    author['updated'] = str(datetime.now())
    author['publications'] = {v['author_pub_id']: v for v in author['publications']}
    return author

def main():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Attempt {attempt}/{MAX_RETRIES} — fetching author data...")
            author = fetch_author_data()

            # 输出结果目录
            os.makedirs('results', exist_ok=True)
            with open('results/gs_data.json', 'w', encoding='utf-8') as f:
                json.dump(author, f, ensure_ascii=False, indent=2)

            # 生成 Shields.io JSON
            shieldio_data = {
                "schemaVersion": 1,
                "label": "citations",
                "message": f"{author['citedby']}",
            }
            with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
                json.dump(shieldio_data, f, ensure_ascii=False)

            print("✅ Successfully fetched and saved author data.")
            break  # 成功就退出循环

        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"⏳ Waiting {RETRY_DELAY / 60} minutes before retrying...")
                time.sleep(RETRY_DELAY)
            else:
                print("🚨 All attempts failed. Exiting.")
                raise  # 抛出最后一次异常让 CI 报错

if __name__ == "__main__":
    main()
