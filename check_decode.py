import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Find the question about 解码方法
for i, q in enumerate(data):
    if '解码方法' in q['question'] or '贪心搜索' in q['question']:
        print(f"=== Q{i+1} ===")
        print(f"Question: {q['question']}")
        print(f"Answer: {q['answer']}")
        for k, v in q['options'].items():
            print(f"  {k} repr: {repr(v)}")
        print(f"\nExplanation: {q['explanation'][:200]}")
        break
