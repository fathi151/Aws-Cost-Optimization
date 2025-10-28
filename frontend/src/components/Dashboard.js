import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, AlertCircle, Zap } from 'lucide-react';

const API_BASE = 'http://localhost:5000/api';
const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'];

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [summaryRes, insightsRes] = await Promise.all([
        axios.get(`${API_BASE}/summary`),
        axios.get(`${API_BASE}/insights`)
      ]);

      setSummary(summaryRes.data);
      setInsights(insightsRes.data.insights || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const topInsights = insights.slice(0, 5);
  const highPriority = insights.filter(i => i.priority === 'High').length;
  const mediumPriority = insights.filter(i => i.priority === 'Medium').length;

  const priorityData = [
    { name: 'High', value: highPriority, color: '#ef4444' },
    { name: 'Medium', value: mediumPriority, color: '#f59e0b' },
    { name: 'Low', value: insights.filter(i => i.priority === 'Low').length, color: '#10b981' }
  ];

  const savingsByCategory = insights.reduce((acc, insight) => {
    const existing = acc.find(i => i.name === insight.category);
    if (existing) {
      existing.value += insight.potential_savings;
    } else {
      acc.push({ name: insight.category, value: insight.potential_savings });
    }
    return acc;
  }, []);

  return (
    <div className="p-8 space-y-8">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-semibold">Total Insights</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">{summary?.total_insights || 0}</p>
            </div>
            <Zap className="text-purple-600" size={32} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-semibold">Total Savings</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">${(summary?.total_potential_savings || 0).toLocaleString()}</p>
            </div>
            <TrendingUp className="text-green-600" size={32} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-semibold">Data Points</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">{(summary?.collection_stats?.cost_records || 0).toLocaleString()}</p>
            </div>
            <AlertCircle className="text-blue-600" size={32} />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-semibold">High Priority</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">{highPriority}</p>
            </div>
            <AlertCircle className="text-orange-600" size={32} />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Priority Distribution */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Insights by Priority</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={priorityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {priorityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Savings by Category */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Potential Savings by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={savingsByCategory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              <Bar dataKey="value" fill="#667eea" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Insights */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">Top Optimization Opportunities</h3>
        <div className="space-y-4">
          {topInsights.map((insight, index) => (
            <div key={index} className="border-l-4 border-purple-600 pl-4 py-2">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-800">{insight.title}</h4>
                  <p className="text-gray-600 text-sm mt-1">{insight.description}</p>
                  <p className="text-gray-700 text-sm mt-2">
                    <strong>Recommendation:</strong> {insight.recommendation}
                  </p>
                </div>
                <div className="text-right ml-4">
                  <div className="text-2xl font-bold text-green-600">
                    ${insight.potential_savings.toLocaleString()}
                  </div>
                  <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold mt-2 ${
                    insight.priority === 'High' ? 'bg-red-100 text-red-800' :
                    insight.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {insight.priority} Priority
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
