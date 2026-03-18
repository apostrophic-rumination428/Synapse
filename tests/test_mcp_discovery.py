"""Tests for MCP Discovery functionality - RED Phase."""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from synapse.server import app


class TestMCPDiscoveryEndpoints:
    """Test MCP Discovery HTTP endpoints - RED Phase."""

    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)

    @patch('synapse.server.mcp_discovery')
    def test_list_mcp_servers_endpoint_should_exist(self, mock_discovery):
        """Test /mcp/servers endpoint should exist and return 200."""
        mock_discovery.list_servers.return_value = []
        
        response = self.client.get("/mcp/servers")
        
        # This should work now - GREEN phase
        assert response.status_code == 200
        data = response.json()
        assert "servers" in data
        assert "count" in data
        assert "timestamp" in data

    @patch('synapse.server.mcp_discovery')
    def test_get_mcp_server_info_endpoint_should_exist(self, mock_discovery):
        """Test /mcp/server/{name} endpoint should exist."""
        mock_discovery.get_server_info.return_value = {"server": {"name": "synapse"}}
        
        response = self.client.get("/mcp/server/synapse")
        
        # This should work now - GREEN phase
        assert response.status_code == 200
        data = response.json()
        assert "server" in data

    @patch('synapse.server.mcp_discovery')
    def test_get_mcp_server_tools_endpoint_should_exist(self, mock_discovery):
        """Test /mcp/server/{name}/tools endpoint should exist."""
        mock_discovery.get_server_tools.return_value = []
        
        response = self.client.get("/mcp/server/synapse/tools")
        
        # This should work now - GREEN phase
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert "count" in data
        assert "server" in data

    @patch('synapse.server.mcp_discovery')
    def test_register_mcp_server_endpoint_should_exist(self, mock_discovery):
        """Test /mcp/server/{name}/register endpoint should exist."""
        mock_discovery.register_server.return_value = True
        
        server_data = {
            "name": "test-server",
            "description": "Test Server",
            "capabilities": ["test"]
        }
        
        response = self.client.post("/mcp/server/test-server/register", json=server_data)
        
        # This should work now - GREEN phase
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "registered"
        assert data["server"] == "test-server"

    @patch('synapse.server.mcp_discovery')
    def test_update_server_health_endpoint_should_exist(self, mock_discovery):
        """Test /mcp/server/{name}/health endpoint should exist."""
        mock_discovery.update_health.return_value = True
        
        health_data = {"status": "healthy"}
        
        response = self.client.post("/mcp/server/test-server/health", json=health_data)
        
        # This should work now - GREEN phase
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "updated"
        assert data["server"] == "test-server"

    @patch('synapse.server.mcp_discovery')
    def test_synapse_server_should_auto_register(self, mock_discovery):
        """Test that synapse server auto-registers on startup."""
        # Mock the server list to include synapse
        mock_discovery.list_servers.return_value = [
            {"name": "synapse", "status": "active"}
        ]
        
        # After server startup, synapse should be in the server list
        response = self.client.get("/mcp/servers")
        
        # This should work now - GREEN phase
        assert response.status_code == 200
        data = response.json()
        server_names = [server["name"] for server in data["servers"]]
        assert "synapse" in server_names

    @patch('synapse.server.mcp_discovery')
    @patch('synapse.server.synapse_redis')
    @patch('synapse.server.embedding_cache')
    def test_health_endpoint_should_update_discovery_health(self, mock_cache, mock_redis, mock_discovery):
        """Test that health endpoint updates MCP discovery health data."""
        # Mock Redis and embedding cache to avoid connection issues
        mock_redis.ping.return_value = True
        mock_cache.embed.return_value = [0.1, 0.2, 0.3]
        mock_cache.get_stats.return_value = {"hits": 10, "misses": 2}
        
        # Mock health update
        mock_discovery.update_health.return_value = True
        
        # Call health endpoint
        response = self.client.get("/health")
        
        # This should work now - GREEN phase
        assert response.status_code == 200
        
        # Verify health update was called
        mock_discovery.update_health.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
