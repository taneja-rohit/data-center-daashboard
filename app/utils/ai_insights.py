import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataCenterAI:
    """
    Class to handle AI functionality for the data center dashboard
    Simulates GenAI capabilities for the demo application
    """
    
    def __init__(self, df=None):
        """Initialize with optional dataframe"""
        self.df = df
    
    def set_data(self, df):
        """Set or update the dataframe"""
        self.df = df
    
    def predict_maintenance_needs(self, time_horizon_days=30):
        """
        Predict equipment that will need maintenance in the next N days
        Returns a dataframe with predicted maintenance needs
        """
        if self.df is None:
            return pd.DataFrame()
        
        # Get unique racks
        racks = self.df['rack_id'].unique()
        
        # Create sample maintenance predictions
        now = datetime.now()
        predictions = []
        
        # For demonstration, create predictions for about 5% of racks
        sample_racks = np.random.choice(racks, size=max(1, int(len(racks) * 0.05)), replace=False)
        
        for rack in sample_racks:
            # Get rack data
            rack_data = self.df[self.df['rack_id'] == rack]
            
            # Calculate metrics for this rack
            avg_temp = rack_data['temperature'].mean()
            temp_std = rack_data['temperature'].std()
            power_avg = rack_data['power_usage'].mean()
            power_std = rack_data['power_usage'].std()
            
            # Determine maintenance type based on metrics
            if avg_temp > 25:
                maintenance_type = "Cooling System"
                confidence = min(0.95, 0.7 + (avg_temp - 25) * 0.05)
                urgency = "High" if avg_temp > 28 else "Medium"
            elif power_avg > 7:
                maintenance_type = "Power Distribution Unit"
                confidence = min(0.95, 0.65 + (power_avg - 7) * 0.07)
                urgency = "High" if power_avg > 8.5 else "Medium"
            else:
                maintenance_type = "Routine Inspection"
                confidence = 0.85
                urgency = "Low"
            
            # Random date within the horizon
            days_ahead = np.random.randint(1, time_horizon_days + 1)
            predicted_date = now + timedelta(days=days_ahead)
            
            predictions.append({
                'rack_id': rack,
                'location': rack_data['location'].iloc[0],
                'maintenance_type': maintenance_type,
                'predicted_date': predicted_date,
                'confidence': confidence,
                'urgency': urgency,
                'estimated_downtime_minutes': np.random.randint(15, 120)
            })
        
        return pd.DataFrame(predictions)
    
    def identify_anomalies(self):
        """
        Identify anomalies in the current data
        Returns a dataframe with detected anomalies
        """
        if self.df is None:
            return pd.DataFrame()
        
        # Group by rack
        grouped = self.df.groupby('rack_id')
        
        anomalies = []
        
        for rack, rack_data in grouped:
            # For temperature: flag if > 3 std dev from mean or > 30°C
            temp_mean = rack_data['temperature'].mean()
            temp_std = rack_data['temperature'].std()
            temp_threshold = max(temp_mean + 3 * temp_std, 30)
            
            temp_anomalies = rack_data[rack_data['temperature'] > temp_threshold]
            
            if not temp_anomalies.empty:
                for _, row in temp_anomalies.iterrows():
                    anomalies.append({
                        'rack_id': rack,
                        'location': row['location'],
                        'timestamp': row['timestamp'],
                        'metric': 'temperature',
                        'value': row['temperature'],
                        'threshold': temp_threshold,
                        'severity': 'High' if row['temperature'] > 32 else 'Medium'
                    })
            
            # For power usage: flag if > 2.5 std dev from mean
            power_mean = rack_data['power_usage'].mean()
            power_std = rack_data['power_usage'].std()
            power_threshold = power_mean + 2.5 * power_std
            
            power_anomalies = rack_data[rack_data['power_usage'] > power_threshold]
            
            if not power_anomalies.empty:
                for _, row in power_anomalies.iterrows():
                    anomalies.append({
                        'rack_id': rack,
                        'location': row['location'],
                        'timestamp': row['timestamp'],
                        'metric': 'power_usage',
                        'value': row['power_usage'],
                        'threshold': power_threshold,
                        'severity': 'High' if row['power_usage'] > power_mean + 3.5 * power_std else 'Medium'
                    })
        
        return pd.DataFrame(anomalies)
    
    def optimize_cooling(self):
        """
        Generate cooling optimization recommendations
        Returns a list of recommendations for cooling optimization
        """
        if self.df is None:
            return []
        
        # Get average temperature by location
        location_temps = self.df.groupby('location')['temperature'].mean()
        
        recommendations = []
        
        # Identify hot zones (locations with avg temp > 24°C)
        hot_zones = location_temps[location_temps > 24].sort_values(ascending=False)
        
        if not hot_zones.empty:
            for location, temp in hot_zones.items():
                # Calculate potential savings
                potential_savings = (temp - 22) * 2.5  # Approx. 2.5% energy savings per degree
                
                recommendations.append({
                    'location': location,
                    'current_avg_temp': temp,
                    'recommended_temp': 22,
                    'potential_energy_savings_pct': min(potential_savings, 20),  # Cap at 20%
                    'implementation_difficulty': 'Medium',
                    'recommendation': f"Optimize cooling in {location} to reduce average temperature from {temp:.1f}°C to 22°C"
                })
        
        # Add general recommendations if we don't have many specific ones
        if len(recommendations) < 3:
            general_recs = [
                {
                    'location': 'All Zones',
                    'current_avg_temp': location_temps.mean(),
                    'recommended_temp': 22,
                    'potential_energy_savings_pct': 8.5,
                    'implementation_difficulty': 'Medium',
                    'recommendation': "Implement AI-controlled dynamic cooling that adjusts based on workload patterns"
                },
                {
                    'location': 'All Zones',
                    'current_avg_temp': location_temps.mean(),
                    'recommended_temp': 23,
                    'potential_energy_savings_pct': 12.3,
                    'implementation_difficulty': 'High',
                    'recommendation': "Deploy hot/cold aisle containment to improve cooling efficiency across all zones"
                }
            ]
            
            recommendations.extend(general_recs)
        
        return recommendations
    
    def predict_resource_needs(self, days_ahead=90):
        """
        Predict future resource needs based on current trends
        Returns a dictionary with predictions for different resources
        """
        if self.df is None:
            return {}
        
        # Get the latest data point's timestamp
        latest_date = self.df['timestamp'].max()
        
        # Calculate average utilization growth over time
        # Group by day to see trends
        daily_data = self.df.groupby(self.df['timestamp'].dt.date).agg({
            'cpu_utilization': 'mean',
            'power_usage': 'mean',
            'network_traffic': 'mean'
        }).reset_index()
        
        # If we have enough data points, calculate trend
        if len(daily_data) > 10:
            # Simple linear trend for CPU (% increase per day)
            cpu_trend = 0.05 + np.random.normal(0, 0.02)  # Simulated ~0.05% increase per day
            
            # Power usage trend (kW increase per day)
            power_trend = 0.003 + np.random.normal(0, 0.001)  # Simulated ~0.003 kW increase per day
            
            # Network traffic trend (Gbps increase per day)
            network_trend = 0.02 + np.random.normal(0, 0.005)  # Simulated ~0.02 Gbps increase per day
        else:
            # Default trends if not enough data
            cpu_trend = 0.05
            power_trend = 0.003
            network_trend = 0.02
        
        # Current values (from latest data)
        current_cpu = daily_data['cpu_utilization'].iloc[-1]
        current_power = daily_data['power_usage'].iloc[-1]
        current_network = daily_data['network_traffic'].iloc[-1]
        
        # Calculate predicted values
        predicted_cpu = current_cpu * (1 + cpu_trend * days_ahead)
        predicted_power = current_power * (1 + power_trend * days_ahead)
        predicted_network = current_network * (1 + network_trend * days_ahead)
        
        # Calculate time until capacity reached (assuming capacity limits)
        cpu_capacity = 85  # 85% utilization
        power_capacity = 8  # 8 kW per rack average
        network_capacity = 15  # 15 Gbps
        
        if cpu_trend > 0:
            days_to_cpu_capacity = max(0, (cpu_capacity - current_cpu) / (cpu_trend * current_cpu))
        else:
            days_to_cpu_capacity = float('inf')
        
        if power_trend > 0:
            days_to_power_capacity = max(0, (power_capacity - current_power) / (power_trend * current_power))
        else:
            days_to_power_capacity = float('inf')
        
        if network_trend > 0:
            days_to_network_capacity = max(0, (network_capacity - current_network) / (network_trend * current_network))
        else:
            days_to_network_capacity = float('inf')
        
        # Return predictions
        return {
            'current_date': latest_date.strftime('%Y-%m-%d'),
            'forecast_date': (latest_date + timedelta(days=days_ahead)).strftime('%Y-%m-%d'),
            'current_values': {
                'cpu_utilization': current_cpu,
                'power_usage': current_power,
                'network_traffic': current_network
            },
            'predicted_values': {
                'cpu_utilization': predicted_cpu,
                'power_usage': predicted_power,
                'network_traffic': predicted_network
            },
            'capacity_analysis': {
                'days_to_cpu_capacity': int(days_to_cpu_capacity),
                'days_to_power_capacity': int(days_to_power_capacity),
                'days_to_network_capacity': int(days_to_network_capacity)
            },
            'recommended_actions': self._generate_capacity_recommendations(
                days_to_cpu_capacity, 
                days_to_power_capacity,
                days_to_network_capacity
            )
        }
    
    def _generate_capacity_recommendations(self, days_to_cpu, days_to_power, days_to_network):
        """
        Generate recommendations based on capacity predictions
        Private helper method
        """
        recommendations = []
        
        # CPU recommendations
        if days_to_cpu < 30:
            recommendations.append(
                "URGENT: CPU capacity will be reached in less than 30 days. Immediately plan for expansion or workload optimization."
            )
        elif days_to_cpu < 90:
            recommendations.append(
                "Plan for CPU capacity expansion within the next quarter to avoid performance issues."
            )
        elif days_to_cpu < 180:
            recommendations.append(
                "Begin evaluating options for CPU capacity expansion or workload redistribution within 6 months."
            )
        
        # Power recommendations
        if days_to_power < 45:
            recommendations.append(
                "URGENT: Power capacity will be reached in less than 45 days. Evaluate power infrastructure upgrades."
            )
        elif days_to_power < 120:
            recommendations.append(
                "Plan for power infrastructure upgrades within 4 months to accommodate growing demand."
            )
        
        # Network recommendations
        if days_to_network < 60:
            recommendations.append(
                "Network bandwidth will reach capacity in less than 60 days. Schedule network infrastructure upgrades."
            )
        elif days_to_network < 150:
            recommendations.append(
                "Begin planning for network capacity expansion within 5 months to maintain performance."
            )
        
        # General recommendations if no immediate concerns
        if len(recommendations) == 0:
            recommendations.append(
                "All resources have sufficient capacity for the next 6 months based on current growth trends. Continue regular monitoring."
            )
        
        return recommendations
    
    def generate_energy_optimization(self):
        """
        Generate energy optimization recommendations
        Returns a list of energy optimization recommendations
        """
        if self.df is None:
            return []
        
        # Calculate current PUE
        current_pue = self.df['pue'].mean()
        
        optimizations = []
        
        # PUE-based recommendations
        if current_pue > 1.5:
            optimizations.append({
                'category': 'Cooling',
                'recommendation': 'Implement AI-controlled cooling system with machine learning for dynamic temperature adjustment',
                'potential_savings': '15-20%',
                'implementation_cost': 'High',
                'roi_months': 18,
                'complexity': 'High'
            })
            
            optimizations.append({
                'category': 'Power',
                'recommendation': 'Upgrade to high-efficiency UPS systems with eco-mode capabilities',
                'potential_savings': '10-15%',
                'implementation_cost': 'High',
                'roi_months': 24,
                'complexity': 'Medium'
            })
        
        # Always include these recommendations
        optimizations.extend([
            {
                'category': 'Workload',
                'recommendation': 'Implement AI workload scheduling to optimize for time-of-day energy costs and renewable energy availability',
                'potential_savings': '8-12%',
                'implementation_cost': 'Medium',
                'roi_months': 12,
                'complexity': 'Medium'
            },
            {
                'category': 'Monitoring',
                'recommendation': 'Deploy IoT sensors throughout facility with ML-based analysis for micro-optimization of environmental conditions',
                'potential_savings': '5-8%',
                'implementation_cost': 'Medium',
                'roi_months': 15,
                'complexity': 'Medium'
            },
            {
                'category': 'Renewable Energy',
                'recommendation': 'Integrate on-site renewable energy sources with AI-optimized usage based on workload patterns',
                'potential_savings': '20-30%',
                'implementation_cost': 'Very High',
                'roi_months': 36,
                'complexity': 'High'
            }
        ])
        
        return optimizations
    
    def get_smart_insights(self):
        """
        Generate AI-powered insights from the data
        Returns a list of insights
        """
        if self.df is None:
            return []
        
        insights = []
        
        # 1. Temperature patterns
        temp_by_hour = self.df.groupby(self.df['timestamp'].dt.hour)['temperature'].mean()
        max_temp_hour = temp_by_hour.idxmax()
        min_temp_hour = temp_by_hour.idxmin()
        
        insights.append(
            f"🌡️ Temperature is consistently highest at {max_temp_hour}:00 and lowest at {min_temp_hour}:00. " +
            "Adjusting cooling schedules to preemptively increase cooling before peak hours could reduce energy usage by 7-12%."
        )
        
        # 2. Power usage insight
        power_by_day = self.df.groupby(self.df['timestamp'].dt.day_name())['power_usage'].mean().sort_values(ascending=False)
        highest_power_day = power_by_day.index[0]
        lowest_power_day = power_by_day.index[-1]
        
        insights.append(
            f"⚡ Power consumption is highest on {highest_power_day}s and lowest on {lowest_power_day}s. " +
            "Consider scheduling non-critical batch workloads for low-usage days to balance power consumption and improve PUE."
        )
        
        # 3. Anomalies insight
        anomalies = self.identify_anomalies()
        if len(anomalies) > 0:
            anomaly_count = len(anomalies)
            most_common_metric = anomalies['metric'].value_counts().idxmax()
            most_affected_location = anomalies['location'].value_counts().idxmax()
            
            insights.append(
                f"⚠️ Detected {anomaly_count} anomalies, primarily in {most_common_metric} readings. " +
                f"Location {most_affected_location} shows the most irregular patterns and may require attention."
            )
        else:
            insights.append(
                "✅ No significant anomalies detected in recent data, indicating stable operations. " +
                "Continue monitoring with current thresholds."
            )
        
        # 4. Correlation insight
        correlation = self.df[['temperature', 'power_usage', 'cpu_utilization']].corr()
        strongest_corr = abs(correlation.unstack()).sort_values(ascending=False)
        strongest_pair = strongest_corr[strongest_corr < 1].index[0]
        corr_value = correlation.loc[strongest_pair]
        
        insights.append(
            f"📊 Strong correlation ({corr_value:.2f}) detected between {strongest_pair[0]} and {strongest_pair[1]}. " +
            "This relationship could be leveraged for predictive modeling and early warning systems."
        )
        
        # 5. Efficiency insight
        avg_pue = self.df['pue'].mean()
        lowest_pue = self.df.groupby(self.df['timestamp'].dt.date)['pue'].mean().min()
        
        pue_improvement = ((avg_pue - lowest_pue) / avg_pue) * 100
        
        insights.append(
            f"💡 Your best-performing PUE day was {pue_improvement:.1f}% better than average. " +
            f"Analyzing conditions on days with PUE below {lowest_pue:.2f} could reveal optimization opportunities for cooling and power systems."
        )
        
        return insights 