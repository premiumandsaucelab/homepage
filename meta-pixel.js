/* Meta Pixel - 피에스랩 픽셀 (ID 2897322043983656) */
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '2897322043983656');
fbq('track', 'PageView');
document.addEventListener('click', function (e) {
  var a = e.target.closest ? e.target.closest('a[href*="open.kakao.com"]') : null;
  if (!a) return;
  var label = (a.innerText || a.getAttribute('aria-label') || a.className || 'kakao').trim().slice(0, 40);
  fbq('track', 'Lead', { content_name: label, page: location.pathname });
}, true);
