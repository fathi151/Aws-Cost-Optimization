"""
Flask API Server for FinOps Chatbot
Provides REST endpoints for chatbot interactions and web UI
"""

import os
import logging
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from finops_chatbot import FinOpsChatbot
from config import config
from database import DatabaseManager
from scheduler import DataSyncScheduler
from advanced_analytics import AdvancedAnalytics
import pandas as pd
from email_routes import email_bp

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = config.SECRET_KEY
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
app.register_blueprint(email_bp)



# Initialize components
chatbot = FinOpsChatbot()
db_manager = DatabaseManager()
data_sync_scheduler = DataSyncScheduler(chatbot)
analytics = AdvancedAnalytics()

# Start scheduler if enabled
if config.ENABLE_SCHEDULER:
    data_sync_scheduler.start()
    data_sync_scheduler.schedule_daily_sync(hour=config.SYNC_HOUR, minute=config.SYNC_MINUTE)
    logger.info("Data sync scheduler started")


@app.route("/", methods=["GET"])
def index():
    """Serve the web UI"""
    return render_template("index_clean.html")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "FinOps Chatbot API"}), 200


@app.route("/api/sync", methods=["POST"])
def sync_aws_data():
    """
    Sync AWS data and generate optimization insights
    
    Request body:
    {
        "days": 30  (optional, default: 30)
    }
    """
    try:
        data = request.get_json() or {}
        days = data.get("days", 30)

        logger.info(f"Syncing AWS data for {days} days")
        result = chatbot.sync_aws_data(days=days)

        return jsonify(result), 200 if result["status"] == "success" else 400

    except Exception as e:
        logger.error(f"Error in sync endpoint: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/query", methods=["POST"])
def query_chatbot():
    """
    Query the FinOps chatbot
    
    Request body:
    {
        "query": "What are my highest cost services?"
    }
    """
    try:
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({"status": "error", "message": "Query is required"}), 400

        user_query = data.get("query")
        logger.info(f"Processing query: {user_query}")

        result = chatbot.query(user_query)

        return jsonify(result), 200 if result["status"] == "success" else 400

    except Exception as e:
        logger.error(f"Error in query endpoint: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/summary", methods=["GET"])
def get_summary():
    """Get chatbot summary and statistics"""
    try:
        logger.info("Fetching summary")
        summary = chatbot.get_summary()

        return jsonify(summary), 200 if summary["status"] != "error" else 400

    except Exception as e:
        logger.error(f"Error in summary endpoint: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/report", methods=["GET"])
def get_report():
    """Get optimization report"""
    try:
        logger.info("Generating optimization report")
        report = chatbot.get_optimization_report()

        return jsonify({"status": "success", "report": report}), 200

    except Exception as e:
        logger.error(f"Error in report endpoint: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear_data():
    """Clear all stored data"""
    try:
        logger.info("Clearing all data")
        result = chatbot.clear_data()

        return jsonify(result), 200 if result["status"] == "success" else 400

    except Exception as e:
        logger.error(f"Error in clear endpoint: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/insights", methods=["GET"])
def get_insights():
    """Get all optimization insights"""
    try:
        logger.info("Fetching insights")
        insights = chatbot.optimization_insights

        return jsonify({
            "status": "success",
            "insights": insights,
            "total": len(insights),
            "total_savings": sum(i.get("potential_savings", 0) for i in insights)
        }), 200

    except Exception as e:
        logger.error(f"Error in insights endpoint: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Interactive chat endpoint with conversation history
    
    Request body:
    {
        "message": "What are my top cost drivers?",
        "conversation_id": "optional-id"
    }
    """
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"status": "error", "message": "Message is required"}), 400

        user_message = data.get("message")
        conversation_id = data.get("conversation_id", "default")

        logger.info(f"Chat message from {conversation_id}: {user_message}")

        # Process the message
        result = chatbot.query(user_message)

        response = {
            "status": "success",
            "conversation_id": conversation_id,
            "user_message": user_message,
            "bot_response": result.get("response", ""),
            "relevant_data": {
                "costs": result.get("relevant_costs", []),
                "resources": result.get("relevant_resources", []),
                "optimizations": result.get("relevant_optimizations", [])
            }
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"status": "error", "message": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False") == "True"

    logger.info(f"Starting FinOps Chatbot API on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
