import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AlertCircle, TrendingUp, Zap } from 'lucide-react';

const API_BASE = 'http://localhost:5000/api';

function InsightsPanel() {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/insights`);
      setInsights(response.data.insights || []);
    } catch (error) {
      console.error('Error fetching insights:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredInsights = filter === 'all' 
    ? insights 
    : insights.filter(i => i.priority === filter);

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'High':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'Low':
        return 'bg-green-100 text-green-800 border-green-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Cost Optimization':
        return '💰';
      case 'Right-sizing':
        return '📊';
      case 'Resource Cleanup':
        return '🧹';
      case 'Architecture Optimization':
        return '🏗️';
      default:
        return '💡';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading insights...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">Optimization Insights</h2>
        <p className="text-gray-600">AI-powered recommendations to optimize your AWS costs</p>
      </div>

      {/* Filters */}
      <div className="flex gap-3 mb-8">
        {['all', 'High', 'Medium', 'Low'].map((priority) => (
          <button
            key={priority}
            onClick={() => setFilter(priority)}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              filter === priority
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            {priority === 'all' ? 'All' : `${priority} Priority`}
            {priority !== 'all' && ` (${insights.filter(i => i.priority === priority).length})`}
          </button>
        ))}
      </div>

      {/* Insights Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredInsights.map((insight, index) => (
          <div
            key={index}
            className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-600 hover:shadow-lg transition animate-slide-in"
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">{getCategoryIcon(insight.category)}</span>
                  <h3 className="text-lg font-bold text-gray-800">{insight.title}</h3>
                </div>
                <p className="text-xs text-gray-500">{insight.category}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getPriorityColor(insight.priority)}`}>
                {insight.priority}
              </span>
            </div>

            {/* Description */}
            <p className="text-gray-700 text-sm mb-4">{insight.description}</p>

            {/* Recommendation */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
              <p className="text-xs font-semibold text-blue-900 mb-1">Recommendation:</p>
              <p className="text-sm text-blue-800">{insight.recommendation}</p>
            </div>

            {/* Savings */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200">
              <div className="flex items-center gap-2">
                <TrendingUp className="text-green-600" size={20} />
                <span className="text-sm text-gray-600">Potential Savings</span>
              </div>
              <span className="text-2xl font-bold text-green-600">
                ${insight.potential_savings.toLocaleString()}
              </span>
            </div>
          </div>
        ))}
      </div>

      {filteredInsights.length === 0 && (
        <div className="text-center py-12">
          <AlertCircle className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600">No insights found for the selected filter.</p>
        </div>
      )}

      {/* Summary */}
      {insights.length > 0 && (
        <div className="mt-8 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg p-6">
          <h3 className="text-lg font-bold mb-4">Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-purple-200 text-sm mb-1">Total Insights</p>
              <p className="text-3xl font-bold">{insights.length}</p>
            </div>
            <div>
              <p className="text-purple-200 text-sm mb-1">Total Potential Savings</p>
              <p className="text-3xl font-bold">${insights.reduce((sum, i) => sum + i.potential_savings, 0).toLocaleString()}</p>
            </div>
            <div>
              <p className="text-purple-200 text-sm mb-1">High Priority Actions</p>
              <p className="text-3xl font-bold">{insights.filter(i => i.priority === 'High').length}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default InsightsPanel;
