import os
import re

strings_dict = {
    "CivicResolve": "civicresolve",
    "New": "new_status",
    "Active": "active",
    "Resolved": "resolved",
    "Charts": "charts",
    "My Reports": "my_reports",
    "Community Hub": "community_hub",
    "Sort & Filter": "sort_filter",
    "Newest First": "newest_first",
    "Oldest First": "oldest_first",
    "Highest Rated": "highest_rated",
    "Most Upvotes": "most_upvotes",
    "Search issues...": "search_issues",
    "Report your first issue to get started!": "report_first_issue",
    "Your community is improving.": "your_community_is_improving",
    "Everything looks good in your area! Tap + to report a new issue and help your community.": "everything_looks_good_area_help",
    "Everything looks good in your area!\\nTap + to report a new issue.": "everything_looks_good_area_tap",
    "You're all caught up!": "you_re_all_caught_up",
    "My District": "my_district",
    "Local": "local",
    "Global Feed": "global_feed",
    "Complaints by Status": "complaints_by_status",
    "Complaints by Category": "complaints_by_category",
    "No data for pie chart": "no_data_for_pie_chart",
    "Report an Issue": "report_an_issue"
}

kt_file = "app/src/main/java/com/example/complaintportal/ui/screens/user/UserDashboardScreen.kt"

with open(kt_file, "r", encoding="utf-8") as f:
    content = f.read()

for text, key in strings_dict.items():
    if text == "New":
        content = re.sub(r'(?<![a-zA-Z])"New"(?![a-zA-Z])', f'stringResource(R.string.{key})', content)
    elif text == "Active":
        content = re.sub(r'(?<![a-zA-Z])"Active"(?![a-zA-Z])', f'stringResource(R.string.{key})', content)
    elif text == "Resolved":
        content = re.sub(r'(?<![a-zA-Z])"Resolved"(?![a-zA-Z])', f'stringResource(R.string.{key})', content)
    elif text == "Everything looks good in your area!\\nTap + to report a new issue.":
        content = content.replace('"Everything looks good in your area!\\nTap + to report a new issue."', f'stringResource(R.string.{key})')
    else:
        content = content.replace(f'"{text}"', f'stringResource(R.string.{key})')

with open(kt_file, "w", encoding="utf-8") as f:
    f.write(content)

res_file = "app/src/main/res/values/strings.xml"
with open(res_file, "r", encoding="utf-8") as f:
    res_content = f.read()

for text, key in strings_dict.items():
    if f'name="{key}"' not in res_content:
        escaped_text = text.replace("'", "\\'").replace("&", "&amp;").replace("<", "&lt;")
        res_content = res_content.replace('</resources>', f'    <string name="{key}">{escaped_text}</string>\n</resources>')

with open(res_file, "w", encoding="utf-8") as f:
    f.write(res_content)

print("Patch applied.")
