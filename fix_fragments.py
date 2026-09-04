path = '/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/index.html'

with open(path, 'r') as f:
    lines = f.readlines()

# We'll process line by line, skipping known duplicate patterns
result = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check for duplicate fragment pattern:
    # A line with "  try { return JSON.parse(localStorage.getItem(LS_..."
    # followed by a line with just "}"
    if (line.strip().startswith("try { return JSON.parse(localStorage.getItem(LS_USERS)") and
        i + 1 < len(lines) and lines[i+1].strip() == "}"):
        # Skip this duplicate fragment (2 lines)
        i += 2
        continue
    
    if (line.strip().startswith("try { return JSON.parse(localStorage.getItem(LS_WRONG") and
        i + 1 < len(lines) and lines[i+1].strip() == "}"):
        # Skip this duplicate fragment (2 lines)
        i += 2
        continue
    
    if (line.strip().startswith("try { return JSON.parse(localStorage.getItem(LS_EXAM_HISTORY") and
        i + 1 < len(lines) and lines[i+1].strip() == "}"):
        # Skip this duplicate fragment (2 lines)
        i += 2
        continue
    
    result.append(line)
    i += 1

with open(path, 'w') as f:
    f.writelines(result)

print(f"Processed {len(lines)} lines, removed {len(lines) - len(result)} duplicate lines")
