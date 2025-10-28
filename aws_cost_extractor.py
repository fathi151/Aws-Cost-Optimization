"""
AWS Cost Explorer Data Extraction Module
Handles extraction of AWS usage and cost data from AWS Cost Explorer API
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSCostExtractor:
    """Extract AWS cost and usage data from AWS Cost Explorer API"""

    def __init__(self, region: str = "us-east-1"):
        """
        Initialize AWS Cost Explorer client
        
        Args:
            region: AWS region for the client
        """
        self.ce_client = boto3.client("ce", region_name=region)
        self.ec2_client = boto3.client("ec2", region_name=region)
        logger.info("AWS Cost Explorer client initialized")

    def get_cost_and_usage(
        self,
        days: int = 30,
        granularity: str = "DAILY",
        metrics: List[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve cost and usage data from AWS Cost Explorer
        
        Args:
            days: Number of days to retrieve data for
            granularity: DAILY, MONTHLY, or HOURLY
            metrics: List of metrics to retrieve (default: BlendedCost, UsageQuantity)
        
        Returns:
            Dictionary containing cost and usage data
        """
        if metrics is None:
            metrics = ["BlendedCost", "UsageQuantity"]

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        try:
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    "Start": start_date.strftime("%Y-%m-%d"),
                    "End": end_date.strftime("%Y-%m-%d"),
                },
                Granularity=granularity,
                Metrics=metrics,
                GroupBy=[
                    {"Type": "DIMENSION", "Key": "SERVICE"},
                    {"Type": "DIMENSION", "Key": "REGION"},
                ],
                Filter={
                    "Dimensions": {
                        "Key": "PURCHASE_TYPE",
                        "Values": ["On Demand", "Reserved"],
                    }
                },
            )
            logger.info(f"Successfully retrieved cost data for {days} days")
            return response
        except Exception as e:
            logger.error(f"Error retrieving cost data: {str(e)}")
            raise

    def get_service_breakdown(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get cost breakdown by AWS service
        
        Args:
            days: Number of days to analyze
        
        Returns:
            List of dictionaries with service costs
        """
        response = self.get_cost_and_usage(days=days)
        service_costs = []

        for result in response.get("ResultsByTime", []):
            for group in result.get("Groups", []):
                service_name = None
                region = None

                for key in group.get("Keys", []):
                    if key.startswith("Amazon"):
                        service_name = key
                    else:
                        region = key

                metrics = group.get("Metrics", {})
                service_costs.append(
                    {
                        "service": service_name,
                        "region": region,
                        "cost": float(metrics.get("BlendedCost", {}).get("Amount", 0)),
                        "usage": float(metrics.get("UsageQuantity", {}).get("Amount", 0)),
                        "date": result.get("TimePeriod", {}).get("Start"),
                    }
                )

        return service_costs

    def get_ec2_instances(self) -> List[Dict[str, Any]]:
        """
        Get EC2 instance details for optimization analysis
        
        Returns:
            List of EC2 instance information
        """
        instances = []
        try:
            response = self.ec2_client.describe_instances()

            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append(
                        {
                            "instance_id": instance.get("InstanceId"),
                            "instance_type": instance.get("InstanceType"),
                            "state": instance.get("State", {}).get("Name"),
                            "launch_time": instance.get("LaunchTime").isoformat()
                            if instance.get("LaunchTime")
                            else None,
                            "region": instance.get("Placement", {}).get("AvailabilityZone"),
                            "tags": {
                                tag["Key"]: tag["Value"]
                                for tag in instance.get("Tags", [])
                            },
                        }
                    )

            logger.info(f"Retrieved {len(instances)} EC2 instances")
            return instances
        except Exception as e:
            logger.error(f"Error retrieving EC2 instances: {str(e)}")
            return []

    def get_unused_resources(self) -> Dict[str, Any]:
        """
        Identify potentially unused or underutilized resources
        
        Returns:
            Dictionary containing unused resources information
        """
        unused_resources = {
            "stopped_instances": [],
            "unattached_volumes": [],
            "unused_elastic_ips": [],
        }

        try:
            # Get stopped instances
            response = self.ec2_client.describe_instances(
                Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
            )

            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    unused_resources["stopped_instances"].append(
                        {
                            "instance_id": instance.get("InstanceId"),
                            "instance_type": instance.get("InstanceType"),
                            "stopped_since": instance.get("StateTransitionReason"),
                        }
                    )

            # Get unattached volumes
            response = self.ec2_client.describe_volumes(
                Filters=[{"Name": "status", "Values": ["available"]}]
            )

            for volume in response.get("Volumes", []):
                unused_resources["unattached_volumes"].append(
                    {
                        "volume_id": volume.get("VolumeId"),
                        "size": volume.get("Size"),
                        "region": volume.get("AvailabilityZone"),
                    }
                )

            logger.info("Successfully identified unused resources")
            return unused_resources
        except Exception as e:
            logger.error(f"Error identifying unused resources: {str(e)}")
            return unused_resources

    def generate_optimization_data(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate comprehensive optimization data
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Dictionary with all optimization-relevant data
        """
        return {
            "service_breakdown": self.get_service_breakdown(days),
            "ec2_instances": self.get_ec2_instances(),
            "unused_resources": self.get_unused_resources(),
            "timestamp": datetime.now().isoformat(),
        }
