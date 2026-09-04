import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

# Find the Cosine question
for i, q in enumerate(data):
    if 'Cosine' in q['question'] or '学习率衰减' in q['question']:
        print(f"=== Q{i+1} ===")
        print(f"Question repr: {repr(q['question'])}")
        print(f"\nQuestion display:\n{q['question']}")
        print(f"\n---")
        # Check if there are mid-sentence line breaks
        lines = q['question'].split('\n')
        for j, line in enumerate(lines):
            # Check if line ends without punctuation but next line starts with lowercase/continuation
            if j < len(lines) - 1:
                stripped = line.strip()
                next_stripped = lines[j+1].strip()
                # If current line doesn't end with Chinese punctuation and next line doesn't start with punctuation
                if stripped and not stripped[-1] in '。：；，、？！）】）」':
                    if next_stripped and not next_stripped[0] in '（【「（':
                        print(f"  Possible bad break at line {j}: '{stripped}' -> '{next_stripped}'")
