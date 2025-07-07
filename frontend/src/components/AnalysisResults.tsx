'use client';

import { motion } from 'framer-motion';
import { Eye, MessageSquare, Target, Clock, Zap, Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface AnalysisResultsProps {
  data: any;
  onTaskCreate: (task: any) => void;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ data, onTaskCreate }) => {
  const [copiedText, setCopiedText] = useState<string | null>(null);

  if (!data) {
    return (
      <div className="text-center py-12">
        <Eye className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-600 mb-2">No Analysis Data</h3>
        <p className="text-gray-500">
          Upload a screenshot or capture your screen to see analysis results here.
        </p>
      </div>
    );
  }

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedText(label);
    setTimeout(() => setCopiedText(null), 2000);
  };

  const createTaskFromSuggestion = (suggestion: any) => {
    const task = {
      id: Date.now().toString(),
      title: `${suggestion.action.toUpperCase()}: ${suggestion.description}`,
      description: suggestion.description,
      priority: 'medium',
      status: 'pending',
      steps: [
        {
          id: '1',
          description: suggestion.description,
          action: suggestion.action,
          parameters: suggestion.parameters || {},
          coordinates: suggestion.coordinates,
          status: 'pending'
        }
      ],
      created_at: new Date().toISOString(),
      progress: 0,
      confidence: suggestion.confidence
    };
    
    onTaskCreate(task);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-sage-text mb-2">Analysis Results</h2>
        <p className="text-gray-600">
          AI-powered screen analysis with OCR and automation suggestions
        </p>
      </div>

      {/* Analysis Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-sage-bg to-white p-6 rounded-lg shadow-md"
      >
        <h3 className="text-lg font-semibold text-sage-text mb-4 flex items-center">
          <Eye className="w-5 h-5 mr-2" />
          Analysis Overview
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-sage-green">
              {data.detected_elements?.length || 0}
            </div>
            <div className="text-sm text-gray-600">Elements Detected</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-sage-green">
              {Math.round((data.confidence_score || 0) * 100)}%
            </div>
            <div className="text-sm text-gray-600">Confidence Score</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-sage-green">
              {(data.processing_time || 0).toFixed(1)}s
            </div>
            <div className="text-sm text-gray-600">Processing Time</div>
          </div>
        </div>
      </motion.div>

      {/* OCR Results */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white p-6 rounded-lg shadow-md"
      >
        <h3 className="text-lg font-semibold text-sage-text mb-4 flex items-center">
          <MessageSquare className="w-5 h-5 mr-2" />
          Extracted Text (OCR)
        </h3>
        
        <div className="relative">
          <div className="bg-gray-50 p-4 rounded-lg border max-h-40 overflow-y-auto">
            <pre className="text-sm text-gray-700 whitespace-pre-wrap">
              {data.ocr_text || 'No text detected'}
            </pre>
          </div>
          
          {data.ocr_text && (
            <button
              onClick={() => copyToClipboard(data.ocr_text, 'OCR Text')}
              className="absolute top-2 right-2 p-2 bg-white rounded-lg shadow-sm hover:bg-gray-50 transition-colors"
              title="Copy text"
            >
              {copiedText === 'OCR Text' ? (
                <Check className="w-4 h-4 text-green-500" />
              ) : (
                <Copy className="w-4 h-4 text-gray-500" />
              )}
            </button>
          )}
        </div>
      </motion.div>

      {/* AI Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white p-6 rounded-lg shadow-md"
      >
        <h3 className="text-lg font-semibold text-sage-text mb-4 flex items-center">
          <Zap className="w-5 h-5 mr-2" />
          AI Analysis
        </h3>
        
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <p className="text-gray-700">
            {data.ai_analysis || 'No AI analysis available'}
          </p>
        </div>
      </motion.div>

      {/* Detected Elements */}
      {data.detected_elements && data.detected_elements.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white p-6 rounded-lg shadow-md"
        >
          <h3 className="text-lg font-semibold text-sage-text mb-4 flex items-center">
            <Target className="w-5 h-5 mr-2" />
            Detected Elements
          </h3>
          
          <div className="space-y-3 max-h-60 overflow-y-auto">
            {data.detected_elements.map((element: any, index: number) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-800">
                    {element.text || `Element ${index + 1}`}
                  </p>
                  <p className="text-sm text-gray-600">
                    Type: {element.element_type || 'text'} | 
                    Confidence: {Math.round((element.confidence || 0) * 100)}% |
                    Position: ({element.center?.[0] || 0}, {element.center?.[1] || 0})
                  </p>
                </div>
                
                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${
                    (element.confidence || 0) > 0.7 ? 'bg-green-500' :
                    (element.confidence || 0) > 0.5 ? 'bg-yellow-500' : 'bg-red-500'
                  }`} />
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Suggested Actions */}
      {data.suggested_actions && data.suggested_actions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white p-6 rounded-lg shadow-md"
        >
          <h3 className="text-lg font-semibold text-sage-text mb-4 flex items-center">
            <Target className="w-5 h-5 mr-2" />
            Suggested Actions
          </h3>
          
          <div className="space-y-3">
            {data.suggested_actions.map((action: any, index: number) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="flex items-center justify-between p-4 bg-sage-bg rounded-lg border border-sage-green/20"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="px-2 py-1 bg-sage-green text-white text-xs rounded-full uppercase">
                      {action.action}
                    </span>
                    <span className="text-sm text-gray-600">
                      {Math.round((action.confidence || 0) * 100)}% confidence
                    </span>
                  </div>
                  <p className="text-gray-800 font-medium">{action.description}</p>
                  {action.coordinates && (
                    <p className="text-sm text-gray-600 mt-1">
                      Target: ({action.coordinates[0]}, {action.coordinates[1]})
                    </p>
                  )}
                </div>
                
                <motion.button
                  onClick={() => createTaskFromSuggestion(action)}
                  className="px-4 py-2 bg-sage-green text-white rounded-lg hover:bg-sage-dark transition-colors"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Create Task
                </motion.button>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Processing Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-gray-50 p-4 rounded-lg"
      >
        <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
          <Clock className="w-4 h-4 mr-2" />
          Processing Information
        </h4>
        <div className="text-xs text-gray-600 space-y-1">
          <p>Analysis completed at: {new Date(data.timestamp || Date.now()).toLocaleString()}</p>
          <p>Processing time: {(data.processing_time || 0).toFixed(2)} seconds</p>
          <p>Elements detected: {data.detected_elements?.length || 0}</p>
          <p>Suggested actions: {data.suggested_actions?.length || 0}</p>
        </div>
      </motion.div>
    </div>
  );
};

export default AnalysisResults;