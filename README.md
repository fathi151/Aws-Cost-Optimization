# AWS Cost Optimization Chatbot - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technologies](#technologies)
4. [Features](#features)
5. [Installation & Setup](#installation--setup)
6. [Project Structure](#project-structure)
7. [Backend Modules](#backend-modules)
8. [Frontend Components](#frontend-components)
9. [API Endpoints](#api-endpoints)
10. [Configuration](#configuration)
11. [AWS Optimization Guide](#aws-optimization-guide)
12. [Email Service Setup](#email-service-setup)
13. [Usage Guide](#usage-guide)
14. [Troubleshooting](#troubleshooting)
15. [Contributing](#contributing)

---

## Project Overview

**AWS Cost Optimization Chatbot** is an AI-powered application designed to help organizations optimize their AWS spending. The chatbot leverages machine learning and AWS analytics to provide actionable recommendations for cost reduction.

### Key Objectives
- Analyze AWS cost and usage data
- Identify optimization opportunities
- Provide intelligent recommendations through conversational AI
- Generate detailed reports and insights
- Enable FinOps (Financial Operations) best practices

### Target Users
- AWS account administrators
- FinOps teams
- Cloud architects
- Cost optimization specialists

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ┌──────────────┬──────────────┬──────────────┐             │
│  │ ChatInterface│  Dashboard   │ ReportsPanel │             │
│  └──────────────┴──────────────┴──────────────┘             │
└─────────────────────────────────────────────────────────────┘
                          ↓ HTTP/REST
┌────────────────────���────────────────────────────────────────┐
│                  Backend (Flask API)                         │
│  ┌──────────────┬──────────────┬──────────────┐             │
│  │   Chatbot    │  AWS Cost    │   Email      │             │
│  │   Engine     │  Extractor   │   Service    │             │
│  └──────────────┴──────────────┴──────────────┘             │
│  ┌──────────────┬──────────────┬──────────────┐             │
│  │  Analytics   │  Scheduler   │  Database    │             │
│  └──────────────┴──────────────┴──────────────┘             │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌─────────┐          ┌─��───────┐         ┌─────────┐
    │   AWS   │          │ Mistral │         │ SQLite  │
    │   APIs  │          │   AI    │         │   DB    │
    └─────────┘          └─────────┘         └─────────┘
```

### Data Flow

1. **User Input** → Frontend sends query to backend
2. **Processing** → Backend processes with AI engine
3. **AWS Integration** → Fetches cost data from AWS
4. **Analysis** → Advanced analytics processes data
5. **Response** → AI generates recommendations
6. **Output** → Frontend displays results

---

## Technologies

### Backend Stack
- **Language:** Python 3.8+
- **Framework:** Flask
- **AI/ML:** LangChain, Mistral AI
- **Vector Store:** ChromaDB
- **AWS SDK:** Boto3
- **Database:** SQLite
- **Task Scheduling:** APScheduler

### Frontend Stack
- **Framework:** React.js
- **Styling:** CSS3
- **HTTP Client:** Fetch API
- **Build Tool:** npm/webpack

### Infrastructure
- **Cloud Provider:** AWS
- **Services Used:** 
  - AWS Cost Explorer API
  - AWS Billing API
  - CloudWatch
  - IAM

---

## Features

### 1. AWS Cost Analysis
- Real-time cost data retrieval
- Historical cost trends
- Cost breakdown by service
- Cost forecasting

### 2. AI-Powered Recommendations
- Intelligent cost optimization suggestions
- Context-aware recommendations
- Priority-based recommendations
- Implementation guidance

### 3. Interactive Chat Interface
- Natural language queries
- Conversational AI responses
- Multi-turn conversations
- Query history

### 4. Dashboards & Reports
- Cost overview dashboard
- Service-wise cost breakdown
- Trend analysis charts
- Exportable reports

### 5. Email Notifications
- Send optimization reports
- Alert notifications
- Customer inquiry support
- Scheduled reports

### 6. Advanced Analytics
- Cost anomaly detection
- Trend analysis
- Predictive analytics
- Custom metrics

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm
- AWS Account with appropriate permissions
- Git

### Backend Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/fathi151/Aws-Cost-Optimization.git
cd Aws-Cost-Optimization
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables
Create `.env` file in root directory:
```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Mistral AI Configuration
MISTRAL_API_KEY=your_mistral_api_key

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SUPPORT_EMAIL=maddehclement@gmail.com

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key
```

#### Step 5: Initialize Database
```bash
python -c "from backend.database import init_db; init_db()"
```

#### Step 6: Run Backend
```bash
flask run
```
Backend will run on `http://127.0.0.1:5000`

### Frontend Setup

#### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

#### Step 2: Install Dependencies
```bash
npm install
```

#### Step 3: Configure API Endpoint
Update `frontend/src/config.js`:
```javascript
export const API_BASE_URL = 'http://127.0.0.1:5000';
```

#### Step 4: Start Development Server
```bash
npm start
```
Frontend will open at `http://localhost:3000`

---

## Project Structure

```
amazon/
├── backend/                          # Backend Python modules
│   ├── advanced_analytics.py         # Advanced analytics engine
│   ├── app.py                        # Main Flask application
│   ├── app_simple.py                 # Simplified app version
│   ├── aws_cost_extractor.py         # AWS cost extraction
│   ├── aws_cost_extractors.py        # Additional extractors
│   ├── chatbot.py                    # Chatbot core logic
│   ├── chromadb_store.py             # ChromaDB integration
│   ├── data_processor.py             # Data processing utilities
│   ├── database.py                   # Database models
│   ├── email_routes.py               # Email API routes
│   ├── email_service.py              # Email service
│   ├── finops_chatbot.py             # FinOps chatbot
│   ├── finops_chatbot_simple.py      # Simplified FinOps chatbot
│   ├── mistral_ai_engine.py          # Mistral AI integration
│   └── scheduler.py                  # Task scheduler
│
├── frontend/                         # React frontend
│   ├── public/
│   │   └── index.html                # HTML entry point
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.js      # Chat component
│   │   │   ├── Dashboard.js          # Dashboard component
│   │   │   ├── EmailSupport.js       # Email support component
│   │   │   ├── InsightsPanel.js      # Insights component
│   │   │   └── ReportsPanel.js       # Reports component
│   │   ├── App.js                    # Main App component
│   │   ├── index.css                 # Global styles
│   │   └── index.js                  # React entry point
│   ├── package.json                  # Frontend dependencies
│   └── package-lock.json
│
├── config/                           # Configuration files
│   ├── .env.example                  # Environment variables template
│   └── config.py                     # Configuration module
│
├── tests/                            # Test files
│   ├── test_chatbot.py               # Chatbot tests
│   ├── test_data_retrieval.py        # Data retrieval tests
│   └── test_email_credentials.py     # Email service tests
│
├── scripts/                          # Utility scripts
│   ├── batch_commits.ps1             # Batch commit script
│   └── diagnose_issue.py             # Diagnostic script
│
├── docs/                             # Documentation
│   ├── AWS_OPTIMIZATION_GUIDE.md     # AWS optimization guide
│   ├── EMAIL_SETUP.md                # Email setup guide
│   ├── README.md                     # Project README
│   └── PROJECT_DOCUMENTATION.md      # This file
│
���── templates/                        # HTML templates
│   ├── index.html
│   ├── index_clean.html
│   ├── index_enhanced.html
│   └── index_pro.html
│
├── .env                              # Environment variables (not in git)
├── .env.example                      # Environment template
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
├── README.md                         # Project README
└── finops.db                         # SQLite database
```

---

## Backend Modules

### app.py - Main Flask Application
**Purpose:** Entry point for the Flask backend server

**Key Functions:**
- Initialize Flask app
- Register blueprints
- Configure CORS
- Setup error handlers
- Initialize database

**Usage:**
```bash
flask run
```

### chatbot.py - Chatbot Core Logic
**Purpose:** Implements the chatbot conversation engine

**Key Classes:**
- `Chatbot` - Main chatbot class
- `ConversationManager` - Manages conversation history

**Key Methods:**
- `process_query()` - Process user queries
- `generate_response()` - Generate AI responses
- `get_context()` - Retrieve relevant context

### mistral_ai_engine.py - Mistral AI Integration
**Purpose:** Integrates Mistral AI for intelligent responses

**Key Functions:**
- `initialize_mistral()` - Initialize AI engine
- `generate_recommendation()` - Generate recommendations
- `analyze_costs()` - Analyze cost data

### aws_cost_extractor.py - AWS Cost Extraction
**Purpose:** Retrieves cost and usage data from AWS

**Key Functions:**
- `get_cost_and_usage()` - Fetch cost data
- `get_service_costs()` - Get costs by service
- `get_cost_forecast()` - Forecast future costs

**AWS APIs Used:**
- Cost Explorer API
- Billing API
- CloudWatch API

### email_service.py - Email Service
**Purpose:** Handles email sending functionality

**Key Functions:**
- `send_inquiry()` - Send customer inquiry
- `send_report()` - Send cost report
- `send_alert()` - Send alert notification

### database.py - Database Models
**Purpose:** Defines database schema and models

**Key Models:**
- `User` - User information
- `CostData` - Cost records
- `Recommendation` - AI recommendations
- `EmailLog` - Email sending logs

### scheduler.py - Task Scheduler
**Purpose:** Schedules automated tasks

**Scheduled Tasks:**
- Daily cost data refresh
- Weekly report generation
- Monthly optimization review

### advanced_analytics.py - Advanced Analytics
**Purpose:** Performs advanced data analysis

**Key Functions:**
- `detect_anomalies()` - Detect cost anomalies
- `trend_analysis()` - Analyze trends
- `predict_costs()` - Predict future costs

---

## Frontend Components

### ChatInterface.js
**Purpose:** Provides the chat interface for user interaction

**Features:**
- Message input field
- Message history display
- Real-time message updates
- Typing indicators

**Props:**
```javascript
{
  onSendMessage: (message) => void,
  messages: Array,
  isLoading: boolean
}
```

### Dashboard.js
**Purpose:** Displays cost overview and key metrics

**Features:**
- Total cost display
- Cost trend chart
- Service breakdown
- Key metrics

**Data:**
```javascript
{
  totalCost: number,
  monthlyTrend: Array,
  serviceBreakdown: Object,
  savings: number
}
```

### ReportsPanel.js
**Purpose:** Shows detailed reports and analytics

**Features:**
- Report generation
- Report export
- Historical reports
- Custom date ranges

### InsightsPanel.js
**Purpose:** Displays AI-generated insights

**Features:**
- Top recommendations
- Cost anomalies
- Optimization opportunities
- Implementation guides

---

## API Endpoints

### Chat Endpoints

#### POST /api/chat/message
Send a message to the chatbot

**Request:**
```json
{
  "message": "How can I reduce my EC2 costs?",
  "conversation_id": "conv_123"
}
```

**Response:**
```json
{
  "status": "success",
  "response": "Here are some ways to reduce EC2 costs...",
  "recommendations": [...]
}
```

### Cost Endpoints

#### GET /api/costs/summary
Get cost summary

**Response:**
```json
{
  "total_cost": 5000,
  "monthly_average": 4500,
  "trend": "increasing",
  "by_service": {...}
}
```

#### GET /api/costs/by-service
Get costs breakdown by service

**Response:**
```json
{
  "EC2": 2000,
  "RDS": 1000,
  "S3": 500,
  ...
}
```

### Email Endpoints

#### POST /api/email/send-inquiry
Send customer inquiry

**Request:**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "subject": "Cost optimization help",
  "message": "I need help optimizing my AWS costs"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Inquiry sent successfully"
}
```

#### POST /api/email/send-report
Send cost report via email

**Request:**
```json
{
  "recipient_email": "user@example.com",
  "report_type": "monthly",
  "date_range": "2024-01"
}
```

---

## Configuration

### Environment Variables

#### AWS Configuration
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
```

#### Mistral AI Configuration
```env
MISTRAL_API_KEY=your_api_key
MISTRAL_MODEL=mistral-large
```

#### Email Configuration
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SUPPORT_EMAIL=maddehclement@gmail.com
```

#### Flask Configuration
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///finops.db
```

### AWS IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "ce:GetReservationPurchaseRecommendation",
        "ce:GetSavingsPlansPurchaseRecommendation",
        "ce:ListCostAllocationTags",
        "ce:GetDimensionValues",
        "ce:GetTags",
        "ce:DescribeNotificationSubscription",
        "ce:GetPreferences"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## AWS Optimization Guide

### Quick Wins (Immediate Actions)

1. **Enable S3 Intelligent-Tiering**
   - Automatically moves objects between access tiers
   - Saves up to 70% on storage costs

2. **Delete Unused Elastic IPs**
   - Charges apply even when not in use
   - Quick audit and cleanup

3. **Remove Unattached EBS Volumes**
   - Reduces storage costs
   - Use AWS Config to identify

4. **Terminate Idle EC2 Instances**
   - Use CloudWatch metrics
   - Identify underutilized instances

5. **Implement VPC Endpoints**
   - Avoid data transfer charges
   - Reduces NAT gateway costs

### Compute Optimization

#### EC2 Right-Sizing
- Analyze CloudWatch metrics
- Use AWS Compute Optimizer
- Choose appropriate instance types
- Consider Reserved Instances (30-70% savings)
- Use Spot Instances (up to 90% savings)

#### Lambda Optimization
- Right-size memory allocation
- Optimize code execution time
- Use Lambda Layers
- Monitor duration and memory

### Storage Optimization

#### S3 Storage Classes
- **Standard:** Frequently accessed data
- **Intelligent-Tiering:** Automatic optimization
- **Standard-IA:** Infrequent access (30-day minimum)
- **Glacier:** Archive data (90-day minimum)
- **Deep Archive:** Long-term retention (180-day minimum)

#### Lifecycle Policies
- Automatically transition objects
- Delete old versions
- Archive infrequently accessed data

### Database Optimization

#### RDS
- Right-size instances
- Use Aurora for better cost-effectiveness
- Enable automated backups
- Use read replicas
- Consider Reserved Instances

#### DynamoDB
- Use on-demand for unpredictable workloads
- Use provisioned capacity for predictable workloads
- Implement TTL for automatic cleanup
- Monitor consumed capacity

### Networking Optimization

#### VPC Endpoints
- Avoid NAT gateway charges
- Reduce data transfer costs
- Improve security

#### Load Balancing
- Choose appropriate load balancer type
- Remove unused load balancers
- Optimize target groups

---

## Email Service Setup

### Gmail Configuration

1. **Enable 2-Step Verification**
   - Go to Google Account Security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to App passwords
   - Select Mail and your device
   - Copy the 16-character password

3. **Configure .env**
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   ```

### Email API Usage

#### Send Inquiry
```python
from backend.email_service import EmailService

email_service = EmailService()
result = email_service.send_customer_inquiry(
    customer_name="John Doe",
    customer_email="john@example.com",
    subject="Cost optimization help",
    message="I need help with AWS costs"
)
```

#### Send Report
```python
result = email_service.send_cost_report(
    recipient_email="user@example.com",
    report_data={...}
)
```

---

## Usage Guide

### For End Users

#### 1. Access the Application
- Open browser to `http://localhost:3000`
- Login with your credentials

#### 2. Chat with the Chatbot
- Type your AWS cost optimization question
- Receive AI-powered recommendations
- Ask follow-up questions

#### 3. View Dashboard
- See cost overview
- View service breakdown
- Check cost trends

#### 4. Generate Reports
- Select date range
- Choose report type
- Export or email report

#### 5. Get Insights
- View top recommendations
- Check cost anomalies
- Implement suggestions

### For Developers

#### 1. Add New Features
- Create new modules in `backend/`
- Add routes in `app.py`
- Create React components in `frontend/src/components/`

#### 2. Extend AI Capabilities
- Modify `mistral_ai_engine.py`
- Add new prompt templates
- Train on custom data

#### 3. Add New AWS Services
- Extend `aws_cost_extractor.py`
- Add new API calls
- Update analytics

#### 4. Customize Email Templates
- Modify `email_service.py`
- Create HTML templates
- Add custom styling

---

## Troubleshooting

### Backend Issues

#### Issue: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue: "AWS credentials not found"
**Solution:**
- Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env
- Or configure AWS CLI: `aws configure`

#### Issue: "Database locked"
**Solution:**
- Close other connections to database
- Delete `finops.db` and reinitialize

#### Issue: "Mistral API error"
**Solution:**
- Verify MISTRAL_API_KEY in .env
- Check API rate limits
- Verify API key is valid

### Frontend Issues

#### Issue: "Cannot connect to backend"
**Solution:**
- Verify backend is running on port 5000
- Check API_BASE_URL in config
- Check CORS configuration

#### Issue: "Blank page"
**Solution:**
```bash
npm install
npm start
```

#### Issue: "CSS not loading"
**Solution:**
- Clear browser cache
- Rebuild: `npm run build`

### Email Issues

#### Issue: "Email credentials not configured"
**Solution:**
- Set SENDER_EMAIL and SENDER_PASSWORD in .env
- Use App Password for Gmail

#### Issue: "Authentication failed"
**Solution:**
- Verify 2-Step Verification is enabled
- Use correct App Password
- Check email address matches

#### Issue: "Connection refused"
**Solution:**
- Verify SMTP_SERVER and SMTP_PORT
- Check internet connection
- Check firewall settings

---

## Contributing

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Follow code style guidelines
   - Add tests for new features
   - Update documentation

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: description of changes"
   ```

4. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature
   ```

### Code Style Guidelines

- **Python:** Follow PEP 8
- **JavaScript:** Use ES6+ syntax
- **Comments:** Add meaningful comments
- **Functions:** Keep functions small and focused

### Testing

```bash
# Run Python tests
pytest tests/

# Run specific test
pytest tests/test_chatbot.py

# Run with coverage
pytest --cov=backend tests/
```

### Documentation

- Update README for major changes
- Add docstrings to functions
- Update API documentation
- Add examples for new features

---

## Support & Contact

- **Email:** maddehclement@gmail.com
- **GitHub:** https://github.com/fathi151/Aws-Cost-Optimization
- **Issues:** Report bugs on GitHub Issues

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- AWS cost extraction
- AI-powered chatbot
- Email service
- Dashboard and reports
- Advanced analytics

---

**Last Updated:** 2024
**Maintained By:** FinOps Team
