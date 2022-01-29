from app import db


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), index=True)
    url = db.Column(db.String(255), nullable=True)
    alias = db.Column(db.String(200), unique=True, index=True)
    visits = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Site {self.alias} - {self.url} (Visits: {self.visits})>'
