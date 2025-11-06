#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read all_60_products.html
with open('all_60_products.html', 'r', encoding='utf-8') as f:
    new_products = f.read()

# Read web_app.html
with open('web_app.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start and end of the products section
start_marker = '<div id="currencyProductsList"'
end_marker = '</div>\n                    </div>'

# Find start position
start_pos = content.find(start_marker)
if start_pos == -1:
    print("❌ Не найден currencyProductsList")
    exit(1)

# Find the opening div and the content after it
opening_tag_end = content.find('>', start_pos) + 1
line_after_opening = content.find('\n', opening_tag_end)

# Find the second closing </div> after currencyProductsList starts
# We need to find: </div> (closes currencyProductsList) followed by </div> (closes parent)
pos = content.find('</div>', line_after_opening)
next_div_end = content.find('</div>', pos + 6)

# Extract before and after
before = content[:line_after_opening + 1]
after = content[next_div_end + 6:]

# Reconstruct
new_content = before + new_products + '                    </div>'

# Save
with open('web_app.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ web_app.html обновлён со всеми 60 карточками!")
print("📝 Теперь добавьте файлы в Git и отправьте на сервер")










