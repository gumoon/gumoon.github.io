import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

print(f"总题数: {len(data)}")

# 1. 检查选项合并
print("\n=== 1. 检查选项合并（一个选项包含其他选项标记）===")
merged = []
for i, q in enumerate(data):
    opts = q['options']
    for k, v in opts.items():
        for letter in ['A','B','C','D']:
            if letter != k:
                pattern = r'[\s。]\s*' + letter + r'[\.．]\s*'
                if re.search(pattern, v):
                    merged.append((i+1, k, letter, v[:100]))
                    break

if merged:
    for qnum, opt_k, contains, text in merged:
        print(f"Q{qnum} 选项 {opt_k} 可能包含选项 {contains}: {text}")
else:
    print("未发现选项合并问题")

# 2. 检查解析中混入题目
print("\n=== 2. 检查解析中混入其他题目内容 ===")
merged_exp = []
markers = ['\n题目\n', '\n题目：', '：\n题目\n', '：\n题目：', '答案：', '\nA. ', '\nB. ', '\nC. ', '\nD. ']
for i, q in enumerate(data):
    exp = q.get('explanation', '')
    for marker in markers:
        if marker in exp:
            merged_exp.append((i+1, repr(marker), exp[:200]))
            break

if merged_exp:
    for qnum, marker, text in merged_exp:
        print(f"Q{qnum} 解析中可能混入题目内容 (marker={marker})")
else:
    print("未发现解析混入题目的问题")

# 3. 检查缺失选项
print("\n=== 3. 检查缺失选项 ===")
missing = []
for i, q in enumerate(data):
    expected = ['A','B','C','D']
    actual = list(q['options'].keys())
    if set(actual) != set(expected):
        missing.append((i+1, [l for l in expected if l not in actual]))

if missing:
    for qnum, miss in missing:
        print(f"Q{qnum} 缺失选项: {miss}")
else:
    print("所有题目都有 A/B/C/D 四个选项")

# 4. 检查题干是否异常短（可能被截断）
print("\n=== 4. 检查题干异常 ===")
short_q = []
for i, q in enumerate(data):
    qtext = q.get('question', '')
    if len(qtext) < 10:
        short_q.append((i+1, qtext))
    # 检查题干是否以"答案"或"解析"结尾
    if qtext.strip().endswith('答案：') or qtext.strip().endswith('解析：'):
        short_q.append((i+1, f"[以'答案/解析'结尾] {qtext[:80]}"))

if short_q:
    for qnum, text in short_q:
        print(f"Q{qnum} 题干异常: {text}")
else:
    print("未发现异常短题干")

# 5. 检查解析是否为空或异常
print("\n=== 5. 检查解析是否为空或极短 ===")
short_exp = []
for i, q in enumerate(data):
    exp = q.get('explanation', '')
    if len(exp.strip()) < 5:
        short_exp.append((i+1, repr(exp)))

if short_exp:
    for qnum, text in short_exp:
        print(f"Q{qnum} 解析异常短: {text}")
else:
    print("所有题目解析长度正常")

# 6. 检查答案是否在选项中
print("\n=== 6. 检查答案是否存在于选项中 ===")
wrong_ans = []
for i, q in enumerate(data):
    ans = q.get('answer', '')
    opts = q.get('options', {})
    if ans and ans not in opts:
        wrong_ans.append((i+1, ans, list(opts.keys())))

if wrong_ans:
    for qnum, ans, keys in wrong_ans:
        print(f"Q{qnum} 答案 '{ans}' 不在选项 {keys} 中")
else:
    print("所有答案都存在于对应选项中")

print("\n=== 检查完成 ===")
