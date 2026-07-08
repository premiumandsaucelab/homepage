import glob
import re

APP_SCRIPT = "https://docs.google.com/forms/d/e/1FAIpQLSd-yh1RmZEtljz6Pg4IifrBh_mTQYO7jYvX-3GPfFti8hai7Q/viewform?usp=header"
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSd-yh1RmZEtljz6Pg4IifrBh_mTQYO7jYvX-3GPfFti8hai7Q/viewform?usp=header"

# 1. Replace Links and "사전신청"
for file in glob.glob('*.html') + glob.glob('*.js') + glob.glob('*.py'):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        # Replace links
        content = content.replace(APP_SCRIPT, GOOGLE_FORM)
        
        # Replace text in HTML files only
        if file.endswith('.html'):
            content = content.replace('사전신청', '신청')
            content = content.replace('사전 신청', '신청')
            
        if original != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
    except:
        pass

# 2. Append CSS
css_add = """
/* Floating Action Buttons */
.floating-action-buttons {
    position: fixed;
    bottom: 90px;
    right: 24px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    z-index: 9999;
    align-items: flex-end;
}
.fab-btn-container {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}
.fab-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    text-decoration: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.2s, box-shadow 0.2s;
}
.fab-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}
.fab-btn.naver-cafe { background-color: #03c75a; }
.fab-btn.kakao { background-color: #FEE500; }
.fab-btn-label {
    position: absolute;
    right: 64px;
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.2s, visibility 0.2s;
    pointer-events: none;
}
.fab-btn-container:hover .fab-btn-label { opacity: 1; visibility: visible; }
/* Scroll to Top Button */
.scroll-top-btn {
    position: fixed;
    bottom: 30px;
    right: 96px;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background-color: white;
    color: #333;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    cursor: pointer;
    z-index: 9998;
    opacity: 0;
    visibility: hidden;
    transform: translateY(10px);
    transition: all 0.3s ease;
    border: none;
    outline: none;
}
.scroll-top-btn.show { opacity: 1; visibility: visible; transform: translateY(0); }
.scroll-top-btn:hover { background-color: #f1f5f9; box-shadow: 0 6px 16px rgba(0,0,0,0.2); transform: translateY(-2px); }
.scroll-top-btn svg { width: 24px; height: 24px; }
@media (max-width: 768px) {
    .floating-action-buttons { bottom: 80px; right: 16px; }
    .fab-btn { width: 48px; height: 48px; }
    .scroll-top-btn { bottom: 20px; right: 86px; width: 48px; height: 48px; }
}
"""
with open('styles.css', 'a', encoding='utf-8') as f:
    f.write(css_add)

# 3. Append HTML to index.html and songpa_index.html
html_add = """    <!-- Floating Action Buttons -->
    <div class="floating-action-buttons">
        <div class="fab-btn-container">
            <span class="fab-btn-label">네이버 카페</span>
            <a href="https://cafe.naver.com/f-e/cafes/10197921/members/XwxIXUHuaQZL_f4PLfDRheFGNhqU7wpcA-mnAFqEPDs?tab=articles" target="_blank" class="fab-btn naver-cafe">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16.14 15.02L9.46 5.86H4.2V18.14H9.06V8.98L15.74 18.14H21V5.86H16.14V15.02Z" fill="white"/></svg>
            </a>
        </div>
        <div class="fab-btn-container">
            <span class="fab-btn-label">카카오톡 문의</span>
            <a href="https://open.kakao.com/o/s2o9h2Ci" target="_blank" class="fab-btn kakao">
                <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 4c-4.97 0-9 3.185-9 7.115 0 2.557 1.707 4.8 4.27 5.965-.136.467-.487 1.68-.56 1.966-.088.35.122.342.26.246.108-.076 1.7-1.127 2.39-1.583.842.235 1.733.36 2.64.36 4.97 0 9-3.185 9-7.115S16.97 4 12 4z" fill="#3C1E1E"/></svg>
            </a>
        </div>
    </div>
    <!-- Scroll to Top Button -->
    <button class="scroll-top-btn" id="scrollTopBtn" title="위로 가기">
        <svg fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5"></path></svg>
    </button>
    <script>
        (function() {
            const btn = document.getElementById('scrollTopBtn');
            if (btn) {
                window.addEventListener('scroll', () => { if (window.scrollY > 300) btn.classList.add('show'); else btn.classList.remove('show'); });
                btn.addEventListener('click', () => { window.scrollTo({ top: 0, behavior: 'smooth' }); });
            }
        })();
    </script>
</body>"""

for fname in ['index.html', 'songpa_index.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if "floating-action-buttons" not in content:
        content = content.replace("</body>", html_add)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)

# 4. Fix section order in songpa_index.html
with open('songpa_index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = '<section id="announcement" class="section announcement-section bg-light reveal">'
end_str = '</section>'
start_idx = content.find(start_str)
target_str = '<section class="section pain-point-section bg-dark text-center"'
target_idx = content.find(target_str)

if start_idx != -1 and target_idx != -1 and start_idx > target_idx:
    end_idx = content.find(end_str, start_idx) + len(end_str)
    announcement_block = content[start_idx:end_idx]
    content = content[:start_idx] + content[end_idx:]
    target_idx = content.find(target_str) # Recalculate after removal
    content = content[:target_idx] + announcement_block + '\\n\\n' + content[target_idx:]
    with open('songpa_index.html', 'w', encoding='utf-8') as f:
        f.write(content)
