from http.server import BaseHTTPRequestHandler
import subprocess

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Executa o Streamlit em background
        subprocess.Popen([
            "streamlit", 
            "run", 
            "../main.py",
            "--server.port=8501",
            "--server.headless=true"
        ])
        
        self.wfile.write(b"Streamlit app is starting...")