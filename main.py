# -*- coding: utf-8 -*-
# This line specifies the encoding of the Python source file to UTF-8.

from app import app
# This imports the Flask app instance from the 'app' module/package.
# 'app' is typically a Flask application object, defined in the 'app' module.

server = app.server
# This line assigns the 'server' variable to the server component of the Flask app.
# It's a way to reference the server directly, which can be useful in certain deployments.

if __name__ == "__main__":

    app.run_server(host='0.0.0.0', port=80, debug=False, use_reloader=True)
    # This line starts the Flask web server with specific parameters:
    # - host='0.0.0.0' makes the server accessible externally, listening on all network interfaces.
    # - port=80 sets the server to run on port 80, which is the default HTTP port.
    # - debug=False turns off the debug mode, which is recommended for production.
    # - use_reloader=True allows the server to restart automatically if code changes are detected.