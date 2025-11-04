# app/tasks.py
from datetime import date, timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta
from app import db
from app.models import FollowUp
from app.notifications import send_notification
import os

scheduler = None

def calculate_followup_dates(circ_date):
    return [circ_date + relativedelta(weeks=1),
            circ_date + relativedelta(months=1),
            circ_date + relativedelta(months=3)]

def check_and_send_followup_alerts():
    today = date.today()
    upcoming = FollowUp.query.filter(
        FollowUp.followup_date <= today + timedelta(days=2),
        FollowUp.status == 'pending',
        FollowUp.notification_sent == False
    ).all()
    for fu in upcoming:
        client = fu.client
        message = f"Reminder: You have a follow-up on {fu.followup_date.isoformat()}"
        if client.phone:
            send_notification(client.phone, message)
        fu.notification_sent = True
        db.session.add(fu)
    db.session.commit()

def mark_missed_followups():
    today = date.today()
    missed = FollowUp.query.filter(FollowUp.followup_date < today, FollowUp.status == 'pending').all()
    for fu in missed:
        fu.status = 'missed'
        db.session.add(fu)
    db.session.commit()

def scheduled_job(app=None):
    # wrap DB ops in app context if provided
    if app:
        with app.app_context():
            check_and_send_followup_alerts()
            mark_missed_followups()
    else:
        check_and_send_followup_alerts()
        mark_missed_followups()
    print(f"[Scheduler] Checked followups at {datetime.utcnow().isoformat()}")

def start_scheduler(app):
    global scheduler
    if scheduler and scheduler.running:
        return
    scheduler = BackgroundScheduler()
    minutes = app.config.get('SCHEDULER_INTERVAL_MINUTES', 1)
    # schedule with app context wrapper
    scheduler.add_job(func=lambda: scheduled_job(app), trigger='interval', minutes=minutes)
    scheduler.start()
