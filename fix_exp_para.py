import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

def is_option_line(line):
    """检查一行是否是选项分析的开头（如 A正确, B 错误等）"""
    return bool(re.match(r'^[A-D]\s*(正确|错误)', line.strip()))

def fix_explanation(exp):
    """
    修复explanation中的换行：
    - 保留选项标记行（A正确/B错误等）之前的换行
    - 合并同一选项分析内部的排版换行
    """
    lines = exp.split('\n')
    result = []
    current_para = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        if is_option_line(line):
            # 先保存之前的段落
            if current_para:
                result.append(''.join(current_para))
                current_para = []
            # 开始新段落
            current_para.append(stripped)
        else:
            # 不是选项标记行，追加到当前段落
            # 如果当前段落为空（不应该发生），直接添加
            if not current_para:
                current_para.append(stripped)
            else:
                # 判断是否需要加空格连接
                last_char = current_para[-1][-1] if current_para[-1] else ''
                first_char = stripped[0] if stripped else ''
                if last_char.isascii() and first_char.isascii():
                    current_para.append(' ' + stripped)
                else:
                    current_para.append(stripped)
    
    # 保存最后一个段落
    if current_para:
        result.append(''.join(current_para))
    
    return '\n'.join(result)

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
