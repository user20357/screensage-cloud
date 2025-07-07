#!/usr/bin/env python3
"""
ScreenSage Architect - Cloud Backend API
FastAPI server for AI-powered screen analysis and task management
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import base64
import io
import json
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our AI processing modules (adapted from desktop app)
from ai_processor import CloudAIProcessor
from ocr_processor import CloudOCRProcessor
from task_manager import CloudTaskManager
from models import TaskRequest, AnalysisResult, TaskResponse

app = FastAPI(
    title="ScreenSage Architect API",
    description="AI-powered screen analysis and automation API",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
ai_processor = CloudAIProcessor()
ocr_processor = CloudOCRProcessor()
task_manager = CloudTaskManager()

# WebSocket connection manager for real-time features
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Screenshot analysis endpoint
@app.post("/analyze-screenshot", response_model=AnalysisResult)
async def analyze_screenshot(file: UploadFile = File(...)):
    """
    Analyze uploaded screenshot using OCR and AI
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        
        # Process with OCR
        ocr_result = await ocr_processor.process_image(image_data)
        
        # Process with AI
        ai_result = await ai_processor.analyze_screen(image_data, ocr_result)
        
        # Combine results
        analysis_result = AnalysisResult(
            ocr_text=ocr_result.get("text", ""),
            detected_elements=ocr_result.get("elements", []),
            ai_analysis=ai_result.get("analysis", ""),
            suggested_actions=ai_result.get("actions", []),
            confidence_score=ai_result.get("confidence", 0.0),
            processing_time=ai_result.get("processing_time", 0.0)
        )
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error analyzing screenshot: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Task management endpoints
@app.post("/create-task", response_model=TaskResponse)
async def create_task(task_request: TaskRequest):
    """
    Create a new automation task
    """
    try:
        task = await task_manager.create_task(task_request)
        return task
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task creation failed: {str(e)}")

@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks():
    """
    Get all tasks
    """
    try:
        tasks = await task_manager.get_all_tasks()
        return tasks
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task retrieval failed: {str(e)}")

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """
    Get specific task by ID
    """
    try:
        task = await task_manager.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        logger.error(f"Error retrieving task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task retrieval failed: {str(e)}")

@app.put("/tasks/{task_id}/execute")
async def execute_task(task_id: str):
    """
    Execute a task (placeholder for automation)
    """
    try:
        result = await task_manager.execute_task(task_id)
        return {"status": "executed", "result": result}
    except Exception as e:
        logger.error(f"Error executing task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")

# Real-time WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time communication
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "screen_capture":
                # Process real-time screen capture
                result = await process_realtime_capture(message.get("data"))
                await manager.send_personal_message(
                    json.dumps({"type": "analysis_result", "data": result}),
                    websocket
                )
            elif message.get("type") == "task_update":
                # Broadcast task updates
                await manager.broadcast(json.dumps(message))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)

async def process_realtime_capture(capture_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process real-time screen capture data
    """
    try:
        # Convert base64 image to bytes
        image_data = base64.b64decode(capture_data.get("image", ""))
        
        # Quick OCR processing (optimized for speed)
        ocr_result = await ocr_processor.process_image_fast(image_data)
        
        # Quick AI analysis (basic detection)
        ai_result = await ai_processor.analyze_screen_fast(image_data, ocr_result)
        
        return {
            "elements": ocr_result.get("elements", []),
            "text": ocr_result.get("text", ""),
            "suggestions": ai_result.get("actions", []),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing real-time capture: {str(e)}")
        return {"error": str(e)}

# Static files for frontend (in production, served by CDN)
# app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    )