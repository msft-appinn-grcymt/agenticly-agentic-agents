#!/usr/bin/env python3
"""
Development server startup script for MS Roles API
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting MS Roles API development server...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("Health check available at: http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
