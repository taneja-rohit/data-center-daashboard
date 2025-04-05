# Data Center Operations Dashboard

A sophisticated monitoring and analytics dashboard for data center operators, focusing on physical infrastructure management rather than IT/DevOps concerns. This application provides comprehensive visualizations, alerts, and AI-powered insights for managing data center operations.

## Features

- **Operational Metrics Dashboard**
  - Uptime monitoring and SLA tracking
  - Power Usage Effectiveness (PUE) analysis
  - Mean Time To Repair (MTTR) tracking
  - Customer satisfaction and churn metrics
  - Sustainability metrics

- **Resource Management Dashboard**
  - Capacity planning and monitoring
  - Temperature and hotspot visualization
  - Peak load analysis by rack/cabinet
  - Network topology and port availability

- **AI-Powered Insights**
  - Anomaly detection for proactive issue resolution
  - Predictive maintenance scheduling
  - Resource optimization recommendations
  - Energy efficiency analysis

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd data-center-dashboard
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running Locally

Start the Streamlit application:

```
streamlit run app/app.py
```

The application will be available at http://localhost:8501 by default.

## Deployment on Streamlit Cloud

This application can be easily deployed on Streamlit Cloud for private access:

1. Push this repository to GitHub
2. Sign in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" and select this repository
4. Set the main file path to "app/app.py"
5. Set visibility to "Private" if you want to restrict access
6. Deploy the app
7. Invite team members using their email addresses through the Streamlit Cloud dashboard

### Environment Variables

If you need to set environment variables for production (e.g., API keys, database connections), you can create a `.streamlit/secrets.toml` file (not included in version control) with the following format:

```toml
[general]
password = "your_password"

[connections]
database_url = "your_db_connection_string"
```

## Demo Data

The application generates sample data internally for demonstration purposes. In a production environment, you would connect this to your actual data sources:

- Building Management Systems (BMS)
- Power monitoring systems
- Environmental sensors
- DCIM (Data Center Infrastructure Management) systems
- Customer relationship management systems

## AI Features

The dashboard includes several AI-powered features:

1. **Predictive Analytics**: Forecasts future resource needs and potential issues
2. **Root Cause Analysis**: Identifies underlying causes of anomalies
3. **Dynamic Resource Optimization**: Recommendations for optimizing cooling, power, and workload
4. **Enhanced Visualizations**: Converts complex data into actionable insights

## Customization

The dashboard can be customized for your specific data center environment by:

1. Connecting to your existing data sources
2. Adjusting thresholds and alert parameters
3. Adding additional metrics specific to your infrastructure
4. Customizing the AI models for your operational patterns

## Project Structure

```
app/
├── app.py               # Main application file
├── components/          # Reusable UI components
├── data/                # Data handling and processing
├── pages/               # Additional dashboard pages
│   └── ai_insights.py   # AI insights page
├── static/              # Static assets
│   ├── css/             # Custom CSS
│   └── images/          # Images
└── utils/               # Utility functions
    └── ai_insights.py   # AI utilities
```

## Future Enhancements

- Integration with real-time alerting systems
- Mobile application for on-the-go monitoring
- Advanced AI models for more precise predictions
- Integration with automation systems for closed-loop optimization
- Expanded sustainability metrics and carbon footprint analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit, Pandas, Plotly, and other open-source technologies
- Designed for data center operators focused on physical infrastructure 