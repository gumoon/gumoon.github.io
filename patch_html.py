import re

path = "/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/index.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update input field: maxlength 20 -> 50, update placeholder
content = content.replace(
    'placeholder="请输入昵称" maxlength="20"',
    'placeholder="请输入昵称，字母开头，仅含字母和数字" maxlength="50"'
)

# 2. Update handleAuth function
old_auth = '''function handleAuth() {
  var input = document.getElementById('nicknameInput');
  var error = document.getElementById('authError');
  var name = input.value.trim();
  if (!name) { error.textContent = '请输入昵称'; return; }
  if (name.length > 20) { error.textContent = '昵称不能超过20个字符'; return; }
  var users = getUsers();
  if (!users.includes(name)) {
    users.push(name);
    saveUsers(users);
  }
  currentUser = name;
  setCurrentUser(name);
  showHome();
}'''

new_auth = '''function handleAuth() {
  var input = document.getElementById('nicknameInput');
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
}'''

if old_auth in content:
    content = content.replace(old_auth, new_auth)
    print("handleAuth replaced successfully")
else:
    print("ERROR: handleAuth not found!")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
