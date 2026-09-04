import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

def remove_chinese_spaces(text):
    """Remove spaces between Chinese characters, handling overlapping matches"""
    pattern = re.compile(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])')
    while True:
        new_text = pattern.sub(r'\1\2', text)
        if new_text == text:
            break
        text = new_text
    return text

# Apply to all fields
fixed_count = 0
for q in data:
    # Fix question
    original = q['question']
    fixed = remove_chinese_spaces(original)
    if fixed != original:
        q['question'] = fixed
        fixed_count += 1
    
    # Fix options
    for k, v in q['options'].items():
        fixed = remove_chinese_spaces(v)
        if fixed != v:
            q['options'][k] = fixed
            fixed_count += 1
    
    # Fix explanation
    original = q['explanation']
    fixed = remove_chinese_spaces(original)
    if fixed != original:
        q['explanation'] = fixed
        fixed_count += 1

print(f"Fixed {fixed_count} fields with iterative Chinese-space removal")

# Verify Q22
q22 = data[21]
print(f"\nQ22 after fix: {repr(q22['question'])}")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("\nWritten to", path)
