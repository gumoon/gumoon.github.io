import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Check specific suspicious explanations
suspicious = [34, 63, 70, 77, 83, 85, 86, 87, 88, 89, 90, 91, 92, 104, 107, 108]
for idx in suspicious:
    q = data[idx]
    exp = q['explanation']
    print(f"\n=== Q{idx+1} ===")
    print(f"Last 80 chars: {repr(exp[-80:])}")
