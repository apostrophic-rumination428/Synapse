"""MCP Patch Handler - Atomic Node Mutation."""

from typing import Any, Dict, List

from .base import MCPBase


class MCPPatch(MCPBase):
    """MCP handler for patch state operations."""

    def __init__(self, redis_client: Any) -> None:
        """Initialize with Redis client."""
        super().__init__()
        self.redis = redis_client

        # Register patch method
        self.register("patch_state")(self.handle_patch)

    def handle_patch(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle patch request: validate → check existence → atomic update."""
        try:
            # Validate required fields
            self._validate_params(params)

            # Extract parameters
            node_id = params["node_id"]
            operations = params["operations"]

            # Validate operations
            self._validate_operations(operations)

            # Check if node exists
            node = self.redis.get_node(node_id)
            if not node:
                return {"status": "error", "error": f"Node {node_id} not found"}

            # Convert operations to Redis format
            redis_operations = []
            updated_fields = []

            for op in operations:
                redis_op = {
                    "path": op["path"],
                    "op": op["op"],
                    "value": op.get("value"),
                }
                redis_operations.append(redis_op)
                updated_fields.append(op["path"])

            # Apply atomic operations
            success = self.redis.update_node(node_id, redis_operations)

            if success:
                return {"status": "success", "updated_fields": updated_fields}
            else:
                return {"status": "error", "error": "Failed to apply operations"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _validate_params(self, params: Dict[str, Any]) -> None:
        """Validate patch request parameters."""
        if "node_id" not in params:
            raise ValueError("Missing required field: node_id")

        if "operations" not in params:
            raise ValueError("Missing required field: operations")

        node_id = params["node_id"]
        if not node_id or not isinstance(node_id, str):
            raise ValueError("Node ID must be a non-empty string")

        operations = params["operations"]
        if not isinstance(operations, list) or len(operations) == 0:
            raise ValueError("Operations must be a non-empty list")

    def _validate_operations(self, operations: List[Dict[str, Any]]) -> None:
        """Validate individual operations."""
        valid_ops = ["set", "delete", "append"]

        for i, op in enumerate(operations):
            if not isinstance(op, dict):
                raise ValueError(f"Operation {i} must be a dictionary")

            if "path" not in op:
                raise ValueError(f"Operation {i} missing required field: path")

            if "op" not in op:
                raise ValueError(f"Operation {i} missing required field: op")

            if op["op"] not in valid_ops:
                raise ValueError(
                    f"Operation {i} has invalid op: {op['op']}. Must be one of: {valid_ops}"
                )

            # Validate value requirement
            if op["op"] in ["set", "append"] and "value" not in op:
                raise ValueError(
                    f"Operation {i} with op='{op['op']}' requires value field"
                )
