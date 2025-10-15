"""
Web-based GUI for the test generator using Flask.
"""

import os
import json
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from .generator_core import GeneratorCore
from .config import GeneratorConfig
from .web_gui_templates import WebGUITemplates


class WebGUI:
    """Web-based GUI for the test generator."""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.generator = GeneratorCore()
        self.templates = WebGUITemplates()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main page."""
            return render_template_string(self.templates.get_html_template())
        
        @self.app.route('/generate', methods=['POST'])
        def generate_tests():
            """Generate tests endpoint."""
            try:
                data = request.get_json()
                
                # Get source code
                source_code = data.get('code', '')
                if not source_code:
                    return jsonify({'error': 'No source code provided'}), 400
                
                # Get options
                options = {
                    'mock_level': data.get('mockLevel', 'comprehensive'),
                    'coverage': data.get('coverage', 'comprehensive'),
                    'output_dir': data.get('outputDir', 'tests'),
                    'include_private': data.get('includePrivate', False)
                }
                
                # Generate tests
                result = self.generator.generate_tests_from_code(
                    source_code, 
                    options
                )
                
                return jsonify({
                    'success': True,
                    'message': 'Tests generated successfully',
                    'files': result.get('files', []),
                    'tests_count': result.get('tests_count', 0),
                    'coverage': result.get('coverage', 0)
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/analyze', methods=['POST'])
        def analyze_code():
            """Analyze code endpoint."""
            try:
                data = request.get_json()
                source_code = data.get('code', '')
                
                if not source_code:
                    return jsonify({'error': 'No source code provided'}), 400
                
                # Analyze code
                analysis = self.generator.analyze_code(source_code)
                
                return jsonify({
                    'success': True,
                    'analysis': analysis
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/files/<path:filename>')
        def serve_file(filename):
            """Serve generated test files."""
            try:
                return send_from_directory(
                    self.generator.config.output_dir,
                    filename,
                    as_attachment=True
                )
            except Exception as e:
                return jsonify({'error': str(e)}), 404
        
        @self.app.route('/download/<path:filename>')
        def download_file(filename):
            """Download generated test files."""
            try:
                return send_from_directory(
                    self.generator.config.output_dir,
                    filename,
                    as_attachment=True,
                    download_name=f"test_{filename}"
                )
            except Exception as e:
                return jsonify({'error': str(e)}), 404
        
        @self.app.errorhandler(404)
        def not_found(error):
            """404 error handler."""
            return render_template_string(
                self.templates.get_error_template("Page not found")
            ), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """500 error handler."""
            return render_template_string(
                self.templates.get_error_template("Internal server error")
            ), 500
    
    def run(self, host='127.0.0.1', port=5000, debug=False):
        """Run the web GUI."""
        print(f"🌐 Starting Web GUI on http://{host}:{port}")
        print("📝 Features:")
        print("  • Generate tests from Python code")
        print("  • Analyze code complexity and testability")
        print("  • Download generated test files")
        print("  • Real-time test generation")
        
        self.app.run(host=host, port=port, debug=debug)


def create_web_gui() -> WebGUI:
    """Create and return a web GUI instance."""
    return WebGUI()


def run_web_gui(host='127.0.0.1', port=5000, debug=False):
    """Run the web GUI."""
    gui = create_web_gui()
    gui.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_gui()