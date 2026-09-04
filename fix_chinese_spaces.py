import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Pattern: Chinese char + space + Chinese char (this should not exist)
chinese_space_chinese = re.compile(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])')

issues = []
for i, q in enumerate(data):
    # Check question
    text = q['question']
    matches = chinese_space_chinese.findall(text)
    if matches:
        issues.append((i+1, 'question', text, matches))
    
    # Check options
    for k, v in q['options'].items():
        matches = chinese_space_chinese.findall(v)
        if matches:
            issues.append((i+1, f'option_{k}', v, matches))
    
    # Check explanation
    exp = q['explanation']
    matches = chinese_space_chinese.findall(exp)
    if matches:
        issues.append((i+1, 'explanation', exp, matches))

print(f"Found {len(issues)} instances of Chinese-char-space-Chinese-char:")
for qnum, field, text, matches in issues:
    print(f"\nQ{qnum} {field}: {text[:100]}")
    print(f"  Matches: {matches}")

# Fix all
fixed_count = 0
for q in data:
    # Fix question
    original = q['question']
    fixed = chinese_space_chinese.sub(r'\1\2', original)
    if fixed != original:
        q['question'] = fixed
        fixed_count += 1
    
    # Fix options
    for k, v in q['options'].items():
        fixed = chinese_space_chinese.sub(r'\1\2', v)
        if fixed != v:
            q['options'][k] = fixed
            fixed_count += 1
    
    # Fix explanation
    original = q['explanation']
    fixed = chinese_space_chinese.sub(r'\1\2', original)
    if fixed != original:
        q['explanation'] = fixed
        fixed_count += 1

print(f"\nFixed {fixed_count} fields")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("Written to", path)
