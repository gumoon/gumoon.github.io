import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Fix Q9 (index 8): B contains C and D
q9 = data[8]
print("Before Q9 fix:")
print(f"  B: {q9['options']['B']}")

# Split B option by C. and D. markers
b_text = q9['options']['B']
# The text is: "随机遮盖输入序列中的部分词元并进行重构 C.同时预测输入序列中所有位置的词元 D.将输入序列转换为图像特征进行识别"
# We need to split by " C." and " D."

parts = re.split(r'\s+C[\.．]\s*', b_text, maxsplit=1)
if len(parts) == 2:
    b_new = parts[0].strip()
    remainder = parts[1]
    parts2 = re.split(r'\s+D[\.．]\s*', remainder, maxsplit=1)
    if len(parts2) == 2:
        c_new = parts2[0].strip()
        d_new = parts2[1].strip()
        q9['options']['B'] = b_new
        q9['options']['C'] = c_new
        q9['options']['D'] = d_new
        print("After Q9 fix:")
        print(f"  B: {b_new}")
        print(f"  C: {c_new}")
        print(f"  D: {d_new}")
    else:
        print("Could not split D from Q9")
else:
    print("Could not split C from Q9")

# Fix Q109 (index 108): A contains B
q109 = data[108]
print("\nBefore Q109 fix:")
print(f"  A: {q109['options']['A']}")

a_text = q109['options']['A']
# The text is: "训练数据中特定群体的样本数量不足 B.模型算法的计算速度过快"
parts = re.split(r'\s+B[\.．]\s*', a_text, maxsplit=1)
if len(parts) == 2:
    a_new = parts[0].strip()
    b_new = parts[1].strip()
    q109['options']['A'] = a_new
    q109['options']['B'] = b_new
    print("After Q109 fix:")
    print(f"  A: {a_new}")
    print(f"  B: {b_new}")
else:
    print("Could not split B from Q109")

# Verify fixes
print("\n=== Verification ===")
for i in [8, 108]:
    q = data[i]
    print(f"Q{i+1} options: {list(q['options'].keys())}")
    for k, v in q['options'].items():
        print(f"  {k}: {v}")

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("\nWritten to", path)
