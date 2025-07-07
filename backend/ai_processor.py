#!/usr/bin/env python3
"""
Cloud AI Processor - Adapted from desktop ScreenSage Architect
Handles AI-powered screen analysis in the cloud
"""

import base64
import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
import json
import io
from PIL import Image
import os
from datetime import datetime
from openrouter_processor import openrouter_processor

logger = logging.getLogger(__name__)

class CloudAIProcessor:
    """
    Cloud-based AI processor for screen analysis
    Now using OpenRouter.ai instead of OpenAI
    """
    
    def __init__(self):
        self.openrouter = openrouter_processor
        
        # Cloud-optimized settings
        self.max_image_size = (1024, 768)  # Reduce for faster processing
        self.supported_formats = ['png', 'jpg', 'jpeg', 'webp']
        
        logger.info("CloudAIProcessor initialized with OpenRouter.ai")
        
    def setup_ai_clients(self):
        """Initialize AI clients - now handled by OpenRouter processor"""
        pass  # OpenRouter processor handles initialization
    
    async def analyze_screen(self, image_data: bytes, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive screen analysis using AI
        """
        start_time = time.time()
        
        try:
            # Prepare image for AI analysis
            image = self._prepare_image(image_data)
            
            # Get AI analysis using OpenRouter
            analysis = await self.openrouter.analyze_screenshot(image_data, ocr_result.get("text", ""))
            
            processing_time = time.time() - start_time
            
            return {
                "analysis": analysis.get("description", ""),
                "actions": analysis.get("suggested_actions", []),
                "confidence": analysis.get("confidence", 0.0),
                "processing_time": processing_time,
                "elements_detected": len(ocr_result.get("elements", [])),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in screen analysis: {e}")
            return {
                "analysis": f"Analysis failed: {str(e)}",
                "actions": [],
                "confidence": 0.0,
                "processing_time": time.time() - start_time,
                "error": str(e)
            }
    
    async def analyze_screen_fast(self, image_data: bytes, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fast screen analysis for real-time processing
        """
        try:
            # Quick analysis based on OCR results
            text = ocr_result.get("text", "")
            elements = ocr_result.get("elements", [])
            
            # Basic pattern matching for common UI elements
            actions = self._generate_quick_actions(text, elements)
            
            return {
                "actions": actions,
                "confidence": 0.7,  # Lower confidence for quick analysis
                "processing_time": 0.1,  # Estimated fast processing
                "type": "quick_analysis"
            }
            
        except Exception as e:
            logger.error(f"Error in fast analysis: {e}")
            return {"actions": [], "confidence": 0.0, "error": str(e)}
    
    async def _analyze_with_openai(self, image: Image.Image, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze screen using OpenAI Vision API
        """
        try:
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Prepare prompt with OCR context
            ocr_text = ocr_result.get("text", "")
            elements = ocr_result.get("elements", [])
            
            prompt = f"""
            Analyze this screenshot for automation opportunities.
            
            OCR Text Detected: {ocr_text}
            UI Elements Found: {len(elements)} elements
            
            Provide:
            1. Description of what's visible
            2. Specific automation actions possible
            3. Confidence level (0-1)
            
            Focus on actionable UI elements like buttons, links, input fields.
            """
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            return self._parse_ai_response(result)
            
        except Exception as e:
            logger.error(f"OpenAI analysis error: {e}")
            return await self._analyze_with_fallback(image, ocr_result)
    
    async def _analyze_with_fallback(self, image: Image.Image, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback analysis using pattern matching and heuristics
        """
        try:
            text = ocr_result.get("text", "").lower()
            elements = ocr_result.get("elements", [])
            
            # Pattern-based analysis
            description = self._generate_description(text, elements)
            actions = self._generate_actions(text, elements)
            confidence = self._calculate_confidence(text, elements)
            
            return {
                "description": description,
                "suggested_actions": actions,
                "confidence": confidence,
                "method": "pattern_matching"
            }
            
        except Exception as e:
            logger.error(f"Fallback analysis error: {e}")
            return {
                "description": "Analysis unavailable",
                "suggested_actions": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _generate_description(self, text: str, elements: List[Dict]) -> str:
        """Generate description based on detected elements"""
        descriptions = []
        
        # Check for common applications
        if "calculator" in text:
            descriptions.append("Calculator application detected")
        elif "chrome" in text or "firefox" in text or "browser" in text:
            descriptions.append("Web browser detected")
        elif "notepad" in text or "text editor" in text:
            descriptions.append("Text editor detected")
        elif "file explorer" in text or "folder" in text:
            descriptions.append("File manager detected")
        
        # Check for UI elements
        if len(elements) > 0:
            descriptions.append(f"Detected {len(elements)} interactive elements")
        
        return "; ".join(descriptions) if descriptions else "Screen content analyzed"
    
    def _generate_actions(self, text: str, elements: List[Dict]) -> List[Dict[str, Any]]:
        """Generate suggested actions based on content"""
        actions = []
        
        # Common automation patterns
        if "login" in text or "sign in" in text:
            actions.append({
                "action": "login",
                "description": "Login form detected",
                "confidence": 0.8
            })
        
        if "search" in text:
            actions.append({
                "action": "search",
                "description": "Search functionality available",
                "confidence": 0.7
            })
        
        if "download" in text:
            actions.append({
                "action": "download",
                "description": "Download action available",
                "confidence": 0.6
            })
        
        # Add element-based actions
        for element in elements[:5]:  # Limit to top 5
            if element.get("confidence", 0) > 0.5:
                actions.append({
                    "action": "click",
                    "description": f"Click on '{element.get('text', 'element')}'",
                    "coordinates": element.get("center", [0, 0]),
                    "confidence": element.get("confidence", 0.5)
                })
        
        return actions
    
    def _generate_quick_actions(self, text: str, elements: List[Dict]) -> List[Dict[str, Any]]:
        """Generate quick actions for real-time processing"""
        actions = []
        
        # Fast pattern matching
        patterns = {
            "click": ["button", "link", "click"],
            "type": ["input", "textbox", "search"],
            "scroll": ["scroll", "page", "down", "up"]
        }
        
        text_lower = text.lower()
        for action_type, keywords in patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                actions.append({
                    "action": action_type,
                    "description": f"{action_type.title()} action available",
                    "confidence": 0.6
                })
        
        return actions
    
    def _calculate_confidence(self, text: str, elements: List[Dict]) -> float:
        """Calculate confidence score based on detection quality"""
        confidence = 0.0
        
        # Text quality indicators
        if len(text) > 10:
            confidence += 0.3
        if len(text.split()) > 5:
            confidence += 0.2
        
        # Element quality indicators
        if len(elements) > 0:
            confidence += 0.2
        if any(elem.get("confidence", 0) > 0.7 for elem in elements):
            confidence += 0.3
        
        return min(confidence, 1.0)
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        try:
            # Try to extract structured information
            lines = response.split('\n')
            
            description = ""
            actions = []
            confidence = 0.5
            
            for line in lines:
                line = line.strip()
                if line.startswith("Description:"):
                    description = line.replace("Description:", "").strip()
                elif line.startswith("Action:"):
                    action_text = line.replace("Action:", "").strip()
                    actions.append({
                        "action": "general",
                        "description": action_text,
                        "confidence": 0.7
                    })
                elif "confidence" in line.lower():
                    # Extract confidence value
                    try:
                        conf_str = line.split(":")[-1].strip()
                        confidence = float(conf_str.replace("%", "")) / 100
                    except:
                        pass
            
            return {
                "description": description or response[:200],
                "suggested_actions": actions,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return {
                "description": response[:200],
                "suggested_actions": [],
                "confidence": 0.3
            }
    
    def _prepare_image(self, image_data: bytes) -> Image.Image:
        """Prepare image for AI processing"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large
            if image.size[0] > self.max_image_size[0] or image.size[1] > self.max_image_size[1]:
                image.thumbnail(self.max_image_size, Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            logger.error(f"Error preparing image: {e}")
            raise