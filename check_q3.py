import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Check Q3 question text in detail
q3 = data[2]
print("=== Q3 question ===")
print(repr(q3['question']))
print("\n=== Display ===")
print(q3['question'])
