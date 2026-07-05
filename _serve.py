from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
class NoCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        super().end_headers()
ThreadingHTTPServer(("0.0.0.0", 8931), NoCache).serve_forever()
