import pdfplumber

pdf_path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI人工智能/考证/LMCC/CCF大模型能力认证大纲.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue
        if "通信开销" in text and "Gradient Checkpointing" in text:
            print(f"\n=== Page {page_num + 1} ===")
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if "通信开销" in line:
                    start = max(0, i - 15)
                    end = min(len(lines), i + 25)
                    print('\n'.join(lines[start:end]))
                    print("---")
                    break
