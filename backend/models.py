#!/usr/bin/env python3
"""
Data models for ScreenSage Architect Cloud API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ActionType(str, Enum):
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    WAIT = "wait"
    SCREENSHOT = "screenshot"
    CUSTOM = "custom"

class DetectedElement(BaseModel):
    """Represents a detected UI element"""
    text: str = Field(..., description="Text content of the element")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence")
    bbox: List[List[int]] = Field(..., description="Bounding box coordinates")
    center: List[int] = Field(..., description="Center point [x, y]")
    element_type: str = Field(default="text", description="Type of element")

class SuggestedAction(BaseModel):
    """Represents a suggested automation action"""
    action: ActionType = Field(..., description="Type of action")
    description: str = Field(..., description="Human-readable description")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    coordinates: Optional[List[int]] = Field(None, description="Target coordinates [x, y]")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Additional parameters")

class AnalysisResult(BaseModel):
    """Result of screenshot analysis"""
    ocr_text: str = Field(..., description="Extracted text from OCR")
    detected_elements: List[DetectedElement] = Field(..., description="Detected UI elements")
    ai_analysis: str = Field(..., description="AI analysis description")
    suggested_actions: List[SuggestedAction] = Field(..., description="Suggested actions")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class TaskStep(BaseModel):
    """Individual step in a task"""
    id: str = Field(..., description="Step ID")
    description: str = Field(..., description="Step description")
    action: ActionType = Field(..., description="Action type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Step parameters")
    expected_result: Optional[str] = Field(None, description="Expected result")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Step status")
    result: Optional[Dict[str, Any]] = Field(None, description="Step result")
    screenshot_before: Optional[str] = Field(None, description="Screenshot before step")
    screenshot_after: Optional[str] = Field(None, description="Screenshot after step")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")

class TaskRequest(BaseModel):
    """Request to create a new task"""
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    steps: List[TaskStep] = Field(..., description="Task steps")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout: int = Field(default=300, description="Task timeout in seconds")
    auto_execute: bool = Field(default=False, description="Auto-execute the task")
    tags: List[str] = Field(default_factory=list, description="Task tags")

class TaskResponse(BaseModel):
    """Response containing task information"""
    id: str = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    priority: TaskPriority = Field(..., description="Task priority")
    status: TaskStatus = Field(..., description="Task status")
    steps: List[TaskStep] = Field(..., description="Task steps")
    progress: float = Field(..., ge=0.0, le=1.0, description="Task progress (0-1)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    started_at: Optional[datetime] = Field(None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    execution_time: Optional[float] = Field(None, description="Total execution time")
    success_rate: float = Field(..., ge=0.0, le=1.0, description="Success rate of steps")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    tags: List[str] = Field(default_factory=list, description="Task tags")
    
    # Metadata
    total_steps: int = Field(..., description="Total number of steps")
    completed_steps: int = Field(..., description="Number of completed steps")
    failed_steps: int = Field(..., description="Number of failed steps")
    pending_steps: int = Field(..., description="Number of pending steps")

class ScreenCaptureRequest(BaseModel):
    """Request for screen capture analysis"""
    image_data: str = Field(..., description="Base64 encoded image data")
    analysis_type: str = Field(default="full", description="Type of analysis to perform")
    include_ocr: bool = Field(default=True, description="Include OCR processing")
    include_ai: bool = Field(default=True, description="Include AI analysis")
    max_elements: int = Field(default=50, description="Maximum elements to detect")

class ScreenCaptureResponse(BaseModel):
    """Response from screen capture analysis"""
    analysis_result: AnalysisResult = Field(..., description="Analysis results")
    suggested_tasks: List[Dict[str, Any]] = Field(..., description="Suggested task templates")
    processing_stats: Dict[str, Any] = Field(..., description="Processing statistics")

class UserPreferences(BaseModel):
    """User preferences for automation"""
    auto_execute_safe_tasks: bool = Field(default=False, description="Auto-execute safe tasks")
    confirmation_required: bool = Field(default=True, description="Require confirmation")
    max_execution_time: int = Field(default=300, description="Maximum execution time")
    preferred_ai_provider: str = Field(default="openai", description="Preferred AI provider")
    ocr_engine: str = Field(default="auto", description="Preferred OCR engine")
    screenshot_quality: str = Field(default="medium", description="Screenshot quality")
    logging_level: str = Field(default="info", description="Logging level")

class SystemStatus(BaseModel):
    """System status information"""
    status: str = Field(..., description="System status")
    uptime: float = Field(..., description="System uptime in seconds")
    active_tasks: int = Field(..., description="Number of active tasks")
    total_tasks: int = Field(..., description="Total tasks processed")
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    disk_usage: float = Field(..., description="Disk usage percentage")
    api_version: str = Field(..., description="API version")
    last_updated: datetime = Field(..., description="Last update timestamp")

class WebSocketMessage(BaseModel):
    """WebSocket message structure"""
    type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    client_id: Optional[str] = Field(None, description="Client ID")
    session_id: Optional[str] = Field(None, description="Session ID")

class ErrorResponse(BaseModel):
    """Error response structure"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request ID")

# Configuration models
class AIConfig(BaseModel):
    """AI configuration"""
    provider: str = Field(default="openai", description="AI provider")
    model: str = Field(default="gpt-4-vision-preview", description="AI model")
    api_key: Optional[str] = Field(None, description="API key")
    max_tokens: int = Field(default=500, description="Maximum tokens")
    temperature: float = Field(default=0.1, description="Temperature setting")
    timeout: int = Field(default=30, description="Request timeout")

class OCRConfig(BaseModel):
    """OCR configuration"""
    engine: str = Field(default="auto", description="OCR engine")
    language: str = Field(default="en", description="OCR language")
    confidence_threshold: float = Field(default=0.3, description="Confidence threshold")
    max_image_size: List[int] = Field(default=[1920, 1080], description="Maximum image size")
    preprocessing: bool = Field(default=True, description="Enable preprocessing")

class AppConfig(BaseModel):
    """Application configuration"""
    ai_config: AIConfig = Field(default_factory=AIConfig)
    ocr_config: OCRConfig = Field(default_factory=OCRConfig)
    max_concurrent_tasks: int = Field(default=5, description="Maximum concurrent tasks")
    task_timeout: int = Field(default=300, description="Default task timeout")
    enable_websockets: bool = Field(default=True, description="Enable WebSocket support")
    cors_origins: List[str] = Field(default=["*"], description="CORS origins")
    log_level: str = Field(default="INFO", description="Logging level")
    debug_mode: bool = Field(default=False, description="Debug mode")