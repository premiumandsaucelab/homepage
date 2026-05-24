// script.js — 손용주 학생 리포트 (용남고 3학년)

document.addEventListener('DOMContentLoaded', () => {
    // ─── Chart.js — 내신 추이 ───
    const ctx = document.getElementById('gradeChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1학년 1학기', '1학년 2학기', '2학년 1학기', '2학년 2학기'],
            datasets: [{
                label: '내신 등급',
                data: [1.92, 1.75, 1.80, 1.92],
                borderColor: '#002F6C',
                backgroundColor: 'rgba(0, 47, 108, 0.08)',
                borderWidth: 3,
                pointBackgroundColor: ['#64748B', '#002F6C', '#002F6C', '#E11D48'],
                pointBorderColor: '#fff',
                pointBorderWidth: 2.5,
                pointRadius: 7,
                fill: true,
                tension: 0.35
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    reverse: true,
                    min: 1.4,
                    max: 2.4,
                    ticks: {
                        stepSize: 0.2,
                        callback: v => v.toFixed(1) + '등급',
                        font: { family: 'Pretendard', size: 12 }
                    },
                    grid: { color: '#F1F5F9' }
                },
                x: {
                    ticks: { font: { family: 'Pretendard', size: 11 } },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => `${ctx.parsed.y}등급`,
                        title: items => items[0].label
                    },
                    bodyFont: { family: 'Pretendard' },
                    titleFont: { family: 'Pretendard' }
                }
            }
        }
    });
});

// ─── Popup Data ───
const popupData = {
    mentor1: {
        title: '전동훈 멘토 — 한양대 공과대학 26학번',
        desc: `<strong>합격 대학</strong><br>
            한양대 공과대학 · 성균관대 공과대학 (모두 학종 합격)<br><br>
            <strong>내신 궤적</strong><br>
            2.25 → 2.05 → 1.75 (총 평균 2.1등급)<br><br>
            <strong>전문 분야</strong><br>
            공학 계열 생기부 설계 · 이공계 세특 스토리 기획 · 건설/환경 공학 입시 전략<br><br>
            <strong>핵심 메시지</strong><br>
            "저와 용주 학생의 내신 차이는 0.25등급입니다. 그 차이를 만든 건 세특 하나였습니다. 수과학 1등급 위에 공학적 탐구가 완성되는 순간, 입학사정관은 그 서류를 내려놓지 못합니다."`
    },
    mentor2: {
        title: '고대현 멘토 — 경희대 이과대학 26학번',
        desc: `<strong>합격 대학</strong><br>
            경희대 이과대학 · 아주대 교통시스템공학과 (학종 합격)<br><br>
            <strong>내신 궤적</strong><br>
            2.7 → 2.6 → 3.0 (총 평균 2.7등급)<br><br>
            <strong>핵심 메시지</strong><br>
            "합격의 핵심은 생기부 디자인입니다. 농어촌·고른기회 전형이 왜 기회의 땅인지, 면접에서 무엇이 갈리는지 — 직접 겪은 경험으로 알려드립니다."`
    },
    team_kyoho: {
        title: '김호민 — 서울대 경제학부 26학번',
        desc: `<strong>주요 합격 실적</strong><br>
            서울대 경제학부 · 고려대 전자전기공학부 차석 · 한양대 인터칼리지 수석<br><br>
            <strong>전문 영역</strong><br>
            정시 전략 · 수학 집중 보완 · 최상위권 수시 서류 전략<br><br>
            <em>PS:LAB 내 수능/정시 전략 총괄</em>`
    },
    team_junhwan: {
        title: '유준환 — 고려대 경영학부 26학번',
        desc: `<strong>합격 대학</strong><br>
            고려대 경영학부 · 연세대 경영학과 · 서강대 경제학과 · 성균관대 경영학과<br><br>
            <strong>내신 궤적</strong><br>
            2.7 → 1.4 (우상향) · PS:LAB 공동 창립<br><br>
            <em>PS:LAB 내 인문계열 컨설팅 담당</em>`
    },
    team_jewook: {
        title: '배제욱 — 한양대 자연과학대학 26학번',
        desc: `<strong>역할</strong><br>
            PS:LAB 자연과학계열 자문위원<br><br>
            <strong>전문 영역</strong><br>
            자연과학 계열 진로 설계 · 탐구 주제 고도화<br><br>
            <em>PS:LAB 내 자연과학 계열 전문 자문 담당</em>`
    },
    action1: {
        title: '탐구 1 — GPR 기반 스마트 지하 인프라 안전진단 시스템 설계',
        desc: `<strong>연계 과목:</strong> 물리학 / 건설·토목 공학 연계<br><br>
            <strong>탐구 배경</strong><br>
            2학년 물리학Ⅰ에서 GPR의 파동 반사·굴절 원리를 탐구한 경험을 발전시켜, 실제 도시 지하 인프라(지하철·상수도관·전력 케이블)의 균열을 탐지하는 스마트 모니터링 시스템 설계안을 작성합니다.<br><br>
            <strong>탐구 방법</strong><br>
            1. GPR 장비 원리 수식 기반 분석 (파동 반사·굴절 법칙)<br>
            2. 실제 도시 지하 구조물 균열 탐지 사례 2건 선정·분석<br>
            3. AI 센서 융합 모니터링 시스템 개선안 도출<br>
            4. 소논문 A4 2매 또는 탐구 포스터<br><br>
            <strong>세특 활용법</strong><br>
            물리학 세특에 '파동 심화 + 공학 적용'으로 기재. 기술·가정 3D 모델링과 연계해 '시스템 설계 능력'을 동시 어필. 고려대·한양대 면접의 '탐구 경험' 질문에 대응 가능.`
    },
    action2: {
        title: '탐구 2 — 스마트 수처리 시스템과 이온교환수지 정책 제안',
        desc: `<strong>연계 과목:</strong> 화학Ⅰ / 환경공학 연계<br><br>
            <strong>탐구 배경</strong><br>
            2학년 화학 세특에서 제안한 스마트 수처리 + 킬레이팅 수지 아이디어를 실제 국내 폐수처리장 운영 현황과 비교·분석합니다.<br><br>
            <strong>탐구 방법</strong><br>
            1. 이온교환수지 원리와 폐수 처리 적용 사례 정리<br>
            2. 국내 폐수처리장 수질 기준과 현행 기술의 한계 분석<br>
            3. AI 센서 기반 실시간 수질 모니터링 도입 정책 제안서 작성<br><br>
            <strong>세특 활용법</strong><br>
            화학 세특에 '화학 이론→실제 정책 적용' 형식으로 기재. 고려대 환경공학과 면접 소재로 강력 활용.`
    },
    action3: {
        title: '탐구 3 — 도시 열섬 현상 통계 모델링과 쿨루프 정책 효과 예측',
        desc: `<strong>연계 과목:</strong> 확률과 통계 / 도시환경 데이터 분석<br><br>
            <strong>탐구 배경</strong><br>
            2학년 쿨루프·투수성 포장 시연 경험을 발전시켜, 통계 모델을 적용해 도시 열섬 완화 효과를 정량적으로 예측하는 분석 보고서를 작성합니다.<br><br>
            <strong>탐구 방법</strong><br>
            1. 기상청·서울시 공공 데이터에서 도시별 온도 데이터 수집<br>
            2. 이항분포/정규분포로 쿨루프 설치 면적별 온도 감소 예측 모델링<br>
            3. 정책 권고안 형태로 결론 도출<br><br>
            <strong>세특 활용법</strong><br>
            확통 세특에 '통계 → 환경 정책 데이터 분석'으로 기재. 시립대·연세대 도시공학과 면접 소재로 최적.`
    },
    action4: {
        title: '설계 — 스마트 그린 주거 모델 3D 설계 및 에너지 분석',
        desc: `<strong>연계 과목:</strong> 기술·가정 / 물리학(에너지) 연계<br><br>
            <strong>탐구 배경</strong><br>
            2학년 기술·가정 세특에서 완성한 2층 주택 3D 모델링을 발전시켜, 태양광·고성능 단열재·스마트 모션 센서를 결합한 저에너지 스마트 주거 설계안을 완성합니다.<br><br>
            <strong>탐구 방법</strong><br>
            1. 저에너지 주거 설계 기준 조사 (패시브하우스 기준 참고)<br>
            2. 태양광 발전량·단열 효율 계산 (물리학 에너지 공식 연계)<br>
            3. 스마트홈 IoT 연결 설계 포함<br>
            4. 최종 3D 모델 + A4 2매 보고서<br><br>
            <strong>세특 활용법</strong><br>
            기술·가정 세특에 '설계 역량 + 에너지 공학 융합'으로 기재. 건설환경공학부의 직접적 전공 역량 증빙.`
    },
    action5: {
        title: '독서 계획 — 도시공학 연계 독서 2권 & 세특 직접 적용',
        desc: `<strong>왜 중요한가?</strong><br>
            공학계 독서는 '원리 이해'보다 '비판적 적용'을 보여줘야 입학사정관이 주목합니다.<br><br>
            <strong>추천 도서</strong><br>
            · <em>『스마트시티, 더 나은 도시를 만들다』</em> — 블루 어바니즘 탐구 심화 연계<br>
            · <em>『도시의 생존』 (에드워드 글레이저)</em> — 도시 경제학·공학적 시선<br>
            · <em>『기후변화의 경제학』</em> — 환경공학·정책 데이터 탐구 연계<br><br>
            <strong>세특 적용 방법</strong><br>
            독서록 A4 1매 작성 → 확통·물리·화학 세특 담당 선생님 제출 → '독서를 통해 확장된 공학적 관점'으로 기재 요청.`
    },
    action6: {
        title: '수능 전략 — 탐구 과목 집중 관리와 수능 최저 확립',
        desc: `<strong>왜 지금인가?</strong><br>
            현재 수능 성적으로는 상위권 최저 기준이 다소 빡빡합니다. 홍익대 최저(2합5)를 달성하면 수시 카드 전략이 극적으로 확장됩니다.<br><br>
            <strong>수능 최저 목표 설정</strong><br>
            · 1순위: 홍익대 학종 최저 2합5 (안정 확보)<br>
            · 2순위: 고려대 학우 전형 4합8 (수능 성적 향상 시)<br><br>
            <strong>실행 전략</strong><br>
            · 매주 토요일 수능 실전 시간표 응시 (국·수·영·탐)<br>
            · 탐구 과목(물리/화학) 3학년 개념 완성 우선 배치<br>
            · 3월 학평 성적 PS:LAB 공유 → 전형 전략 최종 확정`
    }
};

function openPopup(id) {
    const data = popupData[id];
    if (!data) return;

    document.getElementById('modalBody').innerHTML = `
        <h3 class="popup-title">${data.title}</h3>
        <p class="popup-desc">${data.desc}</p>
    `;
    document.getElementById('popupModal').classList.add('active');
}

function closePopup(e, force = false) {
    if (force || e.target.id === 'popupModal') {
        document.getElementById('popupModal').classList.remove('active');
    }
}

// ─── Scroll animation ───
const sections = document.querySelectorAll('.report-section, .toc-section');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s cubic-bezier(0.16,1,0.3,1) both';
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.08 });

sections.forEach(sec => {
    sec.style.opacity = '0';
    observer.observe(sec);
});
