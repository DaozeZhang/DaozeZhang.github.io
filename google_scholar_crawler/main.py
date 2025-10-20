from scholarly import scholarly
import jsonpickle, json
from datetime import datetime
import os

author = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])

# 补充时间戳，并把 publications 转成 {author_pub_id: pub_obj} 的字典
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']: v for v in author['publications']}

# 输出到 results 目录
os.makedirs('results', exist_ok=True)
with open('results/gs_data.json', 'w', encoding='utf-8') as f:
    json.dump(author, f, ensure_ascii=False, indent=2)

# 生成 Shields.io endpoint 用的 JSON（徽章）
shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author['citedby']}",
}
with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
    json.dump(shieldio_data, f, ensure_ascii=False)
