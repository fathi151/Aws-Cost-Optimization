"""
Unit tests for FinOps Chatbot
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finops_chatbot import FinOpsChatbot
from data_processor import DataProcessor
from advanced_analytics import AdvancedAnalytics
import pandas as pd


class TestFinOpsChatbot:
    """Test FinOps Chatbot functionality"""

    @pytest.fixture
    def chatbot(self):
        """Create chatbot instance"""
        return FinOpsChatbot()

    def test_chatbot_initialization(self, chatbot):
        """Test chatbot initialization"""
        assert chatbot is not None
        assert chatbot.vector_store is not None
        assert chatbot.ai_engine is not None

    def test_get_summary(self, chatbot):
        """Test getting summary"""
        summary = chatbot.get_summary()
        assert summary is not None
        assert "status" in summary
        assert "collection_stats" in summary

    def test_clear_data(self, chatbot):
        """Test clearing data"""
        result = chatbot.clear_data()
        assert result["status"] == "success"


class TestDataProcessor:
    """Test data processing functionality"""

    @pytest.fixture
    def sample_data(self):
        """Create sample cost data"""
        return [
            {
                "service": "Amazon EC2",
                "region": "us-east-1",
                "cost": 100.0,
                "usage": 50.0,
                "date": datetime.now().isoformat(),
            },
            {
                "service": "Amazon S3",
                "region": "us-east-1",
                "cost": 50.0,
                "usage": 100.0,
                "date": datetime.now().isoformat(),
            },
        ]

    def test_process_cost_data(self, sample_data):
        """Test cost data processing"""
        df = DataProcessor.process_cost_data(sample_data)
        assert len(df) == 2
        assert "cost" in df.columns
        assert "service" in df.columns

    def test_calculate_trends(self, sample_data):
        """Test trend calculation"""
        df = DataProcessor.process_cost_data(sample_data)
        trends = DataProcessor.calculate_trends(df)
        assert "trend" in trends
        assert "percentage_change" in trends

    def test_analyze_service_distribution(self, sample_data):
        """Test service distribution analysis"""
        df = DataProcessor.process_cost_data(sample_data)
        distribution = DataProcessor.analyze_service_distribution(df)
        assert len(distribution) > 0
        assert "service" in distribution[0]
        assert "total_cost" in distribution[0]

    def test_generate_summary_stats(self, sample_data):
        """Test summary statistics generation"""
        df = DataProcessor.process_cost_data(sample_data)
        stats = DataProcessor.generate_summary_stats(df)
        assert "total_cost" in stats
        assert "average_cost" in stats
        assert "record_count" in stats


class TestAdvancedAnalytics:
    """Test advanced analytics functionality"""

    @pytest.fixture
    def sample_cost_df(self):
        """Create sample cost dataframe"""
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        data = {
            'date': dates,
            'service': ['EC2'] * 30,
            'region': ['us-east-1'] * 30,
            'cost': [100 + i * 2 for i in range(30)],
            'usage': [50 + i for i in range(30)],
        }
        return pd.DataFrame(data)

    def test_identify_cost_drivers(self, sample_cost_df):
        """Test cost driver identification"""
        drivers = AdvancedAnalytics.identify_cost_drivers(sample_cost_df)
        assert len(drivers) > 0
        assert "service" in drivers[0]
        assert "total_cost" in drivers[0]

    def test_calculate_cost_elasticity(self, sample_cost_df):
        """Test elasticity calculation"""
        elasticity = AdvancedAnalytics.calculate_cost_elasticity(sample_cost_df)
        assert "elasticity" in elasticity
        assert "correlation" in elasticity

    def test_calculate_roi(self):
        """Test ROI calculation"""
        roi = AdvancedAnalytics.calculate_roi_for_optimization(
            current_cost=1000,
            optimization_savings=200,
            implementation_cost=500,
            months=12
        )
        assert "roi_percentage" in roi
        assert "payback_period_months" in roi
        assert roi["roi_percentage"] > 0

    def test_compare_scenarios(self):
        """Test scenario comparison"""
        scenarios = [
            {"name": "Current", "cost": 1000},
            {"name": "Optimized", "cost": 700},
            {"name": "Aggressive", "cost": 500},
        ]
        comparison = AdvancedAnalytics.compare_cost_scenarios(scenarios)
        assert "best_scenario" in comparison
        assert "worst_scenario" in comparison
        assert comparison["best_scenario"] == "Aggressive"


class TestIntegration:
    """Integration tests"""

    def test_end_to_end_workflow(self):
        """Test end-to-end workflow"""
        # Create sample data
        sample_data = [
            {
                "service": "Amazon EC2",
                "region": "us-east-1",
                "cost": 100.0,
                "usage": 50.0,
                "date": datetime.now().isoformat(),
            },
        ]

        # Process data
        df = DataProcessor.process_cost_data(sample_data)
        assert len(df) > 0

        # Analyze data
        trends = DataProcessor.calculate_trends(df)
        assert "trend" in trends

        # Generate insights
        drivers = AdvancedAnalytics.identify_cost_drivers(df)
        assert len(drivers) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
