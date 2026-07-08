import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove hero-marquee-left and hero-marquee-right
def remove_tag(html, start_marker):
    start = html.find(start_marker)
    if start == -1: return html
    
    # Simple nested div counter to find the exact end of the block
    count = 0
    i = start
    while i < len(html):
        if html.startswith('<div', i):
            count += 1
        elif html.startswith('</div', i):
            count -= 1
            if count == 0:
                end = i + 6 # length of </div>
                return html[:start] + html[end:]
        i += 1
    return html

content = remove_tag(content, '<!-- Left Marquee (Mentors')
content = remove_tag(content, '<!-- Right Marquee (Local High Schools)')
content = remove_tag(content, '<div class="hero-marquee-left">')
content = remove_tag(content, '<div class="hero-marquee-right">')


# 2. Swap logo-marquee and announcement sections back to original
marquee_start = content.find('<!-- Partner & Univ Logo Marquee -->')
marquee_end = content.find('</section>', marquee_start) + 10
if marquee_start != -1:
    marquee_content = content[marquee_start:marquee_end]
    content = content[:marquee_start] + content[marquee_end:]
    
    announcement_start = content.find('<section id="announcement"')
    if announcement_start != -1:
        # Insert marquee BEFORE announcement
        content = content[:announcement_start] + marquee_content + '\n\n' + content[announcement_start:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Restored successfully.')