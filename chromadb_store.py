"""
ChromaDB Vector Store Module
Handles storage and retrieval of AWS cost data using ChromaDB for efficient similarity search
"""

import chromadb
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChromaDBStore:
    """Manage AWS cost data storage and retrieval using ChromaDB"""

    def __init__(self, persist_directory: str = "./data/chromadb"):
        """
        Initialize ChromaDB client
        
        Args:
            persist_directory: Path to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        self.client = chromadb.Client()
        
        # Create or get collections
        self.cost_collection = self.client.get_or_create_collection(
            name="aws_costs",
            metadata={"hnsw:space": "cosine"}
        )
        self.optimization_collection = self.client.get_or_create_collection(
            name="optimization_insights",
            metadata={"hnsw:space": "cosine"}
        )
        self.resource_collection = self.client.get_or_create_collection(
            name="aws_resources",
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"ChromaDB initialized with persist directory: {persist_directory}")

    def add_cost_data(self, cost_data: List[Dict[str, Any]]) -> None:
        """
        Add cost data to ChromaDB
        
        Args:
            cost_data: List of cost data dictionaries
        """
        try:
            # Skip if no data to add
            if not cost_data:
                logger.info("No cost data to add to ChromaDB")
                return

            documents = []
            metadatas = []
            ids = []

            for idx, data in enumerate(cost_data):
                doc_id = hashlib.md5(
                    f"{data.get('service')}{data.get('date')}{idx}".encode()
                ).hexdigest()

                document = f"""
                Service: {data.get('service', 'Unknown')}
                Region: {data.get('region', 'Unknown')}
                Cost: ${data.get('cost', 0):.2f}
                Usage: {data.get('usage', 0)}
                Date: {data.get('date', 'Unknown')}
                """

                documents.append(document)
                metadatas.append(
                    {
                        "service": data.get("service", ""),
                        "region": data.get("region", ""),
                        "cost": str(data.get("cost", 0)),
                        "date": data.get("date", ""),
                    }
                )
                ids.append(doc_id)

            self.cost_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(cost_data)} cost records to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding cost data to ChromaDB: {str(e)}")
            raise

    def add_resource_data(self, resource_data: List[Dict[str, Any]]) -> None:
        """
        Add resource data to ChromaDB
        
        Args:
            resource_data: List of resource information dictionaries
        """
        try:
            # Skip if no data to add
            if not resource_data:
                logger.info("No resource data to add to ChromaDB")
                return

            documents = []
            metadatas = []
            ids = []

            for idx, resource in enumerate(resource_data):
                doc_id = hashlib.md5(
                    f"{resource.get('instance_id', idx)}".encode()
                ).hexdigest()

                document = f"""
                Instance ID: {resource.get('instance_id', 'Unknown')}
                Instance Type: {resource.get('instance_type', 'Unknown')}
                State: {resource.get('state', 'Unknown')}
                Region: {resource.get('region', 'Unknown')}
                Launch Time: {resource.get('launch_time', 'Unknown')}
                Tags: {json.dumps(resource.get('tags', {}))}
                """

                documents.append(document)
                metadatas.append(
                    {
                        "instance_id": resource.get("instance_id", ""),
                        "instance_type": resource.get("instance_type", ""),
                        "state": resource.get("state", ""),
                        "region": resource.get("region", ""),
                    }
                )
                ids.append(doc_id)

            self.resource_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(resource_data)} resource records to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding resource data to ChromaDB: {str(e)}")
            raise

    def add_optimization_insights(self, insights: List[Dict[str, Any]]) -> None:
        """
        Add optimization insights to ChromaDB
        
        Args:
            insights: List of optimization insight dictionaries
        """
        try:
            # Skip if no data to add
            if not insights:
                logger.info("No optimization insights to add to ChromaDB")
                return

            documents = []
            metadatas = []
            ids = []

            for idx, insight in enumerate(insights):
                doc_id = hashlib.md5(
                    f"{insight.get('title', idx)}{datetime.now().isoformat()}".encode()
                ).hexdigest()

                document = f"""
                Title: {insight.get('title', 'Unknown')}
                Description: {insight.get('description', 'Unknown')}
                Potential Savings: ${insight.get('potential_savings', 0):.2f}
                Priority: {insight.get('priority', 'Medium')}
                Category: {insight.get('category', 'Unknown')}
                """

                documents.append(document)
                metadatas.append(
                    {
                        "title": insight.get("title", ""),
                        "priority": insight.get("priority", ""),
                        "category": insight.get("category", ""),
                        "savings": str(insight.get("potential_savings", 0)),
                    }
                )
                ids.append(doc_id)

            self.optimization_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(insights)} optimization insights to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding optimization insights to ChromaDB: {str(e)}")
            raise

    def query_costs(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query cost data using natural language
        
        Args:
            query: Natural language query
            n_results: Number of results to return
        
        Returns:
            Query results with costs and metadata
        """
        try:
            results = self.cost_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying costs: {str(e)}")
            return {"documents": [], "metadatas": [], "distances": []}

    def query_resources(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query resource data using natural language
        
        Args:
            query: Natural language query
            n_results: Number of results to return
        
        Returns:
            Query results with resources and metadata
        """
        try:
            results = self.resource_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying resources: {str(e)}")
            return {"documents": [], "metadatas": [], "distances": []}

    def query_optimizations(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query optimization insights using natural language
        
        Args:
            query: Natural language query
            n_results: Number of results to return
        
        Returns:
            Query results with optimization insights
        """
        try:
            results = self.optimization_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying optimizations: {str(e)}")
            return {"documents": [], "metadatas": [], "distances": []}

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored collections
        
        Returns:
            Dictionary with collection statistics
        """
        return {
            "cost_records": self.cost_collection.count(),
            "resource_records": self.resource_collection.count(),
            "optimization_records": self.optimization_collection.count(),
            "timestamp": datetime.now().isoformat(),
        }

    def search_costs(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search cost data and return formatted results
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of cost data dictionaries
        """
        try:
            results = self.query_costs(query, n_results=limit)
            formatted_results = []
            
            if results.get("metadatas") and len(results["metadatas"]) > 0:
                for metadata in results["metadatas"][0]:
                    formatted_results.append({
                        "service": metadata.get("service", ""),
                        "region": metadata.get("region", ""),
                        "cost": float(metadata.get("cost", 0)),
                        "date": metadata.get("date", ""),
                    })
            
            logger.info(f"Search costs returned {len(formatted_results)} results for query: {query}")
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching costs: {str(e)}")
            return []

    def search_resources(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search resource data and return formatted results
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of resource data dictionaries
        """
        try:
            results = self.query_resources(query, n_results=limit)
            formatted_results = []
            
            if results.get("metadatas") and len(results["metadatas"]) > 0:
                for metadata in results["metadatas"][0]:
                    formatted_results.append({
                        "instance_id": metadata.get("instance_id", ""),
                        "instance_type": metadata.get("instance_type", ""),
                        "state": metadata.get("state", ""),
                        "region": metadata.get("region", ""),
                    })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching resources: {str(e)}")
            return []

    def search_optimizations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search optimization insights and return formatted results
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of optimization insight dictionaries
        """
        try:
            results = self.query_optimizations(query, n_results=limit)
            formatted_results = []
            
            if results.get("metadatas") and len(results["metadatas"]) > 0:
                for metadata in results["metadatas"][0]:
                    formatted_results.append({
                        "title": metadata.get("title", ""),
                        "priority": metadata.get("priority", ""),
                        "category": metadata.get("category", ""),
                        "savings": float(metadata.get("savings", 0)),
                    })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching optimizations: {str(e)}")
            return []

    def clear_collections(self) -> None:
        """Clear all collections"""
        try:
            self.client.delete_collection(name="aws_costs")
            self.client.delete_collection(name="optimization_insights")
            self.client.delete_collection(name="aws_resources")
            
            # Recreate collections
            self.cost_collection = self.client.get_or_create_collection(
                name="aws_costs",
                metadata={"hnsw:space": "cosine"}
            )
            self.optimization_collection = self.client.get_or_create_collection(
                name="optimization_insights",
                metadata={"hnsw:space": "cosine"}
            )
            self.resource_collection = self.client.get_or_create_collection(
                name="aws_resources",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("All collections cleared and recreated")
        except Exception as e:
            logger.error(f"Error clearing collections: {str(e)}")
