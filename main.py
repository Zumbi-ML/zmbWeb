# -*- coding: utf-8 -*-

from app import app

server = app.server

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)
