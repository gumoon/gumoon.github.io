import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

def is_code_line(line):
    stripped = line.strip()
    code_prefixes = ('import ', 'from ', 'def ', 'class ', 'if ', 'for ', 'while ', 'return ', 'print(', '#', 'try:', 'except', 'elif ', 'else:', 'with ', 'assert ', 'pass', 'break', 'continue', 'yield ', 'lambda ', 'global ', 'nonlocal ', 'del ', 'raise ', 'finally', 'async ', 'await ')
    code_suffixes = (':', ')', ']', '}', ';')
    if any(stripped.startswith(p) for p in code_prefixes):
        return True
    if '=' in stripped and any(stripped.endswith(s) for s in code_suffixes):
        return True
    if stripped.startswith('#'):
        return True
    if stripped.endswith(')') and '(' in stripped:
        return True
    return False

def should_merge(line, next_line):
    """判断两行是否应该合并（去掉软换行）"""
    s1 = line.rstrip()
    s2 = next_line.lstrip()
    
    if not s1 or not s2:
        return False
    
    if is_code_line(line) or is_code_line(next_line):
        return False
    
    end_punct = '。：；，、？！）】」》〉. '
    if s1[-1] in end_punct:
        return False
    
    start_punct = '（【「《〈（ '
    if s2[0] in start_punct:
        return False
    
    # Don't merge if next line starts with option marker
    if re.match(r'^[A-D]\s*(正确|错误)', s2):
        return False
    
    # If line ends with alpha and next starts with alpha
    if s1[-1].isalpha() and s2[0].isalpha():
        return True
    
    if '\u4e00' <= s1[-1] <= '\u9fff' and '\u4e00' <= s2[0] <= '\u9fff':
        return True
    
    if s1[-1].isalnum() or s1[-1] in '）">]':
        if '\u4e00' <= s2[0] <= '\u9fff':
            return True
    
    if '\u4e00' <= s1[-1] <= '\u9fff':
        if s2[0].isalnum():
            return True
    
    return False

def fix_paragraph_linebreaks(text):
    """Fix linebreaks within a paragraph (not across option boundaries)"""
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        current = lines[i]
        while i + 1 < len(lines) and should_merge(current, lines[i + 1]):
            next_line = lines[i + 1].strip()
            if current.rstrip()[-1].isascii() and next_line[0].isascii():
                current = current.rstrip() + ' ' + next_line
            else:
                current = current.rstrip() + next_line
            i += 1
        result.append(current)
        i += 1
    return '\n'.join(result)

def fix_explanation(text):
    """
    Fix explanation formatting:
    1. Split by option markers (A/B/C/D)
    2. Fix linebreaks within each paragraph
    3. Rejoin with newlines
    """
    # Split by option markers, keeping the markers
    parts = re.split(r'(?=^[A-D]\s*(正确|错误))', text, flags=re.MULTILINE)
    
    # Filter out empty parts
    parts = [p for p in parts if p.strip()]
    
    fixed_parts = []
    for part in parts:
        fixed_parts.append(fix_paragraph_linebreaks(part))
    
    return '\n'.join(fixed_parts)

# Test on Q53
q53 = data[52]
test = fix_explanation(q53['explanation'])
print("=== Q53 BEFORE ===")
print(q53['explanation'])
print("\n=== Q53 AFTER ===")
print(test)

# Apply to all
fixed_count = 0
for q in data:
    original = q['explanation']
    fixed = fix_explanation(original)
    if fixed != original:
        q['explanation'] = fixed
        fixed_count += 1

print(f"\n\nFixed {fixed_count} explanations")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("Written to", path)
