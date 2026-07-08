import os

old_scroll = """    <!-- Scroll To Top Button -->
    <div id="scrollToTop" class="scroll-to-top"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div>
    <script>
        const scrollToTopBtn = document.getElementById('scrollToTop');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollToTopBtn.classList.add('show');
            } else {
                scrollToTopBtn.classList.remove('show');
            }
        });
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    </script>"""

old_group = """    <!-- Floating CTA Group -->
    <div class="floating-cta-group">
        <a href="https://cafe.naver.com/f-e/cafes/10197921/members/XwxIXUHuaQZL_f4PLfDRheFGNhqU7wpcA-mnAFqEPDs" target="_blank" class="floating-cta-btn suman-btn" title="수만휘 칼럼">
            <img src="assets/cta_naver_cafe.png" alt="Naver Cafe" style="width:100%; height:100%; object-fit:cover; border-radius:50%;">
            <span class="tooltip">수만휘 칼럼</span>
        </a>
        <a href="https://open.kakao.com/o/s2o9h2Ci" target="_blank" class="floating-cta-btn kakao-btn" title="카카오톡 1:1 문의">
            <svg viewBox="0 0 24 24" fill="#3C1E1E" style="width: 55%; height: 55%;"><path d="M12 3c-5.5 0-10 3.5-10 8 0 2.6 1.4 4.8 3.6 6.3-.3 1.1-1.1 3.5-1.1 3.5s-.1.3.1.4c.2.1.5.1.5.1 1.6-.1 3.7-1.2 3.7-1.2.9.2 1.9.3 2.8.3 5.5 0 10-3.5 10-8s-4.5-8-10-8z"/></svg>
            <span class="tooltip">카카오톡 문의</span>
        </a>
        <a href="mailto:daehyunkoh@pslabedu.kr" class="floating-cta-btn email-btn" title="이메일 문의">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path></svg>
            <span class="tooltip">이메일 문의</span>
        </a>
    </div>"""

new_group = """    <!-- Floating CTA Group -->
    <div class="floating-cta-group">
        <a href="#" class="floating-cta-btn top-btn" title="맨 위로" id="scrollToTopBtn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
            <span class="tooltip">맨 위로</span>
        </a>
        <a href="https://cafe.naver.com/f-e/cafes/10197921/members/XwxIXUHuaQZL_f4PLfDRheFGNhqU7wpcA-mnAFqEPDs" target="_blank" class="floating-cta-btn suman-btn" title="수만휘 칼럼">
            <img src="assets/cta_naver_cafe.png" alt="Naver Cafe" style="width:100%; height:100%; object-fit:cover; border-radius:50%;">
            <span class="tooltip">수만휘 칼럼</span>
        </a>
        <a href="https://open.kakao.com/o/s2o9h2Ci" target="_blank" class="floating-cta-btn kakao-btn" title="카카오톡 1:1 문의">
            <svg viewBox="0 0 24 24" fill="#3C1E1E" style="width: 55%; height: 55%;"><path d="M12 3c-5.5 0-10 3.5-10 8 0 2.6 1.4 4.8 3.6 6.3-.3 1.1-1.1 3.5-1.1 3.5s-.1.3.1.4c.2.1.5.1.5.1 1.6-.1 3.7-1.2 3.7-1.2.9.2 1.9.3 2.8.3 5.5 0 10-3.5 10-8s-4.5-8-10-8z"/></svg>
            <span class="tooltip">카카오톡 문의</span>
        </a>
    </div>"""

files = ['index.html', 'songpa_index.html', 'b2b_partnership_proposal.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace(old_scroll, '')
    content = content.replace(old_scroll.replace('M12 19V5M5 12l7-7 7 7', 'm18 15-6-6-6 6'), '') # Just in case

    if f != 'b2b_partnership_proposal.html':
        content = content.replace(old_group, new_group)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Patch complete.")
