import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# List of known contamination patterns at the END of explanations
# Each is (pattern_to_find, description)
end_contaminations = [
    (r'○ 知识点：.*$', '知识点标记'),
    (r'○ 扩展知识点.*$', '扩展知识点标记'),
    (r'○ 考核方式.*$', '考核方式标记'),
    (r'题目：.*$', '题目标记'),
    (r'解码与部署$', '模块标题'),
    (r'预训练技术$', '模块标题'),
    (r'模型评测$', '模块标题'),
    (r'模型伦理与安全$', '模块标题'),
    (r'人类对齐$', '模块标题'),
    (r'智能体$', '模块标题'),
    (r'复杂推理$', '模块标题'),
    (r'指令微调$', '模块标题'),
    (r'提示学习$', '模块标题'),
    (r'检索增强$', '模块标题'),
    (r'知识利用$', '模块标题'),
    (r'解码方法$', '模块标题'),
    (r'高效训练技术$', '模块标题'),
    (r'分布式训练$', '模块标题'),
    (r'数据组织策略$', '模块标题'),
    (r'反馈$', '不完整结尾'),
    (r'间的关系$', '不完整结尾'),
    (r'的使用$', '混入结尾'),
    (r'的是$', '混入结尾'),
    (r'数学、代码、科学任务任务$', '混入内容'),
    (r'开卷问答、知识不全）及对应指标$', '混入内容'),
    (r'数据集的使用$', '混入结尾'),
    (r'习的关系$', '混入结尾'),
]

fixed_count = 0
for i, q in enumerate(data):
    exp = q['explanation']
    original = exp
    
    # Split into lines and check each line's end
    lines = exp.split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned = line
        for pattern, desc in end_contaminations:
            # Only remove if the contamination is at the end of the line
            # and the line without it still has meaningful content
            match = re.search(pattern, cleaned)
            if match:
                # Check if this match is at the end of the line
                if match.end() == len(cleaned):
                    before = cleaned[:match.start()].strip()
                    # Only remove if there's still content left
                    if before and len(before) > 10:
                        cleaned = before
                        print(f"Q{i+1}: removed '{desc}' -> {repr(line[max(0,match.start()-20):])}")
                        break
        cleaned_lines.append(cleaned)
    
    new_exp = '\n'.join(cleaned_lines)
    if new_exp != original:
        q['explanation'] = new_exp
        fixed_count += 1

print(f"\nFixed {fixed_count} explanations")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("Written to", path)
