"""
CLI commands for AI assistant functionality.
"""

import click
import sys
from typing import Optional
from .ai_assistant import AIAssistant
from .ai_config import AIConfigManager
from .ai_command_helpers import AICommandHelpers


@click.command()
@click.argument('question', required=True)
@click.option('--file', '-f', help='File to provide as context for the question')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed response information')
def ask_command(question: str, file: Optional[str], verbose: bool):
    """Ask the AI assistant a question about testing."""
    try:
        assistant, init_result = AICommandHelpers.initialize_assistant()
        
        if not AICommandHelpers.check_initialization(init_result):
            sys.exit(1)
        
        if verbose:
            AICommandHelpers.format_verbose_info(init_result, file)
        
        # Prepare context
        context = AICommandHelpers.prepare_context(file)
        
        # Ask question
        click.echo("🤔 Asking AI assistant...")
        response = assistant.ask(question, context)
        
        AICommandHelpers.display_response(response, verbose)
            
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@click.command()
@click.argument('test_file', required=True)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed explanation')
def explain_command(test_file: str, verbose: bool):
    """Explain what tests will be generated or what existing tests do."""
    try:
        assistant, init_result = AICommandHelpers.initialize_assistant()
        
        if not AICommandHelpers.check_initialization(init_result):
            sys.exit(1)
        
        # Check if file exists
        if not AICommandHelpers.validate_file_exists(test_file):
            sys.exit(1)
        
        click.echo(f"🔍 Explaining tests in: {test_file}")
        
        # Get explanation
        response = assistant.explain_generation([test_file])
        
        AICommandHelpers.display_response(response, verbose, "explanation")
            
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@click.command()
@click.argument('source_file', required=True)
@click.option('--tests', '-t', help='Existing test file to compare against')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed suggestions')
def suggest_command(source_file: str, tests: Optional[str], verbose: bool):
    """Suggest test improvements or new tests for source code."""
    try:
        assistant, init_result = AICommandHelpers.initialize_assistant()
        
        if not AICommandHelpers.check_initialization(init_result):
            sys.exit(1)
        
        # Check if source file exists
        if not AICommandHelpers.validate_file_exists(source_file, "source file"):
            sys.exit(1)
        
        click.echo(f"💡 Analyzing: {source_file}")
        
        # Analyze source code
        analysis_response = assistant.analyze_code(source_file)
        
        if not analysis_response["success"]:
            click.echo(f"❌ Analysis failed: {analysis_response['error']}")
            sys.exit(1)
        
        # Prepare context for suggestions
        context = {
            "source_code": analysis_response["analysis"],
            "existing_tests": ""
        }
        
        if tests and AICommandHelpers.validate_file_exists(tests, "test file"):
            try:
                context["existing_tests"] = AICommandHelpers.read_file_content(tests)
                if verbose:
                    click.echo(f"📁 Comparing with existing tests: {tests}")
            except Exception as e:
                click.echo(f"⚠️  Warning: Could not read test file {tests}: {e}")
        
        # Get suggestions
        response = assistant.suggest_tests(context)
        
        AICommandHelpers.display_response(response, verbose, "suggestions")
            
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@click.command()
@click.argument('test_directory', default='tests/')
@click.option('--detailed', '-d', is_flag=True, help='Show detailed review')
@click.option('--verbose', '-v', is_flag=True, help='Show token usage')
def review_command(test_directory: str, detailed: bool, verbose: bool):
    """Review all tests in a directory and provide feedback."""
    try:
        assistant, init_result = AICommandHelpers.initialize_assistant()
        
        if not AICommandHelpers.check_initialization(init_result):
            sys.exit(1)
        
        # Find test files
        test_files = AICommandHelpers.find_test_files(test_directory)
        
        if not test_files:
            click.echo(f"❌ No test files found in: {test_directory}")
            sys.exit(1)
        
        click.echo(f"📋 Reviewing {len(test_files)} test files...")
        
        # Get review
        response = assistant.explain_generation(test_files)
        
        AICommandHelpers.display_response(response, verbose, "review")
            
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@click.command()
@click.option('--interactive', '-i', is_flag=True, help='Start interactive mode')
def assistant_command(interactive: bool):
    """Launch AI assistant in interactive mode."""
    try:
        assistant, init_result = AICommandHelpers.initialize_assistant()
        
        if not AICommandHelpers.check_initialization(init_result):
            sys.exit(1)
        
        if interactive:
            AICommandHelpers.handle_interactive_mode(assistant)
        else:
            click.echo("Use --interactive flag to start interactive mode.")
            
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@click.command()
def ai_status_command():
    """Check AI assistant configuration and status."""
    try:
        AICommandHelpers.display_ai_status()
            
    except Exception as e:
        click.echo(f"❌ Error checking status: {e}")
        sys.exit(1)