"""
Dashboard CSS styles and styling utilities.
"""


class DashboardCSS:
    """Dashboard CSS styles and styling utilities."""
    
    @staticmethod
    def get_base_styles() -> str:
        """Get base CSS styles."""
        return """
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .widget {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }}
        
        .widget:hover {{
            transform: translateY(-5px);
        }}
        
        .widget-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .widget-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .status-indicator {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #27ae60;
            animation: pulse 2s infinite;
        }}
        
        .status-indicator.warning {{ background: #f39c12; }}
        .status-indicator.error {{ background: #e74c3c; }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .metric-card {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #3498db;
        }}
        
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        .metric-unit {{
            font-size: 0.8em;
            color: #95a5a6;
        }}
        
        .job-list {{
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .job-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        
        .job-item.completed {{ border-left-color: #27ae60; }}
        .job-item.failed {{ border-left-color: #e74c3c; }}
        .job-item.running {{ border-left-color: #f39c12; }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #ecf0f1;
            border-radius: 4px;
            overflow: hidden;
            margin: 5px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            transition: width 0.3s ease;
        }}
        
        .alert-item {{
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border-left: 4px solid;
            background: #f8f9fa;
        }}
        
        .alert-item.info {{ border-left-color: #3498db; }}
        .alert-item.warning {{ border-left-color: #f39c12; }}
        .alert-item.error {{ border-left-color: #e74c3c; }}
        .alert-item.critical {{ border-left-color: #8e44ad; }}
        
        .alert-title {{
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .alert-message {{
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 0 0 15px 15px;
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .refresh-info {{
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 20px;
        }}
        
        .chart-container {{
            position: relative;
            height: 200px;
            margin-top: 15px;
        }}
        
        .loading {{
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
        }}
        
        .error {{
            color: #e74c3c;
            text-align: center;
            padding: 20px;
        }}
        """

    @staticmethod
    def get_javascript() -> str:
        """Get JavaScript code for the dashboard."""
        return """
        // WebSocket connection for real-time updates
        const ws = new WebSocket('ws://localhost:8000/ws/dashboard');
        
        ws.onmessage = function(event) {{
            const data = JSON.parse(event.data);
            if (data.event_type === 'data_update') {{
                updateDashboard(data.event_data);
            }}
        }};
        
        ws.onerror = function(error) {{
            console.log('WebSocket error:', error);
        }};
        
        function updateDashboard(data) {{
            // Update dashboard with new data
            location.reload(); // Simple refresh for now
        }}
        
        // Auto-refresh every 30 seconds as fallback
        setInterval(() => {{
            location.reload();
        }}, 30000);
        """
