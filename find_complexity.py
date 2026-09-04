import pdfplumber

pdf_path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI人工智能/考证/LMCC/CCF大模型能力认证大纲.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue
        if "Decoder-only" in text or "乘加运算" in text or "Self-Attention" in text and "复杂度" in text:
            print(f"\n=== Page {page_num + 1} ===")
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if "Decoder-only" in line or "乘加运算" in line:
                    start = max(0, i - 15)
                    end = min(len(lines), i + 20)
                    print('\n'.join(lines[start:end]))
                    print("---")
                    break
