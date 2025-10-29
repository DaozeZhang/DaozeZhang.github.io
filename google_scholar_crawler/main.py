import os, json, time, random, datetime
import requests
from bs4 import BeautifulSoup

SCHOLAR_ID = os.environ["GOOGLE_SCHOLAR_ID"]
URL = f"https://scholar.google.com/citations?hl=en&user={SCHOLAR_ID}"

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
]

def fetch_citations(max_retries=4):
    for i in range(max_retries):
        try:
            headers = {"User-Agent": random.choice(UA_LIST)}
            r = requests.get(URL, headers=headers, timeout=15)  # 硬超时
            r.raise_for_status()
            # 简单的反爬页判断：如果被重定向/出现验证码，直接重试
            if "gs_md_c" in r.text and "Please show you're not a robot" in r.text:
                raise RuntimeError("Captcha page")
            soup = BeautifulSoup(r.text, "html.parser")
            # 引用量在“概览”右侧统计表的第一个 td.gsc_rsb_std
            td = soup.select_one("td.gsc_rsb_std")
            if not td:
                raise RuntimeError("citation cell not found")
            count = int(td.get_text(strip=True).replace(",", ""))
            return count
        except Exception as e:
            # 退避一点点再重试
            time.sleep(1.5 * (i + 1))
    raise RuntimeError("Failed to fetch citations after retries")

def main():
    citations = fetch_citations()
    data = {
        "updated": datetime.datetime.utcnow().isoformat() + "Z",
        "citedby": citations
    }
    os.makedirs("results", exist_ok=True)
    with open("results/gs_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
        json.dump({"schemaVersion":1,"label":"citations","message":str(citations)}, f)

if __name__ == "__main__":
    main()
