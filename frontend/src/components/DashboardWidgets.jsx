import React from 'react';

export default function DashboardWidgets({ data }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-dark-800 p-6 rounded-xl border border-dark-700 shadow-lg hover:border-brand-500 transition-colors">
        <h3 className="text-gray-400 font-medium mb-1">Videos Generated Today</h3>
        <p className="text-4xl font-bold text-white">{data.videos_day}</p>
        <span className="text-sm text-green-400 mt-2 inline-block">↑ Velocity Mode Active</span>
      </div>

      <div className="bg-dark-800 p-6 rounded-xl border border-dark-700 shadow-lg hover:border-purple-500 transition-colors">
        <h3 className="text-gray-400 font-medium mb-1">Total Views</h3>
        <p className="text-4xl font-bold text-white">{data.views.toLocaleString()}</p>
        <span className="text-sm text-green-400 mt-2 inline-block">↑ Scaling Engine active on 2 videos</span>
      </div>

      <div className="bg-dark-800 p-6 rounded-xl border border-dark-700 shadow-lg hover:border-green-500 transition-colors">
        <h3 className="text-gray-400 font-medium mb-1">Revenue Today</h3>
        <p className="text-4xl font-bold text-green-400">${data.revenue.toFixed(2)}</p>
        <span className="text-sm text-gray-500 mt-2 inline-block">Attributed across 4 active funnels</span>
      </div>
    </div>
  );
}
