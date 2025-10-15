"""
Web GUI HTML templates.
"""

from .web_gui_styles import WebGUIStyles


class WebGUITemplates:
    """Web GUI HTML templates."""
    
    def __init__(self):
        self.styles = WebGUIStyles()
    
    def get_html_template(self) -> str:
        """Get the main HTML template."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pytest Code Generator</title>
    <style>
        {self.styles.get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Pytest Code Generator</h1>
            <p>Generate comprehensive test cases from your Python code</p>
        </div>
        
        <div class="content">
            <div class="tabs">
                <div class="tab active" onclick="showTab('generate')">Generate Tests</div>
                <div class="tab" onclick="showTab('analyze')">Analyze Code</div>
                <div class="tab" onclick="showTab('settings')">Settings</div>
            </div>
            
            <div id="generate" class="tab-content active">
                <div class="section">
                    <h3>📁 Source Code</h3>
                    <div class="form-group">
                        <label for="sourceType">Source Type:</label>
                        <select id="sourceType" onchange="updateSourceInput()">
                            <option value="file">File</option>
                            <option value="directory">Directory</option>
                            <option value="code">Paste Code</option>
                        </select>
                    </div>
                    <div id="fileInput" class="form-group">
                        <label for="sourceFile">Select Python File:</label>
                        <input type="file" id="sourceFile" accept=".py" onchange="loadFile()">
                    </div>
                    <div id="directoryInput" class="form-group" style="display: none;">
                        <label for="sourceDirectory">Select Directory:</label>
                        <input type="file" id="sourceDirectory" webkitdirectory directory multiple onchange="loadDirectory()">
                    </div>
                    <div id="codeInput" class="form-group" style="display: none;">
                        <label for="sourceCode">Paste your Python code:</label>
                        <textarea id="sourceCode" rows="10" placeholder="def example_function():
    return 'Hello, World!'"></textarea>
                    </div>
                </div>
                
                <div class="section">
                    <h3>⚙️ Generation Options</h3>
                    <div class="grid">
                        <div>
                            <div class="form-group">
                                <label for="mockLevel">Mock Level:</label>
                                <select id="mockLevel">
                                    <option value="none">None</option>
                                    <option value="basic">Basic</option>
                                    <option value="comprehensive" selected>Comprehensive</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="coverage">Coverage Level:</label>
                                <select id="coverage">
                                    <option value="happy_path">Happy Path</option>
                                    <option value="comprehensive" selected>Comprehensive</option>
                                    <option value="full">Full</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <div class="form-group">
                                <label for="outputDir">Output Directory:</label>
                                <input type="text" id="outputDir" value="tests" placeholder="tests">
                            </div>
                            <div class="form-group">
                                <label>
                                    <input type="checkbox" id="includePrivate"> Include Private Methods
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <button onclick="generateTests()">🚀 Generate Tests</button>
                    <div id="progress" style="display: none;">
                        <div class="progress-bar">
                            <div class="progress-fill" id="progressFill"></div>
                        </div>
                        <div id="progressText">Generating tests...</div>
                    </div>
                    <div id="result" class="result" style="display: none;"></div>
                </div>
            </div>
            
            <div id="analyze" class="tab-content">
                <div class="section">
                    <h3>🔍 Code Analysis</h3>
                    <div class="form-group">
                        <label for="analyzeFile">Select Python File to Analyze:</label>
                        <input type="file" id="analyzeFile" accept=".py" onchange="analyzeCode()">
                    </div>
                    <div id="analysisResult" class="result" style="display: none;"></div>
                </div>
            </div>
            
            <div id="settings" class="tab-content">
                <div class="section">
                    <h3>⚙️ Settings</h3>
                    <div class="form-group">
                        <label for="maxLines">Maximum Lines per Test File:</label>
                        <input type="number" id="maxLines" value="200" min="50" max="1000">
                    </div>
                    <div class="form-group">
                        <label for="splitFiles">Split Large Files:</label>
                        <input type="checkbox" id="splitFiles" checked>
                    </div>
                    <div class="form-group">
                        <label for="verbose">Verbose Output:</label>
                        <input type="checkbox" id="verbose">
                    </div>
                    <button onclick="saveSettings()">💾 Save Settings</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        {self.styles.get_javascript()}
    </script>
</body>
</html>
        """

    @staticmethod
    def get_error_template(error_message: str) -> str:
        """Get error template."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Pytest Code Generator</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .error-container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
            text-align: center;
        }}
        .error-icon {{
            font-size: 48px;
            margin-bottom: 20px;
        }}
        .error-message {{
            color: #721c24;
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }}
        .back-button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">❌</div>
        <h1>Error</h1>
        <div class="error-message">{error_message}</div>
        <a href="/" class="back-button">← Back to Generator</a>
    </div>
</body>
</html>
        """
