"""
Helper functions for AI CLI commands.
"""

import click
import sys
import os
import glob
from typing import Dict, Any, Optional
from .ai_assistant import AIAssistant


class AICommandHelpers:
    """Helper functions for AI CLI commands."""
    
    @staticmethod
    def initialize_assistant() -> tuple[AIAssistant, Dict[str, Any]]:
        """Initialize AI assistant and return assistant and result."""
        assistant = AIAssistant()
        init_result = assistant.initialize()
        return assistant, init_result
    
    @staticmethod
    def check_initialization(init_result: Dict[str, Any]) -> bool:
        """Check if initialization was successful."""
        if not init_result["success"]:
            click.echo("❌ AI Assistant initialization failed:")
            for error in init_result.get("errors", []):
                click.echo(f"  • {error}")
            return False
        return True
    
    @staticmethod
    def prepare_context(file: Optional[str]) -> Dict[str, Any]:
        """Prepare context data from file if provided."""
        context = {}
        if file:
            try:
                with open(file, 'r') as f:
                    context["file_content"] = f.read()
                    context["file_path"] = file
            except Exception as e:
                click.echo(f"⚠️  Warning: Could not read file {file}: {e}")
        return context
    
    @staticmethod
    def display_response(response: Dict[str, Any], verbose: bool, command_type: str = "response"):
        """Display AI response with appropriate formatting."""
        if response["success"]:
            click.echo(f"\n💬 AI {command_type.title()}:")
            click.echo("=" * 50)
            click.echo(response["response"])
            
            if verbose and response.get("tokens_used", 0) > 0:
                click.echo(f"\n📊 Tokens used: {response['tokens_used']}")
        else:
            click.echo(f"❌ Error: {response['error']}")
            sys.exit(1)
    
    @staticmethod
    def find_test_files(directory: str) -> list[str]:
        """Find test files in a directory."""
        test_files = []
        if os.path.isdir(directory):
            test_files = glob.glob(os.path.join(directory, "test_*.py"))
            test_files.extend(glob.glob(os.path.join(directory, "*_test.py")))
        elif os.path.isfile(directory):
            test_files = [directory]
        return test_files
    
    @staticmethod
    def read_file_content(file_path: str) -> str:
        """Read file content safely."""
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Failed to read file {file_path}: {e}")
    
    @staticmethod
    def validate_file_exists(file_path: str, file_type: str = "file") -> bool:
        """Validate that a file exists."""
        if not os.path.exists(file_path):
            click.echo(f"❌ {file_type.title()} not found: {file_path}")
            return False
        return True
    
    @staticmethod
    def format_verbose_info(init_result: Dict[str, Any], file: Optional[str] = None):
        """Format verbose information for display."""
        click.echo(f"🤖 Using {init_result['provider']} ({init_result['model']})")
        if file:
            click.echo(f"📁 Using file context: {file}")
    
    @staticmethod
    def handle_interactive_mode(assistant: AIAssistant):
        """Handle interactive mode for AI assistant."""
        click.echo("🤖 AI Testing Assistant")
        click.echo("=" * 30)
        click.echo("Type 'quit' or 'exit' to end the session.")
        click.echo("Ask me anything about testing, mocking, or test generation!\n")
        
        while True:
            try:
                question = click.prompt("You", type=str)
                
                if question.lower() in ['quit', 'exit', 'q']:
                    click.echo("👋 Goodbye!")
                    break
                
                if not question.strip():
                    continue
                
                response = assistant.ask(question)
                
                if response["success"]:
                    click.echo(f"\n🤖 AI: {response['response']}\n")
                else:
                    click.echo(f"\n❌ Error: {response['error']}\n")
                    
            except (KeyboardInterrupt, EOFError):
                click.echo("\n👋 Goodbye!")
                break
            except Exception as e:
                click.echo(f"\n❌ Error: {e}\n")
    
    @staticmethod
    def display_ai_status():
        """Display AI assistant status information."""
        from .ai_config import AIConfigManager
        
        config_manager = AIConfigManager()
        config = config_manager.get_config()
        validation = config_manager.validate_config()
        
        click.echo("🤖 AI Assistant Status")
        click.echo("=" * 25)
        
        click.echo(f"Enabled: {'✅' if config.enabled else '❌'}")
        click.echo(f"Provider: {config.provider.value}")
        click.echo(f"Model: {config.model}")
        click.echo(f"API Key: {'✅ Set' if config.api_key else '❌ Not set'}")
        
        if validation["valid"]:
            click.echo("Configuration: ✅ Valid")
        else:
            click.echo("Configuration: ❌ Invalid")
            for error in validation["errors"]:
                click.echo(f"  • {error}")
        
        if validation["warnings"]:
            click.echo("\n⚠️  Warnings:")
            for warning in validation["warnings"]:
                click.echo(f"  • {warning}")
        
        if config.provider.value == "openai":
            click.echo("\n💡 To set up OpenAI:")
            click.echo("export OPENAI_API_KEY='your-api-key-here'")
        elif config.provider.value == "anthropic":
            click.echo("\n💡 To set up Anthropic:")
            click.echo("export ANTHROPIC_API_KEY='your-api-key-here'")
