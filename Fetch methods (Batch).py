import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os

# ---------- 参数部分 （新手只需修改这里）----------
search_query = "metformin and cancer cells"   # 请输入搜索关键词
max_results = 10                              # 请输入抓取篇数
save_path = r"E:\PHD WORK\PHD\Articles\metformin_methods_auto.csv" #请输入输出路径和输出文件名（csv格式）
keywords = ['method', 'protocol', 'experimental', 'materials'] # Methods 标题关键词（一般不用改）
# 目标抓取关键词（核心参数），如需多个关键词，用|分隔如需多个关键词，请使用正则OR逻辑，例如: r'\b(metformin|rapamycin|cisplatin)\b'；如需同时匹配单复数（如 cell / cells），可在词尾加?
extract_targets = {
    "metformin": r"\bmetformin\b",
    "cells": r"\b(cells?|cell lines?)\b"
}
# ------------------------------

# 自动创建保存目录
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# ---------- Step 1：通过 Europe PMC 检索 PMC ID ----------
print(f"🔍 正在检索文献：{search_query}")

search_url = (
    f"https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    f"?query={search_query}&resultType=core&format=json&pageSize={max_results}"
)
res = requests.get(search_url, timeout=20)
data = res.json()

pmc_ids = []
for hit in data.get("resultList", {}).get("result", []):
    if "pmcid" in hit:
        pmc_ids.append(hit["pmcid"])

if not pmc_ids:
    print("⚠️ 未检索到可用的 PMC 文献。请更换关键词。")
    exit()

print(f"✅ 共找到 {len(pmc_ids)} 篇文献：{pmc_ids}")

# ---------- Step 2：抓取每篇Methods及目标段落 ----------
split_sent_regex = re.compile(r'(?<=[\.\?\!\;\n])\s+')
results = []

for pmc_id in pmc_ids:
    print(f"\n=== 正在处理 {pmc_id} ===")
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc_id}/fullTextXML"

    try:
        res = requests.get(url, timeout=20)
        res.encoding = 'utf-8'


        def parse_xml_with_fallback(xml_text):
            #优先使用 lxml-xml 解析 PMC XML，若不可用则自动退回到 html.parser（保证可运行）#
            try:
                return BeautifulSoup(xml_text, 'lxml-xml')
            except Exception:
                print("⚠️ 未检测到 lxml-xml，尝试使用 html.parser 解析（兼容模式）")
                return BeautifulSoup(xml_text, 'html.parser')

        soup = parse_xml_with_fallback(res.text)
        title_tag = soup.find('article-title')
        title = title_tag.get_text(strip=True) if title_tag else "No title"

        body = soup.find('body')

        # 为每个关键词准备一个结果容器
        extracted_paragraphs = {k: [] for k in extract_targets}
        all_method_paragraphs = []

        if body:
            for sec in body.find_all('sec'):
                sec_title = sec.find('title')
                if sec_title and any(
                        k in sec_title.get_text(strip=True).lower() for k in keywords
                ):
                    for p in sec.find_all('p'):
                        text = p.get_text(" ", strip=True)
                        all_method_paragraphs.append(text)

                        # 核心：自动匹配所有用户定义的关键词
                        for name, pattern in extract_targets.items():
                            if re.search(pattern, text, re.I):
                                extracted_paragraphs[name].append(text)

        # 构建输出行
        row = {
            "pmc_id": pmc_id,
            "title": title,
            "methods_text_full": " || ".join(all_method_paragraphs)
        }

        for name, paragraphs in extracted_paragraphs.items():
            row[f"methods_paragraphs_with_{name}"] = " || ".join(paragraphs)

        results.append(row)

        print(
            f"✅ {pmc_id} 完成 | "
            + " | ".join(
                f"{k}: {len(v)}" for k, v in extracted_paragraphs.items()
            )
        )

        time.sleep(1)

    except Exception as e:
        print(f"❌ {pmc_id} 出错：{e}")
        results.append({
            "pmc_id": pmc_id,
            "title": "Error",
            "methods_text_full": ""
        })
# ---------- Step 3：导出 ----------
df = pd.DataFrame(results)
df.to_csv(save_path, index=False, encoding="utf-8-sig")
print(f"\n🎉 批量抓取完成！结果已保存到：{save_path}")
