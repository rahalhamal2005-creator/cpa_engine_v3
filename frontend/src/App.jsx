import React, { useState, useEffect } from 'react';
import DashboardWidgets from './components/DashboardWidgets';

function App() {
  const [data, setData] = useState({
    videos_day: 0,
    views: 0,
    revenue: 0
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // In production, fetch from /api/dashboard
    setData({
      videos_day: 32,
      views: 184500,
      revenue: 554.20
    });
  }, []);

  const forceRun = () => {
    setLoading(true);
    // fetch('/api/force_run', { method: 'POST' })
    setTimeout(() => {
      setLoading(false);
      alert('Autonomous Cycle Started!');
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-dark-900 text-white font-sans p-6">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              CPA Gaming Profit Engine v3
            </h1>
            <p className="text-gray-400 mt-2">Autonomous Execution & Tracking Dashboard</p>
          </div>
          <button 
            onClick={forceRun}
            disabled={loading}
            className="bg-brand-500 hover:bg-brand-400 text-white px-6 py-2 rounded-lg font-semibold transition-colors disabled:opacity-50"
          >
            {loading ? 'Booting Cycle...' : 'Force Engine Run (Override)'}
          </button>
        </header>

        <DashboardWidgets data={data} />
      </div>
    </div>
  )
}

export default App;
