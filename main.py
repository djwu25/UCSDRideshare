from website import create_app
from os import environ

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)