#!/usr/bin/env python3
"""
Cloud Task Manager - Adapted from desktop ScreenSage Architect
Handles task creation, execution, and management in the cloud
"""

import uuid
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from models import TaskRequest, TaskResponse, TaskStatus, TaskStep, TaskPriority

logger = logging.getLogger(__name__)

class CloudTaskManager:
    """
    Cloud-based task manager for automation workflows
    """
    
    def __init__(self):
        self.tasks: Dict[str, TaskResponse] = {}
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.task_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        
    async def create_task(self, task_request: TaskRequest) -> TaskResponse:
        """
        Create a new automation task
        """
        try:
            task_id = str(uuid.uuid4())
            current_time = datetime.now()
            
            # Create task response
            task_response = TaskResponse(
                id=task_id,
                title=task_request.title,
                description=task_request.description,
                priority=task_request.priority,
                status=TaskStatus.PENDING,
                steps=task_request.steps,
                progress=0.0,
                created_at=current_time,
                updated_at=current_time,
                success_rate=0.0,
                tags=task_request.tags,
                total_steps=len(task_request.steps),
                completed_steps=0,
                failed_steps=0,
                pending_steps=len(task_request.steps)
            )
            
            # Store task
            self.tasks[task_id] = task_response
            
            # Auto-execute if requested
            if task_request.auto_execute:
                await self.execute_task(task_id)
            
            logger.info(f"Created task {task_id}: {task_request.title}")
            return task_response
            
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise
    
    async def get_task(self, task_id: str) -> Optional[TaskResponse]:
        """
        Get task by ID
        """
        return self.tasks.get(task_id)
    
    async def get_all_tasks(self) -> List[TaskResponse]:
        """
        Get all tasks
        """
        return list(self.tasks.values())
    
    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        """
        Execute a task
        """
        try:
            task = self.tasks.get(task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            if task.status == TaskStatus.PROCESSING:
                return {"status": "already_running", "task_id": task_id}
            
            # Update task status
            task.status = TaskStatus.PROCESSING
            task.started_at = datetime.now()
            task.updated_at = datetime.now()
            
            # Create execution task
            execution_task = asyncio.create_task(self._execute_task_steps(task_id))
            self.active_tasks[task_id] = execution_task
            
            logger.info(f"Started execution of task {task_id}")
            return {"status": "started", "task_id": task_id}
            
        except Exception as e:
            logger.error(f"Error executing task {task_id}: {e}")
            # Update task status
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.FAILED
                self.tasks[task_id].error_message = str(e)
                self.tasks[task_id].updated_at = datetime.now()
            raise
    
    async def _execute_task_steps(self, task_id: str):
        """
        Execute all steps in a task
        """
        try:
            task = self.tasks[task_id]
            start_time = datetime.now()
            
            completed_steps = 0
            failed_steps = 0
            
            for i, step in enumerate(task.steps):
                try:
                    # Execute step
                    logger.info(f"Executing step {i+1}/{len(task.steps)}: {step.description}")
                    
                    step_result = await self._execute_step(step)
                    
                    # Update step status
                    step.status = TaskStatus.COMPLETED
                    step.result = step_result
                    step.execution_time = step_result.get("execution_time", 0.0)
                    
                    completed_steps += 1
                    
                    # Update task progress
                    task.progress = completed_steps / len(task.steps)
                    task.completed_steps = completed_steps
                    task.updated_at = datetime.now()
                    
                    logger.info(f"Step {i+1} completed successfully")
                    
                except Exception as e:
                    logger.error(f"Step {i+1} failed: {e}")
                    
                    # Update step status
                    step.status = TaskStatus.FAILED
                    step.error_message = str(e)
                    
                    failed_steps += 1
                    task.failed_steps = failed_steps
                    task.updated_at = datetime.now()
                    
                    # Check if we should continue or stop
                    if not self._should_continue_after_failure(task, step):
                        break
            
            # Update final task status
            end_time = datetime.now()
            task.execution_time = (end_time - start_time).total_seconds()
            task.completed_at = end_time
            task.updated_at = end_time
            
            if failed_steps == 0:
                task.status = TaskStatus.COMPLETED
                task.success_rate = 1.0
            elif completed_steps > 0:
                task.status = TaskStatus.COMPLETED  # Partial success
                task.success_rate = completed_steps / len(task.steps)
            else:
                task.status = TaskStatus.FAILED
                task.success_rate = 0.0
            
            # Update counters
            task.pending_steps = len(task.steps) - completed_steps - failed_steps
            
            # Add to history
            self._add_to_history(task)
            
            logger.info(f"Task {task_id} execution completed. Success rate: {task.success_rate:.2%}")
            
        except Exception as e:
            logger.error(f"Task {task_id} execution failed: {e}")
            
            # Update task status
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.updated_at = datetime.now()
            
        finally:
            # Clean up
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
    
    async def _execute_step(self, step: TaskStep) -> Dict[str, Any]:
        """
        Execute a single step
        """
        start_time = datetime.now()
        
        try:
            # Simulate step execution based on action type
            if step.action.value == "click":
                result = await self._simulate_click(step)
            elif step.action.value == "type":
                result = await self._simulate_type(step)
            elif step.action.value == "scroll":
                result = await self._simulate_scroll(step)
            elif step.action.value == "wait":
                result = await self._simulate_wait(step)
            elif step.action.value == "screenshot":
                result = await self._simulate_screenshot(step)
            else:
                result = await self._simulate_custom(step)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _simulate_click(self, step: TaskStep) -> Dict[str, Any]:
        """
        Simulate click action
        """
        # In a real implementation, this would:
        # 1. Take a screenshot
        # 2. Find the target element
        # 3. Click on it
        # 4. Verify the action
        
        await asyncio.sleep(0.5)  # Simulate processing time
        
        coordinates = step.parameters.get("coordinates", [0, 0])
        
        return {
            "action": "click",
            "coordinates": coordinates,
            "success": True,
            "message": f"Clicked at {coordinates}"
        }
    
    async def _simulate_type(self, step: TaskStep) -> Dict[str, Any]:
        """
        Simulate typing action
        """
        await asyncio.sleep(0.3)  # Simulate processing time
        
        text = step.parameters.get("text", "")
        
        return {
            "action": "type",
            "text": text,
            "success": True,
            "message": f"Typed: '{text}'"
        }
    
    async def _simulate_scroll(self, step: TaskStep) -> Dict[str, Any]:
        """
        Simulate scroll action
        """
        await asyncio.sleep(0.2)  # Simulate processing time
        
        direction = step.parameters.get("direction", "down")
        amount = step.parameters.get("amount", 3)
        
        return {
            "action": "scroll",
            "direction": direction,
            "amount": amount,
            "success": True,
            "message": f"Scrolled {direction} by {amount}"
        }
    
    async def _simulate_wait(self, step: TaskStep) -> Dict[str, Any]:
        """
        Simulate wait action
        """
        duration = step.parameters.get("duration", 1.0)
        await asyncio.sleep(duration)
        
        return {
            "action": "wait",
            "duration": duration,
            "success": True,
            "message": f"Waited {duration} seconds"
        }
    
    async def _simulate_screenshot(self, step: TaskStep) -> Dict[str, Any]:
        """
        Simulate screenshot action
        """
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "action": "screenshot",
            "success": True,
            "message": "Screenshot taken",
            "filename": f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        }
    
    async def _simulate_custom(self, step: TaskStep) -> Dict[str, Any]:
        """
        Simulate custom action
        """
        await asyncio.sleep(0.5)  # Simulate processing time
        
        return {
            "action": "custom",
            "success": True,
            "message": f"Executed custom action: {step.description}",
            "parameters": step.parameters
        }
    
    def _should_continue_after_failure(self, task: TaskResponse, failed_step: TaskStep) -> bool:
        """
        Determine if task should continue after a step failure
        """
        # Check if the step is critical
        if failed_step.parameters.get("critical", False):
            return False
        
        # Check failure rate
        if task.failed_steps / len(task.steps) > 0.5:  # More than 50% failed
            return False
        
        # Check priority
        if task.priority == TaskPriority.HIGH and task.failed_steps > 2:
            return False
        
        return True
    
    def _add_to_history(self, task: TaskResponse):
        """
        Add task to history
        """
        try:
            history_entry = {
                "task_id": task.id,
                "title": task.title,
                "status": task.status.value,
                "success_rate": task.success_rate,
                "execution_time": task.execution_time,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "step_count": len(task.steps),
                "completed_steps": task.completed_steps,
                "failed_steps": task.failed_steps
            }
            
            self.task_history.append(history_entry)
            
            # Limit history size
            if len(self.task_history) > self.max_history:
                self.task_history = self.task_history[-self.max_history:]
                
        except Exception as e:
            logger.error(f"Error adding task to history: {e}")
    
    async def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """
        Cancel a running task
        """
        try:
            task = self.tasks.get(task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            # Cancel active execution
            if task_id in self.active_tasks:
                execution_task = self.active_tasks[task_id]
                execution_task.cancel()
                del self.active_tasks[task_id]
            
            # Update task status
            task.status = TaskStatus.CANCELLED
            task.updated_at = datetime.now()
            
            logger.info(f"Cancelled task {task_id}")
            return {"status": "cancelled", "task_id": task_id}
            
        except Exception as e:
            logger.error(f"Error cancelling task {task_id}: {e}")
            raise
    
    async def get_task_stats(self) -> Dict[str, Any]:
        """
        Get task statistics
        """
        try:
            total_tasks = len(self.tasks)
            active_tasks = len(self.active_tasks)
            
            status_counts = {}
            for status in TaskStatus:
                status_counts[status.value] = sum(1 for task in self.tasks.values() if task.status == status)
            
            avg_success_rate = sum(task.success_rate for task in self.tasks.values()) / total_tasks if total_tasks > 0 else 0
            
            return {
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
                "status_counts": status_counts,
                "average_success_rate": avg_success_rate,
                "history_size": len(self.task_history)
            }
            
        except Exception as e:
            logger.error(f"Error getting task stats: {e}")
            return {
                "total_tasks": 0,
                "active_tasks": 0,
                "status_counts": {},
                "average_success_rate": 0.0,
                "history_size": 0,
                "error": str(e)
            }