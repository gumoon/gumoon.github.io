import json, re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

def is_code_line(line):
    stripped = line.strip()
    code_prefixes = ('import ', 'from ', 'def ', 'class ', 'if ', 'for ', 'while ', 'return ', 'print(', '#', 'try:', 'except', 'elif ', 'else:', 'with ', 'assert ', 'pass', 'break', 'continue', 'yield ', 'lambda ', 'global ', 'nonlocal ', 'del ', 'raise ', 'finally', 'async ', 'await ')
    code_suffixes = (':', ')', ']', '}', ';')
    if any(stripped.startswith(p) for p in code_prefixes):
        return True
    if '=' in stripped and any(stripped.endswith(s) for s in code_suffixes):
        return True
    if stripped.startswith('#'):
        return True
    if stripped.endswith(')') and '(' in stripped:
        return True
    return False

issues = []
for i, q in enumerate(data):
    text = q['question']
    if '\n' not in text:
        continue
    lines = text.split('\n')
    bad_breaks = []
    for j, line in enumerate(lines):
        if j >= len(lines) - 1:
            continue
        stripped = line.strip()
        next_stripped = lines[j+1].strip()
        if not stripped or not next_stripped:
            continue
        # Skip code blocks
        if is_code_line(line) or is_code_line(lines[j+1]):
            continue
        # Skip if current line ends with punctuation
        end_punct = '。：；，、？！）】」》〉. '
        if stripped[-1] in end_punct:
            continue
        # Check if it's a real bad break: line doesn't end with punctuation AND next line starts with continuation
        if stripped[-1].isalpha() and next_stripped[0].isalpha():
            bad_breaks.append((j, stripped[-20:], next_stripped[:20]))
    if bad_breaks:
        issues.append((i+1, bad_breaks))

print(f"Found {len(issues)} questions with bad line breaks:")
for qnum, breaks in issues:
    print(f"\nQ{qnum}: {data[qnum-1]['question'][:60]}...")
    for idx, line, next_line in breaks:
        print(f"  Break: '{line}' -> '{next_line}'")

if not issues:
    print("\nAll line breaks look good!")
