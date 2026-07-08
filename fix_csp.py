import glob

OLD_CSP = """<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' data: https://cdn.jsdelivr.net https://fonts.gstatic.com; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'self';">"""
NEW_CSP = """<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://*.channel.io; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' data: https://cdn.jsdelivr.net https://fonts.gstatic.com; connect-src 'self' https://*.channel.io wss://*.channel.io; frame-src 'self' https://*.channel.io; object-src 'none'; base-uri 'self';">"""

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    if OLD_CSP in content:
        content = content.replace(OLD_CSP, NEW_CSP)
    elif "https://*.channel.io" not in content:
        print(f"Warning: CSP might be different in {file}")
        
    if original != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSP in {file}")

print("Done.")
