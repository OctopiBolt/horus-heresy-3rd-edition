from pathlib import Path
import re

path = Path("Legiones Astartes.json")
text = path.read_text(encoding="utf-8")

weapon_id = '"id": "lb-vigil-755d-985b-1f83-800c"'
start = text.find(weapon_id)
if start < 0:
    raise SystemExit("Target Vigil-pattern Heavy bolter entry not found")

costs = text.find('"costs": [', start)
if costs < 0 or costs > start + 3000:
    raise SystemExit("Target costs block not found")

value_match = re.search(r'"value":\s*(\d+)', text[costs:costs + 1000])
if not value_match:
    raise SystemExit("Point value not found")

absolute_start = costs + value_match.start(1)
absolute_end = costs + value_match.end(1)
old_value = int(value_match.group(1))

if old_value != 15:
    text = text[:absolute_start] + "15" + text[absolute_end:]

rev = re.search(r'"revision":\s*(\d+)', text)
if rev and old_value != 15:
    n = int(rev.group(1)) + 1
    text = text[:rev.start(1)] + str(n) + text[rev.end(1):]

path.write_text(text, encoding="utf-8")
print(f"Vigil Heavy bolter price: {old_value} -> 15")
