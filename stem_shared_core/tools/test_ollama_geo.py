import urllib.request
import json
import re

prompt = """You are a geometric CAD parser. Convert the user request into a JSON list of geometric actions.
Available actions:
[
  {"action": "triangle_right", "at": "A", "points": ["A", "B", "C"]},
  {"action": "triangle_equilateral", "points": ["A", "B", "C"]},
  {"action": "triangle_general", "points": ["A", "B", "C"]},
  {"action": "altitude", "from": "A", "to": "BC", "name": "H"},
  {"action": "median", "from": "A", "to": "BC", "name": "M"},
  {"action": "incenter", "triangle": ["A", "B", "C"], "name": "I"},
  {"action": "circumcenter", "triangle": ["A", "B", "C"], "name": "O"}
]

User request: "Cho tam giác ABC vuông tại A, vẽ đường cao AH và tâm đường tròn nội tiếp I"

Return ONLY the raw JSON array. Do not include markdown codeblocks or thinking tags in your final answer if possible, or put JSON inside [ ... ]."""

data = {
    'model': 'deepseek-r1:1.5b',
    'prompt': prompt,
    'stream': False,
    'options': {'temperature': 0.1}
}

req = urllib.request.Request(
    'http://localhost:11434/api/generate',
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        raw_out = res.get('response', '')
        print('Raw Response:')
        print(raw_out)
except Exception as e:
    print('Error:', e)
