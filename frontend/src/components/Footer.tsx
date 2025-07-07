'use client';

import { motion } from 'framer-motion';
import { Heart, Coffee, Code, Zap } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-sage-text text-white py-8 mt-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand Section */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-sage-green rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-bold">ScreenSage Architect</h3>
            </div>
            <p className="text-gray-300 text-sm">
              AI-powered screen analysis and automation assistant. From desktop to cloud.
            </p>
          </div>

          {/* Links Section */}
          <div>
            <h4 className="font-semibold mb-4">Resources</h4>
            <div className="space-y-2 text-sm">
              <a href="#" className="text-gray-300 hover:text-sage-light transition-colors block">
                Documentation
              </a>
              <a href="#" className="text-gray-300 hover:text-sage-light transition-colors block">
                API Reference
              </a>
              <a href="#" className="text-gray-300 hover:text-sage-light transition-colors block">
                Desktop App
              </a>
              <a href="#" className="text-gray-300 hover:text-sage-light transition-colors block">
                GitHub Repository
              </a>
            </div>
          </div>

          {/* Cloud Platform Info */}
          <div>
            <h4 className="font-semibold mb-4">Cloud Platform</h4>
            <div className="space-y-2 text-sm text-gray-300">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>Frontend: Vercel</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span>Backend: Render</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span>AI: HuggingFace</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <span>Models: Kaggle</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-600 mt-8 pt-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <p className="text-gray-400 text-sm">
              © 2024 ScreenSage Architect. Built with{' '}
              <Heart className="w-4 h-4 inline text-red-500" /> and{' '}
              <Coffee className="w-4 h-4 inline text-yellow-500" />
            </p>
            
            <div className="flex items-center space-x-4 mt-4 md:mt-0">
              <motion.div
                className="text-xs text-gray-400"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
              >
                <Code className="w-4 h-4 inline mr-1" />
                Open Source
              </motion.div>
              
              <div className="text-xs text-gray-400">
                v1.0.0-cloud
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;