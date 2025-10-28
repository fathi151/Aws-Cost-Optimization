"""
Advanced Analytics Module
Provides deep cost analysis, ML-based insights, and predictive analytics
"""

import logging
import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import pandas as pd
from scipy import stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedAnalytics:
    """Advanced analytics for AWS cost optimization"""

    @staticmethod
    def detect_cost_anomalies_advanced(
        cost_data: pd.DataFrame,
        method: str = "isolation_forest",
        contamination: float = 0.1
    ) -> List[Dict[str, Any]]:
        """
        Detect cost anomalies using advanced statistical methods
        
        Args:
            cost_data: DataFrame with cost data
            method: Detection method (isolation_forest, zscore, iqr)
            contamination: Expected proportion of anomalies
        
        Returns:
            List of detected anomalies with details
        """
        try:
            if cost_data.empty:
                return []

            daily_costs = cost_data.groupby("date")["cost"].sum()
            costs = daily_costs.values.reshape(-1, 1)

            anomalies = []

            if method == "zscore":
                z_scores = np.abs(stats.zscore(costs))
                threshold = 3
                anomaly_indices = np.where(z_scores > threshold)[0]

            elif method == "iqr":
                Q1 = np.percentile(costs, 25)
                Q3 = np.percentile(costs, 75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                anomaly_indices = np.where((costs < lower_bound) | (costs > upper_bound))[0]

            else:  # isolation_forest
                try:
                    from sklearn.ensemble import IsolationForest
                    iso_forest = IsolationForest(contamination=contamination, random_state=42)
                    predictions = iso_forest.fit_predict(costs)
                    anomaly_indices = np.where(predictions == -1)[0]
                except ImportError:
                    logger.warning("scikit-learn not installed, using IQR method")
                    Q1 = np.percentile(costs, 25)
                    Q3 = np.percentile(costs, 75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    anomaly_indices = np.where((costs < lower_bound) | (costs > upper_bound))[0]

            # Build anomaly details
            dates = daily_costs.index
            for idx in anomaly_indices:
                anomalies.append({
                    "date": dates[idx].isoformat(),
                    "cost": float(costs[idx][0]),
                    "method": method,
                    "severity": "high" if costs[idx][0] > np.mean(costs) * 1.5 else "medium",
                })

            logger.info(f"Detected {len(anomalies)} anomalies using {method}")
            return anomalies

        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return []

    @staticmethod
    def calculate_cost_elasticity(
        cost_data: pd.DataFrame,
        service: str = None
    ) -> Dict[str, Any]:
        """
        Calculate cost elasticity and sensitivity
        
        Args:
            cost_data: DataFrame with cost data
            service: Specific service to analyze (optional)
        
        Returns:
            Dictionary with elasticity metrics
        """
        try:
            if cost_data.empty:
                return {}

            if service:
                data = cost_data[cost_data["service"] == service]
            else:
                data = cost_data

            if data.empty:
                return {}

            # Group by date
            daily_costs = data.groupby("date")["cost"].sum()
            daily_usage = data.groupby("date")["usage"].sum()

            # Calculate percentage changes
            cost_pct_change = daily_costs.pct_change().dropna()
            usage_pct_change = daily_usage.pct_change().dropna()

            # Calculate elasticity
            if len(cost_pct_change) > 0 and len(usage_pct_change) > 0:
                elasticity = cost_pct_change.mean() / usage_pct_change.mean() if usage_pct_change.mean() != 0 else 0
            else:
                elasticity = 0

            return {
                "elasticity": float(elasticity),
                "cost_volatility": float(cost_pct_change.std()),
                "usage_volatility": float(usage_pct_change.std()),
                "correlation": float(daily_costs.corr(daily_usage)),
                "service": service or "all",
            }

        except Exception as e:
            logger.error(f"Error calculating elasticity: {str(e)}")
            return {}

    @staticmethod
    def forecast_with_confidence_intervals(
        cost_data: pd.DataFrame,
        days_ahead: int = 30,
        confidence: float = 0.95
    ) -> List[Dict[str, Any]]:
        """
        Generate cost forecasts with confidence intervals
        
        Args:
            cost_data: DataFrame with cost data
            days_ahead: Number of days to forecast
            confidence: Confidence level (0.95 = 95%)
        
        Returns:
            List of forecasts with confidence intervals
        """
        try:
            if cost_data.empty:
                return []

            daily_costs = cost_data.groupby("date")["cost"].sum()

            # Calculate statistics
            mean = daily_costs.mean()
            std = daily_costs.std()
            n = len(daily_costs)

            # Calculate trend
            x = np.arange(n)
            y = daily_costs.values
            coeffs = np.polyfit(x, y, 1)
            poly = np.poly1d(coeffs)

            # Calculate residuals
            residuals = y - poly(x)
            residual_std = np.std(residuals)

            # Z-score for confidence interval
            z_score = stats.norm.ppf((1 + confidence) / 2)

            # Generate forecast
            forecast = []
            last_date = daily_costs.index[-1]

            for i in range(1, days_ahead + 1):
                forecast_date = last_date + timedelta(days=i)
                forecast_value = poly(n + i - 1)

                # Calculate confidence interval
                margin_of_error = z_score * residual_std * np.sqrt(1 + 1/n)
                lower_bound = max(0, forecast_value - margin_of_error)
                upper_bound = forecast_value + margin_of_error

                forecast.append({
                    "date": forecast_date.isoformat(),
                    "forecasted_cost": float(forecast_value),
                    "lower_bound": float(lower_bound),
                    "upper_bound": float(upper_bound),
                    "confidence": confidence,
                })

            logger.info(f"Generated {len(forecast)} forecasts with confidence intervals")
            return forecast

        except Exception as e:
            logger.error(f"Error generating forecasts: {str(e)}")
            return []

    @staticmethod
    def identify_cost_drivers(
        cost_data: pd.DataFrame,
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Identify top cost drivers with contribution analysis
        
        Args:
            cost_data: DataFrame with cost data
            top_n: Number of top drivers to return
        
        Returns:
            List of cost drivers with metrics
        """
        try:
            if cost_data.empty:
                return []

            # Group by service and region
            drivers = cost_data.groupby(["service", "region"]).agg({
                "cost": ["sum", "mean", "std"],
                "usage": "sum"
            }).reset_index()

            drivers.columns = ["service", "region", "total_cost", "avg_cost", "std_cost", "total_usage"]

            # Calculate metrics
            total_cost = drivers["total_cost"].sum()
            drivers["percentage"] = (drivers["total_cost"] / total_cost * 100) if total_cost > 0 else 0
            drivers["cumulative_percentage"] = drivers["percentage"].cumsum()
            drivers["cost_per_unit"] = (drivers["total_cost"] / drivers["total_usage"]
                                       if drivers["total_usage"] > 0 else 0)

            # Sort by cost
            drivers = drivers.sort_values("total_cost", ascending=False).head(top_n)

            result = []
            for _, row in drivers.iterrows():
                result.append({
                    "service": row["service"],
                    "region": row["region"],
                    "total_cost": float(row["total_cost"]),
                    "percentage": float(row["percentage"]),
                    "cumulative_percentage": float(row["cumulative_percentage"]),
                    "cost_per_unit": float(row["cost_per_unit"]),
                    "volatility": float(row["std_cost"]),
                })

            logger.info(f"Identified {len(result)} top cost drivers")
            return result

        except Exception as e:
            logger.error(f"Error identifying cost drivers: {str(e)}")
            return []

    @staticmethod
    def calculate_roi_for_optimization(
        current_cost: float,
        optimization_savings: float,
        implementation_cost: float,
        months: int = 12
    ) -> Dict[str, Any]:
        """
        Calculate ROI for optimization initiatives
        
        Args:
            current_cost: Current monthly cost
            optimization_savings: Expected monthly savings
            implementation_cost: One-time implementation cost
            months: Analysis period in months
        
        Returns:
            ROI metrics
        """
        try:
            total_savings = optimization_savings * months
            net_benefit = total_savings - implementation_cost
            roi = (net_benefit / implementation_cost * 100) if implementation_cost > 0 else 0
            payback_period = (implementation_cost / optimization_savings
                            if optimization_savings > 0 else float('inf'))

            return {
                "roi_percentage": float(roi),
                "total_savings": float(total_savings),
                "net_benefit": float(net_benefit),
                "payback_period_months": float(payback_period) if payback_period != float('inf') else None,
                "analysis_period_months": months,
                "monthly_savings": float(optimization_savings),
            }

        except Exception as e:
            logger.error(f"Error calculating ROI: {str(e)}")
            return {}

    @staticmethod
    def compare_cost_scenarios(
        scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare multiple cost scenarios
        
        Args:
            scenarios: List of scenario dictionaries with costs
        
        Returns:
            Comparison analysis
        """
        try:
            if not scenarios:
                return {}

            comparison = {
                "scenarios": [],
                "best_scenario": None,
                "worst_scenario": None,
                "average_cost": 0,
                "cost_range": 0,
            }

            costs = []
            for scenario in scenarios:
                cost = scenario.get("cost", 0)
                costs.append(cost)
                comparison["scenarios"].append({
                    "name": scenario.get("name", "Unknown"),
                    "cost": float(cost),
                    "description": scenario.get("description", ""),
                })

            if costs:
                min_cost = min(costs)
                max_cost = max(costs)
                avg_cost = sum(costs) / len(costs)

                comparison["best_scenario"] = scenarios[costs.index(min_cost)].get("name")
                comparison["worst_scenario"] = scenarios[costs.index(max_cost)].get("name")
                comparison["average_cost"] = float(avg_cost)
                comparison["cost_range"] = float(max_cost - min_cost)
                comparison["savings_potential"] = float(max_cost - min_cost)

            logger.info(f"Compared {len(scenarios)} scenarios")
            return comparison

        except Exception as e:
            logger.error(f"Error comparing scenarios: {str(e)}")
            return {}

    @staticmethod
    def calculate_unit_economics(
        cost_data: pd.DataFrame,
        business_metric: str = "requests"
    ) -> Dict[str, Any]:
        """
        Calculate unit economics (cost per business metric)
        
        Args:
            cost_data: DataFrame with cost data
            business_metric: Business metric name
        
        Returns:
            Unit economics analysis
        """
        try:
            if cost_data.empty:
                return {}

            total_cost = cost_data["cost"].sum()
            total_usage = cost_data["usage"].sum()

            cost_per_unit = (total_cost / total_usage) if total_usage > 0 else 0

            # Calculate by service
            service_economics = []
            for service in cost_data["service"].unique():
                service_data = cost_data[cost_data["service"] == service]
                service_cost = service_data["cost"].sum()
                service_usage = service_data["usage"].sum()
                service_cpu = (service_cost / service_usage) if service_usage > 0 else 0

                service_economics.append({
                    "service": service,
                    "cost_per_unit": float(service_cpu),
                    "total_cost": float(service_cost),
                    "total_usage": float(service_usage),
                })

            return {
                "overall_cost_per_unit": float(cost_per_unit),
                "business_metric": business_metric,
                "total_cost": float(total_cost),
                "total_usage": float(total_usage),
                "by_service": service_economics,
            }

        except Exception as e:
            logger.error(f"Error calculating unit economics: {str(e)}")
            return {}
