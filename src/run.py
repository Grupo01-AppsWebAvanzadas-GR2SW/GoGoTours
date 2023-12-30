from flask import Flask
from infrastructure.firebase.config import initialize_firebase


initialize_firebase()


app = Flask(__name__)


if __name__ == "__main__":
    app.run()
