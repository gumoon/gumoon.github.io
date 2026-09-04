import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

q22 = data[21]
text = q22['question']
print("Q22 question chars:")
for i, c in enumerate(text[:30]):
    print(f"  [{i}] U+{ord(c):04X} = {repr(c)}")

print(f"\nFull repr: {repr(text)}")
