from scholarly import scholarly, ProxyGenerator  # daoze modified
from scholarly.author_parser import AuthorParser
import json
from datetime import datetime
import logging
import os
import time

# 诊断：打开 scholarly 的 INFO 日志（每次请求的状态码 / 验证码 / 超时 / 异常原因）；secret 会被 GitHub Actions 自动打码
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
logging.getLogger('scholarly').setLevel(logging.INFO)

MAX_RETRIES = 3        # 最多重试 3 次
RETRY_DELAY = 180      # 每次失败后等待 3 分钟（180 秒）

def setup_proxy():
    """有 SCRAPER_API_KEY 就走 ScraperAPI 代理；没有就直连（GitHub runner 直连大概率被 Scholar 封）"""
    key = os.environ.get('SCRAPER_API_KEY')
    if not key:
        print("SCRAPER_API_KEY not set — connecting directly.")
        return
    pg = ProxyGenerator()
    if not pg.ScraperAPI(key):
        raise RuntimeError("ScraperAPI setup failed (invalid key or credits exhausted).")
    # 主/副代理都用 ScraperAPI；只传一个参数时 scholarly 会自动去试免费代理
    scholarly.use_proxy(pg, pg)
    print("Using ScraperAPI proxy.")

def fetch_author_data():
    """尝试抓取 Google Scholar 作者数据"""
    # 只请求 1 次 Scholar 主页（原 search_author_id + fill 会请求 2 次，ScraperAPI 每次 Google 请求 25 credits）
    # 不联网构造与 search_author_id 相同的初始 author 对象，再一次 fill 全部所需 sections，输出字段不变
    author = AuthorParser(None).get_author(os.environ['GOOGLE_SCHOLAR_ID'])
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    author['updated'] = str(datetime.now())
    author['publications'] = {v['author_pub_id']: v for v in author['publications']}
    return author

def main():
    setup_proxy()
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
