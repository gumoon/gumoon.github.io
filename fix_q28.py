import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Fix Q28 explanation
q28 = data[27]
old_exp = q28['explanation']

# Split at the marker
split_marker = "\n：\n题目\n"
if split_marker in old_exp:
    q28['explanation'] = old_exp.split(split_marker)[0].strip()
    print("Q28 explanation fixed")
else:
    print("Split marker not found")

print(f"Q28 new explanation:\n{q28['explanation']}\n")

# Extract new question from remainder
remainder = old_exp.split(split_marker, 1)[1] if split_marker in old_exp else ""

new_question = {
    "question": "在分布式训练中，通信开销（Communication Overhead）是影响训练速度的关键瓶颈之一。以下哪项技术不是主要用于减少通信开销的？",
    "options": {
        "A": "Gradient Checkpointing（梯度检查点）",
        "B": "All-Reduce 算法优化（如Ring All-Reduce）",
        "C": "ZeRO 优化器（特别是ZeRO-2/3）",
        "D": "Token Compression（词元压缩）"
    },
    "answer": "A",
    "explanation": "A错误：Gradient Checkpointing 主要目的是减少显存占用，通过重计算来换取显存，它不会减少通信开销，反而可能因为引入额外的计算图而间接增加一些同步开销。\nB、C、D 都是通信优化的范畴：All-Reduce 是高效的聚合梯度通信算法；ZeRO 通过分片减少了需要传输的梯度和参数量；Token Compression 理论上可以减少需要传输的 token 数量（如果是在模型间传输某些中间表示）。",
    "category": "预训练技术"
}

# Parse remainder to confirm
def parse_mixed_content(remainder):
    lines = remainder.strip().split('\n')
    question_lines = []
    options = {}
    answer = ''
    explanation_lines = []
    current = 'question'
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('A. '):
            current = 'options'
            options['A'] = line[3:]
        elif line.startswith('B. '):
            options['B'] = line[3:]
        elif line.startswith('C. '):
            options['C'] = line[3:]
        elif line.startswith('D. '):
            options['D'] = line[3:]
        elif line.startswith('答案：'):
            answer = line[3:].strip()
            current = 'answer'
        elif line == '解析：':
            current = 'explanation'
        elif current == 'question':
            question_lines.append(line)
        elif current == 'explanation':
            explanation_lines.append(line)
        i += 1
    return '\n'.join(question_lines).strip(), options, answer, '\n'.join(explanation_lines).strip()

if remainder:
    q, opts, ans, exp = parse_mixed_content(remainder)
    if q:
        new_question['question'] = q
    if opts:
        new_question['options'] = opts
    if ans:
        new_question['answer'] = ans
    if exp:
        new_question['explanation'] = exp
    print(f"Extracted from remainder: Q={q[:50]}..., A={ans}")

# Insert at index 28 (becomes new Q29)
data.insert(28, new_question)
print(f"\nNew question inserted at index 28")
print(f"Total questions now: {len(data)}")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("Written to", path)
