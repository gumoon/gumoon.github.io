path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/index.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Update 114 to 115 for total question count
content = content.replace('value="114" min="1" max="114"', 'value="115" min="1" max="115"')
content = content.replace('id="quizMaxCount">114</span>', 'id="quizMaxCount">115</span>')
content = content.replace('id="quizTotalNum">114</span>', 'id="quizTotalNum">115</span>')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated 114 -> 115 in index.html")
