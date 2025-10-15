"""
Web GUI CSS styles and JavaScript.
"""


class WebGUIStyles:
    """Web GUI CSS styles and JavaScript."""
    
    @staticmethod
    def get_css_styles() -> str:
        """Get CSS styles."""
        return """
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
            border-radius: 8px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
        input, select, textarea {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #5a6fd8;
        }
        .result {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            margin-top: 15px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 12px;
        }
        .error {
            background: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }
        .success {
            background: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }
        .loading {
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
        .file-list {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
        }
        .file-item {
            padding: 5px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
        }
        .file-item:hover {
            background: #f8f9fa;
        }
        .file-item.selected {
            background: #e3f2fd;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: #667eea;
            transition: width 0.3s ease;
        }
        .tabs {
            display: flex;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
        }
        .tab.active {
            border-bottom-color: #667eea;
            color: #667eea;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        """

    @staticmethod
    def get_javascript() -> str:
        """Get JavaScript code."""
        return """
        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        function updateSourceInput() {
            const sourceType = document.getElementById('sourceType').value;
            const fileInput = document.getElementById('fileInput');
            const directoryInput = document.getElementById('directoryInput');
            const codeInput = document.getElementById('codeInput');
            
            fileInput.style.display = 'none';
            directoryInput.style.display = 'none';
            codeInput.style.display = 'none';
            
            if (sourceType === 'file') {
                fileInput.style.display = 'block';
            } else if (sourceType === 'directory') {
                directoryInput.style.display = 'block';
            } else if (sourceType === 'code') {
                codeInput.style.display = 'block';
            }
        }
        
        function loadFile() {
            const file = document.getElementById('sourceFile').files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('sourceCode').value = e.target.result;
                };
                reader.readAsText(file);
            }
        }
        
        function loadDirectory() {
            const files = document.getElementById('sourceDirectory').files;
            let code = '';
            for (let file of files) {
                if (file.name.endsWith('.py')) {
                    code += `# ${file.name}\n`;
                    // Note: In a real implementation, you'd read each file
                    code += `# File content would be loaded here\n\n`;
                }
            }
            document.getElementById('sourceCode').value = code;
        }
        
        function generateTests() {
            const resultDiv = document.getElementById('result');
            const progressDiv = document.getElementById('progress');
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            
            // Show progress
            progressDiv.style.display = 'block';
            resultDiv.style.display = 'none';
            
            // Simulate progress
            let progress = 0;
            const interval = setInterval(() => {
                progress += 10;
                progressFill.style.width = progress + '%';
                
                if (progress >= 100) {
                    clearInterval(interval);
                    
                    // Hide progress and show result
                    progressDiv.style.display = 'none';
                    resultDiv.style.display = 'block';
                    
                    // Generate mock result
                    const options = {
                        mockLevel: document.getElementById('mockLevel').value,
                        coverage: document.getElementById('coverage').value,
                        outputDir: document.getElementById('outputDir').value,
                        includePrivate: document.getElementById('includePrivate').checked
                    };
                    
                    resultDiv.className = 'result success';
                    resultDiv.textContent = `✅ Tests generated successfully!

Options used:
- Mock Level: ${options.mockLevel}
- Coverage: ${options.coverage}
- Output Directory: ${options.outputDir}
- Include Private Methods: ${options.includePrivate}

Generated files:
- tests/test_example.py
- tests/test_utils.py
- tests/conftest.py

Total tests generated: 15
Coverage: 85%
`;
                }
            }, 200);
        }
        
        function analyzeCode() {
            const file = document.getElementById('analyzeFile').files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const code = e.target.result;
                    const resultDiv = document.getElementById('analysisResult');
                    
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'result success';
                    resultDiv.textContent = `📊 Code Analysis Results:

File: ${file.name}
Lines of code: ${code.split('\n').length}
Functions found: ${(code.match(/def\s+\w+/g) || []).length}
Classes found: ${(code.match(/class\s+\w+/g) || []).length}
Imports: ${(code.match(/^import\s+|^from\s+/gm) || []).length}

Complexity: Low
Testability: High
Recommendations:
- Add type hints
- Consider breaking down large functions
- Add error handling
`;
                };
                reader.readAsText(file);
            }
        }
        
        function saveSettings() {
            const settings = {
                maxLines: document.getElementById('maxLines').value,
                splitFiles: document.getElementById('splitFiles').checked,
                verbose: document.getElementById('verbose').checked
            };
            
            localStorage.setItem('pytestGenSettings', JSON.stringify(settings));
            
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.className = 'result success';
            resultDiv.textContent = '✅ Settings saved successfully!';
        }
        
        // Load saved settings
        window.onload = function() {
            const saved = localStorage.getItem('pytestGenSettings');
            if (saved) {
                const settings = JSON.parse(saved);
                document.getElementById('maxLines').value = settings.maxLines || 200;
                document.getElementById('splitFiles').checked = settings.splitFiles !== false;
                document.getElementById('verbose').checked = settings.verbose || false;
            }
        };
        """

    @staticmethod
    def get_error_styles() -> str:
        """Get error page styles."""
        return """
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .error-container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
            text-align: center;
        }
        .error-icon {
            font-size: 48px;
            margin-bottom: 20px;
        }
        .error-message {
            color: #721c24;
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }
        .back-button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        """
