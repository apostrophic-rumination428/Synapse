"""Graph Resolution Engine - 1-degree traversal."""

from typing import Any, Dict, List, Set


class GraphResolver:
    """Graph resolver for 1-degree node traversal."""

    def __init__(self, redis_client: Any) -> None:
        """Initialize with Redis client."""
        self.redis = redis_client

    def resolve_1_degree(self, node_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Resolve 1-degree graph traversal from a node."""
        # Get the source node
        source_node = self.redis.get_node(node_id)
        if not source_node:
            return {"nodes": [], "edges": []}

        # Collect all nodes and edges
        nodes = [source_node]
        edges = []

        # Get all linked node IDs (remove duplicates)
        linked_ids = self._get_unique_linked_ids(source_node)

        if not linked_ids:
            return {"nodes": nodes, "edges": []}

        # Get linked nodes
        linked_nodes = self.redis.get_linked_nodes(node_id, depth=1)

        # Add linked nodes to result
        for linked_node in linked_nodes:
            if linked_node and linked_node.get("id") in linked_ids:
                nodes.append(linked_node)

        # Create edges based on link directions
        self._create_edges(source_node, linked_ids, edges)

        return {"nodes": nodes, "edges": edges}

    def _get_unique_linked_ids(self, node: Dict[str, Any]) -> Set[str]:
        """Get unique set of linked node IDs."""
        links = node.get("links", {})
        inbound = set(links.get("inbound", []))
        outbound = set(links.get("outbound", []))

        return inbound.union(outbound)

    def _create_edges(
        self,
        source_node: Dict[str, Any],
        linked_ids: Set[str],
        edges: List[Dict[str, str]],
    ) -> None:
        """Create edges based on link directions."""
        source_id = source_node["id"]
        links = source_node.get("links", {})

        # Track created edges to avoid duplicates
        seen_edges = set()

        # Create inbound edges (other -> source)
        for inbound_id in links.get("inbound", []):
            if inbound_id in linked_ids:
                edge_key = (inbound_id, source_id, "linked")
                if edge_key not in seen_edges:
                    edges.append(
                        {
                            "source": inbound_id,
                            "target": source_id,
                            "relation_type": "linked",
                        }
                    )
                    seen_edges.add(edge_key)

        # Create outbound edges (source -> other)
        for outbound_id in links.get("outbound", []):
            if outbound_id in linked_ids:
                edge_key = (source_id, outbound_id, "linked")
                if edge_key not in seen_edges:
                    edges.append(
                        {
                            "source": source_id,
                            "target": outbound_id,
                            "relation_type": "linked",
                        }
                    )
                    seen_edges.add(edge_key)
