from app import app, db
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    db = SQLAlchemy(app)
    app.run(debug=True)
