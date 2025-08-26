from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
import os

from config import Config
from models import db, User, Product, PriceHistory, PriceTracker, Notification
from scrapers.scraper_factory import ScraperFactory
from services.price_monitor import PriceMonitor
from services.email_service import EmailService

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize services
price_monitor = PriceMonitor(app)
email_service = EmailService()

# Timezone helpers (use India Standard Time)
IST = ZoneInfo("Asia/Kolkata")

def _as_ist(dt: datetime) -> datetime | None:
    if dt is None:
        return None
    # Assume UTC when tzinfo is missing
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(IST)

def format_dt_ist(dt: datetime | None, fmt: str = '%Y-%m-%d %H:%M') -> str:
    local_dt = _as_ist(dt)
    return local_dt.strftime(fmt) if local_dt else ''

def to_inr(amount_usd: float | None) -> float:
    if amount_usd is None:
        return 0.0
    return round(amount_usd * Config.USD_TO_INR, 2)

def format_money(amount: float | None, currency: str = 'USD') -> str:
    if amount is None:
        return ''
    if currency.upper() == 'INR':
        return f"₹{amount:,.2f}"
    return f"${amount:,.2f}"

@app.context_processor
@app.context_processor
def inject_time_helpers():
    helpers = dict(
        format_dt_ist=format_dt_ist,
        to_inr=to_inr,
        format_money=format_money,
        usd_to_inr=Config.USD_TO_INR,
    )
    app.jinja_env.globals.update(helpers)
    return helpers

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        email_service.send_welcome_email(email, username)
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's active trackers
    trackers = PriceTracker.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    # Get recent notifications
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', trackers=trackers, notifications=notifications)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        url = request.form['url']
        target_price = float(request.form['target_price'])
        
        # Validate URL
        if not ScraperFactory.is_supported_url(url):
            flash('Unsupported website. Currently supports Amazon and eBay.')
            return redirect(url_for('add_product'))
        
        # Check if product already exists
        existing_product = Product.query.filter_by(url=url).first()
        if existing_product:
            product = existing_product
        else:
            # Scrape product information
            scraper = ScraperFactory.get_scraper(url)
            product_info = scraper.scrape_product(url)
            
            if not product_info:
                flash('Could not retrieve product information. Please check the URL.')
                return redirect(url_for('add_product'))
            
            # Create new product
            product = Product(
                name=product_info['name'],
                url=url,
                website=product_info['website'],
                product_id=product_info.get('product_id'),
                image_url=product_info.get('image_url'),
                description=product_info.get('description')
            )
            db.session.add(product)
            db.session.commit()
        
        # Create price tracker
        tracker = PriceTracker(
            user_id=current_user.id,
            product_id=product.id,
            target_price=target_price
        )
        db.session.add(tracker)
        db.session.commit()
        
        flash('Product added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_product.html')

@app.route('/tracker/<int:tracker_id>')
@login_required
def tracker_detail(tracker_id):
    tracker = PriceTracker.query.filter_by(id=tracker_id, user_id=current_user.id).first_or_404()
    
    # Get price history
    price_history = PriceHistory.query.filter_by(product_id=tracker.product_id).order_by(PriceHistory.timestamp.desc()).limit(30).all()
    
    # Prepare chart data (reverse to chronological order)
    sorted_history = list(reversed(price_history))
    labels = [_as_ist(h.timestamp).strftime('%m/%d %H:%M') for h in sorted_history]
    prices = [h.price for h in sorted_history]
    
    return render_template(
        'tracker_detail.html',
        tracker=tracker,
        price_history=price_history,
        labels_json=labels,
        prices_json=prices,
    )

@app.route('/tracker/<int:tracker_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tracker(tracker_id):
    tracker = PriceTracker.query.filter_by(id=tracker_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        tracker.target_price = float(request.form['target_price'])
        tracker.is_active = 'is_active' in request.form
        db.session.commit()
        flash('Tracker updated successfully!')
        return redirect(url_for('tracker_detail', tracker_id=tracker_id))
    
    return render_template('edit_tracker.html', tracker=tracker)

@app.route('/tracker/<int:tracker_id>/delete', methods=['POST'])
@login_required
def delete_tracker(tracker_id):
    tracker = PriceTracker.query.filter_by(id=tracker_id, user_id=current_user.id).first_or_404()
    db.session.delete(tracker)
    db.session.commit()
    flash('Tracker deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/check_price/<int:tracker_id>', methods=['POST'])
@login_required
def check_price_now(tracker_id):
    tracker = PriceTracker.query.filter_by(id=tracker_id, user_id=current_user.id).first_or_404()
    
    if price_monitor.check_price_now(tracker_id):
        flash('Price checked successfully!')
    else:
        flash('Error checking price. Please try again.')
    
    return redirect(url_for('tracker_detail', tracker_id=tracker_id))

@app.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first_or_404()
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Start price monitoring
    price_monitor.start_monitoring()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
