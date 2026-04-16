from datetime import datetime
from . import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    show_time = db.Column(db.DateTime, nullable=False)
    ticket_open_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    seats = db.relationship('Seat', backref='event', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'show_time': self.show_time.isoformat() if self.show_time else None,
            'ticket_open_time': self.ticket_open_time.isoformat() if self.ticket_open_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    # CRUD Methods
    @classmethod
    def create(cls, data):
        new_event = cls(**data)
        db.session.add(new_event)
        db.session.commit()
        return new_event

    @classmethod
    def get_by_id(cls, event_id):
        return cls.query.get(event_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Seat(db.Model):
    __tablename__ = 'seats'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    seat_number = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='AVAILABLE', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    orders = db.relationship('Order', backref='seat', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'seat_number': self.seat_number,
            'price': self.price,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    # CRUD Methods
    @classmethod
    def create(cls, data):
        new_seat = cls(**data)
        db.session.add(new_seat)
        db.session.commit()
        return new_seat

    @classmethod
    def get_by_id(cls, seat_id):
        return cls.query.get(seat_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
