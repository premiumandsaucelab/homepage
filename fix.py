import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update all Google form links to Apps Script link
content = re.sub(r'https://docs\.google\.com/forms/d/e/[a-zA-Z0-9_-]+/viewform\?usp=sf_link', 
                 'https://docs.google.com/forms/d/e/1FAIpQLSd-yh1RmZEtljz6Pg4IifrBh_mTQYO7jYvX-3GPfFti8hai7Q/viewform?usp=header', content)

# 2. Replace popup HTML completely
popup_start = content.find('<!-- Popup Modal -->')
if popup_start != -1:
    popup_end = content.find('</div>\n    </div>\n', popup_start) + 18
    content = content[:popup_start] + content[popup_end:]

new_popup = '''
    <!-- Popup Modal -->
    <div id="pslabPromoPopup" class="pslab-popup-overlay">
        <div class="pslab-popup-container">
            <div class="pslab-popup-body">
                <div class="pslab-popup-title">pslab 7월 수시 컨설팅 오픈</div>
                
                <div class="pslab-popup-text" style="line-height: 1.6; word-break: keep-all;">
                    <img src="assets/logo_full.png" alt="pslab" style="height: 14px; vertical-align: middle; margin-right: 4px; margin-bottom: 2px;">
                    송파·강동 학종 전문, 첫 정식 오픈<br>
                    30명 한정, <mark style="background-color: #fef08a; color: #111; padding: 0 4px; font-weight: 700; border-radius: 2px;">"현재 17자리 남음"</mark>
                </div>
                
                <div class="pslab-popup-divider"></div>

                <div class="pslab-popup-text" style="line-height: 1.7; word-break: keep-all;">
                    <strong>런칭 멤버 혜택</strong><br>
                    - 런칭 특별 플랜 "사전진단" 이용 가능<br>
                    - 런칭 혜택가 적용 <a href="#programs" onclick="document.getElementById('pslabPromoPopup').classList.remove('active')" style="color: #2563eb; font-weight: 700; text-decoration: underline; font-size: 0.95em; margin-left: 2px;">[플랜 보러가기]</a><br>
                    - 대표 멘토 직접 응대
                </div>
                
                <div class="pslab-popup-text" style="font-weight: 700; color: #1e3a8a; margin-top: 16px; font-size: 13.5px; word-break: keep-all;">
                    - 고려대, 경희대, KIST가 지원하는 pslab
                </div>

                <div class="pslab-popup-buttons">
                    <a href="https://docs.google.com/forms/d/e/1FAIpQLSd-yh1RmZEtljz6Pg4IifrBh_mTQYO7jYvX-3GPfFti8hai7Q/viewform?usp=header" target="_blank" class="pslab-popup-btn pslab-popup-btn-blue">사전 진단 신청하기</a>
                    <a href="https://open.kakao.com/o/siqpqtli" target="_blank" class="pslab-popup-btn pslab-popup-btn-kakao">카카오톡 문의하기</a>
                </div>
            </div>
            <div class="pslab-popup-footer">
                <button id="pslabPopupClose">닫기</button>
            </div>
        </div>
    </div>
'''
content = content.replace('</body>', new_popup + '\n</body>')

# 3. Move logo marquee
marquee_start = content.find('<!-- Partner & Univ Logo Marquee -->')
if marquee_start != -1:
    marquee_end = content.find('</section>', marquee_start) + 10
    marquee_content = content[marquee_start:marquee_end]
    content = content[:marquee_start] + content[marquee_end:]
    
    announcement_start = content.find('<section id="announcement"')
    announcement_end = content.find('</section>', announcement_start) + 10
    content = content[:announcement_end] + '\\n\\n    ' + marquee_content + content[announcement_end:]

# 4. Insert vertical marquees in Hero
hero_html = '''
          <!-- Left Marquee (Mentors' Universities) -->
          <div class="hero-marquee-left">
              <div class="hero-marquee-track-vertical">
                  <!-- Group 1 -->
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/snu.png" alt="서울대"></div>
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/korea_univ.svg" alt="고려대"></div>
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/hyu.png" alt="한양대"></div>
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/cau_med_logo.svg" alt="중앙대"></div>
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/kyunghee.svg" alt="경희대"></div>
                  <!-- Group 2 -->
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/snu.png" alt="서울대"></div>
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/korea_univ.svg" alt="고려대"></div>
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/hyu.png" alt="한양대"></div>
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/cau_med_logo.svg" alt="중앙대"></div>
                  <div class="hero-marquee-item grayscale-logo"><img src="assets/kyunghee.svg" alt="경희대"></div>
              </div>
          </div>
          <!-- Right Marquee (Local High Schools) -->
          <div class="hero-marquee-right">
              <div class="hero-marquee-track-vertical reverse">
                  <!-- Group 1 -->
                  <div class="hero-marquee-item"><img src="assets/deoksu_logo.svg" alt="덕수고"></div>
                  <div class="hero-marquee-item"><img src="assets/bangsan_logo.svg" alt="방산고"></div>
                  <div class="hero-marquee-item"><img src="assets/boseong_logo.png" alt="보성고"></div>
                  <div class="hero-marquee-item"><div class="placeholder-logo">영파여고</div></div>
                  <div class="hero-marquee-item"><img src="assets/ogeum_logo.webp" alt="오금고"></div>
                  <div class="hero-marquee-item"><img src="assets/jamsin_logo.webp" alt="잠신고"></div>
                  <div class="hero-marquee-item"><div class="placeholder-logo">잠실고</div></div>
                  <div class="hero-marquee-item"><div class="placeholder-logo">잠실여고</div></div>
                  <div class="hero-marquee-item"><img src="assets/changdeok_logo.jpeg" alt="창덕여고"></div>
                  <div class="hero-marquee-item"><div class="placeholder-logo">광문고</div></div>
                  <div class="hero-marquee-item"><img src="assets/dongbuk_logo.svg" alt="동북고"></div>
                  <div class="hero-marquee-item"><img src="assets/hanyoung_logo.svg" alt="한영외고"></div>
                  <!-- Group 2 -->
                  <div class="hero-marquee-item"><img src="assets/deoksu_logo.svg" alt="덕수고"></div>
                  <div class="hero-marquee-item"><img src="assets/bangsan_logo.svg" alt="방산고"></div>
                  <div class="hero-marquee-item"><img src="assets/boseong_logo.png" alt="보성고"></div>
                  <div class="hero-marquee-item"><div class="placeholder-logo">영파여고</div></div>
                  <div class="hero-marquee-item"><img src="assets/ogeum_logo.webp" alt="오금고"></div>
                  <div class="hero-marquee-item"><img src="assets/jamsin_logo.webp" alt="잠신고"></div>
                  <div class="hero-marquee-item"><div class="placeholder-logo">잠실고</div></div>
                  <div class="hero-marquee-item"><div class="placeholder-logo">잠실여고</div></div>
                  <div class="hero-marquee-item"><img src="assets/changdeok_logo.jpeg" alt="창덕여고"></div>
                  <div class="hero-marquee-item"><div class="placeholder-logo">광문고</div></div>
                  <div class="hero-marquee-item"><img src="assets/dongbuk_logo.svg" alt="동북고"></div>
                  <div class="hero-marquee-item"><img src="assets/hanyoung_logo.svg" alt="한영외고"></div>
              </div>
          </div>
'''
content = content.replace('<div class="hero-content"', hero_html + '          <div class="hero-content"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied fix script.")