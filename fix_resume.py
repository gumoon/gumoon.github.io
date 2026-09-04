import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Fix Q109 explanation: keep only its own explanation
q109 = data[108]
old_exp = q109['explanation']
# Split at the marker where the next question starts
split_marker = "\n：\n题目\n"
if split_marker in old_exp:
    q109['explanation'] = old_exp.split(split_marker)[0].strip()
    print("Q109 explanation fixed")
else:
    print("Split marker not found, trying alternative...")
    # The old explanation might have slightly different formatting
    # Try to find where the next question starts
    lines = old_exp.split('\n')
    cut_idx = None
    for i, line in enumerate(lines):
        if line == '题目' or '某公司开发' in line:
            cut_idx = i
            break
    if cut_idx is not None:
        q109['explanation'] = '\n'.join(lines[:cut_idx]).strip()
        print(f"Q109 explanation cut at line {cut_idx}")

# Also fix the missing first character "训" if needed
if q109['explanation'].startswith('练数据中'):
    q109['explanation'] = '训' + q109['explanation']
    print("Fixed missing first character in Q109 explanation")

print(f"Q109 new explanation:\n{q109['explanation']}")

# Insert the new question after Q109 (at index 109)
new_question = {
    "question": "某公司开发了一款基于大模型的自动化简历筛选系统，由于训练数据中历史高管多为男性，导致系统自动调低了女性应聘者的评分。这种现象主要体现了模型偏见的哪种实际影响？",
    "options": {
        "A": "损害了算法的计算效率",
        "B": "导致了社会不公平的自动化与规模化",
        "C": "增加了模型部署的硬件成本",
        "D": "提升了模型处理长文本的理解能力"
    },
    "answer": "B",
    "explanation": "模型偏见在实际应用中（如招聘、信贷、司法预测）会直接导致对特定群体的歧视，从而将现实中的社会不公通过算法进行放大和自动化执行。这属于算法伦理层面的重大风险，与计算效率、硬件成本等无关。",
    "category": "大模型基础概念"
}

# Extract the new question's explanation from the old Q109 explanation if possible
if split_marker in old_exp:
    remainder = old_exp.split(split_marker, 1)[1]
    # Parse the remainder to get question, options, answer, explanation
    # The format is:
    # 题目
    # <question text>
    # A. <option A>
    # B. <option B>
    # C. <option C>
    # D. <option D>
    # 答案：B
    # 解析：
    # <explanation>
    
    lines = remainder.strip().split('\n')
    # First line should be "题目", second line starts the question
    if lines[0] == '题目':
        question_lines = []
        options = {}
        answer = ''
        explanation_lines = []
        
        current_section = 'question'
        i = 1
        while i < len(lines):
            line = lines[i]
            if line.startswith('A. '):
                current_section = 'options'
                options['A'] = line[3:]
            elif line.startswith('B. '):
                options['B'] = line[3:]
            elif line.startswith('C. '):
                options['C'] = line[3:]
            elif line.startswith('D. '):
                options['D'] = line[3:]
            elif line.startswith('答案：'):
                answer = line[3:].strip()
                current_section = 'answer'
            elif line == '解析：':
                current_section = 'explanation'
            elif current_section == 'question':
                question_lines.append(line)
            elif current_section == 'explanation':
                explanation_lines.append(line)
            i += 1
        
        new_question['question'] = '\n'.join(question_lines).strip()
        new_question['options'] = options
        new_question['answer'] = answer
        new_question['explanation'] = '\n'.join(explanation_lines).strip()
        
        print(f"\nNew question extracted from Q109 explanation:")
        print(f"Question: {new_question['question'][:80]}")
        print(f"Answer: {new_question['answer']}")
        print(f"Options: {new_question['options']}")

# Insert the new question at index 109
data.insert(109, new_question)
print(f"\nNew question inserted at index 109 (Q110)")
print(f"Total questions now: {len(data)}")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("\nWritten to", path)
