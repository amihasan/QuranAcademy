# Email Configuration Guide

The admin panel includes a Payment Reports feature that allows sending email reminders to students about their monthly tuition fees.

## Setup Instructions

### 1. Configure Email Settings

Copy `.env.example` to create your `.env` file:
```bash
copy .env.example .env
```

### 2. Gmail Configuration (Recommended)

If using Gmail:

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the generated 16-character password
3. Update `.env` file:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

### 3. Other Email Providers

For other providers, update these settings in `.env`:
```
MAIL_SERVER=smtp.your-provider.com
MAIL_PORT=587
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-password
```

Common SMTP settings:
- **Outlook/Hotmail**: smtp.office365.com, port 587
- **Yahoo**: smtp.mail.yahoo.com, port 587
- **Custom SMTP**: Check with your email provider

## Using Payment Reports

### Access Reports
1. Login as admin (username: `admin`, password: `Admin@1234`)
2. Click "Reports" in the navigation menu
3. View all active student enrollments with payment status

### Send Payment Reminders
- Click "Send Reminder" button next to any student
- Automated email will be sent with:
  - Course name
  - Monthly fee amount
  - Payment due date
  - Overdue status (if applicable)
  - Last payment date

### Payment Status Indicators
- **Red (Overdue)**: Payment is past due date
- **Yellow (Due Soon)**: Payment due within 7 days
- **Green (Current)**: Payment not due for more than 7 days

## Testing Email Functionality

For testing without actual email:
1. Leave default configuration (emails will fail silently)
2. Check console output for email errors
3. Configure real SMTP settings when ready for production

## Security Notes

- Never commit `.env` file to version control
- Use App Passwords, not your main account password
- The `.env` file is already added to `.gitignore`
- Change default admin password in production
