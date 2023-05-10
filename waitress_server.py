from waitress import serve
from main import app

if __name__ == '__main__':
    serve(app.server, host='0.0.0.0', port=8050)
