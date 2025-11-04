# Email Service Setup Guide

## Overview
This guide explains how to set up and use the email service to allow customers to send AWS optimization inquiries to your support email (maddehclement@gmail.com).

## Setup Instructions

### 1. Configure Environment Variables

Add the following to your `.env` file:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SUPPORT_EMAIL=maddehclement@gmail.com
```

### 2. Gmail App Password Setup (Important!)

If using Gmail, you need to create an **App Password** (not your regular Gmail password):

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled
3. Go to **App passwords** (appears after 2FA is enabled)
4. Select "Mail" and "Windows Computer" (or your device)
5. Google will generate a 16-character password
6. Copy this password and use it as `SENDER_PASSWORD` in your `.env` file

### 3. Install Required Package

The email service uses Python's built-in `smtplib`, so no additional packages are needed. However, ensure you have the `python-dotenv` package:

```bash
pip install python-dotenv
```

## API Endpoints

### 1. Send Customer Inquiry

**Endpoint:** `POST /api/email/send-inquiry`

**Description:** Send a general inquiry to support

**Request Body:**
```json
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "subject": "How to optimize my AWS costs",
    "message": "I have 50 EC2 instances running and want to reduce costs. What are the best practices?"
}
```

**Response (Success):**
```json
{
    "status": "success",
    "message": "Your inquiry has been sent to our support team at maddehclement@gmail.com",
    "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Response (Error):**
```json
{
    "status": "error",
    "message": "Failed to send inquiry: [error details]",
    "timestamp": "2024-01-15T10:30:45.123456"
}
```

### 2. Send AWS Optimization Question

**Endpoint:** `POST /api/email/send-optimization-question`

**Description:** Send a specific AWS optimization question to support

**Request Body:**
```json
{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "question": "How can I reduce my RDS database costs?",
    "aws_context": "We have 3 RDS instances (MySQL, PostgreSQL, Aurora) with 500GB total storage"
}
```

**Response (Success):**
```json
{
    "status": "success",
    "message": "Your question has been sent to our support team at maddehclement@gmail.com",
    "timestamp": "2024-01-15T10:30:45.123456"
}
```

### 3. Health Check

**Endpoint:** `GET /api/email/health`

**Description:** Check if email service is properly configured

**Response:**
```json
{
    "status": "ok",
    "message": "Email service is ready",
    "support_email": "maddehclement@gmail.com"
}
```

## Integration with Flask App

To integrate the email routes into your Flask app, add this to your `app.py`:

```python
from email_routes import email_bp

# Register email blueprint
app.register_blueprint(email_bp)
```

## Frontend Integration (React)

### Example: Send Inquiry from React Component

```javascript
const sendInquiry = async (formData) => {
    try {
        const response = await fetch('/api/email/send-inquiry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_name: formData.name,
                customer_email: formData.email,
                subject: formData.subject,
                message: formData.message
            })
        });

        const result = await response.json();
        
        if (result.status === 'success') {
            alert('Your inquiry has been sent to our support team!');
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error sending inquiry:', error);
        alert('Failed to send inquiry');
    }
};
```

### Example: Send Optimization Question

```javascript
const sendOptimizationQuestion = async (formData) => {
    try {
        const response = await fetch('/api/email/send-optimization-question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_name: formData.name,
                customer_email: formData.email,
                question: formData.question,
                aws_context: formData.awsContext
            })
        });

        const result = await response.json();
        
        if (result.status === 'success') {
            alert('Your question has been sent to our support team!');
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error sending question:', error);
        alert('Failed to send question');
    }
};
```

## Testing the Email Service

### Using Python

```python
from email_service import EmailService

email_service = EmailService()

# Test sending inquiry
result = email_service.send_customer_inquiry(
    customer_name="Test Customer",
    customer_email="test@example.com",
    subject="Test Subject",
    message="This is a test message"
)

print(result)
```

### Using cURL

```bash
curl -X POST http://localhost:5000/api/email/send-inquiry \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "subject": "How to optimize my AWS costs",
    "message": "I have 50 EC2 instances running..."
  }'
```

## Troubleshooting

### Issue: "Email credentials not configured"
**Solution:** Make sure you have set `SENDER_EMAIL` and `SENDER_PASSWORD` in your `.env` file

### Issue: "Authentication failed"
**Solution:** 
- If using Gmail, ensure you're using an **App Password**, not your regular Gmail password
- Verify 2-Step Verification is enabled on your Google Account
- Check that the email address in `SENDER_EMAIL` matches your Gmail account

### Issue: "Connection refused"
**Solution:**
- Verify `SMTP_SERVER` and `SMTP_PORT` are correct
- Check your internet connection
- Ensure your firewall allows SMTP connections on port 587

### Issue: Emails not received
**Solution:**
- Check the spam/junk folder
- Verify the recipient email address is correct
- Check application logs for error messages

## Email Templates

The email service automatically formats emails with:
- Professional HTML styling
- Customer information section
- Message/question content
- Timestamp of submission
- Support contact information

All emails are sent to: **maddehclement@gmail.com**

## Security Notes

1. **Never commit `.env` file** - Keep your email credentials private
2. **Use App Passwords** - Don't use your main Gmail password
3. **Validate input** - The API validates all required fields
4. **HTTPS only** - Use HTTPS in production to protect email data in transit

## Support

For issues or questions about the email service, contact: maddehclement@gmail.com
