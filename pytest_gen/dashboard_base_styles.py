"""
Base CSS styles for dashboard layout and structure.
"""


class DashboardBaseStyles:
    """Base CSS styles for dashboard layout."""
    
    @staticmethod
    def get_base_styles() -> str:
        """Get base CSS styles."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .widget {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .widget:hover {
            transform: translateY(-5px);
        }
        
        .widget-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .widget-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .widget-content {
            padding: 10px 0;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        
        .status-healthy { background-color: #27ae60; }
        .status-warning { background-color: #f39c12; }
        .status-critical { background-color: #e74c3c; }
        .status-info { background-color: #3498db; }
        
        .metric-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #007bff;
        }
        
        .metric-value {
            font-size: 1.8em;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #6c757d;
            margin-top: 5px;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background-color: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }
        
        .alert-item {
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            border-left: 4px solid;
        }
        
        .alert-info { 
            background-color: #d1ecf1; 
            border-left-color: #17a2b8; 
        }
        
        .alert-warning { 
            background-color: #fff3cd; 
            border-left-color: #ffc107; 
        }
        
        .alert-critical { 
            background-color: #f8d7da; 
            border-left-color: #dc3545; 
        }
        
        .job-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 8px;
            margin: 5px 0;
        }
        
        .job-name {
            font-weight: 500;
        }
        
        .job-status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 500;
        }
        
        .status-running { background-color: #d4edda; color: #155724; }
        .status-completed { background-color: #cce5ff; color: #004085; }
        .status-failed { background-color: #f8d7da; color: #721c24; }
        """
    
    @staticmethod
    def get_responsive_styles() -> str:
        """Get responsive CSS styles."""
        return """
        @media (max-width: 768px) {
            .dashboard {
                grid-template-columns: 1fr;
                padding: 10px;
                gap: 15px;
            }
            
            .widget {
                padding: 15px;
            }
            
            .widget-title {
                font-size: 1.1em;
            }
            
            .metric-value {
                font-size: 1.5em;
            }
        }
        
        @media (max-width: 480px) {
            .dashboard {
                padding: 5px;
            }
            
            .widget {
                padding: 10px;
                border-radius: 10px;
            }
            
            .widget-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
        """
