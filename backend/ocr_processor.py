#!/usr/bin/env python3
"""
Cloud OCR Processor - Adapted from desktop ScreenSage Architect
Handles text extraction from screenshots in the cloud
"""

import io
import logging
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from PIL import Image
import cv2
import pytesseract
from datetime import datetime

logger = logging.getLogger(__name__)

class CloudOCRProcessor:
    """
    Cloud-based OCR processor for text extraction
    Optimized for web deployment with multiple OCR engines
    """
    
    def __init__(self):
        self.setup_ocr_engines()
        
        # Cloud-optimized settings
        self.max_image_size = (1920, 1080)
        self.min_confidence = 0.3
        self.processing_timeout = 30  # seconds
        
    def setup_ocr_engines(self):
        """Initialize OCR engines"""
        try:
            # Test Tesseract availability
            pytesseract.get_tesseract_version()
            self.tesseract_available = True
            logger.info("Tesseract OCR initialized")
        except Exception as e:
            logger.warning(f"Tesseract not available: {e}")
            self.tesseract_available = False
            
        # Try to import EasyOCR for better accuracy
        try:
            import easyocr
            self.easyocr_reader = easyocr.Reader(['en'])
            self.easyocr_available = True
            logger.info("EasyOCR initialized")
        except ImportError:
            logger.warning("EasyOCR not available, using Tesseract only")
            self.easyocr_available = False
            
    async def process_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Process image with comprehensive OCR
        """
        start_time = time.time()
        
        try:
            # Prepare image
            image = self._prepare_image(image_data)
            cv_image = self._pil_to_cv2(image)
            
            # Run OCR with timeout
            result = await asyncio.wait_for(
                self._extract_text_and_elements(cv_image),
                timeout=self.processing_timeout
            )
            
            processing_time = time.time() - start_time
            
            return {
                "text": result.get("text", ""),
                "elements": result.get("elements", []),
                "confidence": result.get("confidence", 0.0),
                "processing_time": processing_time,
                "method": result.get("method", "unknown"),
                "timestamp": datetime.now().isoformat()
            }
            
        except asyncio.TimeoutError:
            logger.error("OCR processing timeout")
            return {
                "text": "",
                "elements": [],
                "confidence": 0.0,
                "processing_time": self.processing_timeout,
                "error": "Processing timeout"
            }
        except Exception as e:
            logger.error(f"OCR processing error: {e}")
            return {
                "text": "",
                "elements": [],
                "confidence": 0.0,
                "processing_time": time.time() - start_time,
                "error": str(e)
            }
    
    async def process_image_fast(self, image_data: bytes) -> Dict[str, Any]:
        """
        Fast OCR processing for real-time use
        """
        start_time = time.time()
        
        try:
            # Prepare image (lower quality for speed)
            image = self._prepare_image(image_data, fast=True)
            cv_image = self._pil_to_cv2(image)
            
            # Use fastest OCR method
            result = await asyncio.to_thread(self._fast_ocr, cv_image)
            
            processing_time = time.time() - start_time
            
            return {
                "text": result.get("text", ""),
                "elements": result.get("elements", []),
                "confidence": result.get("confidence", 0.0),
                "processing_time": processing_time,
                "method": "fast_ocr"
            }
            
        except Exception as e:
            logger.error(f"Fast OCR error: {e}")
            return {
                "text": "",
                "elements": [],
                "confidence": 0.0,
                "processing_time": time.time() - start_time,
                "error": str(e)
            }
    
    async def _extract_text_and_elements(self, cv_image: np.ndarray) -> Dict[str, Any]:
        """
        Extract text and UI elements from image
        """
        # Try EasyOCR first (better accuracy)
        if self.easyocr_available:
            try:
                result = await asyncio.to_thread(self._easyocr_extract, cv_image)
                if result.get("confidence", 0) > 0.5:
                    return result
            except Exception as e:
                logger.warning(f"EasyOCR failed: {e}")
        
        # Fallback to Tesseract
        if self.tesseract_available:
            try:
                result = await asyncio.to_thread(self._tesseract_extract, cv_image)
                return result
            except Exception as e:
                logger.warning(f"Tesseract failed: {e}")
        
        # Last resort: basic text detection
        return await asyncio.to_thread(self._basic_text_detection, cv_image)
    
    def _easyocr_extract(self, cv_image: np.ndarray) -> Dict[str, Any]:
        """
        Extract text using EasyOCR
        """
        try:
            results = self.easyocr_reader.readtext(cv_image)
            
            text_parts = []
            elements = []
            confidences = []
            
            for (bbox, text, confidence) in results:
                if confidence > self.min_confidence:
                    text_parts.append(text)
                    confidences.append(confidence)
                    
                    # Calculate center point
                    x_coords = [point[0] for point in bbox]
                    y_coords = [point[1] for point in bbox]
                    center_x = sum(x_coords) / len(x_coords)
                    center_y = sum(y_coords) / len(y_coords)
                    
                    elements.append({
                        "text": text,
                        "confidence": confidence,
                        "bbox": bbox,
                        "center": [int(center_x), int(center_y)],
                        "type": "text"
                    })
            
            full_text = " ".join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                "text": full_text,
                "elements": elements,
                "confidence": avg_confidence,
                "method": "easyocr"
            }
            
        except Exception as e:
            logger.error(f"EasyOCR extraction error: {e}")
            raise
    
    def _tesseract_extract(self, cv_image: np.ndarray) -> Dict[str, Any]:
        """
        Extract text using Tesseract
        """
        try:
            # Get text
            text = pytesseract.image_to_string(cv_image)
            
            # Get detailed data
            data = pytesseract.image_to_data(cv_image, output_type=pytesseract.Output.DICT)
            
            elements = []
            confidences = []
            
            n_boxes = len(data['level'])
            for i in range(n_boxes):
                confidence = float(data['conf'][i])
                if confidence > self.min_confidence * 100:  # Tesseract uses 0-100 scale
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    text_piece = data['text'][i].strip()
                    
                    if text_piece:
                        confidences.append(confidence / 100)  # Convert to 0-1 scale
                        elements.append({
                            "text": text_piece,
                            "confidence": confidence / 100,
                            "bbox": [[x, y], [x+w, y], [x+w, y+h], [x, y+h]],
                            "center": [x + w//2, y + h//2],
                            "type": "text"
                        })
            
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                "text": text.strip(),
                "elements": elements,
                "confidence": avg_confidence,
                "method": "tesseract"
            }
            
        except Exception as e:
            logger.error(f"Tesseract extraction error: {e}")
            raise
    
    def _basic_text_detection(self, cv_image: np.ndarray) -> Dict[str, Any]:
        """
        Basic text detection using OpenCV
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours that might be text
            text_regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by size and aspect ratio
                if w > 10 and h > 10 and w < 500 and h < 100:
                    aspect_ratio = w / h
                    if 0.5 < aspect_ratio < 10:  # Reasonable text aspect ratio
                        text_regions.append({
                            "text": f"text_region_{len(text_regions)}",
                            "confidence": 0.3,
                            "bbox": [[x, y], [x+w, y], [x+w, y+h], [x, y+h]],
                            "center": [x + w//2, y + h//2],
                            "type": "text_region"
                        })
            
            return {
                "text": f"Detected {len(text_regions)} text regions",
                "elements": text_regions,
                "confidence": 0.3,
                "method": "basic_detection"
            }
            
        except Exception as e:
            logger.error(f"Basic text detection error: {e}")
            return {
                "text": "",
                "elements": [],
                "confidence": 0.0,
                "method": "basic_detection"
            }
    
    def _fast_ocr(self, cv_image: np.ndarray) -> Dict[str, Any]:
        """
        Fast OCR for real-time processing
        """
        try:
            # Use Tesseract with minimal processing
            if self.tesseract_available:
                # Fast configuration
                config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
                text = pytesseract.image_to_string(cv_image, config=config)
                
                return {
                    "text": text.strip(),
                    "elements": [],  # Skip detailed analysis for speed
                    "confidence": 0.5,
                    "method": "fast_tesseract"
                }
            else:
                # Fallback to basic detection
                return self._basic_text_detection(cv_image)
                
        except Exception as e:
            logger.error(f"Fast OCR error: {e}")
            return {
                "text": "",
                "elements": [],
                "confidence": 0.0,
                "method": "fast_ocr_failed"
            }
    
    def _prepare_image(self, image_data: bytes, fast: bool = False) -> Image.Image:
        """
        Prepare image for OCR processing
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large
            max_size = (800, 600) if fast else self.max_image_size
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            logger.error(f"Error preparing image: {e}")
            raise
    
    def _pil_to_cv2(self, pil_image: Image.Image) -> np.ndarray:
        """
        Convert PIL Image to OpenCV format
        """
        try:
            # Convert PIL to numpy array
            np_array = np.array(pil_image)
            
            # Convert RGB to BGR for OpenCV
            if len(np_array.shape) == 3:
                cv_image = cv2.cvtColor(np_array, cv2.COLOR_RGB2BGR)
            else:
                cv_image = np_array
                
            return cv_image
            
        except Exception as e:
            logger.error(f"Error converting PIL to CV2: {e}")
            raise