import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Fix Q66 explanation formatting - add line breaks between option analyses
q66 = data[65]
old = q66['explanation']
# Replace the single paragraph with formatted lines
new = old.replace('因此最适合B选项的场景。', '因此最适合B选项的场景。\n').replace('A选项需要从零训练，', 'A选项需要从零训练，\n')
# Clean up any double newlines
new = new.replace('\n\n', '\n')

print(f"Q66 BEFORE:\n{old}\n")
print(f"Q66 AFTER:\n{new}\n")

q66['explanation'] = new

# Also check and fix other explanations that might be single-paragraph
# Find explanations that contain multiple option markers but no newlines
for i, q in enumerate(data):
    exp = q['explanation']
    # Count option markers
    import re
    markers = re.findall(r'[A-D](?:正确|错误)', exp)
    if len(markers) > 1 and '\n' not in exp:
        # This explanation has multiple options but no line breaks
        print(f"Q{i+1} has {len(markers)} option markers but no newlines")
        # Try to add line breaks before each option marker (except the first)
        fixed = re.sub(r'(?<![\n])([A-D])(正确|错误)', r'\n\1\2', exp)
        if fixed != exp:
            q['explanation'] = fixed
            print(f"  -> Fixed")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("\nWritten to", path)
