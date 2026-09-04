import re

with open('/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/index.html', 'r') as f:
    content = f.read()

# The file has duplicate code blocks. Let's fix the specific sections.
# Strategy: remove the orphaned code fragments that appear after their correct function definitions.

# Fix 1: After correct getUsers(), there are two duplicate fragments and a duplicate saveUsers
# Remove: the orphaned try blocks and duplicate saveUsers after the first one

# Pattern 1: Remove the two getUsers duplicate fragments and the duplicate saveUsers after them
# The correct sequence is: getUsers() { ... } -> saveUsers(...)
# The damaged part adds: orphaned try block -> orphaned try block -> duplicate saveUsers
pattern1 = r"(function getUsers\(\) \{\s*try \{\s*var data = JSON\.parse\(localStorage\.getItem\(LS_USERS\) \|\| '\\[]'\);\s*return Array\.isArray\(data\) \? data : \[\];\s*\} catch\(e\) \{ return \[\]; \}\s*\}\s*function saveUsers\(users\) \{ localStorage\.setItem\(LS_USERS, JSON\.stringify\(users\)\); \})\s*try \{\s*var data = JSON\.parse\(localStorage\.getItem\(LS_USERS\) \|\| '\\[]'\);\s*return Array\.isArray\(data\) \? data : \[\];\s*\} catch\(e\) \{ return \[\]; \}\s*\}\s*try \{ return JSON\.parse\(localStorage\.getItem\(LS_USERS\) \|\| '\\[]'\); \} catch\(e\) \{ return \[\]; \}\s*\}\s*function saveUsers\(users\) \{ localStorage\.setItem\(LS_USERS, JSON\.stringify\(users\)\); \}"
replacement1 = r"\1"
content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)

# Fix 2: After correct getWrong(), there is a duplicate fragment
pattern2 = r"(function getWrong\(u\) \{\s*try \{\s*var data = JSON\.parse\(localStorage\.getItem\(LS_WRONG\(u\)\) \|\| '\\[]'\);\s*return Array\.isArray\(data\) \? data : \[\];\s*\} catch\(e\) \{ return \[\]; \}\s*\})\s*try \{ return JSON\.parse\(localStorage\.getItem\(LS_WRONG\(u\)\) \|\| '\\[]'\); \} catch\(e\) \{ return \[\]; \}\s*\}"
replacement2 = r"\1"
content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

# Fix 3: After correct getExamHistory(), there is a duplicate fragment  
pattern3 = r"(function getExamHistory\(u\) \{\s*try \{\s*var data = JSON\.parse\(localStorage\.getItem\(LS_EXAM_HISTORY\(u\)\) \|\| '\\[]'\);\s*return Array\.isArray\(data\) \? data : \[\];\s*\} catch\(e\) \{ return \[\]; \}\s*\})\s*try \{ return JSON\.parse\(localStorage\.getItem\(LS_EXAM_HISTORY\(u\)\) \|\| '\\[]'\); \} catch\(e\) \{ return \[\]; \}\s*\}"
replacement3 = r"\1"
content = re.sub(pattern3, replacement3, content, flags=re.DOTALL)

# Fix 4: After correct handleAuth(), there is a duplicate fragment (old handleAuth body without function declaration)
pattern4 = r"(function handleAuth\(\) \{\s*var input = document\.getElementById\('nicknameInput'\);\s*var error = document\.getElementById\('authError'\);\s*error\.textContent = '';\s*var name = input\.value\.trim\(\);\s*if \(!name\) \{ error\.textContent = '请输入昵称'; return; \}\s*if \(name\.length > 50\) \{ error\.textContent = '昵称不能超过50个字符'; return; \}\s*// 必须以字母开头（支持中英文等Unicode字母），只能包含字母和数字\s*var validRegex = /\^\[\\\\p\{L\}\]\[\\\\p\{L\}\\\\p\{N\}\]\*\$/u;\s*if \(!validRegex\.test\(name\)\) \{\s*error\.textContent = '昵称需以字母开头，且仅包含字母和数字';\s*return;\s*\}\s*try \{\s*var users = getUsers\(\);\s*if \(!users\.includes\(name\)\) \{\s*users\.push\(name\);\s*saveUsers\(users\);\s*\}\s*currentUser = name;\s*setCurrentUser\(name\);\s*showHome\(\);\s*\} catch\(e\) \{\s*error\.textContent = '登录失败，请检查浏览器是否开启了隐私模式或禁用了本地存储';\s*console\.error\('Auth error:', e\);\s*\}\s*\})\s*var input = document\.getElementById\('nicknameInput'\);\s*var error = document\.getElementById\('authError'\);\s*var name = input\.value\.trim\(\);\s*if \(!name\) \{ error\.textContent = '请输入昵称'; return; \}\s*if \(name\.length > 50\) \{ error\.textContent = '昵称不能超过50个字符'; return; \}\s*// 必须以字母开头（支持中英文等Unicode字母），只能包含字母和数字\s*var validRegex = /\^\[\\\\p\{L\}\]\[\\\\p\{L\}\\\\p\{N\}\]\*\$/u;\s*if \(!validRegex\.test\(name\)\) \{\s*error\.textContent = '昵称需以字母开头，且仅包含字母和数字';\s*return;\s*\}\s*var users = getUsers\(\);\s*if \(!users\.includes\(name\)\) \{\s*users\.push\(name\);\s*saveUsers\(users\);\s*\}\s*currentUser = name;\s*setCurrentUser\(name\);\s*showHome\(\);\s*\}"

# The regex above is too complex and fragile due to escaping. Let's use a simpler text-based approach.
# Actually, let me just use a simpler string replacement approach.

with open('/Users/zyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/lmcc-quiz/lmcc-quiz/index.html', 'w') as f:
    f.write(content)

print("Attempted regex fix")
PYEOF