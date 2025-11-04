import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import InsightsPanel from './components/InsightsPanel';
import ReportsPanel from './components/ReportsPanel';
import EmailSupport from './components/EmailSupport';
import { Menu, X } from 'lucide-react';

const API_BASE = 'http://localhost:5000/api';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [stats, setStats] = useState({
    totalInsights: 0,
    totalSavings: 0,
    dataPoints: 0,
    status: 'Ready'
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    updateStats();
    const interval = setInterval(updateStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const updateStats = async () => {
    try {
      const response = await axios.get(`${API_BASE}/summary`);
      if (response.data.status === 'success' || response.data.status === 'active') {
        setStats({
          totalInsights: response.data.total_insights || 0,
          totalSavings: response.data.total_potential_savings || 0,
          dataPoints: response.data.collection_stats?.cost_records || 0,
          status: 'Ready'
        });
      }
    } catch (error) {
      console.error('Error updating stats:', error);
    }
  };

  const handleSync = async () => {
    setLoading(true);
    setStats(prev => ({ ...prev, status: 'Syncing...' }));
    try {
      const response = await axios.post(`${API_BASE}/sync`, { days: 30 });
      if (response.data.status === 'success') {
        setStats(prev => ({ ...prev, status: 'Ready' }));
        updateStats();
      }
    } catch (error) {
      console.error('Error syncing:', error);
      setStats(prev => ({ ...prev, status: 'Error' }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* AWS Header Bar */}
      <div className="h-12 bg-[#232F3E] flex items-center px-4 shadow-md">
        <div className="flex items-center gap-2">
          <span className="bg-[#FF9900] text-white px-2 py-1 text-sm font-bold rounded">AWS</span>
          <span className="text-white font-semibold">Cost Management Suite</span>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* AWS Sidebar */}
        <div className="w-60 bg-white border-r border-gray-300 flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Cost Management</h2>
          </div>

          {/* Navigation */}
          <div className="py-2">
            <button
              onClick={() => setActiveTab('chat')}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-50 transition-colors ${
                activeTab === 'chat'
                  ? 'bg-gray-50 border-l-4 border-[#FF9900] font-semibold pl-3'
                  : ''
              }`}
            >
              💬 Chat Assistant
            </button>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-50 transition-colors ${
                activeTab === 'dashboard'
                  ? 'bg-gray-50 border-l-4 border-[#FF9900] font-semibold pl-3'
                  : ''
              }`}
            >
              📊 Cost Explorer
            </button>
            <button
              onClick={() => setActiveTab('insights')}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-50 transition-colors ${
                activeTab === 'insights'
                  ? 'bg-gray-50 border-l-4 border-[#FF9900] font-semibold pl-3'
                  : ''
              }`}
            >
              💡 Recommendations
            </button>
            <button
              onClick={() => setActiveTab('reports')}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-50 transition-colors ${
                activeTab === 'reports'
                  ? 'bg-gray-50 border-l-4 border-[#FF9900] font-semibold pl-3'
                  : ''
              }`}
            >
              📈 Reports
            </button>
          </div>

          {/* Stats Cards */}
          <div className="flex-1 p-4 space-y-3 border-t border-gray-200">
            <div className="bg-gray-50 border border-gray-300 rounded p-3">
              <div className="text-xs text-gray-600 uppercase tracking-wider mb-1">Month-to-Date</div>
              <div className="text-xl font-bold text-[#FF9900]">${stats.totalSavings.toLocaleString()}</div>
            </div>
            <div className="bg-gray-50 border border-gray-300 rounded p-3">
              <div className="text-xs text-gray-600 uppercase tracking-wider mb-1">Recommendations</div>
              <div className="text-xl font-bold text-gray-900">{stats.totalInsights}</div>
            </div>
            <div className="bg-gray-50 border border-gray-300 rounded p-3">
              <div className="text-xs text-gray-600 uppercase tracking-wider mb-1">Resources</div>
              <div className="text-xl font-bold text-gray-900">{stats.dataPoints.toLocaleString()}</div>
            </div>
            <div className="bg-gray-50 border border-gray-300 rounded p-3">
              <div className="text-xs text-gray-600 uppercase tracking-wider mb-1">Status</div>
              <div className="text-sm font-semibold text-gray-900">{stats.status}</div>
            </div>
          </div>

          {/* Actions */}
          <div className="p-4 border-t border-gray-200 space-y-2">
            <button
              onClick={handleSync}
              disabled={loading}
              className="w-full bg-[#FF9900] hover:bg-[#ec7211] disabled:bg-gray-400 text-white py-2 px-4 rounded text-sm font-semibold transition-colors"
            >
              {loading ? 'Syncing...' : 'Sync Data'}
            </button>
            <button
              onClick={() => setActiveTab('reports')}
              className="w-full bg-white hover:bg-gray-50 text-gray-900 border border-gray-300 py-2 px-4 rounded text-sm font-semibold transition-colors"
            >
              Generate Report
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Content Header */}
          <div className="bg-white border-b border-gray-200 px-6 py-4">
            <h1 className="text-2xl font-semibold text-gray-900">
              {activeTab === 'chat' && 'Cost Optimization Assistant'}
              {activeTab === 'dashboard' && 'Cost Explorer Dashboard'}
              {activeTab === 'insights' && 'Cost Recommendations'}
              {activeTab === 'reports' && 'Cost Reports'}
               {activeTab === 'email' && 'Cost Reports'}
            </h1>
            <p className="text-sm text-gray-600 mt-1">Powered by AI-driven cost analysis</p>
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-auto bg-gray-50">
            {activeTab === 'dashboard' && <Dashboard />}
            {activeTab === 'chat' && <ChatInterface onStatsUpdate={updateStats} />}
            {activeTab === 'insights' && <InsightsPanel />}
            {activeTab === 'reports' && <ReportsPanel />}
            {activeTab==='email' && <EmailSupport />}
          </div>
        </div>
      </div>

      {/* Email Support Button */}
      <EmailSupport />
    </div>
  );
}

export default App;
