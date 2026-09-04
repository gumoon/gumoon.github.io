import pdfplumber

pdf_path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI人工智能/考证/LMCC/CCF大模型能力认证大纲.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Look for the relevant questions - they're likely in the appendix with sample questions
    # Check all pages for "下一个词元预测", "参数量", "显存", "偏见"
    targets = ["下一个词元预测", "参数量", "训练显存", "单次\n前向", "偏见"]
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue
        for t in targets:
            if t in text:
                print(f"\n=== Page {page_num + 1} contains '{t}' ===")
                # Print surrounding context
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if t in line:
                        start = max(0, i - 8)
                        end = min(len(lines), i + 12)
                        print('\n'.join(lines[start:end]))
                        print("---")
                        break
                break
