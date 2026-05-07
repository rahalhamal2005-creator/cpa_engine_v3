import React, { useState } from 'react';

export default function NicheFinder({ apiUrl }) {
  const [keyword, setKeyword] = useState('');
  const [country, setCountry] = useState('US');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!keyword) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiUrl}/api/niche/search?query=${encodeURIComponent(keyword)}&country=${encodeURIComponent(country)}`);
      if (!res.ok) throw new Error('Failed to fetch from backend');
      const data = await res.json();
      setResults(data.niches || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-dark-800 p-6 rounded-xl border border-dark-700 shadow-lg">
      <h2 className="text-2xl font-bold text-white mb-4">CPA Trend & Niche Analyzer</h2>
      <p className="text-gray-400 mb-6">Discover trending niches per country, view velocity, and CPA intent to dominate search results.</p>
      
      <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4 mb-8">
        <input 
          type="text" 
          placeholder="e.g. Mobile Games, Finance, Gift Cards..."
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          className="flex-1 bg-dark-900 border border-dark-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-brand-500"
        />
        <select 
          value={country} 
          onChange={(e) => setCountry(e.target.value)}
          className="bg-dark-900 border border-dark-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-brand-500"
        >
          <option value="US">🇺🇸 United States (Tier 1)</option>
          <option value="GB">🇬🇧 United Kingdom (Tier 1)</option>
          <option value="AU">🇦🇺 Australia (Tier 1)</option>
          <option value="FR">🇫🇷 France (Tier 2)</option>
          <option value="DE">🇩🇪 Germany (Tier 2)</option>
          <option value="BR">🇧🇷 Brazil (Tier 3)</option>
          <option value="MA">🇲🇦 Morocco (Tier 3)</option>
        </select>
        <button 
          type="submit" 
          disabled={loading}
          className="bg-brand-500 hover:bg-brand-400 text-white px-6 py-2 rounded-lg font-semibold transition-colors disabled:opacity-50 min-w-[150px]"
        >
          {loading ? 'Analyzing...' : 'Analyze Trends'}
        </button>
      </form>

      {error && <div className="text-red-400 mb-4">{error}</div>}

      <div className="space-y-4">
        {results.map((niche, idx) => (
          <div key={idx} className="bg-dark-900 p-5 rounded-lg border border-dark-600 hover:border-brand-500/50 transition-colors shadow-lg">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-2xl font-bold text-brand-300">{niche.game}</h3>
                <p className="text-red-400 font-semibold mt-1">🔥 Trending: {niche.trending_aspect}</p>
              </div>
              <span className="bg-dark-800 text-gray-300 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border border-dark-600">Target: {niche.audience}</span>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-6">
              <div className="bg-dark-800 p-3 rounded-md border border-dark-700">
                <span className="text-gray-500 block text-xs uppercase mb-1">Search Volume</span>
                <span className="text-white font-bold text-lg">{niche.search_volume}</span>
              </div>
              <div className="bg-dark-800 p-3 rounded-md border border-dark-700">
                <span className="text-gray-500 block text-xs uppercase mb-1">CPA Competition</span>
                <span className={`font-bold text-lg ${niche.competition === 'Low' ? 'text-green-400' : niche.competition === 'Medium' ? 'text-yellow-400' : 'text-red-400'}`}>{niche.competition}</span>
              </div>
              <div className="bg-dark-800 p-3 rounded-md border border-dark-700">
                <span className="text-gray-500 block text-xs uppercase mb-1">Avg YT Views</span>
                <span className="text-white font-bold text-lg">{niche.avg_views}</span>
              </div>
              <div className="bg-dark-800 p-3 rounded-md border border-dark-700">
                <span className="text-gray-500 block text-xs uppercase mb-1">Top Sources</span>
                <span className="text-brand-400 font-bold text-sm leading-tight">{niche.traffic_sources}</span>
              </div>
            </div>

            <div className="space-y-4 mt-2">
              {niche.viral_title && (
                <div className="bg-gradient-to-r from-yellow-900/20 to-orange-900/10 border border-yellow-700/50 p-4 rounded-lg shadow-inner">
                    <h4 className="text-yellow-400 text-sm font-bold mb-2 uppercase tracking-wide flex items-center gap-2">🔥 Viral Title Idea</h4>
                    <p className="text-white text-lg font-bold">"{niche.viral_title}"</p>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {niche.video_idea && (
                  <div className="bg-indigo-900/10 border border-indigo-900/40 p-4 rounded-lg">
                      <h4 className="text-indigo-400 text-sm font-bold mb-2 uppercase tracking-wide flex items-center gap-2">🎬 Video Idea</h4>
                      <p className="text-gray-300 text-sm leading-relaxed">{niche.video_idea}</p>
                  </div>
                )}
                
                {niche.cpa_integration && (
                  <div className="bg-pink-900/10 border border-pink-900/40 p-4 rounded-lg">
                      <h4 className="text-pink-400 text-sm font-bold mb-2 uppercase tracking-wide flex items-center gap-2">🔗 CPA Integration</h4>
                      <p className="text-gray-300 text-sm leading-relaxed mb-2">
                        <strong className="text-pink-300">Angle:</strong> {niche.offer_angle || 'Mod Menu / Free Skins'}
                      </p>
                      <p className="text-gray-300 text-sm leading-relaxed">
                        <strong className="text-pink-300">Call to Action:</strong> {niche.cpa_integration}
                      </p>
                  </div>
                )}
              </div>

              <div className="bg-blue-900/10 border border-blue-900/40 p-4 rounded-lg">
                  <h4 className="text-blue-400 text-sm font-bold mb-2 uppercase tracking-wide">📹 Promotion Strategy</h4>
                  <p className="text-gray-300 text-sm leading-relaxed">{niche.promotion_strategy}</p>
              </div>

              <div className="bg-green-900/10 border border-green-900/40 p-4 rounded-lg">
                  <h4 className="text-green-400 text-sm font-bold mb-2 uppercase tracking-wide">🔒 Content Locker Strategy</h4>
                  <p className="text-gray-300 text-sm leading-relaxed">{niche.locker_strategy}</p>
              </div>

              {niche.trend_prediction && (
                <div className="bg-purple-900/10 border border-purple-900/40 p-4 rounded-lg">
                    <h4 className="text-purple-400 text-sm font-bold mb-2 uppercase tracking-wide">📈 Trend Forecast</h4>
                    <p className="text-gray-300 text-sm leading-relaxed">{niche.trend_prediction}</p>
                </div>
              )}
            </div>
          </div>
        ))}
        {results.length === 0 && !loading && !error && (
            <div className="flex flex-col items-center justify-center py-16 border-2 border-dashed border-dark-600 rounded-xl text-gray-500">
                <svg className="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                <p>Select a country and enter a keyword to uncover CPA trends.</p>
            </div>
        )}
      </div>
    </div>
  );
}
