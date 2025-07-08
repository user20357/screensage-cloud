'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Monitor, Play, Square, Camera, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

interface ScreenCaptureProps {
  onAnalysisComplete: (data: any) => void;
}

const ScreenCapture: React.FC<ScreenCaptureProps> = ({ onAnalysisComplete }) => {
  const [isCapturing, setIsCapturing] = useState(false);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [lastAnalysis, setLastAnalysis] = useState<any>(null);
  const [wsConnected, setWsConnected] = useState(false);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const initWebSocket = () => {
      try {
        const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws';
        wsRef.current = new WebSocket(wsUrl);
        
        wsRef.current.onopen = () => {
          console.log('WebSocket connected');
          setWsConnected(true);
        };
        
        wsRef.current.onmessage = (event) => {
          const message = JSON.parse(event.data);
          if (message.type === 'analysis_result') {
            setLastAnalysis(message.data);
            setIsAnalyzing(false);
          }
        };
        
        wsRef.current.onclose = () => {
          console.log('WebSocket disconnected');
          setWsConnected(false);
        };
        
        wsRef.current.onerror = (error) => {
          console.error('WebSocket error:', error);
          setWsConnected(false);
        };
      } catch (err) {
        console.error('Failed to initialize WebSocket:', err);
        setWsConnected(false);
      }
    };

    initWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const startCapture = async () => {
    try {
      setError(null);
      
      // Check if Screen Capture API is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
        throw new Error('Screen Capture API is not supported in this browser');
      }

      const displayStream = await navigator.mediaDevices.getDisplayMedia({
        video: {
          width: { ideal: 1920 },
          height: { ideal: 1080 },
          frameRate: { ideal: 2 } // Low frame rate for better performance
        },
        audio: false
      });

      setStream(displayStream);
      setIsCapturing(true);

      if (videoRef.current) {
        videoRef.current.srcObject = displayStream;
      }

      // Start real-time analysis if WebSocket is connected
      if (wsConnected) {
        startRealTimeAnalysis();
      }

      // Handle stream ending
      displayStream.getVideoTracks()[0].onended = () => {
        stopCapture();
      };

    } catch (err: any) {
      setError(err.message || 'Failed to start screen capture');
      console.error('Screen capture error:', err);
    }
  };

  const stopCapture = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    
    setIsCapturing(false);
  };

  const startRealTimeAnalysis = () => {
    if (!wsConnected || !wsRef.current) return;

    // Capture and analyze every 2 seconds
    intervalRef.current = setInterval(() => {
      captureAndAnalyze();
    }, 2000);
  };

  const captureAndAnalyze = async () => {
    if (!videoRef.current || !canvasRef.current || !wsRef.current) return;

    try {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      const ctx = canvas.getContext('2d');
      
      if (!ctx) return;

      // Set canvas size to match video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Draw current frame
      ctx.drawImage(video, 0, 0);

      // Convert to base64
      const imageData = canvas.toDataURL('image/png');
      const base64Data = imageData.split(',')[1];

      // Send to backend via WebSocket
      setIsAnalyzing(true);
      wsRef.current.send(JSON.stringify({
        type: 'screen_capture',
        data: {
          image: base64Data,
          timestamp: new Date().toISOString()
        }
      }));

    } catch (err) {
      console.error('Error capturing frame:', err);
      setIsAnalyzing(false);
    }
  };

  const takeScreenshot = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    try {
      setIsAnalyzing(true);
      const canvas = canvasRef.current;
      const video = videoRef.current;
      const ctx = canvas.getContext('2d');
      
      if (!ctx) return;

      // Set canvas size to match video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Draw current frame
      ctx.drawImage(video, 0, 0);

      // Convert to blob and analyze
      canvas.toBlob(async (blob) => {
        if (!blob) return;

        const formData = new FormData();
        formData.append('file', blob, 'screenshot.png');

        try {
          const response = await axios.post('/api/analyze-screenshot', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          onAnalysisComplete(response.data);
          setLastAnalysis(response.data);
        } catch (err: any) {
          setError(err.response?.data?.detail || 'Failed to analyze screenshot');
        } finally {
          setIsAnalyzing(false);
        }
      }, 'image/png');

    } catch (err) {
      console.error('Error taking screenshot:', err);
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-sage-text mb-2">Live Screen Capture</h2>
        <p className="text-gray-600">
          Capture your screen in real-time and get instant AI analysis
        </p>
      </div>

      {/* Status Indicators */}
      <div className="flex justify-center space-x-4 mb-6">
        <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
          isCapturing ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
        }`}>
          <div className={`w-2 h-2 rounded-full ${
            isCapturing ? 'bg-green-500 animate-pulse' : 'bg-gray-400'
          }`} />
          <span>{isCapturing ? 'Capturing' : 'Not Capturing'}</span>
        </div>
        
        <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
          wsConnected ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'
        }`}>
          <div className={`w-2 h-2 rounded-full ${
            wsConnected ? 'bg-blue-500' : 'bg-gray-400'
          }`} />
          <span>{wsConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </div>

      {/* Video Preview */}
      <div className="relative bg-black rounded-lg overflow-hidden mb-6">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className="w-full h-auto max-h-96 object-contain"
        />
        
        {/* Canvas for capturing frames (hidden) */}
        <canvas
          ref={canvasRef}
          className="hidden"
        />
        
        {/* Overlay for analysis feedback */}
        {lastAnalysis && (
          <div className="absolute top-4 left-4 bg-black bg-opacity-70 text-white p-3 rounded-lg max-w-xs">
            <p className="text-sm font-medium">Latest Analysis:</p>
            <p className="text-xs mt-1">
              {lastAnalysis.text ? `"${lastAnalysis.text.slice(0, 50)}..."` : 'No text detected'}
            </p>
            <p className="text-xs text-gray-300 mt-1">
              {lastAnalysis.elements?.length || 0} elements detected
            </p>
          </div>
        )}
        
        {/* Analysis indicator */}
        {isAnalyzing && (
          <div className="absolute top-4 right-4 bg-sage-green text-white p-2 rounded-full">
            <Loader2 className="w-4 h-4 animate-spin" />
          </div>
        )}
      </div>

      {/* Control Buttons */}
      <div className="flex justify-center space-x-4 mb-6">
        {!isCapturing ? (
          <motion.button
            onClick={startCapture}
            className="flex items-center space-x-2 px-6 py-3 bg-sage-green text-white rounded-lg font-medium hover:bg-sage-dark shadow-lg hover:shadow-xl transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Play className="w-5 h-5" />
            <span>Start Capture</span>
          </motion.button>
        ) : (
          <>
            <motion.button
              onClick={stopCapture}
              className="flex items-center space-x-2 px-6 py-3 bg-red-500 text-white rounded-lg font-medium hover:bg-red-600 shadow-lg hover:shadow-xl transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Square className="w-5 h-5" />
              <span>Stop Capture</span>
            </motion.button>
            
            <motion.button
              onClick={takeScreenshot}
              disabled={isAnalyzing}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium shadow-lg hover:shadow-xl transition-all ${
                isAnalyzing
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              }`}
              whileHover={!isAnalyzing ? { scale: 1.05 } : {}}
              whileTap={!isAnalyzing ? { scale: 0.95 } : {}}
            >
              {isAnalyzing ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Camera className="w-5 h-5" />
              )}
              <span>
                {isAnalyzing ? 'Analyzing...' : 'Take Screenshot'}
              </span>
            </motion.button>
          </>
        )}
      </div>

      {/* Error Message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="p-4 bg-red-50 border border-red-200 rounded-lg mb-6"
          >
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-red-500" />
              <p className="text-red-800 font-medium">Screen Capture Error</p>
            </div>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Browser Support Notice */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-2">
          <Monitor className="w-5 h-5 text-blue-500" />
          <p className="text-blue-800 font-medium">Browser Screen Capture</p>
        </div>
        <p className="text-blue-700 text-sm">
          This feature uses the browser&apos;s Screen Capture API (similar to Google Meet screen sharing).
          You&apos;ll be prompted to select which screen/window to capture.
        </p>
        <p className="text-blue-600 text-xs mt-1">
          Supported browsers: Chrome, Firefox, Safari, Edge (latest versions)
        </p>
      </div>
    </div>
  );
};

export default ScreenCapture;