import re

with open('app/src/main/java/com/example/complaintportal/ui/screens/AuthScreens.kt', 'r') as f:
    content = f.read()

# Remove the color definitions
content = re.sub(r'private val Slate.*?\n', '', content)
content = re.sub(r'private val BgColor.*?\n', '', content)

# Buttons
content = content.replace(
    'containerColor = Slate900,\n                contentColor = Color.White',
    'containerColor = MaterialTheme.colorScheme.primary,\n                contentColor = MaterialTheme.colorScheme.onPrimary'
)

content = content.replace(
    'containerColor = Slate200,\n                contentColor = Slate900',
    'containerColor = MaterialTheme.colorScheme.surfaceVariant,\n                contentColor = MaterialTheme.colorScheme.onSurfaceVariant'
)

# Text Buttons
content = content.replace(
    'containerColor = Slate200,\n                    contentColor = Slate900',
    'containerColor = MaterialTheme.colorScheme.surfaceVariant,\n                    contentColor = MaterialTheme.colorScheme.onSurfaceVariant'
)

# AuthTextField
content = content.replace('unfocusedContainerColor = Color.White', 'unfocusedContainerColor = MaterialTheme.colorScheme.surface')

# Social Login
content = content.replace('color = Color.White', 'color = MaterialTheme.colorScheme.surface')
content = content.replace('border = BorderStroke(1.dp, Color(0xFFF1F5F9))', 'border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)')

# Everything else
content = content.replace('BgColor', 'MaterialTheme.colorScheme.background')
content = content.replace('Slate900', 'MaterialTheme.colorScheme.onBackground')
content = content.replace('Slate700', 'MaterialTheme.colorScheme.onSurfaceVariant')
content = content.replace('Slate500', 'MaterialTheme.colorScheme.outline')
content = content.replace('Slate300', 'MaterialTheme.colorScheme.outlineVariant')
content = content.replace('Slate200', 'MaterialTheme.colorScheme.surfaceVariant')

with open('app/src/main/java/com/example/complaintportal/ui/screens/AuthScreens.kt', 'w') as f:
    f.write(content)
