# 🕌 Quran Academy - Online Islamic Learning Platform

A beautiful, modern web application for online Quran classes with user authentication, course enrollment, and payment processing.

## ✨ Features

- **User Authentication**: Secure registration and login system with password hashing
- **Teacher Management**: Dedicated teacher accounts with course assignments
- **Course Management**: Four comprehensive programs (Learning Quran, Memorizing Quran, Tajweed, Islamic Studies)
- **Admin Course Builder**: Admins can add new courses directly from the UI and assign teachers
- **Teacher Dashboard**: Teachers can view assigned courses and student payment matrix
- **Student Matrix**: Track student enrollments, payments, and due dates by teacher
- **Enrollment System**: Easy course enrollment with status tracking
- **Payment Processing**: Integrated payment system with multiple payment methods
- **Payment Reminders**: Email reminder system for overdue and upcoming payments
- **User Dashboard**: Track enrollments, progress, and payment status
- **Responsive Design**: Beautiful, eye-catching interface that works on all devices
- **Islamic Design**: Carefully crafted UI with Islamic aesthetics and color schemes

## 🎓 Available Courses

1. **Learning Quran** - Comprehensive reading course for beginners ($150/month)
2. **Memorizing Quran** - Structured Hifz program with proven techniques ($200/month)
3. **Tajweed Mastery** - Master the art of Quranic pronunciation ($120/month)
4. **Islamic Studies** - Complete Islamic education covering Fiqh, Hadith, and more ($180/month)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory**:
   ```powershell
   cd c:\QuranAcademy
   ```

2. **Create a virtual environment** (recommended):
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   If you encounter an execution policy error, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Install required packages**:
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask server**:
   ```powershell
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. The application will automatically:
   - Create the SQLite database (`quran_academy.db`)
   - Initialize it with sample courses
   - Start the development server

## 📁 Project Structure

```
QuranAcademy/
│
├── app.py                  # Main Flask application with routes and database models
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── templates/             # HTML templates
│   ├── base.html         # Base template with navbar and footer
│   ├── index.html        # Homepage with hero section and features
│   ├── login.html        # User login page
│   ├── register.html     # User registration page
│   ├── dashboard.html    # User dashboard
│   ├── courses.html      # Course listing page
│   ├── enroll.html       # Course enrollment page
│   ├── payment.html      # Payment processing page
│   ├── admin_courses.html      # Admin course management
│   ├── admin_reports.html      # Admin payment reports
│   ├── admin_teachers.html     # Admin teacher management
│   ├── admin_teacher_report.html # Teacher-specific student report
│   ├── teacher_dashboard.html  # Teacher dashboard with student matrix
│   ├── edit_course.html  # Edit course page
│   ├── founder.html      # Founder's message page
│   ├── about.html        # About us page
│   └── contact.html      # Contact page
│
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet with animations
    ├── js/
    │   └── main.js       # JavaScript for interactivity
    └── images/
        └── logo.png      # Academy logo
```

## 🗄️ Database Schema

### User Table
- id, username, email, password_hash, full_name, phone, is_admin, is_teacher, created_at

### Course Table
- id, name, description, duration, tuition_fee, icon, features, teacher_id, created_at

### Enrollment Table
- id, user_id, course_id, enrollment_date, status, payment_status, next_payment_due, last_payment_date

### Payment Table
- id, enrollment_id, amount, payment_date, payment_method, transaction_id, status

## 🎨 Design Features

- **Modern UI**: Clean, professional design with smooth animations
- **Islamic Theme**: Green and gold color scheme with Islamic patterns
- **Responsive**: Mobile-first design that works on all screen sizes
- **Interactive**: Smooth transitions, hover effects, and scroll animations
- **User-Friendly**: Intuitive navigation and clear call-to-action buttons
- **Shareable**: Every course includes quick share links for Facebook, Twitter, and WhatsApp

## 🔐 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Login required decorators for protected routes
- CSRF protection (can be enhanced with Flask-WTF)

## 💳 Payment Methods Supported

- Credit Card
- Debit Card
- PayPal
- Bank Transfer

*Note: This is a demo system. In production, integrate with real payment gateways like Stripe or PayPal.*

## 🛠️ Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Fonts**: Google Fonts (Amiri for Arabic-style headings, Poppins for body text)
- **Design**: Custom CSS with CSS Grid and Flexbox

## 📝 Usage Guide

### For Students:

1. **Register**: Create an account with your details
2. **Browse Courses**: Explore available programs
3. **Enroll**: Choose a course and confirm enrollment
4. **Pay**: Complete payment to activate your course
5. **Dashboard**: Track your enrollments and progress

### For Teachers:

1. **Login**: Use teacher credentials (username: teacher, password: Teacher@1234)
2. **View Dashboard**: Access "My Classes" from the navigation menu
3. **Monitor Students**: View all students enrolled in your courses
4. **Track Payments**: See payment status and due dates for each student
5. **Student Matrix**: Access detailed payment information organized by course

### For Administrators:

1. **Login**: Use admin credentials (username: admin, password: Admin@1234)
2. **Manage Courses**: 
   - Create new courses with course pictures
   - Edit existing courses
   - Assign teachers to courses
   - Delete courses (if no enrollments exist)
3. **Manage Teachers**:
   - Add new teacher accounts
   - View all teachers and their assigned courses
   - Access teacher-specific student reports
   - Delete teachers (if no courses assigned)
4. **Payment Reports**:
   - View all student enrollments
   - Monitor payment statuses (paid, due soon, overdue)
   - Send email payment reminders to students
   - Track revenue and statistics
5. **Teacher Reports**:
   - View student matrix for each teacher
   - Monitor teacher performance
   - Access detailed payment information by teacher

## 🔄 Future Enhancements

- ✅ Admin panel for course and user management (Completed)
- ✅ Teacher management system (Completed)
- ✅ Payment tracking and reminders (Completed)
- Live class scheduling system
- Video conferencing integration
- Progress tracking with assignments
- Student-teacher messaging system
- Real payment gateway integration (Stripe/PayPal)
- Certificate generation
- Multi-language support (Arabic/English)
- Attendance tracking
- Performance analytics dashboard

## 🐛 Troubleshooting

**Issue**: Database not found
- **Solution**: Run `python app.py` - it will create the database automatically

**Issue**: Port already in use
- **Solution**: Change the port in `app.py`: `app.run(debug=True, port=5001)`

**Issue**: Templates not loading
- **Solution**: Ensure the `templates` and `static` folders are in the same directory as `app.py`

**Issue**: Database schema mismatch after updates
- **Solution**: Delete `instance/quran_academy.db` and restart the server to recreate with new schema

**Issue**: Email reminders not working
- **Solution**: Configure `.env` file with valid SMTP credentials (see EMAIL_SETUP.md)

## 👥 Default User Accounts

The system creates default accounts for testing:

**Admin Account:**
- Username: `admin`
- Password: `Admin@1234`
- Access: Full system administration

**Teacher Account:**
- Username: `teacher`
- Password: `Teacher@1234`
- Access: Teacher dashboard and student matrix

**Note**: Change these passwords in production!

## 📧 Support

For questions or issues, contact: info@raindropsacademy.com

## 📜 License

This project is open source and available for educational purposes.

## 🤲 May Allah bless your learning journey!

---

**Built with ❤️ for the Muslim community**
