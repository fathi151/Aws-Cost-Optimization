"""
Data Processor Module
Handles batch processing of AWS data and optimization analysis
"""

import logging
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and analyze AWS cost and usage data"""

    @staticmethod
    def process_cost_data(raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Process raw cost data into structured format
        
        Args:
            raw_data: Raw cost data from AWS
        
        Returns:
            Processed DataFrame
        """
        try:
            df = pd.DataFrame(raw_data)

            # Convert cost to float
            df["cost"] = pd.to_numeric(df.get("cost", 0), errors="coerce").fillna(0)

            # Convert usage to float
            df["usage"] = pd.to_numeric(df.get("usage", 0), errors="coerce").fillna(0)

            # Convert date to datetime
            df["date"] = pd.to_datetime(df.get("date", datetime.now()))

            logger.info(f"Processed {len(df)} cost records")
            return df

        except Exception as e:
            logger.error(f"Error processing cost data: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def calculate_trends(cost_data: pd.DataFrame, window: int = 7) -> Dict[str, Any]:
        """
        Calculate cost trends
        
        Args:
            cost_data: DataFrame with cost data
            window: Rolling window size
        
        Returns:
            Dictionary with trend analysis
        """
        try:
            if cost_data.empty:
                return {}

            # Group by date and sum costs
            daily_costs = cost_data.groupby("date")["cost"].sum()

            # Calculate rolling average
            rolling_avg = daily_costs.rolling(window=window).mean()

            # Calculate trend
            trend = "increasing" if daily_costs.iloc[-1] > daily_costs.iloc[0] else "decreasing"

            # Calculate percentage change
            pct_change = ((daily_costs.iloc[-1] - daily_costs.iloc[0]) / daily_costs.iloc[0] * 100
                         if daily_costs.iloc[0] != 0 else 0)

            return {
                "trend": trend,
                "percentage_change": pct_change,
                "current_daily_cost": float(daily_costs.iloc[-1]),
                "average_daily_cost": float(rolling_avg.iloc[-1]),
                "min_daily_cost": float(daily_costs.min()),
                "max_daily_cost": float(daily_costs.max()),
            }

        except Exception as e:
            logger.error(f"Error calculating trends: {str(e)}")
            return {}

    @staticmethod
    def identify_anomalies(cost_data: pd.DataFrame, threshold: float = 2.0) -> List[Dict[str, Any]]:
        """
        Identify cost anomalies using statistical analysis
        
        Args:
            cost_data: DataFrame with cost data
            threshold: Standard deviation threshold
        
        Returns:
            List of anomalies
        """
        try:
            if cost_data.empty:
                return []

            # Group by date and sum costs
            daily_costs = cost_data.groupby("date")["cost"].sum()

            # Calculate mean and std
            mean = daily_costs.mean()
            std = daily_costs.std()

            # Identify anomalies
            anomalies = []
            for date, cost in daily_costs.items():
                z_score = abs((cost - mean) / std) if std != 0 else 0

                if z_score > threshold:
                    anomalies.append({
                        "date": date.isoformat(),
                        "cost": float(cost),
                        "z_score": float(z_score),
                        "deviation": float((cost - mean) / mean * 100) if mean != 0 else 0,
                    })

            logger.info(f"Identified {len(anomalies)} cost anomalies")
            return anomalies

        except Exception as e:
            logger.error(f"Error identifying anomalies: {str(e)}")
            return []

    @staticmethod
    def forecast_costs(cost_data: pd.DataFrame, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """
        Forecast future costs using simple trend analysis
        
        Args:
            cost_data: DataFrame with cost data
            days_ahead: Number of days to forecast
        
        Returns:
            List of forecasted costs
        """
        try:
            if cost_data.empty:
                return []

            # Group by date and sum costs
            daily_costs = cost_data.groupby("date")["cost"].sum()

            # Calculate average daily cost
            avg_cost = daily_costs.mean()

            # Calculate trend
            x = range(len(daily_costs))
            y = daily_costs.values

            # Simple linear regression
            n = len(x)
            slope = (n * sum(x[i] * y[i] for i in range(n)) - sum(x) * sum(y)) / (
                n * sum(x[i] ** 2 for i in range(n)) - sum(x) ** 2
            )

            # Generate forecast
            forecast = []
            last_date = daily_costs.index[-1]

            for i in range(1, days_ahead + 1):
                forecast_date = last_date + timedelta(days=i)
                forecast_cost = avg_cost + (slope * i)

                forecast.append({
                    "date": forecast_date.isoformat(),
                    "forecasted_cost": max(0, float(forecast_cost)),
                })

            logger.info(f"Generated {len(forecast)} cost forecasts")
            return forecast

        except Exception as e:
            logger.error(f"Error forecasting costs: {str(e)}")
            return []

    @staticmethod
    def analyze_service_distribution(cost_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Analyze cost distribution by service
        
        Args:
            cost_data: DataFrame with cost data
        
        Returns:
            List of service cost analysis
        """
        try:
            if cost_data.empty:
                return []

            # Group by service
            service_costs = cost_data.groupby("service").agg({
                "cost": ["sum", "mean", "count"],
                "usage": "sum"
            }).reset_index()

            service_costs.columns = ["service", "total_cost", "avg_cost", "count", "total_usage"]

            # Calculate percentage
            total = service_costs["total_cost"].sum()
            service_costs["percentage"] = (service_costs["total_cost"] / total * 100
                                          if total > 0 else 0)

            # Sort by cost
            service_costs = service_costs.sort_values("total_cost", ascending=False)

            result = []
            for _, row in service_costs.iterrows():
                result.append({
                    "service": row["service"],
                    "total_cost": float(row["total_cost"]),
                    "average_cost": float(row["avg_cost"]),
                    "percentage": float(row["percentage"]),
                    "usage_count": int(row["count"]),
                })

            logger.info(f"Analyzed {len(result)} services")
            return result

        except Exception as e:
            logger.error(f"Error analyzing service distribution: {str(e)}")
            return []

    @staticmethod
    def generate_summary_stats(cost_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics
        
        Args:
            cost_data: DataFrame with cost data
        
        Returns:
            Dictionary with summary statistics
        """
        try:
            if cost_data.empty:
                return {}

            return {
                "total_cost": float(cost_data["cost"].sum()),
                "average_cost": float(cost_data["cost"].mean()),
                "min_cost": float(cost_data["cost"].min()),
                "max_cost": float(cost_data["cost"].max()),
                "std_dev": float(cost_data["cost"].std()),
                "total_usage": float(cost_data["usage"].sum()),
                "record_count": len(cost_data),
                "date_range": {
                    "start": cost_data["date"].min().isoformat(),
                    "end": cost_data["date"].max().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"Error generating summary stats: {str(e)}")
            return {}

    @staticmethod
    def export_to_json(data: Any, filepath: str) -> bool:
        """
        Export data to JSON file
        
        Args:
            data: Data to export
            filepath: Output file path
        
        Returns:
            Success status
        """
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, default=str)

            logger.info(f"Data exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return False

    @staticmethod
    def export_to_csv(df: pd.DataFrame, filepath: str) -> bool:
        """
        Export DataFrame to CSV file
        
        Args:
            df: DataFrame to export
            filepath: Output file path
        
        Returns:
            Success status
        """
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Data exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return False
