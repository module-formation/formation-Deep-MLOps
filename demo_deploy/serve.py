from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Allows the port to be passed in as an argument
        port = sys.argv[-1]
    else:
        port = 8000

    test(CORSRequestHandler, HTTPServer, port=port)
