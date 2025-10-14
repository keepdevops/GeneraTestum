"""
Web-based GUI for the test generator using Flask.
"""

import os
import json
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from .generator_core import GeneratorCore
from .config import GeneratorConfig

app = Flask(__name__)

# Initialize generator
generator = GeneratorCore()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pytest Code Generator</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 20px;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
        }
        .section h3 {
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        button:hover {
            opacity: 0.9;
        }
        .btn-secondary {
            background: #6c757d;
        }
        .btn-success {
            background: #28a745;
        }
        .results {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 15px;
            margin-top: 15px;
            white-space: pre-wrap;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
        }
        .file-list {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
        }
        .file-item {
            padding: 8px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
        }
        .file-item:hover {
            background: #f0f0f0;
        }
        .file-item.selected {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        .status {
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Pytest Code Generator</h1>
            <p>Generate comprehensive test cases from Python code</p>
        </div>
        
        <div class="content">
            <!-- File Analysis Section -->
            <div class="section">
                <h3>📁 File Analysis</h3>
                <div class="form-group">
                    <label for="sourcePath">Source File/Directory:</label>
                    <input type="text" id="sourcePath" placeholder="e.g., example_calculator.py" value="example_calculator.py">
                </div>
                <button onclick="analyzeFile()">🔍 Analyze</button>
                <button onclick="generateTests()" class="btn-success">⚡ Generate Tests</button>
                <div id="analysisResults" class="results" style="display:none;"></div>
            </div>

            <!-- Configuration Section -->
            <div class="section">
                <h3>⚙️ Configuration</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="form-group">
                        <label for="mockLevel">Mock Level:</label>
                        <select id="mockLevel">
                            <option value="none">None</option>
                            <option value="basic">Basic</option>
                            <option value="comprehensive" selected>Comprehensive</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="coverageType">Coverage Type:</label>
                        <select id="coverageType">
                            <option value="happy_path">Happy Path</option>
                            <option value="comprehensive" selected>Comprehensive</option>
                            <option value="full">Full</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="outputDir">Output Directory:</label>
                        <input type="text" id="outputDir" value="tests_generated">
                    </div>
                    <div class="form-group">
                        <label for="maxLines">Max Lines per File:</label>
                        <input type="number" id="maxLines" value="200" min="50" max="500">
                    </div>
                </div>
                <div style="margin-top: 15px;">
                    <label>
                        <input type="checkbox" id="includePrivate" checked> Include Private Methods
                    </label>
                    <label style="margin-left: 20px;">
                        <input type="checkbox" id="generateFixtures" checked> Generate Fixtures
                    </label>
                    <label style="margin-left: 20px;">
                        <input type="checkbox" id="splitFiles" checked> Split Large Files
                    </label>
                </div>
            </div>

            <!-- Quick Actions Section -->
            <div class="section">
                <h3>🚀 Quick Actions</h3>
                <button onclick="analyzeFile('example_calculator.py')">📊 Analyze Calculator</button>
                <button onclick="analyzeFile('example_api.py')">🌐 Analyze API</button>
                <button onclick="generateTests('example_calculator.py')">🧮 Generate Calculator Tests</button>
                <button onclick="generateTests('example_api.py')">🔌 Generate API Tests</button>
                <button onclick="showHelp()" class="btn-secondary">❓ Help</button>
            </div>

            <!-- Results Section -->
            <div class="section">
                <h3>📋 Results</h3>
                <div id="status" class="status" style="display:none;"></div>
                <div id="results" class="results" style="display:none;"></div>
            </div>
        </div>
    </div>

    <script>
        function showStatus(message, type = 'info') {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = `status ${type}`;
            status.style.display = 'block';
        }

        function showResults(content) {
            const results = document.getElementById('results');
            results.textContent = content;
            results.style.display = 'block';
        }

        function getConfig() {
            return {
                mock_level: document.getElementById('mockLevel').value,
                coverage_type: document.getElementById('coverageType').value,
                output_dir: document.getElementById('outputDir').value,
                max_lines_per_file: parseInt(document.getElementById('maxLines').value),
                include_private_methods: document.getElementById('includePrivate').checked,
                generate_fixtures: document.getElementById('generateFixtures').checked,
                split_large_tests: document.getElementById('splitFiles').checked
            };
        }

        async function analyzeFile(sourcePath = null) {
            const path = sourcePath || document.getElementById('sourcePath').value;
            if (!path) {
                showStatus('Please enter a source file path', 'error');
                return;
            }

            showStatus('Analyzing file...', 'info');
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({source_path: path})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    const analysisDiv = document.getElementById('analysisResults');
                    analysisDiv.textContent = JSON.stringify(result.analysis, null, 2);
                    analysisDiv.style.display = 'block';
                    showStatus('Analysis completed successfully!', 'success');
                } else {
                    showStatus(`Analysis failed: ${result.error}`, 'error');
                }
            } catch (error) {
                showStatus(`Error: ${error.message}`, 'error');
            }
        }

        async function generateTests(sourcePath = null) {
            const path = sourcePath || document.getElementById('sourcePath').value;
            if (!path) {
                showStatus('Please enter a source file path', 'error');
                return;
            }

            showStatus('Generating tests...', 'info');
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        source_path: path,
                        config: getConfig()
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showResults(result.message);
                    showStatus('Tests generated successfully!', 'success');
                } else {
                    showStatus(`Generation failed: ${result.error}`, 'error');
                }
            } catch (error) {
                showStatus(`Error: ${error.message}`, 'error');
            }
        }

        function showHelp() {
            const helpText = `Pytest Code Generator Help:

1. File Analysis:
   - Enter a Python file path to analyze
   - Click "Analyze" to see what tests would be generated
   - Supports .py files and directories

2. Configuration:
   - Mock Level: How much mocking to include
   - Coverage Type: Test coverage level
   - Output Directory: Where to save generated tests
   - Max Lines: Maximum lines per test file

3. Quick Actions:
   - Pre-configured buttons for common files
   - Generate tests with one click

4. Results:
   - Analysis results show file structure
   - Generation results show created files

Example files available:
- example_calculator.py (Python functions)
- example_api.py (Flask API endpoints)`;
            
            showResults(helpText);
            showStatus('Help information displayed', 'info');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main GUI page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a source file."""
    try:
        data = request.get_json()
        source_path = data.get('source_path')
        
        if not source_path:
            return jsonify({'success': False, 'error': 'No source path provided'})
        
        if not os.path.exists(source_path):
            return jsonify({'success': False, 'error': f'File not found: {source_path}'})
        
        # Analyze the file
        analysis = generator.analyze_source(source_path)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    """Generate tests for a source file."""
    try:
        data = request.get_json()
        source_path = data.get('source_path')
        config_data = data.get('config', {})
        
        if not source_path:
            return jsonify({'success': False, 'error': 'No source path provided'})
        
        if not os.path.exists(source_path):
            return jsonify({'success': False, 'error': f'File not found: {source_path}'})
        
        # Update configuration
        for key, value in config_data.items():
            if hasattr(generator.config, key):
                setattr(generator.config, key, value)
        
        # Generate tests
        test_files = generator.generate_tests(source_path, config_data.get('output_dir'))
        
        if test_files:
            message = f"Generated {len(test_files)} test file(s):\n" + "\n".join(f"- {f}" for f in test_files)
        else:
            message = "No tests were generated. Check the source file and configuration."
        
        return jsonify({
            'success': True,
            'message': message,
            'files': test_files
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/files/<path:filename>')
def serve_file(filename):
    """Serve generated test files."""
    return send_from_directory('tests_generated', filename)

def launch_web_gui(port=5007, host='localhost', debug=False):
    """Launch the web-based GUI."""
    print(f"🚀 Launching Web GUI...")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Features: File analysis, test generation, configuration")
    print("Press Ctrl+C to stop the server")
    
    app.run(host=host, port=port, debug=debug, use_reloader=False)

if __name__ == '__main__':
    launch_web_gui()
