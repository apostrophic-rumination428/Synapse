"""Tests for MCP Recall - Updated for FastMCP."""

from unittest.mock import Mock
import pytest


class TestMCPRecall:
    """Test MCPRecall handler."""

    def test_recall_pipeline(self):
        """Test recall pipeline with mocked Redis."""
        from synapse.mcp.recall import MCPRecall

        mock_redis = Mock()
        mock_redis.search_hybrid.return_value = [
            {"id": "node:test:123", "domain": "test", "type": "entity", "content": "test content"}
        ]
        mock_redis.get_linked_nodes.return_value = []

        mock_embeddings = Mock()
        mock_embeddings.embed.return_value = [0.1] * 384

        recall = MCPRecall(mock_redis, mock_embeddings)
        result = recall.handle_recall({
            "query": "test",
            "domain_filter": ["test"],
            "type_filter": ["entity"],
            "limit": 10
        })

        assert "results" in result
        assert "total" in result
        assert result["total"] >= 0

    def test_recall_returns_error_on_exception(self):
        """Test recall returns error dict on exception."""
        from synapse.mcp.recall import MCPRecall

        mock_redis = Mock()
        mock_redis.search_hybrid.side_effect = Exception("Redis error")
        mock_embeddings = Mock()

        recall = MCPRecall(mock_redis, mock_embeddings)
        result = recall.handle_recall({"query": "test"})

        assert "format" in result
        assert result["format"] == "error"
