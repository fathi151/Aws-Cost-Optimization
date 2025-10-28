import React, { useState } from 'react';
import axios from 'axios';
import { Download, Loader, FileText } from 'lucide-react';

const API_BASE = 'http://localhost:5000/api';

function ReportsPanel() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateReport = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/report`);
      if (response.data.status === 'success') {
        setReport(response.data.report);
      }
    } catch (error) {
      console.error('Error generating report:', error);
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    if (!report) return;
    
    const element = document.createElement('a');
    const file = new Blob([report], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `finops-report-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="p-8 h-full flex flex-col">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">Optimization Report</h2>
        <p className="text-gray-600">Generate comprehensive AWS cost optimization reports</p>
      </div>

      {/* Generate Button */}
      <div className="mb-8">
        <button
          onClick={generateReport}
          disabled={loading}
          className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg transition flex items-center gap-2 font-semibold"
        >
          {loading ? (
            <>
              <Loader className="animate-spin" size={20} />
              Generating Report...
            </>
          ) : (
            <>
              <FileText size={20} />
              Generate Report
            </>
          )}
        </button>
      </div>

      {/* Report Content */}
      {report && (
        <div className="flex-1 flex flex-col bg-white rounded-lg shadow-md overflow-hidden">
          {/* Report Header */}
          <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white p-6 flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold">AWS FinOps Optimization Report</h3>
              <p className="text-purple-200 text-sm mt-1">Generated on {new Date().toLocaleString()}</p>
            </div>
            <button
              onClick={downloadReport}
              className="bg-white text-purple-600 hover:bg-purple-50 px-4 py-2 rounded-lg transition flex items-center gap-2 font-semibold"
            >
              <Download size={18} />
              Download
            </button>
          </div>

          {/* Report Content */}
          <div className="flex-1 overflow-y-auto p-6">
            <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono">
              {report}
            </pre>
          </div>
        </div>
      )}

      {!report && !loading && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <FileText className="mx-auto text-gray-400 mb-4" size={64} />
            <p className="text-gray-600 text-lg mb-4">No report generated yet</p>
            <p className="text-gray-500">Click the button above to generate a comprehensive optimization report</p>
          </div>
        </div>
      )}

      {loading && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Generating your optimization report...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default ReportsPanel;
