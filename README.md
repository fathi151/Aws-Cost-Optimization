# AWS Cost Optimization Chatbot

## Project Description
This project provides an AI-powered chatbot designed to help users optimize their AWS costs. It integrates with AWS services to analyze spending, identify areas for improvement, and offer actionable recommendations. The chatbot aims to simplify FinOps (Financial Operations) by providing an interactive and intelligent interface for cost management.

## Key Features
- **AWS Cost Analysis**: Connects to AWS accounts to retrieve and analyze cost and usage data.
- **AI-Powered Recommendations**: Utilizes a large language model (LLM) to generate tailored cost optimization suggestions.
- **Interactive Chat Interface**: Allows users to query their AWS spending and receive insights through a conversational interface.
- **Reporting and Dashboards**: Provides visualizations and reports on cost trends and optimization opportunities.
- **Email Support**: Integrates with email services for sending reports or alerts.

## Technologies Used
**Backend:**
- Python
- Flask (for API)
- LangChain (for LLM integration)
- ChromaDB (for vector store/knowledge base)
- Boto3 (for AWS SDK)
- SQLite (for local database)

**Frontend:**
- React.js
- HTML/CSS/JavaScript

## Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js and npm (for frontend)
- AWS Account with appropriate permissions to access cost and usage data.

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/fathi151/Aws-Cost-Optimization.git
    cd Aws-Cost-Optimization
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure AWS Credentials:**
    Ensure your AWS credentials are set up. You can configure them via environment variables, AWS CLI, or an `~/.aws/credentials` file. The application uses `boto3` to interact with AWS.

5.  **Environment Variables:**
    Create a `.env` file in the root directory based on `.env.example` and fill in the necessary values, especially for your LLM API key (e.g., Mistral AI) and any email service credentials.

    ```
    # .env example
    MISTRAL_API_KEY=your_mistral_api_key
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    AWS_REGION=your_aws_region
    EMAIL_USERNAME=your_email@example.com
    EMAIL_PASSWORD=your_email_password
    EMAIL_SERVER=smtp.example.com
    EMAIL_PORT=587
    ```

6.  **Run the Flask backend:**
    ```bash
    flask run
    ```
    The backend API will typically run on `http://127.0.0.1:5000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install frontend dependencies:**
    ```bash
    npm install
    ```

3.  **Start the React development server:**
    ```bash
    npm start
    ```
    The frontend application will typically open in your browser at `http://localhost:3000`.

## Usage
Once both the backend and frontend are running:
1.  Open your web browser and navigate to `http://localhost:3000`.
2.  Interact with the chatbot through the chat interface to ask questions about your AWS costs, get optimization recommendations, and view reports.
3.  Use the dashboard and reports panel to visualize your AWS spending.

## Project Structure

```
.
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── advanced_analytics.py    # Advanced analytics module
├── app.py                   # Main Flask application
├── aws_cost_extractor.py    # AWS cost extraction logic
├── AWS_OPTIMIZATION_GUIDE.md # AWS optimization guide
├── chatbot.py               # Chatbot core logic
├── chromadb_store.py        # ChromaDB vector store integration
├── config.py                # Application configuration
├── data_processor.py        # Data processing utilities
├── database.py              # Database utilities (e.g., SQLite)
├── diagnose_issue.py        # Module for diagnosing issues
├── email_routes.py          # Flask routes for email functionality
├── email_service.py         # Email sending service
├── EMAIL_SETUP.md           # Email setup documentation
├── finops_chatbot.py        # FinOps specific chatbot logic
├── mistral_ai_engine.py     # Mistral AI integration
├── requirements.txt         # Python dependencies
├── scheduler.py             # Task scheduler
├── frontend/                # React frontend application
│   ├── public/              # Public assets
│   ├── src/                 # Frontend source code
│   │   ├── components/      # React components (ChatInterface, Dashboard, etc.)
│   │   ├── App.js           # Main App component
│   │   └── index.js         # Entry point
│   ├── package.json         # Frontend dependencies
│   └── package-lock.json    # Frontend dependency lock file
├── templates/               # HTML templates
└── tests/                   # Unit and integration tests
