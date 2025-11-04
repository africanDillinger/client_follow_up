# app/models.py
from datetime import datetime
from app import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    circumcision_date = db.Column(db.Date, nullable=False)
    clinic = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    followups = db.relationship('FollowUp', backref='client', lazy=True)

class FollowUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    followup_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='pending')  # pending / completed / missed
    notification_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
