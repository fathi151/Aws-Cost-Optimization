"""
FinOps Chatbot Main Module
Orchestrates AWS data extraction, storage, and AI-powered optimization insights
"""

import logging
import os
from typing import Dict, Any, List
from datetime import datetime
from dotenv import load_dotenv

from aws_cost_extractor import AWSCostExtractor
from chromadb_store import ChromaDBStore
from mistral_ai_engine import MistralAIEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class FinOpsChatbot:
    """Main FinOps Chatbot orchestrator"""

    def __init__(self):
        """Initialize the FinOps Chatbot"""
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY", "")
        self.chromadb_path = os.getenv("CHROMADB_PATH", "./data/chromadb")

        # Initialize components
        try:
            self.cost_extractor = AWSCostExtractor(region=self.aws_region)
            logger.info("AWS Cost Extractor initialized")
        except Exception as e:
            logger.warning(f"AWS Cost Extractor initialization failed: {str(e)}")
            self.cost_extractor = None

        self.vector_store = ChromaDBStore(persist_directory=self.chromadb_path)
        logger.info("ChromaDB Vector Store initialized")

        self.ai_engine = MistralAIEngine(api_key=self.mistral_api_key)
        logger.info("Mistral AI Engine initialized")

        self.optimization_insights = []
        logger.info("FinOps Chatbot initialized successfully")

    def sync_aws_data(self, days: int = 30) -> Dict[str, Any]:
        """
        Sync AWS data and generate optimization insights
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Dictionary with sync results
        """
        if not self.cost_extractor:
            logger.error("AWS Cost Extractor not available")
            return {"status": "error", "message": "AWS credentials not configured"}

        try:
            logger.info(f"Starting AWS data sync for {days} days")

            # Extract AWS data
            optimization_data = self.cost_extractor.generate_optimization_data(days=days)

            # Store in ChromaDB (these methods now handle empty data gracefully)
            self.vector_store.add_cost_data(optimization_data.get("service_breakdown", []))
            self.vector_store.add_resource_data(optimization_data.get("ec2_instances", []))

            # Generate optimization insights
            self.optimization_insights = self.ai_engine.generate_optimization_insights(
                cost_data=optimization_data.get("service_breakdown", []),
                resource_data=optimization_data.get("ec2_instances", []),
                unused_resources=optimization_data.get("unused_resources", {})
            )

            # Store insights (this method now handles empty data gracefully)
            self.vector_store.add_optimization_insights(self.optimization_insights)

            result = {
                "status": "success",
                "message": "AWS data synced successfully",
                "data_points": len(optimization_data.get("service_breakdown", [])),
                "insights_generated": len(self.optimization_insights),
                "timestamp": datetime.now().isoformat(),
            }

            logger.info(f"AWS data sync completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Error syncing AWS data: {str(e)}")
            return {"status": "error", "message": str(e)}

    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Process user query and return AI-powered response
        
        Args:
            user_query: User's natural language query
        
        Returns:
            Dictionary with response and relevant data
        """
        try:
            logger.info(f"Processing query: {user_query}")

            # Retrieve ALL actual AWS data from vector store (not just search results)
            # This ensures we always get the data, not just search matches
            cost_data = self.vector_store.search_costs(user_query, limit=100)
            resource_data = self.vector_store.search_resources(user_query, limit=100)
            optimization_data = self.vector_store.search_optimizations(user_query, limit=50)

            logger.info(f"Retrieved {len(cost_data)} costs, {len(resource_data)} resources, {len(optimization_data)} optimizations")

            # Build context with real data
            context = {
                "costs": cost_data,
                "resources": resource_data,
                "optimizations": optimization_data,
                "insights": self.optimization_insights[:5],
            }

            # Generate AI response with actual data
            ai_response = self.ai_engine.answer_query(user_query, context)

            result = {
                "status": "success",
                "query": user_query,
                "response": ai_response,
                "relevant_costs": cost_data,
                "relevant_resources": resource_data,
                "relevant_optimizations": optimization_data,
                "timestamp": datetime.now().isoformat(),
            }

            logger.info(f"Query processed successfully with {len(cost_data)} costs and {len(resource_data)} resources")
            return result

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "status": "error",
                "query": user_query,
                "response": f"Error processing query: {str(e)}",
                "relevant_costs": [],
                "relevant_resources": [],
                "relevant_optimizations": [],
                "timestamp": datetime.now().isoformat(),
            }

    def get_optimization_report(self) -> str:
        """
        Generate comprehensive optimization report
        
        Returns:
            Formatted report string
        """
        try:
            logger.info("Generating optimization report")
            report = self.ai_engine.generate_report(self.optimization_insights)
            return report
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return "Error generating report"

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of current state
        
        Returns:
            Dictionary with summary information
        """
        try:
            stats = self.vector_store.get_collection_stats()

            total_potential_savings = sum(
                i.get("potential_savings", 0) for i in self.optimization_insights
            )

            summary = {
                "status": "active",
                "collection_stats": stats,
                "total_insights": len(self.optimization_insights),
                "total_potential_savings": total_potential_savings,
                "top_insights": self.optimization_insights[:5],
                "timestamp": datetime.now().isoformat(),
            }

            return summary
        except Exception as e:
            logger.error(f"Error getting summary: {str(e)}")
            return {"status": "error", "message": str(e)}

    def clear_data(self) -> Dict[str, Any]:
        """
        Clear all stored data
        
        Returns:
            Status dictionary
        """
        try:
            self.vector_store.clear_collections()
            self.optimization_insights = []
            logger.info("All data cleared")
            return {"status": "success", "message": "All data cleared"}
        except Exception as e:
            logger.error(f"Error clearing data: {str(e)}")
            return {"status": "error", "message": str(e)}


def main():
    """Main entry point for testing"""
    logger.info("Starting FinOps Chatbot")

    # Initialize chatbot
    chatbot = FinOpsChatbot()

    # Example usage
    print("\n=== FinOps Chatbot ===\n")

    # Sync AWS data (requires AWS credentials)
    print("Syncing AWS data...")
    sync_result = chatbot.sync_aws_data(days=30)
    print(f"Sync result: {sync_result}\n")

    # Get summary
    print("Getting summary...")
    summary = chatbot.get_summary()
    print(f"Summary: {summary}\n")

    # Example queries
    example_queries = [
        "What are my highest cost services?",
        "How can I optimize my EC2 spending?",
        "What unused resources do I have?",
        "What are the top cost optimization opportunities?",
    ]

    for query in example_queries:
        print(f"Query: {query}")
        response = chatbot.query(query)
        print(f"Response: {response['response']}\n")

    # Generate report
    print("Generating optimization report...")
    report = chatbot.get_optimization_report()
    print(report)


if __name__ == "__main__":
    main()
