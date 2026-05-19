import React, { useState, useEffect } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import axios from 'axios';

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [activeTab, setActiveTab] = useState('constellation');
  const [conflicts, setConflicts] = useState([]);

  useEffect(() => {
    // Fetch mock graph data
    setGraphData({
      nodes: [
        { id: 'Nishant', type: 'PERSON', color: '#ff0000' },
        { id: 'Universal AI Layer', type: 'TECH_STACK', color: '#00ff00' },
        { id: 'WinOptimizer', type: 'TOOL', color: '#0000ff' },
        { id: 'AuthService', type: 'CLASS', color: '#facc15' }
      ],
      links: [
        { source: 'Nishant', target: 'Universal AI Layer', label: 'OWNS' },
        { source: 'Nishant', target: 'WinOptimizer', label: 'OWNS' },
        { source: 'Universal AI Layer', target: 'AuthService', label: 'CONTAINS' }
      ]
    });

    // Mock conflicts
    setConflicts([
      { 
        id1: 1, 
        text1: "Server uses Port 80", 
        id2: 2, 
        text2: "Server uses Port 443", 
        reason: "Logical contradiction on port assignment" 
      }
    ]);
  }, []);

  return (
    <div className="h-screen w-screen bg-slate-900 text-white flex flex-col overflow-hidden font-sans">
      <nav className="bg-slate-800 p-4 flex justify-between items-center border-b border-slate-700">
        <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
          Universal AI Layer v4.0
        </h1>
        <div className="flex gap-4">
          <button 
            onClick={() => setActiveTab('constellation')}
            className={`px-4 py-2 rounded-lg transition ${activeTab === 'constellation' ? 'bg-blue-600' : 'hover:bg-slate-700'}`}
          >
            Constellation
          </button>
          <button 
            onClick={() => setActiveTab('conflicts')}
            className={`px-4 py-2 rounded-lg transition ${activeTab === 'conflicts' ? 'bg-red-600' : 'hover:bg-slate-700'}`}
          >
            Conflicts ({conflicts.length})
          </button>
          <button 
            onClick={() => setActiveTab('impact')}
            className={`px-4 py-2 rounded-lg transition ${activeTab === 'impact' ? 'bg-emerald-600' : 'hover:bg-slate-700'}`}
          >
            Impact Analysis
          </button>
        </div>
      </nav>

      <main className="flex-1 relative">
        {activeTab === 'constellation' && (
          <ForceGraph2D
            graphData={graphData}
            nodeLabel="id"
            nodeAutoColorBy="type"
            linkDirectionalArrowLength={3.5}
            linkDirectionalArrowRelPos={1}
            linkLabel="label"
            backgroundColor="#0f172a"
          />
        )}

        {activeTab === 'conflicts' && (
          <div className="p-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 overflow-y-auto h-full">
            {conflicts.map((conflict, idx) => (
              <div key={idx} className="bg-slate-800 p-6 rounded-xl border border-red-900/30">
                <h3 className="text-red-400 font-bold mb-4">Contradiction Detected</h3>
                <div className="space-y-4 mb-6">
                  <div className="p-3 bg-slate-900 rounded border border-slate-700 italic">"{conflict.text1}"</div>
                  <div className="text-center text-slate-500 font-bold">VS</div>
                  <div className="p-3 bg-slate-900 rounded border border-slate-700 italic">"{conflict.text2}"</div>
                </div>
                <p className="text-sm text-slate-400 mb-6">Reason: {conflict.reason}</p>
                <div className="flex gap-2">
                  <button className="flex-1 bg-blue-600/20 hover:bg-blue-600 py-2 rounded transition">Keep 1</button>
                  <button className="flex-1 bg-emerald-600/20 hover:bg-emerald-600 py-2 rounded transition">Keep 2</button>
                  <button className="flex-1 bg-slate-700 hover:bg-slate-600 py-2 rounded transition">Merge</button>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'impact' && (
          <div className="p-8 max-w-4xl mx-auto h-full overflow-y-auto">
            <h2 className="text-2xl font-bold mb-6">Simulation: Core Principle Change</h2>
            <div className="bg-slate-800 p-6 rounded-xl mb-8">
              <label className="block text-slate-400 text-sm mb-2">Architectural Principle</label>
              <textarea 
                className="w-full bg-slate-900 border border-slate-700 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                rows="3"
                defaultValue="All authentication must go through the centralized AuthService via OAuth 2.0."
              />
              <button className="mt-4 bg-emerald-600 px-6 py-2 rounded-lg hover:bg-emerald-500 transition font-bold">
                Run Impact Analysis
              </button>
            </div>
            <div className="space-y-4">
              <h3 className="text-slate-400 font-bold uppercase tracking-wider text-xs">High Impact Areas</h3>
              <div className="p-4 bg-slate-800/50 rounded-lg border-l-4 border-red-500">
                <span className="font-bold">AuthService.py</span> - Directly implements this logic.
              </div>
              <div className="p-4 bg-slate-800/50 rounded-lg border-l-4 border-yellow-500">
                <span className="font-bold">LoginController.ts</span> - Uses AuthService for token validation.
              </div>
              <div className="p-4 bg-slate-800/50 rounded-lg border-l-4 border-slate-500">
                <span className="font-bold">Database Schema</span> - Stores OAuth tokens.
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
