"""Tests for MCP Patch - Updated for FastMCP."""

from unittest.mock import Mock
import pytest


class TestMCPPatch:
    """Test MCPPatch handler."""

    def test_patch_pipeline(self):
        """Test patch pipeline with mocked Redis."""
        from synapse.mcp.patch import MCPPatch

        mock_redis = Mock()
        mock_redis.get_node.return_value = {"id": "node:test:123", "content": "test"}
        mock_redis.update_node.return_value = True

        patch = MCPPatch(mock_redis)
        result = patch.handle_patch({
            "node_id": "node:test:123",
            "operations": [{"op": "set", "path": "$.metadata.foo", "value": "bar"}]
        })

        assert result["status"] == "success"
        assert result["updated"] is True
        assert result["node_id"] == "node:test:123"

    def test_patch_atomic_operations(self):
        """Test patch applies operations atomically."""
        from synapse.mcp.patch import MCPPatch

        mock_redis = Mock()
        mock_redis.get_node.return_value = {"id": "node:test:123"}
        mock_redis.update_node.return_value = True

        patch = MCPPatch(mock_redis)
        result = patch.handle_patch({
            "node_id": "node:test:123",
            "operations": [
                {"op": "set", "path": "$.field1", "value": "value1"},
                {"op": "append", "path": "$.list", "value": "item1"}
            ]
        })

        assert result["status"] == "success"

    def test_patch_node_not_found(self):
        """Test patch returns error when node not found."""
        from synapse.mcp.patch import MCPPatch

        mock_redis = Mock()
        mock_redis.get_node.return_value = None

        patch = MCPPatch(mock_redis)
        result = patch.handle_patch({
            "node_id": "node:test:nonexistent",
            "operations": [{"op": "set", "path": "$.field", "value": "value"}]
        })

        assert result["status"] == "error"
        assert "not found" in result["error"].lower()

    def test_patch_missing_node_id_returns_error(self):
        """Test patch returns error for missing node_id."""
        from synapse.mcp.patch import MCPPatch

        mock_redis = Mock()
        patch = MCPPatch(mock_redis)
        result = patch.handle_patch({"operations": []})

        assert result["status"] == "error"
        assert "node_id" in result["error"].lower()

    def test_patch_missing_operations_returns_error(self):
        """Test patch returns error for missing operations."""
        from synapse.mcp.patch import MCPPatch

        mock_redis = Mock()
        patch = MCPPatch(mock_redis)
        result = patch.handle_patch({"node_id": "node:test:123"})

        assert result["status"] == "error"
        assert "operations" in result["error"].lower()
