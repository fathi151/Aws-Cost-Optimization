"""
Mistral AI Engine Module
Handles natural language processing and AI-powered optimization insights using Mistral AI
"""

import logging
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

try:
    from mistralai import Mistral
    MISTRAL_AVAILABLE = True
except ImportError as e:
    MISTRAL_AVAILABLE = False
    logger_temp = logging.getLogger(__name__)
    logger_temp.warning(f"Mistral AI client not available: {str(e)}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MistralAIEngine:
    """Generate AI-powered optimization insights using Mistral AI"""

    def __init__(self, api_key: str):
        """
        Initialize Mistral AI client
        
        Args:
            api_key: Mistral AI API key
        """
        self.api_key = api_key
        self.client = None
        
        if MISTRAL_AVAILABLE and api_key:
            try:
                self.client = Mistral(api_key=api_key)
                logger.info("Mistral AI Engine initialized with API client")
            except Exception as e:
                logger.warning(f"Failed to initialize Mistral AI client: {str(e)}")
                self.client = None
        else:
            logger.warning("Mistral AI client not available or API key not provided")

    def generate_optimization_insights(
        self,
        cost_data: List[Dict[str, Any]],
        resource_data: List[Dict[str, Any]],
        unused_resources: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate optimization insights based on AWS data
        
        Args:
            cost_data: List of cost data
            resource_data: List of resource data
            unused_resources: Dictionary of unused resources
        
        Returns:
            List of optimization insights
        """
        insights = []

        # Analyze cost patterns
        insights.extend(self._analyze_cost_patterns(cost_data))

        # Analyze resource utilization
        insights.extend(self._analyze_resource_utilization(resource_data))

        # Analyze unused resources
        insights.extend(self._analyze_unused_resources(unused_resources))

        # Sort by potential savings
        insights.sort(
            key=lambda x: x.get("potential_savings", 0),
            reverse=True
        )

        logger.info(f"Generated {len(insights)} optimization insights")
        return insights

    def _analyze_cost_patterns(self, cost_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze cost patterns and identify optimization opportunities
        
        Args:
            cost_data: List of cost data
        
        Returns:
            List of cost-related insights
        """
        insights = []

        if not cost_data:
            return insights

        # Group costs by service
        service_costs = {}
        for item in cost_data:
            service = item.get("service", "Unknown")
            cost = float(item.get("cost", 0))
            if service not in service_costs:
                service_costs[service] = 0
            service_costs[service] += cost

        # Find top cost drivers
        sorted_services = sorted(
            service_costs.items(),
            key=lambda x: x[1],
            reverse=True
        )

        if sorted_services:
            top_service, top_cost = sorted_services[0]
            insights.append(
                {
                    "title": f"High spending on {top_service}",
                    "description": f"{top_service} is your highest cost driver. Consider reviewing usage patterns and implementing cost controls.",
                    "potential_savings": top_cost * 0.15,  # Estimate 15% savings
                    "priority": "High",
                    "category": "Cost Optimization",
                    "recommendation": f"Review {top_service} usage and consider reserved instances or savings plans.",
                }
            )

        # Check for multi-region costs
        regions = set(item.get("region") for item in cost_data)
        if len(regions) > 3:
            insights.append(
                {
                    "title": "Multi-region deployment detected",
                    "description": f"Your resources are spread across {len(regions)} regions. Consolidation could reduce costs.",
                    "potential_savings": sum(service_costs.values()) * 0.10,
                    "priority": "Medium",
                    "category": "Architecture Optimization",
                    "recommendation": "Evaluate if all regions are necessary and consolidate where possible.",
                }
            )

        return insights

    def _analyze_resource_utilization(
        self,
        resource_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Analyze resource utilization patterns
        
        Args:
            resource_data: List of resource data
        
        Returns:
            List of resource utilization insights
        """
        insights = []

        if not resource_data:
            return insights

        # Count instances by type
        instance_types = {}
        for resource in resource_data:
            itype = resource.get("instance_type", "Unknown")
            if itype not in instance_types:
                instance_types[itype] = 0
            instance_types[itype] += 1

        # Identify large instance types that might be oversized
        large_instances = {
            k: v for k, v in instance_types.items()
            if any(size in k for size in ["xlarge", "2xlarge", "3xlarge"])
        }

        if large_instances:
            total_large = sum(large_instances.values())
            insights.append(
                {
                    "title": f"Large instance types in use ({total_large} instances)",
                    "description": "You have large instance types running. Consider right-sizing to smaller instances if utilization is low.",
                    "potential_savings": total_large * 50,  # Estimate $50 per instance
                    "priority": "Medium",
                    "category": "Right-sizing",
                    "recommendation": "Enable CloudWatch monitoring and analyze CPU/memory utilization to identify right-sizing opportunities.",
                }
            )

        return insights

    def _analyze_unused_resources(
        self,
        unused_resources: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Analyze unused resources and generate cleanup recommendations
        
        Args:
            unused_resources: Dictionary of unused resources
        
        Returns:
            List of unused resource insights
        """
        insights = []

        # Check for stopped instances
        stopped_instances = unused_resources.get("stopped_instances", [])
        if stopped_instances:
            savings = len(stopped_instances) * 30  # Estimate $30 per instance
            insights.append(
                {
                    "title": f"Stopped EC2 instances ({len(stopped_instances)} found)",
                    "description": f"You have {len(stopped_instances)} stopped instances. Consider terminating if no longer needed.",
                    "potential_savings": savings,
                    "priority": "High",
                    "category": "Resource Cleanup",
                    "recommendation": "Review stopped instances and terminate those no longer needed. Consider using Auto Scaling for dynamic capacity.",
                }
            )

        # Check for unattached volumes
        unattached_volumes = unused_resources.get("unattached_volumes", [])
        if unattached_volumes:
            savings = len(unattached_volumes) * 5  # Estimate $5 per volume
            insights.append(
                {
                    "title": f"Unattached EBS volumes ({len(unattached_volumes)} found)",
                    "description": f"You have {len(unattached_volumes)} unattached volumes incurring costs.",
                    "potential_savings": savings,
                    "priority": "Medium",
                    "category": "Resource Cleanup",
                    "recommendation": "Delete unattached volumes or attach them to running instances.",
                }
            )

        # Check for unused Elastic IPs
        unused_eips = unused_resources.get("unused_elastic_ips", [])
        if unused_eips:
            savings = len(unused_eips) * 3.65  # AWS charges for unassociated EIPs
            insights.append(
                {
                    "title": f"Unused Elastic IPs ({len(unused_eips)} found)",
                    "description": f"You have {len(unused_eips)} unassociated Elastic IPs incurring charges.",
                    "potential_savings": savings,
                    "priority": "Low",
                    "category": "Resource Cleanup",
                    "recommendation": "Release unused Elastic IPs or associate them with running instances.",
                }
            )

        return insights

    def answer_query(
        self,
        user_query: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Generate AI-powered response to user query
        
        Args:
            user_query: User's natural language query
            context: Context data (costs, resources, insights)
        
        Returns:
            AI-generated response
        """
        try:
            # Check if we have actual data
            has_data = (
                (context.get("costs") and len(context.get("costs", [])) > 0) or
                (context.get("resources") and len(context.get("resources", [])) > 0) or
                (context.get("optimizations") and len(context.get("optimizations", [])) > 0)
            )
            
            if has_data:
                logger.info("Data available - using data-driven response")
                # Always use data-driven response when we have real data
                return self._get_data_driven_response(user_query, context)
            
            # Try Mistral AI only if no data available
            context_string = self._build_context_string(context)
            response = self._call_mistral_api(user_query, context_string)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            # Return data-driven response as last resort
            return self._get_data_driven_response(user_query, context)

    def _build_context_string(self, context: Dict[str, Any]) -> str:
        """
        Build context string from data
        
        Args:
            context: Context dictionary
        
        Returns:
            Formatted context string
        """
        context_parts = []

        # Add cost data
        if "costs" in context and isinstance(context['costs'], list) and len(context['costs']) > 0:
            costs_str = "\n".join(
                [f"  - {c.get('service', 'Unknown')}: ${c.get('cost', 0):.2f} in {c.get('region', 'Unknown')}" 
                 for c in context['costs'][:5]]
            )
            context_parts.append(f"Cost Data:\n{costs_str}")
        elif "costs" in context and isinstance(context['costs'], (int, float)):
            context_parts.append(f"Total costs: ${context['costs']:.2f}")

        # Add resource data
        if "resources" in context and isinstance(context['resources'], list) and len(context['resources']) > 0:
            resources_str = "\n".join(
                [f"  - {r.get('instance_id', 'Unknown')} ({r.get('instance_type', 'Unknown')}): {r.get('state', 'unknown')} in {r.get('region', 'Unknown')}" 
                 for r in context['resources'][:5]]
            )
            context_parts.append(f"Running Resources:\n{resources_str}")

        # Add optimization insights
        if "insights" in context and isinstance(context["insights"], list) and len(context["insights"]) > 0:
            insights_str = "\n".join(
                [f"- {i.get('title', 'Unknown')}: {i.get('description', '')} (Potential savings: ${i.get('potential_savings', 0):.2f})" 
                 for i in context["insights"][:3]]
            )
            context_parts.append(f"Key Insights:\n{insights_str}")

        # Add optimization recommendations
        if "optimizations" in context and isinstance(context["optimizations"], list) and len(context["optimizations"]) > 0:
            opt_str = "\n".join(
                [f"- {o.get('title', 'Unknown')}: ${o.get('savings', 0):.2f} potential savings" 
                 for o in context["optimizations"][:3]]
            )
            context_parts.append(f"Optimization Opportunities:\n{opt_str}")

        return "\n".join(context_parts) if context_parts else "No AWS data available yet. Please sync your AWS account first."

    def _call_mistral_api(self, query: str, context: str) -> str:
        """
        Call Mistral AI API
        
        Args:
            query: User query
            context: Context information
        
        Returns:
            AI-generated response
        """
        # If Mistral client is available, use it
        if self.client:
            try:
                # Build the system prompt for FinOps context - keep it concise
                system_prompt = """You are an AWS FinOps consultant. Keep responses SHORT and CONCISE (2-3 sentences max).
Focus on actionable AWS cost optimization tips. Be direct and helpful."""

                # Build the user message with context
                user_message = f"""AWS Context: {context}

Question: {query}

Keep your answer brief and actionable (2-3 sentences)."""

                # Call Mistral API with new format
                response = self.client.chat.complete(
                    model="mistral-small-latest",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.5,
                    max_tokens=256
                )
                
                # Extract the response text
                if response and response.choices and len(response.choices) > 0:
                    return response.choices[0].message.content
                else:
                    logger.warning("Empty response from Mistral API")
                    return self._get_fallback_response(query)
                    
            except Exception as e:
                logger.error(f"Error calling Mistral API: {str(e)}")
                return self._get_fallback_response(query)
        else:
            # Fallback to mock responses if client not available
            return self._get_fallback_response(query)

    def _get_data_driven_response(self, query: str, context: Dict[str, Any]) -> str:
        """
        Generate response using actual AWS data when Mistral API is unavailable
        
        Args:
            query: User query
            context: Context data with actual AWS information
        
        Returns:
            Data-driven response
        """
        query_lower = query.lower()
        
        # Check for resource queries
        if any(word in query_lower for word in ["resource", "instance", "running", "ec2"]):
            resources = context.get("resources", [])
            if resources:
                resource_list = ", ".join([f"{r.get('instance_id')} ({r.get('instance_type')})" for r in resources[:3]])
                return f"You have {len(resources)} resources running. Key instances: {resource_list}. Consider using Reserved Instances to optimize costs."
            else:
                return "No resources found in your AWS account. Sync your data first using POST /api/sync."
        
        # Check for cost queries
        if any(word in query_lower for word in ["cost", "spend", "bill", "expensive", "price"]):
            costs = context.get("costs", [])
            if costs:
                total_cost = sum(float(c.get('cost', 0)) for c in costs)
                top_service = costs[0] if costs else None
                if top_service:
                    return f"Your total AWS spending is ${total_cost:.2f}. Top service: {top_service.get('service')} at ${top_service.get('cost'):.2f}. Consider implementing cost optimization strategies."
                return f"Your total AWS spending is ${total_cost:.2f}. Review your services for optimization opportunities."
            else:
                return "No cost data available. Sync your AWS data first using POST /api/sync."
        
        # Check for optimization queries
        if any(word in query_lower for word in ["optim", "save", "reduce", "improve", "recommendation"]):
            optimizations = context.get("optimizations", [])
            insights = context.get("insights", [])
            
            if optimizations or insights:
                items = optimizations + insights
                if items:
                    top_item = items[0]
                    savings = top_item.get('savings') or top_item.get('potential_savings', 0)
                    return f"Top optimization: {top_item.get('title', 'Cost optimization')}. Potential savings: ${savings:.2f}. {top_item.get('description', 'Review your AWS resources for cost reduction opportunities.')}"
            return "Review your AWS resources for optimization opportunities. Focus on right-sizing instances and removing unused resources."
        
        # Default data-driven response
        resources = context.get("resources", [])
        costs = context.get("costs", [])
        
        if resources or costs:
            response_parts = []
            if resources:
                response_parts.append(f"You have {len(resources)} resources running")
            if costs:
                total_cost = sum(float(c.get('cost', 0)) for c in costs)
                response_parts.append(f"with total costs of ${total_cost:.2f}")
            
            if response_parts:
                return ". ".join(response_parts) + ". Review your AWS account for optimization opportunities."
        
        return "No AWS data available. Please sync your account first using POST /api/sync."

    def _get_fallback_response(self, query: str) -> str:
        """
        Get fallback response when Mistral API is not available
        
        Args:
            query: User query
        
        Returns:
            Fallback response
        """
        fallback_responses = {
            "cost": "Based on your AWS usage, I recommend implementing Reserved Instances for your top services, which could save 30-40% on compute costs.",
            "optimization": "To optimize your AWS spending, focus on: 1) Right-sizing instances, 2) Implementing auto-scaling, 3) Using spot instances for non-critical workloads.",
            "savings": "By implementing the recommended optimizations, you could potentially save 25-35% on your monthly AWS bill.",
            "ec2": "EC2 is often the largest cost driver. Consider: 1) Using Reserved Instances for predictable workloads, 2) Spot Instances for flexible workloads, 3) Right-sizing your instances.",
            "unused": "Unused resources are costing you money. Regularly audit and terminate: 1) Stopped instances, 2) Unattached volumes, 3) Unused Elastic IPs.",
            "default": "I can help you optimize your AWS costs. Ask me about specific services, cost patterns, or optimization strategies."
        }

        query_lower = query.lower()
        for key, response in fallback_responses.items():
            if key in query_lower:
                return response

        return fallback_responses["default"]

    def generate_report(self, insights: List[Dict[str, Any]]) -> str:
        """
        Generate a comprehensive optimization report
        
        Args:
            insights: List of optimization insights
        
        Returns:
            Formatted report string
        """
        report = "# AWS FinOps Optimization Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Group insights by priority
        high_priority = [i for i in insights if i.get("priority") == "High"]
        medium_priority = [i for i in insights if i.get("priority") == "Medium"]
        low_priority = [i for i in insights if i.get("priority") == "Low"]

        total_savings = sum(i.get("potential_savings", 0) for i in insights)
        report += f"## Summary\n"
        report += f"Total Potential Savings: ${total_savings:.2f}\n"
        report += f"Total Insights: {len(insights)}\n\n"

        # High priority insights
        if high_priority:
            report += "## High Priority Actions\n"
            for insight in high_priority:
                report += f"### {insight.get('title')}\n"
                report += f"- Description: {insight.get('description')}\n"
                report += f"- Potential Savings: ${insight.get('potential_savings', 0):.2f}\n"
                report += f"- Recommendation: {insight.get('recommendation')}\n\n"

        # Medium priority insights
        if medium_priority:
            report += "## Medium Priority Actions\n"
            for insight in medium_priority:
                report += f"### {insight.get('title')}\n"
                report += f"- Description: {insight.get('description')}\n"
                report += f"- Potential Savings: ${insight.get('potential_savings', 0):.2f}\n\n"

        return report
