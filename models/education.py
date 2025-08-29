from utils.db import db

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(120), nullable=False)
    institution = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(10), nullable=False)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="educations")
