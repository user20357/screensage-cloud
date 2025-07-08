'use client';

import { motion } from 'framer-motion';
import { Zap, ExternalLink } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <motion.div 
            className="flex items-center space-x-3"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="w-10 h-10 bg-sage-green rounded-lg flex items-center justify-center">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-sage-text">ScreenSage Architect</h1>
              <p className="text-sm text-gray-500">Cloud Edition</p>
            </div>
          </motion.div>

          {/* Navigation */}
          <motion.nav 
            className="hidden md:flex items-center space-x-6"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <a 
              href="#features" 
              className="text-gray-600 hover:text-sage-green transition-colors"
            >
              Features
            </a>
            <a 
              href="#docs" 
              className="text-gray-600 hover:text-sage-green transition-colors"
            >
              Docs
            </a>
            <a 
              href="#api" 
              className="text-gray-600 hover:text-sage-green transition-colors"
            >
              API
            </a>
          </motion.nav>

          {/* Action Buttons */}
          <motion.div 
            className="flex items-center space-x-3"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <motion.button
              className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-sage-green transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <ExternalLink className="w-4 h-4" />
              <span className="hidden sm:inline">GitHub</span>
            </motion.button>
            
            <motion.button
              className="flex items-center space-x-2 px-4 py-2 bg-sage-green text-white rounded-lg hover:bg-sage-dark transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <ExternalLink className="w-4 h-4" />
              <span className="hidden sm:inline">Desktop App</span>
            </motion.button>
          </motion.div>
        </div>
      </div>
    </header>
  );
};

export default Header;