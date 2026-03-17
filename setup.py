"""Setup script for Synapse AKG."""

from setuptools import setup, find_packages

setup(
    name="synapse",
    version="0.1.0",
    description="Agentic Knowledge Graph with Hybrid Search",
    author="di5rupt0r",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.100.0",
        "redis>=4.5.0",
        "redisearch>=2.0.0",
        "sentence-transformers>=2.2.0",
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "pydantic>=2.0.0",
        "uvicorn>=0.20.0",
        "python-multipart>=0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-benchmark>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "ruff>=0.1.0",
            "bandit>=1.7.0",
            "safety>=2.3.0",
        ]
    },
)
