import os
import re

kt_dir = "app/src/main/java/com/example/complaintportal/ui"
found_strings = set()

for root, dirs, files in os.walk(kt_dir):
    for f in files:
        if f.endswith(".kt"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                # Find all string literals
                # matches = re.findall(r'"([^"\\]*)"', content)
                # To be safer, we can use a more precise regex:
                matches = re.findall(r'"([A-Z][^"\\]*)"', content)
                for m in matches:
                    if len(m) > 2 and "{" not in m and "$" not in m and "/" not in m and "." not in m and "_" not in m:
                        found_strings.add(m)

for s in found_strings:
    print(s)
