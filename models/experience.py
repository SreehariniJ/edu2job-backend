from utils.db import db

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)        # e.g., "Intern"
    company = db.Column(db.String(120), nullable=False)      # e.g., "Infosys"
    start_year = db.Column(db.String(10), nullable=False)
    end_year = db.Column(db.String(10), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="experiences")
