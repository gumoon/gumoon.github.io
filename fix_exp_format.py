import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

def fix_explanation_format(text):
    """
    Fix explanation formatting by ensuring each option analysis starts on a new line.
    Matches patterns like: A正确, A正确：, A错误, A错误：, B 正确, B 错误, etc.
    """
    # Pattern: option letter + optional space + (正确|错误) + optional colon
    # We want to insert a newline before each option marker except at the start
    pattern = re.compile(r'(?<!^)(?<!\n)([A-D])\s*(正确|错误)')
    
    # Insert newline before each matched option marker
    result = pattern.sub(r'\n\1\2', text)
    
    # Also handle cases where there's a colon immediately after
    # e.g., "A正确：" or "B 错误："
    result = re.sub(r'(?<!^)(?<!\n)([A-D])\s*(正确|错误)(：)', r'\n\1\2\3', result)
    
    # Clean up: if there are consecutive newlines, keep only one
    result = re.sub(r'\n+', '\n', result)
    
    return result

# Test on Q53
q53 = data[52]
test = fix_explanation_format(q53['explanation'])
print("=== Q53 BEFORE ===")
print(q53['explanation'])
print("\n=== Q53 AFTER ===")
print(test)

# Apply to all
fixed_count = 0
for q in data:
    original = q['explanation']
    fixed = fix_explanation_format(original)
    if fixed != original:
        q['explanation'] = fixed
        fixed_count += 1

print(f"\n\nFixed {fixed_count} explanations")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("Written to", path)
