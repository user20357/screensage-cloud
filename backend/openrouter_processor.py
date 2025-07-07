#!/usr/bin/env python3
"""
OpenRouter.ai Integration for ScreenSage Architect
Replaces OpenAI with OpenRouter for better model access and pricing
"""

import os
import requests
import json
import base64
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenRouterProcessor:
    """
    OpenRouter.ai API client for AI processing
    Supports multiple models: GPT-4, Claude, Llama, etc.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        self.app_name = "ScreenSage-Architect"
        self.app_url = "https://github.com/yourusername/screensage-cloud"
        
        # Available models (you can change these)
        self.models = {
            "fast": "openai/gpt-4o-mini",           # Fast and cheap
            "smart": "openai/gpt-4o",              # Best quality
            "claude": "anthropic/claude-3-sonnet", # Alternative to GPT
            "llama": "meta-llama/llama-3-70b",     # Open source
            "vision": "openai/gpt-4-vision-preview" # For image analysis
        }
        
        if not self.api_key or self.api_key == "dummy_key":
            logger.warning("OpenRouter API key not set. Using fallback analysis.")
            self.enabled = False
        else:
            self.enabled = True
            logger.info(f"OpenRouter initialized with model: {self.default_model}")
    
    async def analyze_screenshot(self, image_data: bytes, ocr_text: str, model: str = None) -> Dict[str, Any]:
        """
        Analyze screenshot using OpenRouter AI models
        """
        if not self.enabled:
            return await self._fallback_analysis(ocr_text)
        
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Choose model
            selected_model = model or self.default_model
            if model in self.models:
                selected_model = self.models[model]
            
            # Prepare the prompt
            prompt = self._create_analysis_prompt(ocr_text)
            
            # Make API request
            response = await self._make_request(
                model=selected_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ]
            )
            
            if response and "choices" in response:
                analysis_text = response["choices"][0]["message"]["content"]
                return self._parse_analysis_response(analysis_text)
            else:
                logger.error("Invalid response from OpenRouter")
                return await self._fallback_analysis(ocr_text)
                
        except Exception as e:
            logger.error(f"OpenRouter analysis failed: {e}")
            return await self._fallback_analysis(ocr_text)
    
    async def _make_request(self, model: str, messages: List[Dict], max_tokens: int = 1000) -> Optional[Dict]:
        """
        Make request to OpenRouter API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.app_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"OpenRouter request failed: {e}")
            return None
    
    def _create_analysis_prompt(self, ocr_text: str) -> str:
        """
        Create analysis prompt for the AI model
        """
        return f"""
You are ScreenSage Architect, an AI assistant that analyzes screenshots to help users automate tasks.

SCREENSHOT ANALYSIS:
OCR Text Found: {ocr_text}

Please analyze this screenshot and provide:

1. SCREEN_TYPE: What type of interface is this? (web_page, desktop_app, mobile_app, login_form, etc.)

2. DETECTED_ELEMENTS: List interactive elements you can see (buttons, forms, links, etc.)

3. CURRENT_CONTEXT: What is the user trying to do based on the screen content?

4. AUTOMATION_SUGGESTIONS: Provide 3-5 specific automation actions the user could take, such as:
   - Click on specific buttons
   - Fill out forms
   - Navigate to other sections
   - Extract specific information

5. CONFIDENCE: Rate your analysis confidence (0.0 to 1.0)

Format your response as JSON:
{{
    "screen_type": "...",
    "detected_elements": ["element1", "element2", ...],
    "current_context": "...",
    "automation_suggestions": [
        {{"action": "click", "target": "button_name", "description": "..."}},
        {{"action": "type", "target": "input_field", "text": "...", "description": "..."}},
        {{"action": "extract", "target": "data_element", "description": "..."}}
    ],
    "confidence": 0.85
}}
"""
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse AI response into structured format
        """
        try:
            # Try to extract JSON from response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "{" in response_text and "}" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_text = response_text[json_start:json_end]
            else:
                json_text = response_text
            
            parsed = json.loads(json_text)
            
            return {
                "analysis": parsed.get("current_context", "Screen analysis completed"),
                "actions": parsed.get("automation_suggestions", []),
                "confidence": parsed.get("confidence", 0.7),
                "screen_type": parsed.get("screen_type", "unknown"),
                "elements": parsed.get("detected_elements", []),
                "processing_time": 0.0,
                "model_used": self.default_model
            }
            
        except json.JSONDecodeError:
            # Fallback: parse as plain text
            return {
                "analysis": response_text,
                "actions": self._extract_actions_from_text(response_text),
                "confidence": 0.6,
                "screen_type": "unknown",
                "elements": [],
                "processing_time": 0.0,
                "model_used": self.default_model
            }
    
    def _extract_actions_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Extract action suggestions from plain text response
        """
        actions = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['click', 'type', 'fill', 'select', 'navigate']):
                actions.append({
                    "action": "general",
                    "description": line,
                    "target": "detected_element"
                })
        
        return actions[:5]  # Limit to 5 actions
    
    async def _fallback_analysis(self, ocr_text: str) -> Dict[str, Any]:
        """
        Fallback analysis when OpenRouter is not available
        """
        logger.info("Using fallback analysis (pattern matching)")
        
        # Simple pattern matching
        actions = []
        elements = []
        
        # Common UI patterns
        if "login" in ocr_text.lower() or "sign in" in ocr_text.lower():
            actions.append({
                "action": "fill_login",
                "description": "Fill login credentials",
                "target": "login_form"
            })
            elements.extend(["username_field", "password_field", "login_button"])
        
        if "search" in ocr_text.lower():
            actions.append({
                "action": "search",
                "description": "Perform search operation",
                "target": "search_box"
            })
            elements.append("search_input")
        
        if "submit" in ocr_text.lower() or "send" in ocr_text.lower():
            actions.append({
                "action": "submit",
                "description": "Submit form",
                "target": "submit_button"
            })
            elements.append("submit_button")
        
        # Default actions if nothing specific found
        if not actions:
            actions = [
                {
                    "action": "analyze",
                    "description": "Analyze screen content for automation opportunities",
                    "target": "screen"
                },
                {
                    "action": "extract_text",
                    "description": "Extract all visible text",
                    "target": "text_elements"
                }
            ]
        
        return {
            "analysis": f"Pattern-based analysis of screen content. Found {len(ocr_text.split())} words of text.",
            "actions": actions,
            "confidence": 0.5,
            "screen_type": "unknown",
            "elements": elements,
            "processing_time": 0.1,
            "model_used": "fallback_pattern_matching"
        }
    
    async def get_available_models(self) -> List[Dict[str, str]]:
        """
        Get list of available models from OpenRouter
        """
        if not self.enabled:
            return [{"id": "fallback", "name": "Pattern Matching (Fallback)"}]
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                models_data = response.json()
                return [
                    {
                        "id": model["id"],
                        "name": model.get("name", model["id"]),
                        "pricing": model.get("pricing", {})
                    }
                    for model in models_data.get("data", [])
                    if "gpt" in model["id"].lower() or "claude" in model["id"].lower()
                ][:10]  # Limit to 10 models
            else:
                return list(self.models.items())
                
        except Exception as e:
            logger.error(f"Failed to get models: {e}")
            return list(self.models.items())

# Global instance
openrouter_processor = OpenRouterProcessor()