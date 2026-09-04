import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Fix known truncated explanations
fixes = {
    # Q9: Missing start + extra "习的关系" at end
    8: {
        "old": "心训练任务，模型根据已有的前文序列预测下一个词元。B选项描述的是掩码语言模型（如 BERT）的训练方式。C 和D选项都不是标准的语言模型训练方式。习的关系",
        "new": "A正确：下一个词元预测是自回归语言模型（如 GPT）的核心训练任务，模型根据已有的前文序列预测下一个词元。B选项描述的是掩码语言模型（如 BERT）的训练方式。C和D选项都不是标准的语言模型训练方式。"
    },
    # Q52: Extra "解码与部署" at end
    51: {
        "old": "RAG 通过在生成前从外部可靠知识库检索相关文档并作为上下文输入给模型，显著降低了模型因知识遗忘或缺失而产生的事实性幻觉。CoT 主要解决推理逻辑问题，不能直接提供模型未学过的实时事实。解码与部署",
        "new": "B正确：RAG 通过在生成前从外部可靠知识库检索相关文档并作为上下文输入给模型，显著降低了模型因知识遗忘或缺失而产生的事实性幻觉。CoT 主要解决推理逻辑问题，不能直接提供模型未学过的实时事实。"
    },
    # Q66: Missing start + extra "的使用" at end
    65: {
        "old": "型的知识，通过设计合适的提示来引导模型完成特定任务，无需大量标注数据和重新训练。因此最适合B选项的场景。A 选项需要从零训练，C 和 D 选项不是提示学习的典型应用场景。的使用",
        "new": "B正确：提示学习（Prompt Learning）的核心思想是利用预训练模型已学到的知识，通过设计合适的提示来引导模型完成特定任务，无需大量标注数据和重新训练。因此最适合B选项的场景。A选项需要从零训练，C和D选项不是提示学习的典型应用场景。"
    },
    # Q99: Extra "数据集的使用" at end
    98: {
        "old": "A正确：评测公平性受多方面因素影响，包括数据分布、指标选择、评测设置等\nB错误：数据集的分布偏差是公平性问题的重要方面\nC错误：不同评测基准可能对不同架构或训练方式的模型有天然偏向\nD错误：评测公平性仍是活跃的研究领域数据集的使用",
        "new": "A正确：评测公平性受多方面因素影响，包括数据分布、指标选择、评测设置等\nB错误：数据集的分布偏差是公平性问题的重要方面\nC错误：不同评测基准可能对不同架构或训练方式的模型有天然偏向\nD错误：评测公平性仍是活跃的研究领域。"
    },
}

for idx, fix in fixes.items():
    q = data[idx]
    if q['explanation'] == fix['old']:
        q['explanation'] = fix['new']
        print(f"Q{idx+1} fixed")
    else:
        print(f"Q{idx+1} MISMATCH - current: {repr(q['explanation'][:100])}")

# Now do a broader scan for contamination in explanations
print("\n=== Broader scan for contamination ===")
contamination_markers = [
    '○ 考核方式', '○ 扩展知识点', '○ 知识点', '题目：',
    '解码与部署', '预训练技术', '模型评测', '模型伦理',
    '人类对齐', '智能体', '复杂推理', '指令微调',
    '提示学习', '检索增强', '知识利用',
    '的使用', '的关系', '的是',
]

for i, q in enumerate(data):
    exp = q['explanation']
    for marker in contamination_markers:
        if marker in exp:
            # Skip if it's a legitimate part of the explanation
            if marker in ['的使用', '的关系', '的是']:
                # Only flag if it appears at the very end
                if not exp.endswith(marker):
                    continue
            print(f"Q{i+1} may have contamination: '{marker}' in explanation")
            print(f"  Context: ...{exp[max(0, exp.find(marker)-30):exp.find(marker)+len(marker)+10]}")
            break

# Write back
output = "const QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)

print("\nWritten to", path)
