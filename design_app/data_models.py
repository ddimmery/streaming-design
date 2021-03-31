"""Data models."""
from . import db


class State(db.Model):
    __tablename__ = 'state'
    update_id = db.Column(
        db.Integer,
        primary_key=True
    )
    update_time = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    state = db.Column(
        db.UnicodeText(),
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<State {}>'.format(self.update_id)


class Respondent(db.Model):
    """Data model for respondents."""

    __tablename__ = 'respondents'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    anonid = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    assignment = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    data = db.Column(
        db.UnicodeText(),
        index=False,
        unique=False,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<Respondent {}>'.format(self.id)