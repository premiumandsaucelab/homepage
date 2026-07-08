import glob

# Read index.html to extract the popup block
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

start_marker = "<!-- Popup Modal -->"
end_marker = "<!-- Floating Action Buttons -->"

start_idx = index_content.find(start_marker)
end_idx = index_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    popup_html = index_content[start_idx:end_idx]
    
    html_files = glob.glob('*.html')
    for file in html_files:
        if file == 'index.html':
            continue
            
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        
        if "pslabPromoPopup" not in content:
            if "<!-- Floating Action Buttons -->" in content:
                content = content.replace("<!-- Floating Action Buttons -->", popup_html + "<!-- Floating Action Buttons -->")
            else:
                content = content.replace("</body>", popup_html + "</body>")
                
        if original != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added popup to {file}")

print("Done.")
