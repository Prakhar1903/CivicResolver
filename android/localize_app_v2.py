import os
import re
import urllib.request
import urllib.parse
import json
import concurrent.futures

def translate(text, target_lang):
    if target_lang == "en": return text
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        return "".join([x[0] for x in data[0]])
    except Exception as e:
        return text

languages = ["hi", "bn", "te", "mr", "ta", "ur", "gu", "kn", "ml", "or", "pa", "as"]
kt_dir = "app/src/main/java/com/example/complaintportal/ui"
res_dir = "app/src/main/res"

strings_to_localize = set()
for root, dirs, files in os.walk(kt_dir):
    for f in files:
        if f.endswith(".kt"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                matches = re.findall(r'"([A-Z][^"\\]*)"', content)
                for m in matches:
                    if len(m) > 2 and "{" not in m and "$" not in m and "/" not in m and "." not in m and "_" not in m:
                        strings_to_localize.add(m)

extra_strings = [
    "New", "Active", "Resolved", "Charts", "My Reports", "Community Hub", "CivicResolve",
    "Sort & Filter", "Newest First", "Oldest First", "Highest Rated", "Most Upvotes",
    "Report your first issue to get started!", "Your community is improving.", "Search issues...",
    "Everything looks good in your area! Tap + to report a new issue and help your community.",
    "Everything looks good in your area!\\nTap + to report a new issue.", "You're all caught up!"
]
for e in extra_strings:
    strings_to_localize.add(e)

print(f"Found {len(strings_to_localize)} strings to translate.")

string_dict = {}
for s in strings_to_localize:
    key = re.sub(r'[^a-zA-Z0-9]', '_', s.lower()).strip('_')
    key = re.sub(r'_+', '_', key)
    if not key: key = "str"
    if key[0].isdigit() or key == "class" or key == "return": key = "_" + key
    
    orig_key = key
    counter = 1
    while key in string_dict.values():
        key = f"{orig_key}_{counter}"
        counter += 1
    string_dict[s] = key

def merge_strings_xml(filepath, new_strings, lang="en"):
    existing = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(r'<string name="([^"]+)">([^<]*)</string>', content)
            for k, v in matches:
                existing[k] = v
                
    for s, key in new_strings.items():
        if key not in existing:
            trans = translate(s, lang) if lang != "en" else s
            existing[key] = trans.replace("'", "\\'").replace("&", "&amp;").replace("<", "&lt;")
            
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n')
        for k, v in existing.items():
            f.write(f'    <string name="{k}">{v}</string>\n')
        f.write('</resources>')

merge_strings_xml(os.path.join(res_dir, "values", "strings.xml"), string_dict, "en")

def translate_lang(lang):
    print(f"Translating to {lang}...")
    dir_path = os.path.join(res_dir, f"values-{lang}")
    merge_strings_xml(os.path.join(dir_path, "strings.xml"), string_dict, lang)
    print(f"Finished {lang}")

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(translate_lang, languages)

for root, dirs, files in os.walk(kt_dir):
    for f in files:
        if f.endswith(".kt"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            
            orig_content = content
            
            sorted_items = sorted(string_dict.items(), key=lambda x: len(x[0]), reverse=True)
            
            for s, key in sorted_items:
                search = f'"{s}"'
                replace = f'stringResource(R.string.{key})'
                if search in content:
                    content = content.replace(search, replace)

            if content != orig_content:
                if "import androidx.compose.ui.res.stringResource" not in content:
                    lines = content.split('\n')
                    last_import_idx = -1
                    for i, line in enumerate(lines):
                        if line.startswith('import '):
                            last_import_idx = i
                    if last_import_idx != -1:
                        lines.insert(last_import_idx + 1, "import androidx.compose.ui.res.stringResource")
                        lines.insert(last_import_idx + 2, "import com.example.complaintportal.R")
                        content = '\n'.join(lines)
                    else:
                        content = content.replace("package com.example.complaintportal.ui", "package com.example.complaintportal.ui\n\nimport androidx.compose.ui.res.stringResource\nimport com.example.complaintportal.R")
                
                with open(path, "w", encoding="utf-8") as file:
                    file.write(content)

print("Done with script!")
