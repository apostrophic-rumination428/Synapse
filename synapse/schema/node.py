"""Node schema for Synapse AKG."""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
import re
import uuid


class SynapseNode(BaseModel):
    """Polymorphic node schema for AKG."""
    
    id: str = Field(..., pattern=r"^node:[a-z_]+:[a-f0-9-]{36}$")
    domain: str = Field(..., description="TAG indexable domain")
    type: Literal["entity", "observation", "relation", "chunk"]
    content: str = Field(..., description="Core payload")
    embedding: List[float] = Field(..., description="768-dim vector")
    links: Optional[Dict[str, List[str]]] = Field(default_factory=lambda: {"inbound": [], "outbound": []})
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    
    @field_validator('embedding')
    @classmethod
    def validate_embedding_dim(cls, v):
        """Validate embedding dimension."""
        if len(v) != 768:
            raise ValueError("Embedding must be 768 dimensions")
        return v
    
    @field_validator('id')
    @classmethod
    def validate_id_format(cls, v):
        """Validate node ID format."""
        pattern = r"^node:[a-z_]+:[a-f0-9-]{36}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid node ID format, expected: node:domain:uuid")
        return v
