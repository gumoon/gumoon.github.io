path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/index.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Update 113 to 114 for total question count
content = content.replace('value="113" min="1" max="113"', 'value="114" min="1" max="114"')
content = content.replace('id="quizMaxCount">113</span>', 'id="quizMaxCount">114</span>')
content = content.replace('id="quizTotalNum">113</span>', 'id="quizTotalNum">114</span>')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated 113 -> 114 in index.html")
