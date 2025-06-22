from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)    
    date = db.Column(db.DateTime, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    #relationship
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    guests = association_proxy('appearances', 'guest')

    #serialization
    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f'<Episode {self.title}>'


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=True)

    #relationship
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')    
    episodes = association_proxy('appearances', 'episode')

    # serialization
    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.name}>'


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    # relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    # serialization
    serialize_rules = ('-episode.appearances', '-guest.appearances')

    # validation
    @validates('rating')
    def validate_rating(self, key, value):
        if value is not None and (value < 1 or value > 5):
            raise ValueError("Rating must be between 1 and 5.")
        return value

    def __repr__(self):
        guest_name = self.guest.name if self.guest else 'Unknown Guest'
        episode_date = self.episode.date if self.episode else 'Unknown Date'
        return f'<Appearance {guest_name} on {episode_date} >'



    






    