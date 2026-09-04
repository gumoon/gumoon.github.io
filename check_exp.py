import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Check Q53 explanation
q53 = data[52]
print("=== Q53 explanation ===")
print(repr(q53['explanation']))
print("\n=== Display ===")
print(q53['explanation'])
