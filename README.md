# 这是一个基于 Europe PMC API 的 Python 脚本，用于：
1. 批量检索 PMC 可获取全文的论文
2. 自动定位 Methods 部分
3. 按关键词提取包含特定实验信息的“完整段落”
4. 将结果整理为 CSV，便于后续人工筛选或二次分析
# Overview
This is a Python script based on the Europe PMC API that is designed to:
1. Batch search PMC articles with full-text availability
2. Automatically locate the Methods / Materials and Methods sections
3. Extract complete paragraphs containing user-defined experimental keywords
4. Export results to CSV format for downstream manual screening or secondary analysis
   
# 本工具适用于：
1. 药物处理条件（如浓度、处理时间），细胞系等实验条件的快速调研
2. 系统性文献整理
3. 对无计算机背景用户友好，只需修改参数部分
   例: #---------- 参数部分 （只需修改这里）---------- 
      search_query = "metformin and cancer cells" # 请输入搜索关键词 
      max_results = 10 # 请输入抓取篇数 
      save_path = r"E:\PHD WORK\PHD\Articles\metformin_methods_auto.csv" #请输入输出路径和输出文件名（csv格式） 
      keywords = ['method', 'protocol', 'experimental', 'materials'] # Methods 标题关键词（一般不用改） 
      #目标抓取关键词（核心参数），如需多个关键词，用|分隔如需多个关键词，请使用正则OR逻辑，例如: r'\b(metformin|rapamycin|cisplatin)\b'；如需同时匹配单复数（如 cell / cells），可在词尾加? 
      extract_targets = { 
      "metformin": r"\bmetformin\b", 
      "cells": r"\b(cells?|cell lines?)\b" 
      } 
# Intended Use Cases
This tool is particularly useful for:
1. Rapid surveying of experimental conditions such as drug treatments (e.g. concentration, duration) and cell lines
2. Systematic literature collection and organization
3. Users without a programming background — only a small parameter section needs to be modified
   Example: #----------only the parameter section needs to be edited---------- 
      search_query = "metformin and cancer cells" # Keywords of literature topic 
      max_results = 10 # Number of articles to retrieve 
      save_path = r"E:\PHD WORK\PHD\Articles\metformin_methods_auto.csv" # Output file path 
      keywords = ['method', 'protocol', 'experimental', 'materials'] # Keywords used to identify Methods sections 
      #Target keywords to extract paragraphs of interest (core parameters)
      extract_targets = { 
      "metformin": r"\bmetformin\b", 
      "cells": r"\b(cells?|cell lines?)\b" 
      } 
# 功能概览
1. 支持自定义检索关键词
2. 支持自定义 抓取篇数
3. 自动识别Methods，Materials and Methods，Experimental Procedures 等常见标题
4. 同时输出含目标关键词的Methods选段与完整 Methods（按段落拼接）
# Features
1. Customizable literature search queries
2. User-defined number of articles to retrieve
3. Automatic recognition of common Methods section titles (e.g. Methods, Materials and Methods, Experimental Procedures)
4. Simultaneous output of: Methods paragraphs containing target keywords; The full Methods text, concatenated by paragraph
   
# 输出示例（CSV 列说明）
pmc_id：PMC 文献编号
title：文章标题
methods_paragraphs_with_key word：Methods 中包含关键词的段落
methods_text_full：完整 Methods（按段落拼接，不同段落之间使用||分隔）
# Output Description (CSV Columns)
pmc_id: PMC article identifier
title: Article title
methods_paragraphs_with_keyword: Methods paragraphs containing the target keyword(s)
methods_text_full: Full Methods section (paragraphs concatenated with || as separators)

# 工作环境准备
1. 安装 Python（推荐 3.8+）
确认命令行可用：python --version
2. 安装所需 Python 包
在命令行中执行：pip install requests beautifulsoup4 pandas
# Environment Setup
1. Install Python
Python 3.8 or higher is recommended.
Verify installation: python --version
2. Install Required Python Packages
Run the following command in your terminal: pip install requests beautifulsoup4 pandas

# 常见问题（FAQ）
1. 报错：PermissionError: [Errno 13] Permission denied
   原因：CSV 正在被 Excel 打开
   解决：关闭 Excel，重新运行脚本
2. 为什么会抓到 review？
   本工具不自动区分研究论文与综述
   建议：1. 提高 max_results；2. 在 CSV 中人工筛选（如通过title判断）
3. 为什么有些论文抓不到 Methods？
   可能原因：Methods 标题命名不规范；实验细节写在 Supplementary/Figure legend（本工具已尽量覆盖主流写法，但无法 100% 保证）
# Frequently Asked Questions (FAQ)
1. Error: PermissionError: [Errno 13] Permission denied
Cause: The output CSV file is currently open in Excel.
Solution: Close the CSV file and rerun the script.
2. Why are review articles included?
This tool does not automatically distinguish between original research articles and reviews.
Suggestions: Increase max_results; Manually filter results in the CSV file (e.g. by checking titles)
3. Why are Methods sections missing for some articles?
Possible reasons include: Non-standard naming of Methods sections; Experimental details placed in Supplementary Materials or figure legends.
This script attempts to cover common cases, but 100% coverage cannot be guaranteed.

# 免责声明
1. 本工具仅用于学术研究与文献整理
2. 本工具不替代人工阅读，仅用于缩小文献范围
3. 数据来源：Europe PMC（开放获取）
4. 请遵守原文献版权与引用规范
# Disclaimer
1. This tool is intended for academic research and literature organization only.
2. It does not replace manual reading, but helps narrow down relevant literature.
3. Data source: Europe PMC (open-access content).
4. Users are responsible for complying with copyright and citation requirements of the original publications.
