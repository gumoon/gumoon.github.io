import json

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/questions.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
json_str = content[len("const QUESTIONS = "):].rstrip().rstrip(';')
data = json.loads(json_str)

q53 = data[52]
print("Q53 A option:", repr(q53['options']['A']))

# Also verify Q22 and Q27
q22 = data[21]
print("Q22 question:", repr(q22['question']))

q27 = data[26]
print("Q27 question:", repr(q27['question']))
