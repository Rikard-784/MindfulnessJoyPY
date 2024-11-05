class Progress(db.Model):
 # class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
 # date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    notes = db.Column(db.String(200), nullable=True)
 # 4


