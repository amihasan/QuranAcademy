# 🕌 Quran Academy - Online Islamic Learning Platform

A beautiful, modern web application for online Quran classes with user authentication, course enrollment, and payment processing.

## ✨ Features

- **User Authentication**: Secure registration and login system with password hashing
- **Course Management**: Four comprehensive programs (Learning Quran, Memorizing Quran, Tajweed, Islamic Studies)
- **Admin Course Builder**: Admins can add new courses directly from the UI and instantly publish them
- **Enrollment System**: Easy course enrollment with status tracking
- **Payment Processing**: Integrated payment system with multiple payment methods
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
│   ├── about.html        # About us page
│   └── contact.html      # Contact page
│
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet with animations
    └── js/
        └── main.js       # JavaScript for interactivity
```

## 🗄️ Database Schema

### User Table
- id, username, email, password_hash, full_name, phone, created_at

### Course Table
- id, name, description, duration, tuition_fee, icon, features, created_at

### Enrollment Table
- id, user_id, course_id, enrollment_date, status, payment_status

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

### For Administrators:

The database can be managed through:
- Direct database access using SQLite browser
- Python shell for programmatic access
- Future admin panel (can be added)

## 🔄 Future Enhancements

- Admin panel for course and user management
- Live class scheduling system
- Video conferencing integration
- Progress tracking with assignments
- Student-teacher messaging system
- Real payment gateway integration
- Email notifications
- Certificate generation
- Multi-language support (Arabic/English)

## 🐛 Troubleshooting

**Issue**: Database not found
- **Solution**: Run `python app.py` - it will create the database automatically

**Issue**: Port already in use
- **Solution**: Change the port in `app.py`: `app.run(debug=True, port=5001)`

**Issue**: Templates not loading
- **Solution**: Ensure the `templates` and `static` folders are in the same directory as `app.py`

## 📧 Support

For questions or issues, contact: info@quranacademy.com

## 📜 License

This project is open source and available for educational purposes.

## 🤲 May Allah bless your learning journey!

---

**Built with ❤️ for the Muslim community**
