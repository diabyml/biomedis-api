#!/usr/bin/env python3
"""
Simple start script for Render.com deployment
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Lab Equipment Company on {host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        workers=1,  # Start with 1 worker for free tier
        log_level="info"
    )