"""
Template loader for built-in test templates.
"""

from jinja2 import BaseLoader


class TemplateLoader(BaseLoader):
    """Custom template loader for built-in templates."""
    
    def __init__(self):
        self.templates = {
            'test_function': '''def test_{{ function.name }}({% for param in function.parameters %}{{ param[0] }}{% if not loop.last %}, {% endif %}{% endfor %}):
    """Test {{ function.name }} function."""
    # Arrange
    {% for param in function.parameters %}
    {{ param[0] }} = {{ param[1] or 'None' }}  # TODO: Set appropriate value
    {% endfor %}
    
    # Act
    result = {{ function.name }}({% for param in function.parameters %}{{ param[0] }}{% if not loop.last %}, {% endif %}{% endfor %})
    
    # Assert
    {% if function.return_annotation %}
    assert isinstance(result, {{ function.return_annotation }})
    {% else %}
    assert result is not None
    {% endif %}
''',
            'test_class': '''class {{ class_name }}:
    """Test class for {{ class_name }}."""
    
    {% for method in methods %}
    def test_{{ method.name }}(self{% for param in method.parameters %}, {{ param[0] }}{% endfor %}):
        """Test {{ method.name }} method."""
        # Arrange
        {% for param in method.parameters %}
        {{ param[0] }} = {{ param[1] or 'None' }}  # TODO: Set appropriate value
        {% endfor %}
        
        # Act
        result = self.instance.{{ method.name }}({% for param in method.parameters %}{{ param[0] }}{% if not loop.last %}, {% endif %}{% endfor %})
        
        # Assert
        {% if method.return_annotation %}
        assert isinstance(result, {{ method.return_annotation }})
        {% else %}
        assert result is not None
        {% endif %}
    {% endfor %}
''',
            'test_api_endpoint': '''def test_{{ endpoint.name }}({{ endpoint.method.lower() }}_client):
    """Test {{ endpoint.name }} endpoint."""
    # Arrange
    {% for param in endpoint.parameters %}
    {{ param[0] }} = {{ param[1] or 'None' }}  # TODO: Set appropriate value
    {% endfor %}
    
    # Act
    response = {{ endpoint.method.lower() }}_client.{{ endpoint.path }}(
        {% for param in endpoint.parameters %}{{ param[0] }}={{ param[0] }}{% if not loop.last %}, {% endif %}{% endfor %}
    )
    
    # Assert
    assert response.status_code == 200
    {% if endpoint.return_type %}
    assert response.json() is not None
    {% endif %}
''',
            'fixture': '''@pytest.fixture(scope="{{ fixture.scope }}", autouse={{ fixture.autouse }})
def {{ fixture.name }}():
    """{{ fixture.name }} fixture."""
    {% for line in fixture.setup_code %}
    {{ line }}
    {% endfor %}
''',
            'mock': '''@patch('{{ mock.patch_path }}')
def test_with_{{ mock.target.replace('.', '_') }}(self, {{ mock.mock_name }}):
    """Test with mocked {{ mock.target }}."""
    # Arrange
    {{ mock.mock_name }}.return_value = {{ mock.return_value or 'None' }}
    
    # Act
    result = function_under_test()
    
    # Assert
    {{ mock.mock_name }}.assert_called_once()
    assert result is not None
''',
            'parametrize': '''@pytest.mark.parametrize("{{ parametrize.parameter_name }}", [
    {% for case in parametrize.test_cases %}
    ({% for param_name, param_value in case.parameters.items() %}{{ param_value }}{% if not loop.last %}, {% endif %}{% endfor %}){% if not loop.last %},{% endif %}
    {% endfor %}
])
def test_{{ parametrize.parameter_name }}_parametrized({{ parametrize.parameter_name }}):
    """Test {{ parametrize.parameter_name }} with multiple values."""
    # Test implementation here
    assert {{ parametrize.parameter_name }} is not None
'''
        }
    
    def get_source(self, environment, name):
        if name in self.templates:
            return self.templates[name], name, lambda: True
        raise FileNotFoundError(f"Template '{name}' not found")
