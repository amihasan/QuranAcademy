from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import stripe

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quran_academy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'icons')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}

# Email configuration (configure with your SMTP settings)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@raindropsacademy.com')

# Stripe configuration
stripe_secret = os.environ.get('STRIPE_SECRET_KEY', '')
stripe_public = os.environ.get('STRIPE_PUBLIC_KEY', '')

# Only set Stripe key if it's a valid key (not placeholder)
if stripe_secret and not stripe_secret.endswith('_here') and stripe_secret.startswith('sk_'):
    stripe.api_key = stripe_secret
else:
    stripe.api_key = None  # Will trigger demo mode
    
app.config['STRIPE_PUBLIC_KEY'] = stripe_public if (stripe_public and stripe_public.startswith('pk_')) else ''

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Helper function for file uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function for sending emails
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    is_teacher = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Teacher profile fields
    profile_picture = db.Column(db.String(200))
    bio = db.Column(db.Text)
    qualifications = db.Column(db.Text)  # Degrees and certifications
    specializations = db.Column(db.Text)  # Areas of strength
    experience_years = db.Column(db.Integer)
    languages = db.Column(db.String(200))
    ijazah = db.Column(db.String(200))  # Ijazah certificates
    teaching_style = db.Column(db.Text)
    
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    teaching_courses = db.relationship('Course', backref='teacher', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    tuition_fee = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(50))
    features = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, active, completed
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, paid
    next_payment_due = db.Column(db.DateTime)  # Next monthly payment due date
    last_payment_date = db.Column(db.DateTime)  # Last payment received date
    payment = db.relationship('Payment', backref='enrollment', uselist=False, lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))  # 'stripe', 'cash', 'bank_transfer', etc.
    transaction_id = db.Column(db.String(100))  # Stripe payment intent ID
    stripe_payment_intent = db.Column(db.String(200))  # Full Stripe payment intent ID
    stripe_customer_id = db.Column(db.String(200))  # Stripe customer ID
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Administrative access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        if not user or not user.is_teacher:
            flash('Teacher access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    courses = Course.query.all()
    teachers = User.query.filter_by(is_teacher=True).limit(3).all()
    return render_template('index.html', courses=courses, teachers=teachers)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form.get('phone', '')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            phone=phone
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            session['is_admin'] = user.is_admin
            session['is_teacher'] = user.is_teacher
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect based on user role
            if user.is_teacher and not user.is_admin:
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    enrollments = Enrollment.query.filter_by(user_id=user.id).all()
    
    # Show payment success message if redirected from payment
    if request.args.get('payment') == 'success':
        flash('Payment successful! Your course is now active.', 'success')
    
    return render_template('dashboard.html', user=user, enrollments=enrollments)

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@app.route('/admin/courses', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_courses():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        duration = request.form['duration']
        tuition_fee = float(request.form['tuition_fee'])
        features_raw = request.form.get('features', '')
        features = '|'.join([line.strip() for line in features_raw.split('\n') if line.strip()])

        # Handle file upload (required)
        if 'icon_file' not in request.files or not request.files['icon_file'].filename:
            flash('Course picture is required!', 'danger')
            courses = Course.query.order_by(Course.created_at.desc()).all()
            return render_template('admin_courses.html', courses=courses)
        
        file = request.files['icon_file']
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PNG, JPG, GIF, SVG, or WEBP.', 'danger')
            courses = Course.query.order_by(Course.created_at.desc()).all()
            return render_template('admin_courses.html', courses=courses)
        
        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        icon = f"/static/uploads/icons/{filename}"

        course = Course(
            name=name,
            description=description,
            duration=duration,
            tuition_fee=tuition_fee,
            icon=icon,
            features=features,
            teacher_id=request.form.get('teacher_id') if request.form.get('teacher_id') else None
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully.', 'success')
        return redirect(url_for('admin_courses'))

    courses = Course.query.order_by(Course.created_at.desc()).all()
    teachers = User.query.filter_by(is_teacher=True).all()
    return render_template('admin_courses.html', courses=courses, teachers=teachers)

@app.route('/enroll/<int:course_id>', methods=['GET', 'POST'])
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    user_id = session['user_id']
    
    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        user_id=user_id, 
        course_id=course_id
    ).first()
    
    if existing_enrollment:
        flash('You are already enrolled in this course!', 'warning')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Create enrollment
        new_enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            status='pending',
            payment_status='unpaid',
            next_payment_due=datetime.utcnow() + timedelta(days=7)  # 7 days to make first payment
        )
        db.session.add(new_enrollment)
        db.session.commit()
        
        flash('Enrollment successful! Please proceed with payment.', 'success')
        return redirect(url_for('payment', enrollment_id=new_enrollment.id))
    
    return render_template('enroll.html', course=course)

@app.route('/payment/<int:enrollment_id>', methods=['GET', 'POST'])
@login_required
def payment(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    user = User.query.get(session['user_id'])
    
    # Verify ownership
    if enrollment.user_id != session['user_id']:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if already paid
    if enrollment.payment_status == 'paid':
        flash('This enrollment has already been paid for.', 'info')
        return redirect(url_for('dashboard'))
    
    # Check if Stripe is configured with valid keys
    stripe_configured = (
        stripe.api_key and 
        app.config['STRIPE_PUBLIC_KEY'] and
        app.config['STRIPE_PUBLIC_KEY'].startswith('pk_') and
        not app.config['STRIPE_PUBLIC_KEY'].endswith('_here')
    )
    
    # Handle demo mode POST for non-Stripe payments
    if request.method == 'POST' and not stripe_configured:
        # Create payment record for demo
        new_payment = Payment(
            enrollment_id=enrollment_id,
            amount=enrollment.course.tuition_fee,
            payment_method='demo',
            transaction_id=f'DEMO{datetime.utcnow().strftime("%Y%m%d%H%M%S")}{enrollment_id}',
            status='completed'
        )
        
        # Update enrollment status
        enrollment.payment_status = 'paid'
        enrollment.status = 'active'
        enrollment.last_payment_date = datetime.utcnow()
        enrollment.next_payment_due = datetime.utcnow() + timedelta(days=30)
        
        db.session.add(new_payment)
        db.session.commit()
        
        flash('Demo payment successful! Your course is now active.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('payment.html', 
                         enrollment=enrollment,
                         stripe_public_key=app.config['STRIPE_PUBLIC_KEY'],
                         stripe_configured=stripe_configured)

@app.route('/create-payment-intent/<int:enrollment_id>', methods=['POST'])
@login_required
def create_payment_intent(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    user = User.query.get(session['user_id'])
    
    # Verify ownership
    if enrollment.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Check if Stripe is configured
    if not stripe.api_key or not stripe.api_key.startswith('sk_'):
        return jsonify({'error': 'Stripe is not configured. Using demo mode instead.'}), 400
    
    try:
        # Create or retrieve Stripe customer
        if not user.email:
            return jsonify({'error': 'Email required for payment. Please update your profile.'}), 400
        
        # Create Stripe customer if doesn't exist
        customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name,
            metadata={'user_id': user.id}
        )
        
        # Create payment intent
        amount = int(enrollment.course.tuition_fee * 100)  # Convert to cents
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            customer=customer.id,
            metadata={
                'enrollment_id': enrollment_id,
                'user_id': user.id,
                'course_id': enrollment.course_id,
                'course_name': enrollment.course.name
            },
            description=f'Payment for {enrollment.course.name}'
        )
        
        return jsonify({
            'clientSecret': intent.client_secret,
            'amount': enrollment.course.tuition_fee
        })
    
    except stripe.error.AuthenticationError as e:
        return jsonify({'error': 'Stripe authentication failed. Please check your API keys.'}), 400
    except stripe.error.StripeError as e:
        return jsonify({'error': f'Stripe error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Payment initialization failed: {str(e)}'}), 400

@app.route('/payment-success/<int:enrollment_id>', methods=['POST'])
@login_required
def payment_success(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    # Verify ownership
    if enrollment.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    payment_intent_id = data.get('payment_intent_id')
    
    if not payment_intent_id:
        return jsonify({'error': 'No payment intent ID provided'}), 400
    
    try:
        # Check if Stripe is configured
        if not stripe.api_key or not stripe.api_key.startswith('sk_'):
            # Stripe not configured - this shouldn't happen if we got here
            return jsonify({'error': 'Stripe is not properly configured'}), 400
        
        # Verify payment with Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == 'succeeded':
            # Create payment record
            new_payment = Payment(
                enrollment_id=enrollment_id,
                amount=enrollment.course.tuition_fee,
                payment_method='stripe',
                transaction_id=payment_intent_id,
                stripe_payment_intent=payment_intent_id,
                stripe_customer_id=intent.customer,
                status='completed'
            )
            
            # Update enrollment status
            enrollment.payment_status = 'paid'
            enrollment.status = 'active'
            enrollment.last_payment_date = datetime.utcnow()
            enrollment.next_payment_due = datetime.utcnow() + timedelta(days=30)
            
            db.session.add(new_payment)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Payment successful!'})
        else:
            return jsonify({'error': f'Payment status is {intent.status}, not succeeded'}), 400
    
    except stripe.error.InvalidRequestError as e:
        # Payment intent not found or invalid
        return jsonify({'error': f'Invalid payment: {str(e)}'}), 400
    except stripe.error.AuthenticationError as e:
        return jsonify({'error': 'Stripe authentication failed. Check your secret key.'}), 400
    except stripe.error.StripeError as e:
        return jsonify({'error': f'Stripe error: {str(e)}'}), 400
    except Exception as e:
        # Log the full error for debugging
        print(f"Payment success error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Payment verification failed: {str(e)}'}), 400

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/founder')
def founder():
    return render_template('founder.html')

# Public Teacher Routes
@app.route('/teachers')
def teachers():
    all_teachers = User.query.filter_by(is_teacher=True).all()
    return render_template('teachers.html', teachers=all_teachers)

@app.route('/teachers/<int:teacher_id>')
def teacher_public_profile(teacher_id):
    teacher = User.query.get_or_404(teacher_id)
    
    if not teacher.is_teacher:
        flash('Teacher not found.', 'danger')
        return redirect(url_for('teachers'))
    
    # Get courses taught by this teacher
    courses = Course.query.filter_by(teacher_id=teacher.id).all()
    
    return render_template('teacher_public_profile.html', teacher=teacher, courses=courses)

@app.route('/admin/courses/edit/<int:course_id>', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        course.name = request.form['name']
        course.description = request.form['description']
        course.duration = request.form['duration']
        course.tuition_fee = float(request.form['tuition_fee'])
        
        # Handle file upload
        if 'icon_file' in request.files and request.files['icon_file'].filename:
            file = request.files['icon_file']
            if allowed_file(file.filename):
                # Delete old picture file
                if course.icon and course.icon.startswith('/static/uploads/'):
                    old_file = os.path.join(os.path.dirname(__file__), course.icon.lstrip('/'))
                    if os.path.exists(old_file):
                        os.remove(old_file)
                
                filename = secure_filename(file.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                course.icon = f"/static/uploads/icons/{filename}"
            else:
                flash('Invalid file type. Please upload PNG, JPG, GIF, SVG, or WEBP.', 'danger')
                return render_template('edit_course.html', course=course)
        
        features_raw = request.form.get('features', '')
        course.features = '|'.join([line.strip() for line in features_raw.split('\n') if line.strip()])
        
        # Update teacher assignment
        teacher_id = request.form.get('teacher_id')
        course.teacher_id = int(teacher_id) if teacher_id else None
        
        db.session.commit()
        flash(f'Course "{course.name}" updated successfully!', 'success')
        return redirect(url_for('admin_courses'))
    
    teachers = User.query.filter_by(is_teacher=True).all()
    return render_template('edit_course.html', course=course, teachers=teachers)

@app.route('/admin/courses/delete/<int:course_id>', methods=['POST'])
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    course_name = course.name
    
    # Check if there are enrollments for this course
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    if enrollments:
        flash(f'Cannot delete "{course_name}" because it has active enrollments.', 'danger')
        return redirect(url_for('admin_courses'))
    
    db.session.delete(course)
    db.session.commit()
    flash(f'Course "{course_name}" deleted successfully!', 'success')
    return redirect(url_for('admin_courses'))

@app.route('/admin/reports')
@login_required
@admin_required
def admin_reports():
    # Get all active enrollments with payment information
    enrollments = db.session.query(Enrollment, User, Course).join(
        User, Enrollment.user_id == User.id
    ).join(
        Course, Enrollment.course_id == Course.id
    ).filter(
        Enrollment.status == 'active'
    ).all()
    
    # Calculate payment status for each enrollment
    report_data = []
    current_date = datetime.utcnow()
    
    for enrollment, user, course in enrollments:
        # Calculate days until next payment or overdue
        days_until_due = None
        is_overdue = False
        overdue_days = 0
        
        if enrollment.next_payment_due:
            time_diff = enrollment.next_payment_due - current_date
            days_until_due = time_diff.days
            if days_until_due < 0:
                is_overdue = True
                overdue_days = abs(days_until_due)
        
        report_data.append({
            'enrollment': enrollment,
            'user': user,
            'course': course,
            'monthly_fee': course.tuition_fee,
            'days_until_due': days_until_due,
            'is_overdue': is_overdue,
            'overdue_days': overdue_days
        })
    
    # Sort by overdue first, then by days until due
    report_data.sort(key=lambda x: (not x['is_overdue'], x['days_until_due'] if x['days_until_due'] is not None else 999))
    
    return render_template('admin_reports.html', report_data=report_data)

@app.route('/admin/send-reminder/<int:enrollment_id>', methods=['POST'])
@login_required
@admin_required
def send_payment_reminder(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    user = User.query.get(enrollment.user_id)
    course = Course.query.get(enrollment.course_id)
    
    # Prepare email content
    subject = f"Payment Reminder - {course.name}"
    
    if enrollment.next_payment_due:
        due_date = enrollment.next_payment_due.strftime('%B %d, %Y')
        days_diff = (enrollment.next_payment_due - datetime.utcnow()).days
        
        if days_diff < 0:
            status_text = f"<strong style='color: #dc3545;'>OVERDUE by {abs(days_diff)} days</strong>"
        elif days_diff == 0:
            status_text = "<strong style='color: #ffc107;'>DUE TODAY</strong>"
        else:
            status_text = f"due in {days_diff} days"
    else:
        due_date = "Not set"
        status_text = "pending"
    
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #1e5a7d, #2d8659); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .detail-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #2d8659; }}
            .amount {{ font-size: 28px; color: #1e5a7d; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            .btn {{ display: inline-block; padding: 12px 30px; background: #2d8659; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💧 Raindrops Academy</h1>
                <p>Payment Reminder</p>
            </div>
            <div class="content">
                <p>Dear {user.full_name},</p>
                
                <p>This is a friendly reminder about your monthly tuition payment for <strong>{course.name}</strong>.</p>
                
                <div class="detail-box">
                    <p><strong>Course:</strong> {course.name}</p>
                    <p><strong>Monthly Fee:</strong> <span class="amount">${course.tuition_fee:.2f}</span></p>
                    <p><strong>Next Payment Due:</strong> {due_date} ({status_text})</p>
                    <p><strong>Last Payment:</strong> {enrollment.last_payment_date.strftime('%B %d, %Y') if enrollment.last_payment_date else 'No payment recorded'}</p>
                </div>
                
                <p>Please ensure your payment is submitted on time to continue enjoying uninterrupted access to your course.</p>
                
                <p>If you have already made the payment, please disregard this reminder.</p>
                
                <div class="footer">
                    <p>Thank you for being part of Raindrops Academy!</p>
                    <p>For any questions, please contact us at admin@raindropsacademy.com</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send email
    if send_email(user.email, subject, body):
        flash(f'Payment reminder sent successfully to {user.full_name} ({user.email})', 'success')
    else:
        flash(f'Failed to send email to {user.email}. Please check email configuration.', 'danger')
    
    return redirect(url_for('admin_reports'))

# Teacher Routes
@app.route('/teacher/profile', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_profile():
    teacher = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Update basic info
        teacher.full_name = request.form.get('full_name', teacher.full_name)
        teacher.phone = request.form.get('phone', teacher.phone)
        teacher.bio = request.form.get('bio', '')
        teacher.experience_years = int(request.form.get('experience_years', 0)) if request.form.get('experience_years') else None
        teacher.languages = request.form.get('languages', '')
        teacher.ijazah = request.form.get('ijazah', '')
        teacher.teaching_style = request.form.get('teaching_style', '')
        
        # Handle qualifications (degrees)
        qualifications_raw = request.form.get('qualifications', '')
        teacher.qualifications = '|'.join([line.strip() for line in qualifications_raw.split('\n') if line.strip()])
        
        # Handle specializations (areas of strength)
        specializations_raw = request.form.get('specializations', '')
        teacher.specializations = '|'.join([line.strip() for line in specializations_raw.split('\n') if line.strip()])
        
        # Handle profile picture upload
        if 'profile_picture' in request.files and request.files['profile_picture'].filename:
            file = request.files['profile_picture']
            if allowed_file(file.filename):
                # Delete old profile picture if exists
                if teacher.profile_picture and teacher.profile_picture.startswith('/static/uploads/'):
                    old_file = os.path.join(os.path.dirname(__file__), teacher.profile_picture.lstrip('/'))
                    if os.path.exists(old_file):
                        os.remove(old_file)
                
                # Save new profile picture
                filename = secure_filename(file.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                filename = f"teacher_{teacher.id}_{timestamp}_{filename}"
                
                # Create teachers folder if not exists
                teachers_folder = os.path.join(app.config['UPLOAD_FOLDER'], '..', 'teachers')
                os.makedirs(teachers_folder, exist_ok=True)
                
                filepath = os.path.join(teachers_folder, filename)
                file.save(filepath)
                teacher.profile_picture = f"/static/uploads/teachers/{filename}"
            else:
                flash('Invalid file type for profile picture. Please upload PNG, JPG, GIF, SVG, or WEBP.', 'danger')
                return render_template('teacher_profile.html', teacher=teacher)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('teacher_profile'))
    
    return render_template('teacher_profile.html', teacher=teacher)

@app.route('/teacher/dashboard')
@login_required
@teacher_required
def teacher_dashboard():
    teacher = User.query.get(session['user_id'])
    courses = Course.query.filter_by(teacher_id=teacher.id).all()
    
    # Get student matrix for teacher's courses
    student_data = []
    for course in courses:
        enrollments = Enrollment.query.filter_by(course_id=course.id).all()
        for enrollment in enrollments:
            student = User.query.get(enrollment.user_id)
            
            # Calculate payment status
            payment_status = 'No payment yet'
            status_class = 'warning'
            days_until_due = None
            
            if enrollment.next_payment_due:
                days_until_due = (enrollment.next_payment_due - datetime.utcnow()).days
                
                if days_until_due < 0:
                    payment_status = f'Overdue by {abs(days_until_due)} days'
                    status_class = 'danger'
                elif days_until_due == 0:
                    payment_status = 'Due today'
                    status_class = 'warning'
                elif days_until_due <= 7:
                    payment_status = f'Due in {days_until_due} days'
                    status_class = 'warning'
                else:
                    payment_status = f'Due in {days_until_due} days'
                    status_class = 'success'
            
            student_data.append({
                'student': student,
                'course': course,
                'enrollment': enrollment,
                'payment_status': payment_status,
                'status_class': status_class,
                'days_until_due': days_until_due
            })
    
    return render_template('teacher_dashboard.html', teacher=teacher, courses=courses, student_data=student_data)

# Admin Teacher Management Routes
@app.route('/admin/teachers', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_teachers():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form.get('phone', '')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('admin_teachers'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('admin_teachers'))
        
        # Create new teacher
        hashed_password = generate_password_hash(password)
        new_teacher = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            phone=phone,
            is_teacher=True
        )
        
        db.session.add(new_teacher)
        db.session.commit()
        flash(f'Teacher {full_name} added successfully!', 'success')
        return redirect(url_for('admin_teachers'))
    
    teachers = User.query.filter_by(is_teacher=True).all()
    return render_template('admin_teachers.html', teachers=teachers)

@app.route('/admin/teachers/delete/<int:teacher_id>', methods=['POST'])
@login_required
@admin_required
def delete_teacher(teacher_id):
    teacher = User.query.get_or_404(teacher_id)
    
    # Check if teacher has assigned courses
    assigned_courses = Course.query.filter_by(teacher_id=teacher_id).count()
    if assigned_courses > 0:
        flash(f'Cannot delete teacher. {assigned_courses} courses are assigned to this teacher. Please reassign courses first.', 'danger')
        return redirect(url_for('admin_teachers'))
    
    db.session.delete(teacher)
    db.session.commit()
    flash(f'Teacher {teacher.full_name} deleted successfully.', 'success')
    return redirect(url_for('admin_teachers'))

@app.route('/admin/reports/teacher/<int:teacher_id>')
@login_required
@admin_required
def admin_teacher_report(teacher_id):
    teacher = User.query.get_or_404(teacher_id)
    
    if not teacher.is_teacher:
        flash('User is not a teacher.', 'danger')
        return redirect(url_for('admin_reports'))
    
    courses = Course.query.filter_by(teacher_id=teacher.id).all()
    
    # Get student matrix for this teacher's courses
    student_data = []
    total_students = 0
    total_revenue = 0
    overdue_count = 0
    
    for course in courses:
        enrollments = Enrollment.query.filter_by(course_id=course.id).all()
        total_students += len(enrollments)
        
        for enrollment in enrollments:
            student = User.query.get(enrollment.user_id)
            
            # Calculate payment status
            payment_status = 'No payment yet'
            status_class = 'warning'
            days_until_due = None
            
            if enrollment.next_payment_due:
                days_until_due = (enrollment.next_payment_due - datetime.utcnow()).days
                
                if days_until_due < 0:
                    payment_status = f'Overdue by {abs(days_until_due)} days'
                    status_class = 'danger'
                    overdue_count += 1
                elif days_until_due == 0:
                    payment_status = 'Due today'
                    status_class = 'warning'
                elif days_until_due <= 7:
                    payment_status = f'Due in {days_until_due} days'
                    status_class = 'warning'
                else:
                    payment_status = f'Due in {days_until_due} days'
                    status_class = 'success'
            
            if enrollment.last_payment_date:
                total_revenue += course.tuition_fee
            
            student_data.append({
                'student': student,
                'course': course,
                'enrollment': enrollment,
                'payment_status': payment_status,
                'status_class': status_class,
                'days_until_due': days_until_due
            })
    
    return render_template('admin_teacher_report.html', 
                         teacher=teacher, 
                         courses=courses, 
                         student_data=student_data,
                         total_students=total_students,
                         total_revenue=total_revenue,
                         overdue_count=overdue_count)

    return redirect(url_for('admin_reports'))

# Initialize database and sample data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if courses already exist
        if Course.query.count() == 0:
            # Add sample courses with placeholder images
            courses_data = [
                {
                    'name': 'Learning Quran',
                    'description': 'Comprehensive Quran reading course for beginners. Learn proper pronunciation, basic rules, and reading fluency with experienced instructors.',
                    'duration': '6 months',
                    'tuition_fee': 150.00,
                    'icon': 'https://images.unsplash.com/photo-1609599006353-e629aaabfeae?w=400&h=300&fit=crop',
                    'features': 'One-on-one sessions|Flexible scheduling|Progress tracking|Certificate upon completion'
                },
                {
                    'name': 'Memorizing Quran',
                    'description': 'Structured Hifz program with proven memorization techniques. Join thousands of students who have completed their Quran memorization with us.',
                    'duration': '2-3 years',
                    'tuition_fee': 200.00,
                    'icon': 'https://images.unsplash.com/photo-1591604466107-ec97de577aff?w=400&h=300&fit=crop',
                    'features': 'Daily revision classes|Memory techniques|Monthly assessments|Ijazah certification'
                },
                {
                    'name': 'Tajweed Mastery',
                    'description': 'Master the art of Tajweed with expert teachers. Perfect your recitation and understand the beauty of Quranic pronunciation.',
                    'duration': '4 months',
                    'tuition_fee': 120.00,
                    'icon': 'https://images.unsplash.com/photo-1542816417-0983c9c9ad53?w=400&h=300&fit=crop',
                    'features': 'Advanced Tajweed rules|Practical exercises|Audio feedback|Makharij training'
                },
                {
                    'name': 'Islamic Studies',
                    'description': 'Comprehensive Islamic education covering Fiqh, Hadith, Seerah, and Islamic history. Deepen your understanding of Islam.',
                    'duration': '8 months',
                    'tuition_fee': 180.00,
                    'icon': 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=400&h=300&fit=crop',
                    'features': 'Expert scholars|Interactive discussions|Study materials|Islamic library access'
                }
            ]
            
            for course_data in courses_data:
                course = Course(**course_data)
                db.session.add(course)
            
            db.session.commit()
            print("Database initialized with sample courses!")

        # Create a default admin user
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@raindropsacademy.com',
                password_hash=generate_password_hash('Admin@1234'),
                full_name='Site Administrator',
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Created default admin user (username: admin, password: Admin@1234)")
        
        # Create a sample teacher user
        if not User.query.filter_by(username='teacher').first():
            teacher_user = User(
                username='teacher',
                email='teacher@raindropsacademy.com',
                password_hash=generate_password_hash('Teacher@1234'),
                full_name='Sample Teacher',
                is_teacher=True,
                phone='+1 (555) 987-6543'
            )
            db.session.add(teacher_user)
            db.session.commit()
            print("Created sample teacher user (username: teacher, password: Teacher@1234)")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
