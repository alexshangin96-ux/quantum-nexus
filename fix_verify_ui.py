#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('web_app.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove excessive UI update code after button replacement
old_pattern = r'                                \}\n                                \n                                // Update task status\n                                const statusText = taskCard\.querySelector\([^)]+\);\n                                if \(statusText\) \{[^}]+\}\n                                \n                                // Add "Готово" badge if not present\n                                const header = taskCard\.querySelector\([^)]+\);\n                                if \(header && ![^}]+\}\n                                \n                                // Update card background to completed style\n                                taskCard\.style\.background = [^;]+;\n                                taskCard\.style\.borderColor = [^;]+;\n                            \}\n                            \n                            // Show brief notification\n                            if \(window\.tg && tg\.showAlert\) \{[^}]+\}'

new_pattern = '                                }'

content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)

# Remove debug alert
content = content.replace("tg.showAlert('🔍 Проверяем подписку...');", '')
content = content.replace('console.log(\'Verification response:\', data); // Debug log', '')

with open('web_app.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed: Removed excessive UI updates from verifyChannelSubscription')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('web_app.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove excessive UI update code after button replacement
old_pattern = r'                                \}\n                                \n                                // Update task status\n                                const statusText = taskCard\.querySelector\([^)]+\);\n                                if \(statusText\) \{[^}]+\}\n                                \n                                // Add "Готово" badge if not present\n                                const header = taskCard\.querySelector\([^)]+\);\n                                if \(header && ![^}]+\}\n                                \n                                // Update card background to completed style\n                                taskCard\.style\.background = [^;]+;\n                                taskCard\.style\.borderColor = [^;]+;\n                            \}\n                            \n                            // Show brief notification\n                            if \(window\.tg && tg\.showAlert\) \{[^}]+\}'

new_pattern = '                                }'

content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)

# Remove debug alert
content = content.replace("tg.showAlert('🔍 Проверяем подписку...');", '')
content = content.replace('console.log(\'Verification response:\', data); // Debug log', '')

with open('web_app.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed: Removed excessive UI updates from verifyChannelSubscription')

