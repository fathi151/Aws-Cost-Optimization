"""
Email Service Module
Handles sending customer inquiries to support email (maddehclement@gmail.com)
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class EmailService:
    """Service for sending customer inquiries to support email"""

    def __init__(self):
        """Initialize email service with SMTP configuration"""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "fathi.maddeh.it@gmail.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "211JMT9653")
        self.support_email = "maddehclement@gmail.com"
        
        if not self.sender_email or not self.sender_password:
            logger.warning("Email credentials not configured in environment variables")

    def send_customer_inquiry(self, customer_name: str, customer_email: str, 
                             subject: str, message: str) -> Dict[str, Any]:
        """
        Send customer inquiry to support email
        
        Args:
            customer_name: Customer's name
            customer_email: Customer's email address
            subject: Subject of the inquiry
            message: Customer's message/question
        
        Returns:
            Dictionary with send status
        """
        try:
            email_subject = f"Customer Inquiry: {subject}"
            
            # Create HTML email body
            html_body = self._create_inquiry_html(
                customer_name, customer_email, subject, message
            )
            
            # Send email to support
            self._send_email(self.support_email, email_subject, html_body)
            
            logger.info(f"Customer inquiry from {customer_email} sent to support")
            return {
                "status": "success",
                "message": f"Your inquiry has been sent to our support team at {self.support_email}",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error sending customer inquiry: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to send inquiry: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def send_aws_optimization_question(self, customer_name: str, customer_email: str,
                                       question: str, aws_context: str = "") -> Dict[str, Any]:
        """
        Send AWS optimization question to support
        
        Args:
            customer_name: Customer's name
            customer_email: Customer's email address
            question: The AWS optimization question
            aws_context: Optional AWS context/details
        
        Returns:
            Dictionary with send status
        """
        try:
            subject = "AWS Optimization Question"
            
            # Create HTML email body
            html_body = self._create_optimization_question_html(
                customer_name, customer_email, question, aws_context
            )
            
            # Send email to support
            self._send_email(self.support_email, subject, html_body)
            
            logger.info(f"AWS optimization question from {customer_email} sent to support")
            return {
                "status": "success",
                "message": f"Your question has been sent to our support team at {self.support_email}",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error sending optimization question: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to send question: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def _send_email(self, recipient: str, subject: str, html_body: str) -> None:
        """
        Internal method to send email via SMTP
        
        Args:
            recipient: Recipient email address
            subject: Email subject
            html_body: HTML email body
        
        Raises:
            Exception: If email sending fails
        """
        if not self.sender_email or not self.sender_password:
            raise Exception("Email credentials not configured. Please set SENDER_EMAIL and SENDER_PASSWORD in .env")

        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = recipient

        # Attach HTML body
        part = MIMEText(html_body, "html")
        message.attach(part)

        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient, message.as_string())

    def _create_inquiry_html(self, customer_name: str, customer_email: str,
                            subject: str, message: str) -> str:
        """Create HTML for customer inquiry email"""
        return f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #FF9900; color: white; padding: 20px; border-radius: 5px; }}
                    .customer-info {{ background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #FF9900; }}
                    .message-box {{ background-color: #f0f8f0; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                    .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                    h1 {{ color: #FF9900; }}
                    h3 {{ color: #333; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>New Customer Inquiry</h1>
                        <p>Received: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <div class="customer-info">
                        <h3>Customer Information:</h3>
                        <p><strong>Name:</strong> {customer_name}</p>
                        <p><strong>Email:</strong> {customer_email}</p>
                        <p><strong>Subject:</strong> {subject}</p>
                    </div>
                    
                    <div class="message-box">
                        <h3>Message:</h3>
                        <p>{message}</p>
                    </div>
                    
                    <p><strong>Action Required:</strong> Please respond to this customer at {customer_email}</p>
                    
                    <div class="footer">
                        <p>FinOps Chatbot - Customer Support System</p>
                    </div>
                </div>
            </body>
        </html>
        """

    def _create_optimization_question_html(self, customer_name: str, customer_email: str,
                                          question: str, aws_context: str = "") -> str:
        """Create HTML for AWS optimization question email"""
        context_section = ""
        if aws_context:
            context_section = f"""
            <div class="context-box">
                <h3>AWS Context:</h3>
                <p>{aws_context}</p>
            </div>
            """

        return f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #FF9900; color: white; padding: 20px; border-radius: 5px; }}
                    .customer-info {{ background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #FF9900; }}
                    .question-box {{ background-color: #e8f4f8; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                    .context-box {{ background-color: #fff3cd; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                    .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                    h1 {{ color: #FF9900; }}
                    h3 {{ color: #333; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>AWS Optimization Question</h1>
                        <p>Received: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <div class="customer-info">
                        <h3>Customer Information:</h3>
                        <p><strong>Name:</strong> {customer_name}</p>
                        <p><strong>Email:</strong> {customer_email}</p>
                    </div>
                    
                    <div class="question-box">
                        <h3>Question:</h3>
                        <p>{question}</p>
                    </div>
                    
                    {context_section}
                    
                    <p><strong>Action Required:</strong> Please provide AWS optimization recommendations and respond to {customer_email}</p>
                    
                    <div class="footer">
                        <p>FinOps Chatbot - Customer Support System</p>
                    </div>
                </div>
            </body>
        </html>
        """


def main():
    """Test email service"""
    logger.info("Testing Email Service")
    
    email_service = EmailService()
    
    # Test sending customer inquiry
    test_result = email_service.send_customer_inquiry(
        customer_name="fathi",
        customer_email="fathi.maddeh.it@gmail.com",
        subject="How to optimize my EC2 costs",
        message="I have 50 EC2 instances running and want to reduce costs. What are the best practices?"
    )
    
    print(f"Test result: {test_result}")


if __name__ == "__main__":
    main()
