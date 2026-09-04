import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

def has_option_prefix(text):
    """检查解析是否以选项分析开头"""
    return bool(re.match(r'^[A-D]\s*(正确|错误)', text.strip()))

def has_category_or_marker_suffix(text):
    """检查解析末尾是否混入了分类标记"""
    markers = ['○ 考核方式', '○ 扩展知识点', '○ 知识点', '题目：',
               '预训练技术', '模型评测', '模型伦理', '人类对齐',
               '智能体', '复杂推理', '指令微调', '提示学习',
               '检索增强', '知识利用', '解码方法', '解码与部署',
               '分布式训练', '数据组织策略', '高效训练技术',
               '多查询注意力', '分组查询注意力', '多头潜在注意力',
               '近似）', '计算、混合精度训练的流程', '融合算子的原理',
               '率预热（Warm-up）', '模型训练的影响',
               '基于排序的人类', '对比、DPO', 'token-level',
               'reference-free DPO', '指令蒸馏方法',
               '结果奖励建模和过程奖励建模',
               '中通过多路径搜索', 'Self-consistency',
               'Tree-of-Thoughts', '智能体能力优化',
               '记忆的存储和读取', '提示学习', '本概念与基础方法',
               '模型量化的基本概念与基础方法', '析与优化',
               '常见推理工具使用（vLLM）', '量化粒度、常见量化方法',
               '量化对模型性能的影响', '回归解码、早退机制、级联解码',
               '解码加速的系统级优化', 'FlashAttention、PagedAttention',
               '批次管理优化', '指令配比、基于导数的指令数据选择',
               '多阶段混合训练（长短指令、数据课程）',
               '调、提示微调', '的指令', '长上下文模型的训练方法',
               'LAMB）', 'C错误）', 'B错误）', 'D错误）',
               'A错误）']
    for m in markers:
        if text.strip().endswith(m):
            return True
    # Also check for partial English word endings
    if re.search(r'[a-zA-Z]{2,}$', text.strip()):
        # Check if the last word looks like a partial module name
        last_word = text.strip().split()[-1] if text.strip() else ''
        if last_word in ['Learning', 'Decoding', 'Training', 'Reasoning',
                         'Alignment', 'Tuning', 'Generation', 'Distillation',
                         'Evaluation', 'Optimization', 'Search', 'Memory',
                         'Agent', 'Tool', 'Attention', 'Parallelism']:
            return True
    return False

print("=== 解析开头缺失（不以 A/B/C/D 开头） ===")
for i, q in enumerate(data):
    exp = q['explanation'].strip()
    if not has_option_prefix(exp):
        # Check if it's a complete sentence starting with something else
        # Some explanations might not use A/B/C/D format
        print(f"Q{i+1} (答案{q['answer']}): {exp[:100]}")

print("\n=== 解析末尾混入内容 ===")
for i, q in enumerate(data):
    exp = q['explanation'].strip()
    if has_category_or_marker_suffix(exp):
        print(f"Q{i+1}: ...{exp[-60:]}")
