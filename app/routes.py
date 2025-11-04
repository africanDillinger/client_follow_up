# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from app import db
from app.models import Client, FollowUp
from app.tasks import calculate_followup_dates

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    month_start = today.replace(day=1)

    weekly = FollowUp.query.filter(FollowUp.followup_date >= week_start,
                                   FollowUp.followup_date <= week_end).count()
    monthly = FollowUp.query.filter(FollowUp.followup_date >= month_start,
                                    FollowUp.followup_date <= today + relativedelta(months=1)).count()
    total = FollowUp.query.count()
    return render_template('index.html', weekly=weekly, monthly=monthly, total=total)

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form.get('age') or None
        phone = request.form.get('phone') or None
        clinic = request.form.get('clinic') or None
        circ_date = datetime.fromisoformat(request.form['circumcision_date']).date()
        client = Client(name=name, age=int(age) if age else None, phone=phone, clinic=clinic, circumcision_date=circ_date)
        db.session.add(client)
        db.session.commit()
        # schedule followups
        dates = calculate_followup_dates(client.circumcision_date)
        for d in dates:
            exists = FollowUp.query.filter_by(client_id=client.id, followup_date=d).first()
            if not exists:
                fu = FollowUp(client_id=client.id, followup_date=d)
                db.session.add(fu)
        db.session.commit()
        return redirect(url_for('routes.clients_view'))
    return render_template('register.html')

@bp.route('/clients')
def clients_view():
    followups = FollowUp.query.order_by(FollowUp.followup_date.asc()).all()
    return render_template('clients.html', followups=followups)

@bp.route('/followup/<int:fid>/complete')
def followup_complete(fid):
    fu = FollowUp.query.get_or_404(fid)
    fu.status = 'completed'
    db.session.add(fu)
    db.session.commit()
    return redirect(url_for('routes.clients_view'))

@bp.route('/api/stats')
def api_stats():
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    month_start = today.replace(day=1)
    weekly = FollowUp.query.filter(FollowUp.followup_date >= week_start, FollowUp.followup_date <= week_end).count()
    monthly = FollowUp.query.filter(FollowUp.followup_date >= month_start, FollowUp.followup_date <= today + relativedelta(months=1)).count()
    total = FollowUp.query.count()
    return jsonify({'weekly': weekly, 'monthly': monthly, 'total': total})
