import os, json, time, random, datetime, re
import requests
from bs4 import BeautifulSoup

SCHOLAR_ID = os.environ["GOOGLE_SCHOLAR_ID"].strip()
URL = f"https://scholar.google.com/citations?hl=en&user={SCHOLAR_ID}"

UA_POOL = [
    # 多几个常见 UA，降低被风控概率
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

def looks_like_captcha(text: str) -> bool:
    t = text.lower()
    # 学术验证码/人机校验的一些关键词（尽量少误报）
    return ("not a robot" in t) or ("detected unusual traffic" in t) or ("id=\"captcha\"" in t) or ("gs_captcha" in t)

def extract_citations(soup: BeautifulSoup) -> int:
    """
    尝试多种定位方式，防止结构轻微变化：
    1) 右侧统计表的第一个 td.gsc_rsb_std（通常是总 citations）
    2) 在右侧统计表里，找“Citations”的行，然后取同一行的数字单元格
    3) 兜底：在页面中搜索 “Citations” 附近的数字
    """
    # 1) 最常见
    td = soup.select_one("td.gsc_rsb_std")
    if td and td.get_text(strip=True):
        txt = td.get_text(strip=True).replace(",", "")
        if txt.isdigit():
            return int(txt)

    # 2) 根据表头匹配行
    for row in soup.select("table.gsc_rsb_st tbody tr"):
        cells = [c.get_text(strip=True) for c in row.select("td")]
        if len(cells) >= 2 and cells[0].lower().startswith("citations"):
            num = re.sub(r"[^\d]", "", cells[1])
            if num:
                return int(num)

    # 3) 兜底在整页搜
    m = re.search(r"Citations[^0-9]{0,20}([0-9][0-9,]*)", soup.get_text(" ", strip=True), flags=re.I)
    if m:
        return int(m.group(1).replace(",", ""))

    raise RuntimeError("citation cell not found")

def fetch_citations(max_retries=6):
    last_err = None
    sess = requests.Session()
    for i in range(max_retries):
        try:
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://scholar.google.com/",
                "Cache-Control": "no-cache",
            }
            # 15s 硬超时；有些 runner 网络波动
            r = sess.get(URL, headers=headers, timeout=15)
            status = r.status_code
            if status != 200:
                raise RuntimeError(f"http {status}")

            text = r.text
            if looks_like_captcha(text):
                raise RuntimeError("captcha page")

            soup = BeautifulSoup(text, "html.parser")
            return extract_citations(soup)

        except Exception as e:
            last_err = e
            # 打一点调试信息，方便在 Actions 日志里定位
            print(f"[attempt {i+1}] fetch failed: {e}")
            # 退避 + 抖动
            time.sleep(1.2 * (i + 1) + random.random())

    # 输出部分页面片段，方便排查（不会泄露隐私）
    try:
        snippet = (text[:800] if 'text' in locals() else '')
        print("---- PAGE SNIPPET START ----")
        print(snippet)
        print("---- PAGE SNIPPET END ----")
    except Exception:
        pass

    raise RuntimeError(f"Failed after {max_retries} retries: {last_err}")

def main():
    citedby = fetch_citations()
    data = {
        "updated": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "citedby": citedby,
    }
    os.makedirs("results", exist_ok=True)
    with open("results/gs_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
        json.dump({"schemaVersion": 1, "label": "citations", "message": str(citedby)}, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
