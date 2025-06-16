from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class JsonData(db.Model):
    id = db.Column(db.String, primary_key=True)
    content = db.Column(db.Text, nullable=False)
