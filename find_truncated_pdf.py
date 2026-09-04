import pdfplumber, re

pdf_path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI人工智能/考证/LMCC/CCF大模型能力认证大纲.pdf"

targets = [
    ("下一个词元预测", ["下一个词元预测", "心训练任务"]),
    ("缓解大模型的幻觉", ["RAG", "外挂知识库"]),
    ("提示学习方法", ["提示学习方法", "预训练模型"]),
    ("评测公平性", ["评测公平性", "数据集"]),
]

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue
        for label, keywords in targets:
            found = any(kw in text for kw in keywords)
            if found:
                print(f"\n=== Page {page_num + 1} - {label} ===")
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if any(kw in line for kw in keywords):
                        start = max(0, i - 8)
                        end = min(len(lines), i + 20)
                        print('\n'.join(lines[start:end]))
                        print("---")
                        break
                break
