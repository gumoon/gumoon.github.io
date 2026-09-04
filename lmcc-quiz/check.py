#!/usr/bin/env python3
"""
LMCC 刷题项目提交前自动检查脚本
运行方式: python3 check.py
"""

import re
import subprocess
import sys
from pathlib import Path

def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def check_js_syntax(filepath, label):
    code, out, err = run(f'node --check "{filepath}"')
    if code != 0:
        print(f"❌ [{label}] JS 语法错误:")
        print(err or out)
        return False
    print(f"✅ [{label}] JS 语法通过")
    return True

def extract_script_from_html(html_path):
    content = open(html_path, encoding='utf-8').read()
    m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if not m:
        print("❌ [index.html] 未找到内联 <script> 标签")
        return None
    return m.group(1)

def check_core_functions(html_path):
    content = open(html_path, encoding='utf-8').read()
    required = ['handleAuth', 'init', 'saveUsers', 'getUsers', 'formatQuestionText', 'isCodeLine']
    missing = [f for f in required if f not in content]
    if missing:
        print(f"❌ [index.html] 缺少核心函数: {', '.join(missing)}")
        return False
    print(f"✅ [index.html] 核心函数齐全 ({len(required)} 个)")
    return True

def check_code_questions(js_path):
    content = open(js_path, encoding='utf-8').read()
    checks = [
        ("GQA 题", 'GroupedQueryAttention'),
        ("温度采样题", 'sample_with_strategies'),
        ("LoRA 题", 'LoRALinear'),
        ("BLEU 题", 'compute_bleu'),
    ]
    all_ok = True
    for name, keyword in checks:
        if keyword in content:
            print(f"✅ [题目] {name} 数据存在")
        else:
            print(f"❌ [题目] {name} 数据缺失（关键字: {keyword}）")
            all_ok = False
    return all_ok

def main():
    base = Path(__file__).parent
    questions_js = base / 'questions.js'
    index_html = base / 'index.html'

    all_ok = True
    print("=" * 50)
    print("LMCC 刷题项目自动检查")
    print("=" * 50)

    # 1. questions.js
    if questions_js.exists():
        all_ok &= check_js_syntax(questions_js, "questions.js")
        all_ok &= check_code_questions(questions_js)
    else:
        print(f"⚠️ 未找到 questions.js")

    # 2. index.html
    if index_html.exists():
        script = extract_script_from_html(index_html)
        if script:
            tmp = base / '.tmp_check.js'
            tmp.write_text(script, encoding='utf-8')
            all_ok &= check_js_syntax(tmp, "index.html script")
            tmp.unlink(missing_ok=True)
        all_ok &= check_core_functions(index_html)
    else:
        print(f"⚠️ 未找到 index.html")

    print("=" * 50)
    if all_ok:
        print("✅ 所有检查通过，可以提交")
        return 0
    else:
        print("❌ 检查未通过，请修复后再提交")
        return 1

if __name__ == '__main__':
    sys.exit(main())
