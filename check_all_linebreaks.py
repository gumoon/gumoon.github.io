import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

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
        
        # Check if English word is broken: current line ends with lowercase/uppercase and next line starts with lowercase
        if stripped[-1].isalpha() and next_stripped[0].isalpha():
            # Could be an English word broken across lines, or Chinese continuation
            # But also check: if line doesn't end with Chinese punctuation
            if stripped[-1] not in '。：；，、？！）】」》〉':
                bad_breaks.append((j, stripped, next_stripped))
    
    if bad_breaks:
        issues.append((i+1, bad_breaks))

print(f"Found {len(issues)} questions with potential bad line breaks in question text:")
for qnum, breaks in issues:
    print(f"\nQ{qnum}: {data[qnum-1]['question'][:80]}...")
    for idx, line, next_line in breaks:
        print(f"  Break at line {idx}: '{line[-20:]}' -> '{next_line[:20]}'")
