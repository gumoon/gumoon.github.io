with open('/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/index.html', 'r') as f:
    lines = f.readlines()

# Find and print duplicate patterns for debugging
for i, line in enumerate(lines):
    if 'function saveUsers(users) { localStorage.setItem(LS_USERS, JSON.stringify(users)); }' in line:
        print(f"saveUsers at line {i+1}: {line.strip()}")
    if 'function getWrong(u) {' in line:
        print(f"getWrong at line {i+1}: {line.strip()}")
    if 'function getExamHistory(u) {' in line:
        print(f"getExamHistory at line {i+1}: {line.strip()}")
    if 'function handleAuth() {' in line:
        print(f"handleAuth at line {i+1}: {line.strip()}")
    if 'function logout() {' in line:
        print(f"logout at line {i+1}: {line.strip()}")
