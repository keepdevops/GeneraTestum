"""
AI-related CLI commands.
"""

import click
import sys
from .ai_commands import (
    ask_command, explain_command, suggest_command, review_command, 
    assistant_command, ai_status_command
)
from .ai_enhanced_assistant import EnhancedAIAssistant


@click.command()
@click.argument('question', required=True)
@click.option('--file', '-f', help='File to provide as context for the question')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed response information')
@click.option('--enhanced', '-e', is_flag=True, help='Use enhanced AI assistant with NLP analysis')
def ask(question, file, verbose, enhanced):
    """Ask the AI assistant a question about testing."""
    if enhanced:
        # Use enhanced AI assistant
        try:
            assistant = EnhancedAIAssistant()
            init_result = assistant.initialize()
            
            if not init_result.get("success", False):
                click.echo(f"❌ AI initialization failed: {init_result.get('errors', ['Unknown error'])}")
                sys.exit(1)
            
            # Prepare context
            context = {}
            if file:
                try:
                    with open(file, 'r') as f:
                        context["current_code"] = f.read()
                except Exception as e:
                    click.echo(f"⚠️  Warning: Could not read file {file}: {e}")
            
            # Ask with enhanced capabilities
            click.echo("🤖 Enhanced AI Assistant analyzing...")
            response = assistant.enhanced_ask(question, context)
            
            if response.get("success", False):
                click.echo("✅ Enhanced Response:")
                click.echo(f"📝 {response['response']}")
                
                if verbose and "query_analysis" in response:
                    analysis = response["query_analysis"]
                    click.echo(f"\n🔍 Query Analysis:")
                    click.echo(f"  Type: {analysis['type']}")
                    click.echo(f"  Confidence: {analysis['confidence']:.2f}")
                    click.echo(f"  Intent: {analysis['intent']}")
                    if analysis.get('keywords'):
                        click.echo(f"  Keywords: {', '.join(analysis['keywords'])}")
                    if analysis.get('suggested_actions'):
                        click.echo(f"  Suggested Actions: {', '.join(analysis['suggested_actions'])}")
                
                if verbose and response.get("tokens_used"):
                    click.echo(f"\n📊 Tokens Used: {response['tokens_used']}")
            else:
                click.echo(f"❌ Error: {response.get('error', 'Unknown error')}")
                sys.exit(1)
                
        except Exception as e:
            click.echo(f"❌ Enhanced AI error: {e}")
            sys.exit(1)
    else:
        # Use standard AI assistant
        ask_command(question, file, verbose)


@click.command()
@click.argument('test_file', required=True)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed explanation')
def explain(test_file, verbose):
    """Explain what tests will be generated or what existing tests do."""
    explain_command(test_file, verbose)


@click.command()
@click.argument('source_file', required=True)
@click.option('--tests', '-t', help='Existing test file to compare against')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed suggestions')
def suggest(source_file, tests, verbose):
    """Suggest test improvements or new tests for source code."""
    suggest_command(source_file, tests, verbose)


@click.command()
@click.argument('test_directory', default='tests/')
@click.option('--detailed', '-d', is_flag=True, help='Show detailed review')
@click.option('--verbose', '-v', is_flag=True, help='Show token usage')
def review(test_directory, detailed, verbose):
    """Review all tests in a directory and provide feedback."""
    review_command(test_directory, detailed, verbose)


@click.command()
@click.option('--interactive', '-i', is_flag=True, help='Start interactive mode')
def assistant(interactive):
    """Launch AI assistant in interactive mode."""
    assistant_command(interactive)


@click.command()
def ai_status():
    """Check AI assistant configuration and status."""
    ai_status_command()


@click.command()
@click.argument('question', required=True)
@click.option('--file', '-f', help='Source file to analyze for suggestions')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed suggestions')
def smart_suggest(question, file, verbose):
    """Get intelligent test suggestions based on code analysis and NLP."""
    try:
        assistant = EnhancedAIAssistant()
        init_result = assistant.initialize()
        
        if not init_result.get("success", False):
            click.echo(f"❌ AI initialization failed: {init_result.get('errors', ['Unknown error'])}")
            sys.exit(1)
        
        # Prepare context
        context = {}
        if file:
            try:
                with open(file, 'r') as f:
                    context["current_code"] = f.read()
            except Exception as e:
                click.echo(f"⚠️  Warning: Could not read file {file}: {e}")
        
        click.echo("🧠 Smart Suggestions Engine analyzing...")
        response = assistant.get_smart_suggestions(question, file, context)
        
        if response.get("success", False):
            click.echo("✅ Smart Suggestions Generated:")
            
            if verbose:
                analysis = response.get("query_analysis", {})
                click.echo(f"\n🔍 Query Analysis:")
                click.echo(f"  Type: {analysis.get('type', 'Unknown')}")
                click.echo(f"  Confidence: {analysis.get('confidence', 0):.2f}")
                click.echo(f"  Intent: {analysis.get('intent', 'Unknown')}")
            
            patterns = response.get("patterns_detected", 0)
            if patterns > 0:
                click.echo(f"\n🎯 Patterns Detected: {patterns}")
            
            recommendations = response.get("recommendations", [])
            if recommendations:
                click.echo(f"\n💡 Recommendations ({len(recommendations)}):")
                for i, rec in enumerate(recommendations, 1):
                    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec["priority"], "⚪")
                    click.echo(f"  {i}. {priority_icon} [{rec['category']}] {rec['title']}")
                    click.echo(f"     {rec['description']}")
                    if verbose and rec.get("examples"):
                        click.echo(f"     Examples: {', '.join(rec['examples'])}")
                    click.echo()
            else:
                click.echo("\n💡 No specific recommendations generated.")
        else:
            click.echo(f"❌ Error: {response.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Smart suggestions error: {e}")
        sys.exit(1)
