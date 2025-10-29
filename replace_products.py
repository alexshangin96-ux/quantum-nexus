#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
import re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read the generated HTML
with open('all_60_products.html', 'r', encoding='utf-8') as f:
    new_products = f.read()

# Read web_app.html
with open('web_app.html', 'r', encoding='utf-8') as f:
    web_app = f.read()

# Find the products section and replace it
# The products start after "<!-- CATEGORY 1:" and end before "</div>" closing the currencyProductsList
start_marker = '<!-- CATEGORY 1:'
end_marker = '</div>\n                    </div>\n                    </div>'

# Find the position of the start marker
start_pos = web_app.find(start_marker)
if start_pos == -1:
    print("❌ Не найден маркер начала товаров")
    exit(1)

# Find the position where currencyProductsList div closes
products_list_start = web_app.find('<div id="currencyProductsList"', start_pos)
if products_list_start == -1:
    print("❌ Не найден currencyProductsList")
    exit(1)

# Find the closing div for currencyProductsList (we need to find the right one)
# Look for the pattern: </div> followed by 2 more </div> tags
pattern = r'</div>\s+</div>\s+</div>'
matches = list(re.finditer(pattern, web_app[products_list_start:]))
if not matches:
    print("❌ Не найден конец currencyProductsList")
    exit(1)

end_pos = products_list_start + matches[-1].end()

# Extract what comes before and after
before = web_app[:start_pos]
after = web_app[end_pos:]

# Reconstruct with new products
new_web_app = before + '<div id="currencyProductsList" style="display:flex;flex-direction:column;gap:8px;max-height:450px;overflow-y:auto;padding-right:5px;">\n' + new_products + '                    </div>\n                    </div>\n                    </div>' + after

# Save
with open('web_app.html', 'w', encoding='utf-8') as f:
    f.write(new_web_app)

print("✅ Товары обновлены в web_app.html")

