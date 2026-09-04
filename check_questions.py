import json, re

with open("/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js", "r", encoding="utf-8") as f:
    content = f.read()

# Strip the JS prefix and trailing semicolon
json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

print(f"Total questions: {len(data)}")

targets = [8, 18, 19, 108]
for i in targets:
    q = data[i]
    print(f"\n=== Q{i+1} (index {i}) ===")
    print(f"Question: {q['question'][:100]}...")
    print(f"Category: {q['category']}")
    print(f"Answer: {q['answer']}")
    for k, v in q['options'].items():
        print(f"  {k}: {v}")

# Check for any other merged options patterns
print("\n\n=== Checking for merged options across all questions ===")
for i, q in enumerate(data):
    opts = q['options']
    for k, v in opts.items():
        for letter in ['A','B','C','D']:
            if letter != k:
                pattern = r'[\s。]\s*' + letter + r'[\.．]\s*'
                if re.search(pattern, v):
                    print(f"Q{i+1} option {k} may contain option {letter}: {v[:150]}")
                    break

# Check for missing options
print("\n=== Checking for missing options ===")
for i, q in enumerate(data):
    expected = ['A','B','C','D']
    missing = [l for l in expected if l not in q['options']]
    if missing:
        print(f"Q{i+1} missing options: {missing}")
