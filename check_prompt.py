import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Find the prompt learning question
for i, q in enumerate(data):
    if '提示学习' in q['question'] and '哪项最适合' in q['question']:
        print(f"=== Q{i+1} ===")
        print(f"Question: {q['question']}")
        print(f"Answer: {q['answer']}")
        print(f"Options: {q['options']}")
        print(f"\nExplanation repr:\n{repr(q['explanation'])}")
        print(f"\nExplanation display:\n{q['explanation']}")
        break
