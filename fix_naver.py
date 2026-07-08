import glob
import re

new_svg = '<svg width="18" height="18" viewBox="0 0 33 33" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21.2 16.3L9.3 0H0V33H9.7V16.7L21.6 33H33V0H21.2V16.3Z" fill="white"/></svg>'

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # We will use regex to find the SVG block inside the "fab-btn naver-cafe" anchor tag
    # The pattern should match <svg ...> ... </svg> right after naver-cafe">
    
    # Actually, a simpler regex just matching the old SVG structure:
    pattern = r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www\.w3\.org/2000/svg">\s*<path d="M16\.14 15\.02L9\.46 5\.86H4\.2V18\.14H9\.06V8\.98L15\.74 18\.14H21V5\.86H16\.14V15\.02Z" fill="white"/>\s*</svg>'
    
    content = re.sub(pattern, new_svg, content)
    
    if original != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
