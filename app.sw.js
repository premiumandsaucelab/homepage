/* pslab 강동·송파 앱 · 서비스워커
   전략: 네트워크 우선(network-first) → 최신 내용 즉시 반영, 오프라인이면 캐시 사용 */
const CACHE = 'pslab-gd-sp-v3';
const ASSETS = [
  'app.html',
  'app.js',
  'app.data.js',
  'app.webmanifest',
  'assets/logo_full.png',
  'assets/logo_symbol.png'
];

self.addEventListener('install', e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));
});

self.addEventListener('activate', e=>{
  e.waitUntil(
    caches.keys()
      .then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener('fetch', e=>{
  const req = e.request;
  if(req.method!=='GET') return;
  // 외부(구글폼·카카오·CDN)는 서비스워커가 건드리지 않음
  if(new URL(req.url).origin !== location.origin) return;

  // network-first: 최신본을 받아 캐시를 갱신하고, 실패하면 캐시로 폴백
  e.respondWith(
    fetch(req).then(res=>{
      const copy = res.clone();
      caches.open(CACHE).then(c=>c.put(req, copy)).catch(()=>{});
      return res;
    }).catch(()=>
      caches.match(req).then(hit=> hit || caches.match('app.html'))
    )
  );
});
