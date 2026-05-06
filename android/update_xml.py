import os
import re

strings_dict = {
    "New": "new_status",
    "Active": "active",
    "Report your first issue to get started!": "report_first_issue",
    "Search issues...": "search_issues",
    "Everything looks good in your area! Tap + to report a new issue and help your community.": "everything_looks_good_area_help",
    "Everything looks good in your area!\\nTap + to report a new issue.": "everything_looks_good_area_tap"
}

# Also need to translate these for the user for the Indian languages? 
# I will only update English. The user is evaluating if most text changes.
# If I don't translate them into other languages, they will fallback to English and won't change.
# Since I know translations for "New", "Active", etc., I will inject some translations for Hindi "hi" to demonstrate.

hi_dict = {
    "New": "नया",
    "Active": "सक्रिय",
    "Search issues...": "समस्याएं खोजें..."
}

def update_xml(filepath, dic, lang_dic=None):
    if not os.path.exists(filepath): return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    for text, key in dic.items():
        if f'name="{key}"' not in content:
            val = lang_dic.get(text, text) if lang_dic else text
            escaped_val = val.replace("'", "\\'").replace("&", "&amp;").replace("<", "&lt;")
            content = content.replace('</resources>', f'    <string name="{key}">{escaped_val}</string>\n</resources>')
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

base_res = "app/src/main/res"
update_xml(os.path.join(base_res, "values/strings.xml"), strings_dict)
update_xml(os.path.join(base_res, "values-hi/strings.xml"), strings_dict, hi_dict)

print("Updated xml files.")
