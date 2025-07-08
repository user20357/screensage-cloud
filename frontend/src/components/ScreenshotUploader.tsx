'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileImage, X, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

interface ScreenshotUploaderProps {
  onAnalysisComplete: (data: any) => void;
}

const ScreenshotUploader: React.FC<ScreenshotUploaderProps> = ({ onAnalysisComplete }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
    setError(null);
    setSuccess(false);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const uploadAndAnalyze = async () => {
    if (files.length === 0) return;

    setUploading(true);
    setError(null);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', files[0]);

      const response = await axios.post('/api/analyze-screenshot', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 1));
          setUploadProgress(progress);
        },
      });

      setSuccess(true);
      onAnalysisComplete(response.data);
      
      // Clear files after successful analysis
      setTimeout(() => {
        setFiles([]);
        setSuccess(false);
      }, 2000);

    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze screenshot');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-sage-text mb-2">Upload Screenshot</h2>
        <p className="text-gray-600">
          Upload a screenshot to get AI-powered analysis and automation suggestions
        </p>
      </div>

      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-sage-green bg-sage-bg scale-105'
            : 'border-gray-300 hover:border-sage-green hover:bg-sage-bg'
        }`}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          {isDragActive ? (
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="text-sage-green"
            >
              <Upload className="w-16 h-16 mx-auto mb-4" />
              <p className="text-lg font-medium">Drop your screenshot here!</p>
            </motion.div>
          ) : (
            <div className="text-gray-500">
              <FileImage className="w-16 h-16 mx-auto mb-4" />
              <p className="text-lg font-medium mb-2">
                Drag & drop your screenshot here
              </p>
              <p className="text-sm">or click to browse files</p>
              <p className="text-xs mt-2 text-gray-400">
                Supports PNG, JPG, GIF, BMP, WebP (max 10MB)
              </p>
            </div>
          )}
        </div>
      </div>

      {/* File Preview */}
      <AnimatePresence>
        {files.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="mt-6"
          >
            <h3 className="text-lg font-medium text-sage-text mb-4">Selected File</h3>
            <div className="space-y-2">
              {files.map((file, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <FileImage className="w-5 h-5 text-sage-green" />
                    <div>
                      <p className="font-medium text-sage-text">{file.name}</p>
                      <p className="text-sm text-gray-500">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeFile(index)}
                    className="text-red-500 hover:text-red-700 p-1"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Upload Progress */}
      <AnimatePresence>
        {uploading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="mt-6"
          >
            <div className="bg-sage-bg border border-sage-green rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sage-text font-medium">Analyzing screenshot...</span>
                <span className="text-sage-text">{uploadProgress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <motion.div
                  className="bg-sage-green h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${uploadProgress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Processing with OCR and AI vision...
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg"
          >
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-red-500" />
              <p className="text-red-800 font-medium">Analysis Failed</p>
            </div>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Success Message */}
      <AnimatePresence>
        {success && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg"
          >
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <p className="text-green-800 font-medium">Analysis Complete!</p>
            </div>
            <p className="text-green-700 text-sm mt-1">
              Check the Analysis Results tab for detailed insights.
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Action Buttons */}
      <div className="mt-8 flex justify-center space-x-4">
        <motion.button
          onClick={uploadAndAnalyze}
          disabled={files.length === 0 || uploading}
          className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all ${
            files.length === 0 || uploading
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-sage-green text-white hover:bg-sage-dark shadow-lg hover:shadow-xl'
          }`}
          whileHover={files.length > 0 && !uploading ? { scale: 1.05 } : {}}
          whileTap={files.length > 0 && !uploading ? { scale: 0.95 } : {}}
        >
          {uploading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Upload className="w-5 h-5" />
          )}
          <span>
            {uploading ? 'Analyzing...' : 'Analyze Screenshot'}
          </span>
        </motion.button>
      </div>
    </div>
  );
};

export default ScreenshotUploader;