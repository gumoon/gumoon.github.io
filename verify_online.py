import sys, json, re

c = sys.stdin.read()
s = c[len("const QUESTIONS = "):].rstrip().rstrip(';')
d = json.loads(s)

q = d[8]
print('Q9 options:', list(q['options'].keys()))
print('B:', q['options']['B'])
print('C:', q['options']['C'])
print('D:', q['options']['D'])

q = d[108]
print('Q109 options:', list(q['options'].keys()))
print('A:', q['options']['A'])
print('B:', q['options']['B'])
