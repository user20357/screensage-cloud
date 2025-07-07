'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Play, 
  Pause, 
  Square, 
  CheckCircle, 
  XCircle, 
  Clock, 
  Target,
  Trash2,
  Eye,
  RotateCcw
} from 'lucide-react';
import axios from 'axios';

interface Task {
  id: string;
  title: string;
  description: string;
  priority: string;
  status: string;
  steps: any[];
  progress: number;
  created_at: string;
  confidence?: number;
}

interface TaskManagerProps {
  tasks: Task[];
  onTaskUpdate: (tasks: Task[]) => void;
}

const TaskManager: React.FC<TaskManagerProps> = ({ tasks, onTaskUpdate }) => {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [executingTasks, setExecutingTasks] = useState<Set<string>>(new Set());
  const [taskDetails, setTaskDetails] = useState<{[key: string]: any}>({});

  useEffect(() => {
    // Fetch task details from API
    const fetchTaskDetails = async () => {
      for (const task of tasks) {
        try {
          const response = await axios.get(`/api/tasks/${task.id}`);
          setTaskDetails(prev => ({
            ...prev,
            [task.id]: response.data
          }));
        } catch (error) {
          console.error(`Failed to fetch details for task ${task.id}:`, error);
        }
      }
    };

    if (tasks.length > 0) {
      fetchTaskDetails();
    }
  }, [tasks]);

  const executeTask = async (taskId: string) => {
    try {
      setExecutingTasks(prev => new Set(prev).add(taskId));
      
      const response = await axios.put(`/api/tasks/${taskId}/execute`);
      
      if (response.data.status === 'started') {
        // Update task status
        onTaskUpdate(tasks.map(task => 
          task.id === taskId 
            ? { ...task, status: 'processing' }
            : task
        ));
        
        // Poll for updates
        pollTaskStatus(taskId);
      }
    } catch (error) {
      console.error('Failed to execute task:', error);
      setExecutingTasks(prev => {
        const newSet = new Set(prev);
        newSet.delete(taskId);
        return newSet;
      });
    }
  };

  const pollTaskStatus = async (taskId: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await axios.get(`/api/tasks/${taskId}`);
        const updatedTask = response.data;
        
        // Update task in list
        onTaskUpdate(tasks.map(task => 
          task.id === taskId ? updatedTask : task
        ));
        
        // Update task details
        setTaskDetails(prev => ({
          ...prev,
          [taskId]: updatedTask
        }));
        
        // Stop polling if task is complete
        if (updatedTask.status === 'completed' || updatedTask.status === 'failed') {
          clearInterval(pollInterval);
          setExecutingTasks(prev => {
            const newSet = new Set(prev);
            newSet.delete(taskId);
            return newSet;
          });
        }
      } catch (error) {
        console.error('Failed to poll task status:', error);
        clearInterval(pollInterval);
      }
    }, 2000);
  };

  const deleteTask = (taskId: string) => {
    onTaskUpdate(tasks.filter(task => task.id !== taskId));
    if (selectedTask?.id === taskId) {
      setSelectedTask(null);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'processing':
        return <RotateCcw className="w-5 h-5 text-blue-500 animate-spin" />;
      default:
        return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <Target className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-600 mb-2">No Tasks Yet</h3>
        <p className="text-gray-500">
          Create tasks from screenshot analysis to see them here.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-sage-text mb-2">Task Manager</h2>
        <p className="text-gray-600">
          Manage and execute your automation tasks
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Task List */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-sage-text mb-4">
              Tasks ({tasks.length})
            </h3>
            
            <div className="space-y-3">
              {tasks.map((task) => (
                <motion.div
                  key={task.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    selectedTask?.id === task.id
                      ? 'border-sage-green bg-sage-bg'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedTask(task)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        {getStatusIcon(task.status)}
                        <h4 className="font-medium text-gray-800">{task.title}</h4>
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-3">{task.description}</p>
                      
                      <div className="flex items-center space-x-4 text-xs">
                        <span className={`px-2 py-1 rounded-full ${getStatusColor(task.status)}`}>
                          {task.status}
                        </span>
                        <span className={`px-2 py-1 rounded-full ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </span>
                        {task.confidence && (
                          <span className="text-gray-500">
                            {Math.round(task.confidence * 100)}% confidence
                          </span>
                        )}
                      </div>
                      
                      {/* Progress Bar */}
                      <div className="mt-3">
                        <div className="flex justify-between text-xs text-gray-600 mb-1">
                          <span>Progress</span>
                          <span>{Math.round(task.progress * 100)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-sage-green h-2 rounded-full transition-all duration-300"
                            style={{ width: `${task.progress * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      {task.status === 'pending' && (
                        <motion.button
                          onClick={(e) => {
                            e.stopPropagation();
                            executeTask(task.id);
                          }}
                          disabled={executingTasks.has(task.id)}
                          className={`p-2 rounded-lg ${
                            executingTasks.has(task.id)
                              ? 'bg-gray-300 cursor-not-allowed'
                              : 'bg-sage-green hover:bg-sage-dark text-white'
                          }`}
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <Play className="w-4 h-4" />
                        </motion.button>
                      )}
                      
                      <motion.button
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteTask(task.id);
                        }}
                        className="p-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <Trash2 className="w-4 h-4" />
                      </motion.button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        {/* Task Details */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 sticky top-6">
            {selectedTask ? (
              <div>
                <h3 className="text-lg font-semibold text-sage-text mb-4">
                  Task Details
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Title</label>
                    <p className="text-gray-800">{selectedTask.title}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-700">Description</label>
                    <p className="text-gray-800">{selectedTask.description}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-700">Status</label>
                    <div className="flex items-center space-x-2 mt-1">
                      {getStatusIcon(selectedTask.status)}
                      <span className="capitalize">{selectedTask.status}</span>
                    </div>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-700">Created</label>
                    <p className="text-gray-800">
                      {new Date(selectedTask.created_at).toLocaleString()}
                    </p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-700">Steps</label>
                    <div className="mt-2 space-y-2">
                      {selectedTask.steps.map((step, index) => (
                        <div key={index} className="flex items-center space-x-2 text-sm">
                          {step.status === 'completed' ? (
                            <CheckCircle className="w-4 h-4 text-green-500" />
                          ) : step.status === 'failed' ? (
                            <XCircle className="w-4 h-4 text-red-500" />
                          ) : (
                            <Clock className="w-4 h-4 text-gray-400" />
                          )}
                          <span className="text-gray-700">{step.description}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {taskDetails[selectedTask.id] && (
                    <div>
                      <label className="text-sm font-medium text-gray-700">Execution Details</label>
                      <div className="mt-2 text-sm text-gray-600">
                        <p>Success Rate: {Math.round((taskDetails[selectedTask.id].success_rate || 0) * 100)}%</p>
                        <p>Completed Steps: {taskDetails[selectedTask.id].completed_steps || 0}</p>
                        <p>Failed Steps: {taskDetails[selectedTask.id].failed_steps || 0}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <Eye className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-500">
                  Select a task to view details
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskManager;