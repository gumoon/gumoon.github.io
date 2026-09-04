import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# ===== Fix 1: Remove trailing contamination =====
trailing_patterns = [
    r'长上下文模型的训练方法$',
    r'近似）$',
    r'对模型训练的影响$',
    r'率预热（Warm-up）$',
    r'LAMB）$',
    r'计算、混合精度训练的流程、融合算子的原理$',
    r'多阶段混合训练（长短指令、数据课程）$',
    r'的指令配比、基于导数的指令数据选择$',
    r'调、提示微调$',
    r'基于排序的人类$',
    r'指标、常见推理工具使用（vLLM）$',
    r'量化粒度、常见量化方法、量化对模型性能的影响$',
    r'本概念与基础方法、模型量化的基本概念与基础方法$',
    r'析与优化$',
    r'结果奖励建模和过程奖励建模$',
    r'智能体能力优化$',
    r'记忆的存储和读取$',
    r'提示学习$',
    r'多查询注意力（MQA）、分组查询注意力（GQA）、多头潜在注意力（MLA）$',
]

for q in data:
    exp = q['explanation']
    for pattern in trailing_patterns:
        match = re.search(pattern, exp)
        if match:
            # Only remove if there's meaningful content before
            before = exp[:match.start()].strip()
            if len(before) > 20:
                q['explanation'] = before
                print(f"Q{data.index(q)+1}: removed trailing contamination '{pattern}'")
                break

# ===== Fix 2: Fix missing prefix for explanations that start mid-sentence =====
# These are explanations where the first word is clearly a continuation
missing_prefix_fixes = {
    # Q11 - starts with "tch" (should be "Batch")
    10: ("tch梯度估计", "B错误：Batch梯度估计的期望等于真实梯度，与batch size无关"),
    # Q12 - starts with "始情况"
    11: ("始情况：", "A正确：初始情况："),
    # Q22 - starts with "中出现"
    21: ("中出现梯度爆炸", "B正确：梯度裁剪通过限制梯度的范数或值，防止训练中出现梯度爆炸"),
    # Q23 - starts with "术。"
    22: ("术。它用 float16", "A正确：混合精度训练是一种加速训练的技术。它用 float16"),
    # Q43 - starts with "有用性"
    42: ("有用性和诚实性", "D正确：人类对齐除了核心的无害性、有用性和诚实性（3H 原则）"),
    # Q65 - starts with "出。"
    64: ("出。其局限性", "C正确：提示工程的优势在于无需改变模型参数即可利用预训练模型的知识。其局限性"),
    # Q67 - starts with "是通过"
    66: ("是通过输入中的示例", "B正确：上下文学习（In-Context Learning）是通过输入中的示例"),
    # Q68 - starts with "降低了"
    67: ("降低了模型直接从问题", "B正确：思维链（CoT）通过生成中间推理步骤，降低了模型直接从问题跳转到复杂答案的推理难度。"),
    # Q79 - starts with "Profile"
    78: ("Profile（画像", "B正确：Profile（画像"),
    # Q82 - starts with "有效的"
    81: ("有效的记忆机制", "B正确：有效的记忆机制"),
    # Q83 - starts with "LLM"
    82: ("LLM 在工具使用中", "B正确：LLM 在工具使用中"),
}

for idx, (old_start, new_start) in missing_prefix_fixes.items():
    q = data[idx]
    exp = q['explanation']
    if exp.startswith(old_start):
        q['explanation'] = new_start + exp[len(old_start):]
        print(f"Q{idx+1}: fixed missing prefix")

# ===== Fix 3: Fix Q66 A/C/D formatting =====
q66 = data[65]
old = q66['explanation']
new = old.replace('A选项需要从零训练，', 'A错误：从零开始训练一个全新的深度学习模型不属于提示学习的应用范畴，提示学习是利用现有预训练模型。\n').replace('C和D选项不是提示学习的典型应用场景。', 'C错误：处理大规模结构化数据的统计分析不是提示学习的典型应用场景。\nD错误：进行复杂的数学公式推导计算也不是提示学习的典型应用场景。')
q66['explanation'] = new
print(f"Q66: fixed A/C/D formatting")

# ===== Fix 4: Fix Q16 AdamW explanation (reformat) =====
q16 = data[15]
old = q16['explanation']
# The current explanation is garbled, let me fix it
new = "A正确：AdamW将权重衰减（weight decay）从梯度更新中解耦出来，直接作用于参数本身，这使得正则化效果更加稳定有效。\nB错误：AdamW保留了Adam的自适应学习率机制。\nC错误：AdamW的计算复杂度没有明显增加。\nD错误：AdamW广泛应用于各类深度学习任务，不限于计算机视觉。"
q16['explanation'] = new
print(f"Q16: fixed garbled explanation")

# ===== Fix 5: Fix Q47 trailing contamination =====
q47 = data[46]
old = q47['explanation']
# Remove trailing contamination
if old.endswith('对比、DPO 模型的变种（token-level DPO 和 reference-free DPO算法）'):
    new = old.replace('对比、DPO 模型的变种（token-level DPO 和 reference-free DPO算法）', '')
    q47['explanation'] = new
    print(f"Q47: removed trailing contamination")

# ===== Fix 6: Fix Q80 trailing contamination =====
q80 = data[79]
old = q80['explanation']
if old.endswith('记忆的存储和读取'):
    new = old.replace('记忆的存储和读取', '')
    q80['explanation'] = new
    print(f"Q80: removed trailing contamination")

# ===== Write back =====
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("\nWritten to", path)
