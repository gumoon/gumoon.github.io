import json, re

with open("/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js", "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Search for questions related to specific topics
searches = [
    ("参数量计算", ["参数量", "参数计算", "可训练参数"]),
    ("训练显存", ["显存", "前向", "反向", "优化器状态"]),
    ("自注意力复杂度", ["复杂度", "乘加运算"]),
]

for label, keywords in searches:
    print(f"\n=== {label} ===")
    for i, q in enumerate(data):
        found = False
        for kw in keywords:
            if kw in q['question']:
                found = True
                break
        if found:
            print(f"Q{i+1}: {q['question'][:60]}...")
            print(f"  Category: {q['category']}")
            print(f"  Answer: {q['answer']}")
            print(f"  Options: {list(q['options'].keys())}")

# Also print all "预训练技术" category questions
print("\n=== All 预训练技术 questions ===")
for i, q in enumerate(data):
    if q['category'] == '预训练技术':
        print(f"Q{i+1}: {q['question'][:80]}...")
        print(f"  Options: {list(q['options'].keys())} -> Answer: {q['answer']}")
