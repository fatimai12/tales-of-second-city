import random
from .app import app

port = random.randint(5000, 10000)
if __name__ == '__main__':
    app.run_server(debug = True, port = port)