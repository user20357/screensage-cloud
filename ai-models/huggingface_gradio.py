#!/usr/bin/env python3
"""
HuggingFace Spaces Gradio Interface for ScreenSage Architect
Creates a demo UI hosted on HuggingFace Spaces
"""

import gradio as gr
import torch
import cv2
import numpy as np
from PIL import Image
import base64
import json
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
import pytesseract
from datetime import datetime

# Initialize models
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Loading models on {device}...")

# Load BLIP for image captioning
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model.to(device)

def analyze_screenshot(image):
    """
    Main analysis function for Gradio interface
    """
    if image is None:
        return "Please upload an image", "", "[]", 0.0
    
    try:
        # Convert to PIL Image if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # OCR Processing
        ocr_text = pytesseract.image_to_string(image)
        
        # AI Analysis with BLIP
        inputs = blip_processor(image, return_tensors="pt").to(device)
        out = blip_model.generate(**inputs, max_length=50)
        ai_caption = blip_processor.decode(out[0], skip_special_tokens=True)
        
        # Combine analysis
        full_analysis = f"🔍 **Visual Analysis**: {ai_caption}\n\n📝 **Text Detected**: {ocr_text.strip() if ocr_text.strip() else 'No text detected'}"
        
        # Generate suggested actions
        actions = generate_automation_actions(ai_caption, ocr_text)
        actions_json = json.dumps(actions, indent=2)
        
        # Calculate confidence
        confidence = calculate_confidence(ai_caption, ocr_text)
        
        return full_analysis, ocr_text, actions_json, confidence
        
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}", "", "[]", 0.0

def generate_automation_actions(caption, ocr_text):
    """
    Generate automation suggestions based on analysis
    """
    actions = []
    
    # Button detection
    if any(word in caption.lower() for word in ['button', 'click', 'press']):
        actions.append({
            "action": "click",
            "description": "Click detected button element",
            "confidence": 0.8,
            "reasoning": "Button-like element detected in image"
        })
    
    # Text input detection
    if any(word in caption.lower() for word in ['text', 'input', 'field', 'box']):
        actions.append({
            "action": "type",
            "description": "Type text in detected input field",
            "confidence": 0.7,
            "reasoning": "Text input element detected"
        })
    
    # Form detection
    if any(word in ocr_text.lower() for word in ['login', 'sign in', 'username', 'password']):
        actions.append({
            "action": "login",
            "description": "Fill login form",
            "confidence": 0.9,
            "reasoning": "Login form detected via OCR"
        })
    
    # Search functionality
    if any(word in ocr_text.lower() for word in ['search', 'find', 'query']):
        actions.append({
            "action": "search",
            "description": "Perform search operation",
            "confidence": 0.8,
            "reasoning": "Search functionality detected"
        })
    
    # Navigation elements
    if any(word in ocr_text.lower() for word in ['menu', 'home', 'back', 'next']):
        actions.append({
            "action": "navigate",
            "description": "Navigate using detected menu/buttons",
            "confidence": 0.6,
            "reasoning": "Navigation elements detected"
        })
    
    return actions

def calculate_confidence(caption, ocr_text):
    """
    Calculate overall confidence score
    """
    confidence = 0.5  # Base confidence
    
    # Boost confidence based on text detection
    if len(ocr_text.strip()) > 10:
        confidence += 0.2
    
    # Boost confidence based on caption quality
    if len(caption.split()) > 3:
        confidence += 0.2
    
    # Boost confidence for specific UI elements
    ui_keywords = ['button', 'text', 'input', 'menu', 'click', 'form']
    if any(keyword in caption.lower() or keyword in ocr_text.lower() for keyword in ui_keywords):
        confidence += 0.1
    
    return min(confidence, 1.0)

def create_task_from_actions(actions_json, task_name):
    """
    Convert actions to a task format
    """
    try:
        actions = json.loads(actions_json)
        
        task = {
            "name": task_name or f"Task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created": datetime.now().isoformat(),
            "steps": []
        }
        
        for i, action in enumerate(actions):
            task["steps"].append({
                "step": i + 1,
                "action": action["action"],
                "description": action["description"],
                "confidence": action["confidence"],
                "status": "pending"
            })
        
        return json.dumps(task, indent=2)
        
    except Exception as e:
        return f"Error creating task: {str(e)}"

# Create Gradio Interface
with gr.Blocks(
    title="ScreenSage Architect - Cloud Demo",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #87A96B, #A3C083);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    """
) as demo:
    
    gr.HTML("""
    <div class="main-header">🎯 ScreenSage Architect</div>
    <div class="subtitle">AI-Powered Screen Analysis & Automation Assistant</div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📤 Upload Screenshot")
            image_input = gr.Image(
                type="pil",
                label="Screenshot",
                height=300
            )
            
            analyze_btn = gr.Button(
                "🔍 Analyze Screenshot",
                variant="primary",
                size="lg"
            )
            
            gr.Markdown("""
            ### 💡 Tips:
            - Upload clear screenshots
            - Include UI elements you want to automate
            - Works best with buttons, forms, and text
            """)
        
        with gr.Column(scale=2):
            gr.Markdown("## 📊 Analysis Results")
            
            with gr.Tabs():
                with gr.TabItem("🧠 AI Analysis"):
                    analysis_output = gr.Markdown(
                        label="Analysis Results",
                        value="Upload an image to see AI analysis..."
                    )
                
                with gr.TabItem("📝 OCR Text"):
                    ocr_output = gr.Textbox(
                        label="Extracted Text",
                        lines=5,
                        placeholder="Detected text will appear here..."
                    )
                
                with gr.TabItem("🎯 Suggested Actions"):
                    actions_output = gr.Code(
                        label="Automation Actions (JSON)",
                        language="json",
                        value="[]"
                    )
                
                with gr.TabItem("📋 Create Task"):
                    with gr.Row():
                        task_name = gr.Textbox(
                            label="Task Name",
                            placeholder="Enter task name..."
                        )
                        create_task_btn = gr.Button("Create Task")
                    
                    task_output = gr.Code(
                        label="Generated Task",
                        language="json"
                    )
            
            confidence_output = gr.Slider(
                label="🎯 Confidence Score",
                minimum=0,
                maximum=1,
                value=0,
                interactive=False
            )
    
    # Event handlers
    analyze_btn.click(
        fn=analyze_screenshot,
        inputs=[image_input],
        outputs=[analysis_output, ocr_output, actions_output, confidence_output]
    )
    
    create_task_btn.click(
        fn=create_task_from_actions,
        inputs=[actions_output, task_name],
        outputs=[task_output]
    )
    
    # Examples
    gr.Markdown("## 🎨 Try These Examples")
    gr.Examples(
        examples=[
            ["examples/login_form.png"],
            ["examples/calculator.png"],
            ["examples/web_browser.png"],
        ],
        inputs=[image_input],
        label="Sample Screenshots"
    )
    
    gr.Markdown("""
    ## 🚀 About ScreenSage Architect
    
    This is a cloud demo of ScreenSage Architect - an AI-powered screen analysis and automation tool.
    
    **Features:**
    - 🔍 Advanced OCR text extraction
    - 🧠 AI-powered visual analysis
    - 🎯 Smart automation suggestions
    - 📋 Task generation and management
    
    **Technology Stack:**
    - 🤗 HuggingFace Transformers (BLIP)
    - 🔤 Tesseract OCR
    - ⚡ PyTorch GPU acceleration
    - 🎨 Gradio interface
    
    **Links:**
    - [GitHub Repository](https://github.com/your-repo/screensage-architect)
    - [Full Web App](https://screensage-architect.vercel.app)
    - [Documentation](https://docs.screensage.com)
    """)

# Launch the demo
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )#!/usr/bin/env python3
"""
HuggingFace Spaces Gradio Interface for ScreenSage Architect
Creates a demo UI hosted on HuggingFace Spaces
"""

import gradio as gr
import torch
import cv2
import numpy as np
from PIL import Image
import base64
import json
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
import pytesseract
from datetime import datetime

# Initialize models
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Loading models on {device}...")

# Load BLIP for image captioning
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model.to(device)

def analyze_screenshot(image):
    """
    Main analysis function for Gradio interface
    """
    if image is None:
        return "Please upload an image", "", "[]", 0.0
    
    try:
        # Convert to PIL Image if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # OCR Processing
        ocr_text = pytesseract.image_to_string(image)
        
        # AI Analysis with BLIP
        inputs = blip_processor(image, return_tensors="pt").to(device)
        out = blip_model.generate(**inputs, max_length=50)
        ai_caption = blip_processor.decode(out[0], skip_special_tokens=True)
        
        # Combine analysis
        full_analysis = f"🔍 **Visual Analysis**: {ai_caption}\n\n📝 **Text Detected**: {ocr_text.strip() if ocr_text.strip() else 'No text detected'}"
        
        # Generate suggested actions
        actions = generate_automation_actions(ai_caption, ocr_text)
        actions_json = json.dumps(actions, indent=2)
        
        # Calculate confidence
        confidence = calculate_confidence(ai_caption, ocr_text)
        
        return full_analysis, ocr_text, actions_json, confidence
        
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}", "", "[]", 0.0

def generate_automation_actions(caption, ocr_text):
    """
    Generate automation suggestions based on analysis
    """
    actions = []
    
    # Button detection
    if any(word in caption.lower() for word in ['button', 'click', 'press']):
        actions.append({
            "action": "click",
            "description": "Click detected button element",
            "confidence": 0.8,
            "reasoning": "Button-like element detected in image"
        })
    
    # Text input detection
    if any(word in caption.lower() for word in ['text', 'input', 'field', 'box']):
        actions.append({
            "action": "type",
            "description": "Type text in detected input field",
            "confidence": 0.7,
            "reasoning": "Text input element detected"
        })
    
    # Form detection
    if any(word in ocr_text.lower() for word in ['login', 'sign in', 'username', 'password']):
        actions.append({
            "action": "login",
            "description": "Fill login form",
            "confidence": 0.9,
            "reasoning": "Login form detected via OCR"
        })
    
    # Search functionality
    if any(word in ocr_text.lower() for word in ['search', 'find', 'query']):
        actions.append({
            "action": "search",
            "description": "Perform search operation",
            "confidence": 0.8,
            "reasoning": "Search functionality detected"
        })
    
    # Navigation elements
    if any(word in ocr_text.lower() for word in ['menu', 'home', 'back', 'next']):
        actions.append({
            "action": "navigate",
            "description": "Navigate using detected menu/buttons",
            "confidence": 0.6,
            "reasoning": "Navigation elements detected"
        })
    
    return actions

def calculate_confidence(caption, ocr_text):
    """
    Calculate overall confidence score
    """
    confidence = 0.5  # Base confidence
    
    # Boost confidence based on text detection
    if len(ocr_text.strip()) > 10:
        confidence += 0.2
    
    # Boost confidence based on caption quality
    if len(caption.split()) > 3:
        confidence += 0.2
    
    # Boost confidence for specific UI elements
    ui_keywords = ['button', 'text', 'input', 'menu', 'click', 'form']
    if any(keyword in caption.lower() or keyword in ocr_text.lower() for keyword in ui_keywords):
        confidence += 0.1
    
    return min(confidence, 1.0)

def create_task_from_actions(actions_json, task_name):
    """
    Convert actions to a task format
    """
    try:
        actions = json.loads(actions_json)
        
        task = {
            "name": task_name or f"Task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created": datetime.now().isoformat(),
            "steps": []
        }
        
        for i, action in enumerate(actions):
            task["steps"].append({
                "step": i + 1,
                "action": action["action"],
                "description": action["description"],
                "confidence": action["confidence"],
                "status": "pending"
            })
        
        return json.dumps(task, indent=2)
        
    except Exception as e:
        return f"Error creating task: {str(e)}"

# Create Gradio Interface
with gr.Blocks(
    title="ScreenSage Architect - Cloud Demo",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #87A96B, #A3C083);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    """
) as demo:
    
    gr.HTML("""
    <div class="main-header">🎯 ScreenSage Architect</div>
    <div class="subtitle">AI-Powered Screen Analysis & Automation Assistant</div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📤 Upload Screenshot")
            image_input = gr.Image(
                type="pil",
                label="Screenshot",
                height=300
            )
            
            analyze_btn = gr.Button(
                "🔍 Analyze Screenshot",
                variant="primary",
                size="lg"
            )
            
            gr.Markdown("""
            ### 💡 Tips:
            - Upload clear screenshots
            - Include UI elements you want to automate
            - Works best with buttons, forms, and text
            """)
        
        with gr.Column(scale=2):
            gr.Markdown("## 📊 Analysis Results")
            
            with gr.Tabs():
                with gr.TabItem("🧠 AI Analysis"):
                    analysis_output = gr.Markdown(
                        label="Analysis Results",
                        value="Upload an image to see AI analysis..."
                    )
                
                with gr.TabItem("📝 OCR Text"):
                    ocr_output = gr.Textbox(
                        label="Extracted Text",
                        lines=5,
                        placeholder="Detected text will appear here..."
                    )
                
                with gr.TabItem("🎯 Suggested Actions"):
                    actions_output = gr.Code(
                        label="Automation Actions (JSON)",
                        language="json",
                        value="[]"
                    )
                
                with gr.TabItem("📋 Create Task"):
                    with gr.Row():
                        task_name = gr.Textbox(
                            label="Task Name",
                            placeholder="Enter task name..."
                        )
                        create_task_btn = gr.Button("Create Task")
                    
                    task_output = gr.Code(
                        label="Generated Task",
                        language="json"
                    )
            
            confidence_output = gr.Slider(
                label="🎯 Confidence Score",
                minimum=0,
                maximum=1,
                value=0,
                interactive=False
            )
    
    # Event handlers
    analyze_btn.click(
        fn=analyze_screenshot,
        inputs=[image_input],
        outputs=[analysis_output, ocr_output, actions_output, confidence_output]
    )
    
    create_task_btn.click(
        fn=create_task_from_actions,
        inputs=[actions_output, task_name],
        outputs=[task_output]
    )
    
    # Examples
    gr.Markdown("## 🎨 Try These Examples")
    gr.Examples(
        examples=[
            ["examples/login_form.png"],
            ["examples/calculator.png"],
            ["examples/web_browser.png"],
        ],
        inputs=[image_input],
        label="Sample Screenshots"
    )
    
    gr.Markdown("""
    ## 🚀 About ScreenSage Architect
    
    This is a cloud demo of ScreenSage Architect - an AI-powered screen analysis and automation tool.
    
    **Features:**
    - 🔍 Advanced OCR text extraction
    - 🧠 AI-powered visual analysis
    - 🎯 Smart automation suggestions
    - 📋 Task generation and management
    
    **Technology Stack:**
    - 🤗 HuggingFace Transformers (BLIP)
    - 🔤 Tesseract OCR
    - ⚡ PyTorch GPU acceleration
    - 🎨 Gradio interface
    
    **Links:**
    - [GitHub Repository](https://github.com/your-repo/screensage-architect)
    - [Full Web App](https://screensage-architect.vercel.app)
    - [Documentation](https://docs.screensage.com)
    """)

# Launch the demo
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )