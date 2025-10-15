"""
API relationship analysis between endpoints.
"""

from typing import Dict, List, Optional
from .integration_test_models import APIRelationship, APIEndpoint
from .api_pattern_detector import APIPatternDetector


class RelationshipAnalyzer:
    """Analyzes relationships between API endpoints."""

    def __init__(self):
        self.pattern_detector = APIPatternDetector()

    def analyze_relationships(self, endpoints: List[APIEndpoint]) -> List[APIRelationship]:
        """Analyze relationships between endpoints."""
        relationships = []
        
        # Group endpoints by base path
        endpoint_groups = self._group_endpoints_by_path(endpoints)
        
        # Analyze relationships within each group
        for group_endpoints in endpoint_groups.values():
            group_relationships = self._analyze_group_relationships(group_endpoints)
            relationships.extend(group_relationships)
        
        # Analyze cross-group relationships
        cross_relationships = self._analyze_cross_group_relationships(endpoint_groups)
        relationships.extend(cross_relationships)
        
        return relationships

    def _group_endpoints_by_path(self, endpoints: List[APIEndpoint]) -> Dict[str, List[APIEndpoint]]:
        """Group endpoints by base path."""
        endpoint_groups = {}
        for endpoint in endpoints:
            base_path = endpoint.path.split('/')[1] if '/' in endpoint.path else endpoint.path
            if base_path not in endpoint_groups:
                endpoint_groups[base_path] = []
            endpoint_groups[base_path].append(endpoint)
        return endpoint_groups

    def _analyze_group_relationships(self, endpoints: List[APIEndpoint]) -> List[APIRelationship]:
        """Analyze relationships within a group of endpoints."""
        relationships = []
        
        for i, source in enumerate(endpoints):
            for j, target in enumerate(endpoints):
                if i != j:
                    relationship = self._determine_relationship(source, target)
                    if relationship:
                        relationships.append(relationship)
        
        return relationships

    def _determine_relationship(self, source: APIEndpoint, target: APIEndpoint) -> Optional[APIRelationship]:
        """Determine relationship between two endpoints."""
        # Check for common relationship patterns
        relationship_type = self.pattern_detector.analyze_method_relationships(
            source.method, target.method
        )
        
        if relationship_type:
            return APIRelationship(
                source_endpoint=f"{source.method} {source.path}",
                target_endpoint=f"{target.method} {target.path}",
                relationship_type=relationship_type,
                data_flow=self._extract_data_flow(source, target),
                conditions=[]
            )
        
        return None

    def _extract_data_flow(self, source: APIEndpoint, target: APIEndpoint) -> Dict[str, str]:
        """Extract data flow between endpoints."""
        data_flow = {}
        
        # Map response fields to request parameters
        for response_field in source.response_fields:
            for param in target.parameters:
                if response_field.lower() in param.lower() or param.lower() in response_field.lower():
                    data_flow[response_field] = param
        
        return data_flow

    def _analyze_cross_group_relationships(self, endpoint_groups: Dict[str, List[APIEndpoint]]) -> List[APIRelationship]:
        """Analyze relationships between different endpoint groups."""
        relationships = []
        
        group_names = list(endpoint_groups.keys())
        for i, source_group in enumerate(group_names):
            for j, target_group in enumerate(group_names):
                if i != j:
                    source_endpoints = endpoint_groups[source_group]
                    target_endpoints = endpoint_groups[target_group]
                    
                    for source in source_endpoints:
                        for target in target_endpoints:
                            relationship = self._determine_relationship(source, target)
                            if relationship:
                                relationships.append(relationship)
        
        return relationships

    def find_dependency_chains(self, relationships: List[APIRelationship]) -> List[List[str]]:
        """Find dependency chains from relationships."""
        chains = []
        
        # Build dependency graph
        dependency_graph = {}
        for rel in relationships:
            if rel.relationship_type == 'dependency_chain':
                source = rel.source_endpoint
                target = rel.target_endpoint
                
                if source not in dependency_graph:
                    dependency_graph[source] = []
                dependency_graph[source].append(target)
        
        # Find chains
        for start_node in dependency_graph:
            chain = self._build_chain(start_node, dependency_graph, set())
            if len(chain) > 1:
                chains.append(chain)
        
        return chains

    def _build_chain(self, node: str, graph: Dict[str, List[str]], visited: set) -> List[str]:
        """Build dependency chain starting from a node."""
        if node in visited:
            return []
        
        visited.add(node)
        chain = [node]
        
        if node in graph:
            for next_node in graph[node]:
                sub_chain = self._build_chain(next_node, graph, visited.copy())
                if sub_chain:
                    chain.extend(sub_chain)
        
        return chain
