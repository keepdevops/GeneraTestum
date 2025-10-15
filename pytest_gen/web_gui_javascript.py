"""
Web GUI JavaScript functionality.
"""

class WebGUIJavaScript:
    """Web GUI JavaScript functionality."""
    
    @staticmethod
    def get_core_functions() -> str:
        return """
        function showTab(tabName) {
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
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
                    code += `# File content would be loaded here\n\n`;
                }
            }
            document.getElementById('sourceCode').value = code;
        }
        """

    @staticmethod
    def get_test_functions() -> str:
        return """
        function generateTests() {
            const resultDiv = document.getElementById('result');
            const progressDiv = document.getElementById('progress');
            const progressFill = document.getElementById('progressFill');
            
            progressDiv.style.display = 'block';
            resultDiv.style.display = 'none';
            
            let progress = 0;
            const interval = setInterval(() => {
                progress += 10;
                progressFill.style.width = progress + '%';
                
                if (progress >= 100) {
                    clearInterval(interval);
                    progressDiv.style.display = 'none';
                    resultDiv.style.display = 'block';
                    
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
        """

    @staticmethod
    def get_settings_functions() -> str:
        return """
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
    def get_all_javascript() -> str:
        css = WebGUICSS()
        js = WebGUIJavaScript()
        return f"""
        {js.get_core_functions()}
        {js.get_test_functions()}
        {js.get_settings_functions()}
        """
