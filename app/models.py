from app import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'completed': self.completed
        }

    @staticmethod
    def get_all():
        return Item.query.all()

    def __repr__(self):
        return '<Item %r>' % (self.name)
