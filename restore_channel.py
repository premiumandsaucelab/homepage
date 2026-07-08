import glob

CHANNEL_SCRIPT = """
<!-- Channel Plugin Scripts -->
<script>
  (function(){var w=window;if(w.ChannelIO){return w.console.error("ChannelIO script included twice.");}var ch=function(){ch.c(arguments);};ch.q=[];ch.c=function(args){ch.q.push(args);};w.ChannelIO=ch;function l(){if(w.ChannelIOInitialized){return;}w.ChannelIOInitialized=true;var s=document.createElement("script");s.type="text/javascript";s.async=true;s.src="https://cdn.channel.io/plugin/ch-plugin-web.js";var x=document.getElementsByTagName("script")[0];if(x.parentNode){x.parentNode.insertBefore(s,x);}}if(document.readyState==="complete"){l();}else{w.addEventListener("DOMContentLoaded",l);w.addEventListener("load",l);}})();

  ChannelIO('boot', {
    "pluginKey": "82738e5c-744b-4a51-9e75-ed5083cb2ece"
  });
</script>
<!-- End Channel Plugin -->
"""

OLD_CSP = """<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' data: https://cdn.jsdelivr.net https://fonts.gstatic.com; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'self';">"""
NEW_CSP = """<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://*.channel.io; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' data: https://cdn.jsdelivr.net https://fonts.gstatic.com; connect-src 'self' https://*.channel.io wss://*.channel.io; frame-src 'self' https://*.channel.io; object-src 'none'; base-uri 'self';">"""

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # Replace CSP
    if OLD_CSP in content:
        content = content.replace(OLD_CSP, NEW_CSP)
        
    # Inject Channel Plugin Scripts
    if "ChannelIO" not in content:
        content = content.replace("</body>", CHANNEL_SCRIPT + "\\n</body>")
        
    # Shrink Naver SVG from 24 to 18
    if '<svg width="24" height="24" viewBox="0 0 33 33"' in content:
        content = content.replace('<svg width="24" height="24" viewBox="0 0 33 33"', '<svg width="18" height="18" viewBox="0 0 33 33"')
        
    if original != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Restored Channel Talk and reduced Naver SVG size.")
