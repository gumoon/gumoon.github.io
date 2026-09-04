import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Check Q28
q28 = data[27]
print("=== Q28 ===")
print(f"Question: {q28['question']}")
print(f"Answer: {q28['answer']}")
print(f"Options: {q28['options']}")
print(f"Explanation:\n{q28['explanation']}")
print("\n" + "="*50)

# Also check around Q28 for context
for i in range(26, 30):
    if i < len(data):
        print(f"\nQ{i+1}: {data[i]['question'][:60]}...")
        print(f"  Answer: {data[i]['answer']}, Options: {list(data[i]['options'].keys())}")
