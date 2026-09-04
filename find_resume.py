import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Search for 简历 or 筛选 in questions and explanations
for i, q in enumerate(data):
    text = q.get('question', '') + ' ' + q.get('explanation', '')
    if '简历' in text or '筛选' in text or '高管' in text or '女性' in text:
        print(f"\n=== Q{i+1} (index {i}) ===")
        print(f"Question: {q['question'][:200]}")
        print(f"Answer: {q['answer']}")
        print(f"Explanation: {q['explanation'][:300]}")
        print("---")

# Also search for 社会不公平 or 自动化与规模化
print("\n=== Search for 社会不公平 ===")
for i, q in enumerate(data):
    text = q.get('question', '') + ' ' + q.get('explanation', '')
    if '社会不公平' in text or '自动化与规模化' in text:
        print(f"Q{i+1}: found in question={('社会不公平' in q['question'])}, explanation={('社会不公平' in q['explanation'])}")
