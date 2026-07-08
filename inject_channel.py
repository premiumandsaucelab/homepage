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

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    if "ChannelIO" not in content:
        # inject before popup modal if it exists, otherwise before </body>
        if "<!-- Popup Modal -->" in content:
            content = content.replace("<!-- Popup Modal -->", CHANNEL_SCRIPT + "\n    <!-- Popup Modal -->")
        else:
            content = content.replace("</body>", CHANNEL_SCRIPT + "\n</body>")
            
    if original != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added Channel Talk to {file}")

print("Done injecting channel talk.")
