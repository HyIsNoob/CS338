import json
import re

tools = set()
args_keys = {}

with open('data/valid_tool_data.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        text = data['text']
        
        # Extract ground truth JSON
        gt_match = re.search(r"<tool_call>\n(.*?)\n</tool_call>", text, re.DOTALL)
        if gt_match:
            try:
                gt_json = json.loads(gt_match.group(1).strip())
                name = gt_json.get("name")
                if name:
                    tools.add(name)
                    if name not in args_keys:
                        args_keys[name] = set()
                    for k in gt_json.get("arguments", {}).keys():
                        args_keys[name].add(k)
            except:
                pass

print("=== TOOLS IN VALID_TOOL_DATA.JSONL ===")
for t in tools:
    print(f"- Tool: {t}")
    print(f"  Arguments: {list(args_keys.get(t, []))}")
