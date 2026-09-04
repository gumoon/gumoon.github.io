import re

path = '/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/index.html'

with open(path, 'r') as f:
    content = f.read()

# Remove fragment 1: old getUsers body without declaration, after correct getUsers
content = re.sub(
    r"(function getUsers\(\) \{[^}]+\}[^}]+\})\s+try \{ return JSON\.parse\(localStorage\.getItem\(LS_USERS\) \|\| '\\\[\]'\); \} catch\(e\) \{ return \[\]; \}\s*\}\s*function saveUsers\(users\)",
    r"\1\nfunction saveUsers(users)",
    content
)

# Remove fragment 2: old getWrong body without declaration
content = re.sub(
    r"(function getWrong\(u\) \{[^}]+\}[^}]+\})\s+try \{ return JSON\.parse\(localStorage\.getItem\(LS_WRONG\(u\)\) \|\| '\\\[\]'\); \} catch\(e\) \{ return \[\]; \}\s*\}\s*function saveWrong\(u, wrong\)",
    r"\1\nfunction saveWrong(u, wrong)",
    content
)

# Remove fragment 3: old getExamHistory body without declaration
content = re.sub(
    r"(function getExamHistory\(u\) \{[^}]+\}[^}]+\})\s+try \{ return JSON\.parse\(localStorage\.getItem\(LS_EXAM_HISTORY\(u\)\) \|\| '\\\[\]'\); \} catch\(e\) \{ return \[\]; \}\s*\}\s*function saveExamHistory\(u, history\)",
    r"\1\nfunction saveExamHistory(u, history)",
    content
)

# Remove fragment 4: old handleAuth body without declaration
# The correct handleAuth ends with "}\n}\n" (closing brace of catch, then closing brace of function)
# The fragment is the old function body lines without the "function handleAuth() {" line
old_handleAuth_body = """  var input = document.getElementById('nicknameInput');
  var error = document.getElementById('authError');
  var name = input.value.trim();
  if (!name) { error.textContent = '请输入昵称'; return; }
  if (name.length > 50) { error.textContent = '昵称不能超过50个字符'; return; }
  // 必须以字母开头（支持中英文等Unicode字母），只能包含字母和数字
  var validRegex = /^[\\p{L}][\\p{L}\\p{N}]*$/u;
  if (!validRegex.test(name)) {
    error.textContent = '昵称需以字母开头，且仅包含字母和数字';
    return;
  }
  var users = getUsers();
  if (!users.includes(name)) {
    users.push(name);
    saveUsers(users);
  }
  currentUser = name;
  setCurrentUser(name);
  showHome();
}"""

# Replace the old body fragment that appears after the correct handleAuth
content = content.replace(old_handleAuth_body + '\n', '', 1)

with open(path, 'w') as f:
    f.write(content)

print("Fixed!")
