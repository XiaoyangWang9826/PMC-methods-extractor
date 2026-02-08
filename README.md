# 这是一个基于 Europe PMC API 的 Python 脚本，用于：
1. 批量检索 PMC 可获取全文的论文
2. 自动定位 Methods 部分
3. 按关键词提取包含特定实验信息的“完整段落”
4. 将结果整理为 CSV，便于后续人工筛选或二次分析

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

# 功能概览
1. 支持自定义检索关键词
2. 支持自定义 抓取篇数
3. 自动识别Methods，Materials and Methods，Experimental Procedures 等常见标题
4. 同时输出含目标关键词的Methods选段与完整 Methods（按段落拼接）
   
# 输出示例（CSV 列说明）
pmc_id：PMC 文献编号
title：文章标题
methods_paragraphs_with_key word：Methods 中包含关键词的段落
methods_text_full：完整 Methods（按段落拼接，不同段落之间使用||分隔）

# 工作环境准备
1. 安装 Python（推荐 3.8+）
确认命令行可用：python --version
2. 安装所需 Python 包
在命令行中执行：pip install requests beautifulsoup4 pandas

# 常见问题（FAQ）
1. 报错：PermissionError: [Errno 13] Permission denied
   原因：CSV 正在被 Excel 打开
   解决：关闭 Excel，重新运行脚本

2. 为什么会抓到 review？
   本工具不自动区分研究论文与综述
   建议：1. 提高 max_results；2. 在 CSV 中人工筛选（如通过title判断）

3. 为什么有些论文抓不到 Methods？
   可能原因：Methods 标题命名不规范；实验细节写在 Supplementary/Figure legend（本工具已尽量覆盖主流写法，但无法 100% 保证）
   
# 免责声明
1. 本工具仅用于学术研究与文献整理
2. 本工具不替代人工阅读，仅用于缩小文献范围
3. 数据来源：Europe PMC（开放获取）
4. 请遵守原文献版权与引用规范
