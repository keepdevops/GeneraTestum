"""
Advanced CSS styles for dashboard components and animations.
"""


class DashboardAdvancedStyles:
    """Advanced CSS styles for dashboard components."""
    
    @staticmethod
    def get_animation_styles() -> str:
        """Get animation and transition styles."""
        return """
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .widget {
            animation: fadeIn 0.5s ease-out;
        }
        
        .loading-spinner {
            width: 20px;
            height: 20px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .pulse-animation {
            animation: pulse 2s infinite;
        }
        
        .slide-in {
            animation: slideIn 0.3s ease-out;
        }
        
        .hover-glow:hover {
            box-shadow: 0 0 20px rgba(52, 152, 219, 0.5);
        }
        
        .status-indicator.blinking {
            animation: pulse 1s infinite;
        }
        """
    
    @staticmethod
    def get_chart_styles() -> str:
        """Get styles for charts and graphs."""
        return """
        .chart-container {
            position: relative;
            height: 200px;
            margin: 15px 0;
        }
        
        .chart-bar {
            display: flex;
            align-items: end;
            height: 150px;
            gap: 5px;
            margin: 20px 0;
        }
        
        .chart-bar-item {
            flex: 1;
            background: linear-gradient(to top, #3498db, #5dade2);
            border-radius: 4px 4px 0 0;
            min-height: 20px;
            transition: all 0.3s ease;
        }
        
        .chart-bar-item:hover {
            background: linear-gradient(to top, #2980b9, #3498db);
            transform: scaleY(1.05);
        }
        
        .chart-line {
            position: relative;
            height: 150px;
            border-bottom: 2px solid #e9ecef;
            border-left: 2px solid #e9ecef;
        }
        
        .line-point {
            position: absolute;
            width: 6px;
            height: 6px;
            background-color: #3498db;
            border-radius: 50%;
            transform: translate(-50%, 50%);
        }
        
        .line-point:hover {
            width: 10px;
            height: 10px;
            background-color: #2980b9;
        }
        
        .gauge-container {
            position: relative;
            width: 120px;
            height: 120px;
            margin: 0 auto;
        }
        
        .gauge-circle {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(
                #27ae60 0deg 216deg,
                #f39c12 216deg 288deg,
                #e74c3c 288deg 360deg
            );
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .gauge-inner {
            width: 80%;
            height: 80%;
            background-color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
        }
        """
    
    @staticmethod
    def get_glassmorphism_styles() -> str:
        """Get glassmorphism effect styles."""
        return """
        .glass-effect {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        
        .glass-widget {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        }
        
        .glass-button {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            padding: 10px 20px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .glass-button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        """
    
    @staticmethod
    def get_dark_mode_styles() -> str:
        """Get dark mode styles."""
        return """
        .dark-mode {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
        }
        
        .dark-mode .widget {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #e0e0e0;
        }
        
        .dark-mode .widget-title {
            color: #ffffff;
        }
        
        .dark-mode .metric-card {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border-left-color: #3498db;
        }
        
        .dark-mode .metric-value {
            color: #ffffff;
        }
        
        .dark-mode .metric-label {
            color: #bdc3c7;
        }
        
        .dark-mode .alert-item {
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        .dark-mode .job-item {
            background-color: rgba(255, 255, 255, 0.05);
        }
        """
