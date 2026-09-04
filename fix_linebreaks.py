import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

def is_code_line(line):
    """判断一行是否是Python代码行"""
    stripped = line.strip()
    code_prefixes = ('import ', 'from ', 'def ', 'class ', 'if ', 'for ', 'while ', 'return ', 'print(', '#', 'try:', 'except', 'elif ', 'else:', 'with ', 'assert ', 'pass', 'break', 'continue', 'yield ', 'lambda ', 'global ', 'nonlocal ', 'del ', 'raise ', 'finally', 'async ', 'await ')
    code_suffixes = (':', ')', ']', '}', ';')
    
    # 如果以Python关键字开头
    if any(stripped.startswith(p) for p in code_prefixes):
        return True
    # 如果包含等号且以特定字符结尾（典型的赋值语句）
    if '=' in stripped and any(stripped.endswith(s) for s in code_suffixes):
        return True
    # 纯注释
    if stripped.startswith('#'):
        return True
    # 看起来像函数调用或方法链
    if stripped.endswith(')') and '(' in stripped:
        return True
    return False

def should_merge(line, next_line):
    """判断两行是否应该合并"""
    s1 = line.rstrip()
    s2 = next_line.lstrip()
    
    if not s1 or not s2:
        return False
    
    # 如果任一行是代码行，不合并
    if is_code_line(line) or is_code_line(next_line):
        return False
    
    # 如果当前行以空格结尾，说明它可能已经是一个完整的语义单元，不合并
    # （但PDF提取的行通常不会以空格结尾）
    
    # 当前行以以下字符结尾，表示语义结束，不合并
    end_punct = '。：；，、？！）】」》〉.'
    if s1[-1] in end_punct:
        return False
    
    # 下一行以以下字符开头，表示新的开始，不合并
    start_punct = '（【「《〈（ '
    if s2[0] in start_punct:
        return False
    
    # 下一行是选项格式
    if re.match(r'^[A-D]\.\s', s2):
        return False
    
    # 下一行是数字列表格式
    if re.match(r'^\d+\.\s', s2):
        return False
    
    # 当前行以英文单词结尾，下一行以英文单词开头（英文被断开）
    if s1[-1].isalpha() and s2[0].isalpha():
        # 检查是否可能是英文单词断开
        return True
    
    # 当前行以中文结尾，下一行以中文开头（中文被断开）
    if '\u4e00' <= s1[-1] <= '\u9fff' and '\u4e00' <= s2[0] <= '\u9fff':
        return True
    
    # 当前行以字母/数字/括号结尾，下一行以中文开头
    if s1[-1].isalnum() or s1[-1] in '）">]':
        if '\u4e00' <= s2[0] <= '\u9fff':
            return True
    
    # 当前行以中文结尾，下一行以英文/数字开头
    if '\u4e00' <= s1[-1] <= '\u9fff':
        if s2[0].isalnum():
            return True
    
    return False

def fix_linebreaks(text):
    """修复PDF提取导致的错误换行"""
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        current = lines[i]
        # 尝试与后续行合并
        while i + 1 < len(lines) and should_merge(current, lines[i + 1]):
            next_line = lines[i + 1].strip()
            # 合并时，如果当前行以英文结尾且下一行以英文开头，加空格
            # 否则直接连接（中文之间不需要空格）
            if current.rstrip()[-1].isascii() and next_line[0].isascii():
                current = current.rstrip() + ' ' + next_line
            else:
                current = current.rstrip() + next_line
            i += 1
        result.append(current)
        i += 1
    return '\n'.join(result)

# Test on the Cosine question first
test_q = data[13]
print("=== BEFORE Q14 ===")
print(test_q['question'])
print("\n=== AFTER ===")
fixed = fix_linebreaks(test_q['question'])
print(fixed)

# Now apply to all questions
fixed_count = 0
for q in data:
    original = q['question']
    fixed = fix_linebreaks(original)
    if fixed != original:
        q['question'] = fixed
        fixed_count += 1

print(f"\n\nFixed linebreaks in {fixed_count} questions")

# Also fix options and explanations for similar issues
for q in data:
    for k, v in q['options'].items():
        fixed = fix_linebreaks(v)
        if fixed != v:
            q['options'][k] = fixed
    fixed_exp = fix_linebreaks(q['explanation'])
    if fixed_exp != q['explanation']:
        q['explanation'] = fixed_exp

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("Written to", path)
