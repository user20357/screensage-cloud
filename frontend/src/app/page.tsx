'use client';

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, Zap, Brain, Target, Monitor, Settings } from 'lucide-react';
import ScreenshotUploader from '../components/ScreenshotUploader';
import AnalysisResults from '../components/AnalysisResults';
import TaskManager from '../components/TaskManager';
import ScreenCapture from '../components/ScreenCapture';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Home() {
  const [activeTab, setActiveTab] = useState<string>('upload');
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);

  const handleAnalysisComplete = useCallback((data: any) => {
    setAnalysisData(data);
    setActiveTab('results');
  }, []);

  const handleTaskCreate = useCallback((task: any) => {
    setTasks(prev => [...prev, task]);
    setActiveTab('tasks');
  }, []);

  const tabs = [
    { id: 'upload', label: 'Upload Screenshot', icon: Upload },
    { id: 'capture', label: 'Live Capture', icon: Monitor },
    { id: 'results', label: 'Analysis Results', icon: Brain },
    { id: 'tasks', label: 'Task Manager', icon: Target },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-sage-bg to-white">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-sage-text mb-4">
            ScreenSage Architect
            <motion.span 
              className="inline-block ml-2"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              🎯
            </motion.span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            AI-powered screen analysis and automation assistant. Upload screenshots or capture your screen 
            to get intelligent insights and automated task suggestions.
          </p>
          
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-2xl mx-auto">
            <motion.div 
              className="bg-white p-6 rounded-lg shadow-lg"
              whileHover={{ scale: 1.02, y: -2 }}
              transition={{ duration: 0.2 }}
            >
              <Brain className="w-8 h-8 text-sage-green mx-auto mb-2" />
              <h3 className="font-semibold text-sage-text">AI Analysis</h3>
              <p className="text-gray-600 text-sm">Advanced OCR + Vision AI</p>
            </motion.div>
            <motion.div 
              className="bg-white p-6 rounded-lg shadow-lg"
              whileHover={{ scale: 1.02, y: -2 }}
              transition={{ duration: 0.2 }}
            >
              <Zap className="w-8 h-8 text-sage-green mx-auto mb-2" />
              <h3 className="font-semibold text-sage-text">Real-time</h3>
              <p className="text-gray-600 text-sm">Live screen capture</p>
            </motion.div>
            <motion.div 
              className="bg-white p-6 rounded-lg shadow-lg"
              whileHover={{ scale: 1.02, y: -2 }}
              transition={{ duration: 0.2 }}
            >
              <Target className="w-8 h-8 text-sage-green mx-auto mb-2" />
              <h3 className="font-semibold text-sage-text">Automation</h3>
              <p className="text-gray-600 text-sm">Smart task suggestions</p>
            </motion.div>
          </div>
        </motion.div>

        {/* Navigation Tabs */}
        <div className="flex flex-wrap justify-center gap-2 mb-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <motion.button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-sage-green text-white shadow-lg'
                    : 'bg-white text-sage-text hover:bg-sage-light hover:text-white'
                }`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </motion.button>
            );
          })}
        </div>

        {/* Content Area */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          {activeTab === 'upload' && (
            <ScreenshotUploader onAnalysisComplete={handleAnalysisComplete} />
          )}
          
          {activeTab === 'capture' && (
            <ScreenCapture onAnalysisComplete={handleAnalysisComplete} />
          )}
          
          {activeTab === 'results' && (
            <AnalysisResults 
              data={analysisData} 
              onTaskCreate={handleTaskCreate}
            />
          )}
          
          {activeTab === 'tasks' && (
            <TaskManager tasks={tasks} onTaskUpdate={setTasks} />
          )}
          
          {activeTab === 'settings' && (
            <div className="text-center py-12">
              <Settings className="w-16 h-16 text-sage-green mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-sage-text mb-2">Settings</h3>
              <p className="text-gray-600">
                Settings panel coming soon! Configure AI providers, OCR engines, and more.
              </p>
            </div>
          )}
        </motion.div>

        {/* Feature Highlights */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-sage-text mb-3">🔍 Smart Analysis</h3>
            <p className="text-gray-600">
              Advanced OCR and AI vision to understand your screen content and suggest automated actions.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-sage-text mb-3">⚡ Real-time Processing</h3>
            <p className="text-gray-600">
              Live screen capture with WebSocket communication for instant analysis and feedback.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-sage-text mb-3">🎯 Task Automation</h3>
            <p className="text-gray-600">
              Convert screen analysis into executable automation tasks with step-by-step guidance.
            </p>
          </div>
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}