import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

for idx in [8, 51, 65, 98]:
    q = data[idx]
    print(f"Q{idx+1}: {repr(q['explanation'])}")
