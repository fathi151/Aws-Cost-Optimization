"""
Email Routes for Flask App
Provides endpoints for customers to send inquiries to support
"""

from flask import Blueprint, request, jsonify
from email_service import EmailService
import logging

logger = logging.getLogger(__name__)

# Create blueprint
email_bp = Blueprint('email', __name__, url_prefix='/api/email')

# Initialize email service
email_service = EmailService()


@email_bp.route('/send-inquiry', methods=['POST'])
def send_inquiry():
    """
    Endpoint for customers to send inquiry to support
    
    Expected JSON:
    {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "subject": "How to optimize my AWS costs",
        "message": "I have 50 EC2 instances..."
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'subject', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(required_fields)}"
            }), 400
        
        # Send inquiry
        result = email_service.send_customer_inquiry(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            subject=data['subject'],
            message=data['message']
        )
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in send_inquiry endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@email_bp.route('/send-optimization-question', methods=['POST'])
def send_optimization_question():
    """
    Endpoint for customers to send AWS optimization questions to support
    
    Expected JSON:
    {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "question": "How can I reduce my EC2 costs?",
        "aws_context": "Optional AWS details about their infrastructure"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'question']
        if not all(field in data for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(required_fields)}"
            }), 400
        
        # Send optimization question
        result = email_service.send_aws_optimization_question(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            question=data['question'],
            aws_context=data.get('aws_context', '')
        )
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in send_optimization_question endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@email_bp.route('/health', methods=['GET'])
def health():
    """Check if email service is configured"""
    try:
        is_configured = email_service.sender_email and email_service.sender_password
        return jsonify({
            "status": "ok" if is_configured else "not_configured",
            "message": "Email service is ready" if is_configured else "Email credentials not configured",
            "support_email": email_service.support_email
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
