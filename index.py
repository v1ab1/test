import http.server
import socketserver

PORT = 1337

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/auth' or self.path == '/auth/doctor' or self.path == '/auth/HEAD' or self.path == '/auth/HR':
            self.path = '/index.html'
        if self.path == '/profile' or self.path == '/calendar' or self.path == '/job' or self.path == '/detect' or self.path == '/doctors':
            self.path = '/index.html'
        if self.path == '/add_doctors' or self.path == 'absence' or self.path == 'absence/add' or self.path == '/settings':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Запускаем HTTP-сервер с нашим пользовательским обработчиком запросов
with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print("Сервер запущен на порту", PORT)
    httpd.serve_forever()
