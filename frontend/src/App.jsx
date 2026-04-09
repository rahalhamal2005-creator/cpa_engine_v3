import React, { useState, useEffect } from 'react';
import DashboardWidgets from './components/DashboardWidgets';
import NicheFinder from './components/NicheFinder';

function App() {
  const [data, setData] = useState({
    videos_day: 0,
    views: 0,
    revenue: 0
  });

  const [loading, setLoading] = useState(false);

  const [activeTab, setActiveTab] = useState('dashboard');
  const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

  useEffect(() => {
    fetch(`${API_URL}/api/dashboard`)
      .then(res => res.json())
      .then(json => {
        if(json) setData(json);
      })
      .catch(err => console.error("Failed to fetch dashboard metrics", err));
  }, []);

  const forceRun = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/force_run`, { method: 'POST' });
      const responseJson = await res.json();
      alert(`Status: ${responseJson.message}`);
    } catch (err) {
      alert('Failed to trigger execution loop.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-900 text-white font-sans p-6">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              CPA Gaming Profit Engine v3
            </h1>
            <p className="text-gray-400 mt-2">Autonomous Execution & Workspace</p>
          </div>
          <div className="flex gap-4">
            <button 
              onClick={forceRun}
              disabled={loading}
              className="bg-purple-600 hover:bg-purple-500 text-white px-6 py-2 rounded-lg font-semibold transition-colors disabled:opacity-50"
            >
              {loading ? 'Booting Cycle...' : 'Force Engine Run'}
            </button>
          </div>
        </header>

        {/* Navigation Tabs */}
        <div className="flex gap-4 mb-8 border-b border-dark-700 pb-2">
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`px-4 py-2 font-medium transition-colors ${activeTab === 'dashboard' ? 'text-brand-400 border-b-2 border-brand-400' : 'text-gray-400 hover:text-white'}`}
          >
            Dashboard (Autopilot)
          </button>
          <button 
            onClick={() => setActiveTab('niche_finder')}
            className={`px-4 py-2 font-medium transition-colors ${activeTab === 'niche_finder' ? 'text-brand-400 border-b-2 border-brand-400' : 'text-gray-400 hover:text-white'}`}
          >
            Niche Finder (Manual)
          </button>
        </div>

        {activeTab === 'dashboard' && <DashboardWidgets data={data} />}
        {activeTab === 'niche_finder' && <NicheFinder apiUrl={API_URL} />}
      </div>
    </div>
  )
}


export default App;
