import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import LineChartCard from './LineChartCard';

/**
 * Dashboard component with full light / dark‑mode support.
 * Tailwind's `dark:` variants are added everywhere a color appears.
 */
function Dashboard({ setIsAuthenticated }) {
  // ────────────────────────────────────────────────────────────────────────────
  // STATE
  // ────────────────────────────────────────────────────────────────────────────
  const [prediction, setPrediction] = useState(null);
  const [timestamp, setTimestamp] = useState(null);
  const [predictionHistory, setPredictionHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [searchDate, setSearchDate] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const navigate = useNavigate();

  // colour of the live value (green / red / yellow)
  const [predictionColor, setPredictionColor] = useState('text-indigo-600');
  const [prevPrediction, setPrevPrediction] = useState(() => {
    const saved = localStorage.getItem('prevPrediction');
    return saved ? parseFloat(saved) : null;
  });

  // ────────────────────────────────────────────────────────────────────────────
  // EFFECTS – fetch data
  // ────────────────────────────────────────────────────────────────────────────
  const fetchHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const { data } = await axios.get('http://localhost:8000/prediction/history', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPredictionHistory(data.history);
      setFilteredHistory(data.history);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    }
  };

  const fetchPrediction = async () => {
    try {
      const token = localStorage.getItem('token');
      const { data } = await axios.get('http://localhost:8000/prediction', {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (data.status === 'ready') {
        const newPrediction = data.prediction;
        if (prevPrediction !== null) {
          const diff = newPrediction - prevPrediction;
          if (diff > 0.00001) setPredictionColor('text-green-500');
          else if (diff < -0.00001) setPredictionColor('text-red-500');
          else setPredictionColor('text-yellow-500');
        }
        setPrevPrediction(newPrediction);
        localStorage.setItem('prevPrediction', newPrediction);
        setPrediction(newPrediction);
        setTimestamp(data.timestamp);
      }
      setError(null);
    } catch (err) {
      if (err.response?.status === 401) {
        setIsAuthenticated(false);
        navigate('/login');
      } else {
        setError('Failed to fetch prediction');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // initial load + polling every 10s
  useEffect(() => {
    (async () => {
      await fetchHistory();
      await fetchPrediction();
    })();
    const interval = setInterval(fetchPrediction, 10_000);
    return () => clearInterval(interval);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ────────────────────────────────────────────────────────────────────────────
  // THEME: persist & toggle
  // ────────────────────────────────────────────────────────────────────────────
  useEffect(() => {
    const stored = localStorage.getItem('theme');
    if (stored === 'dark') setDarkMode(true);
  }, []);

  useEffect(() => {
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  // ────────────────────────────────────────────────────────────────────────────
  // HELPERS
  // ────────────────────────────────────────────────────────────────────────────
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('prevPrediction');
    setIsAuthenticated(false);
    navigate('/login');
  };

  // ────────────────────────────────────────────────────────────────────────────
  // HELPERS
  // ────────────────────────────────────────────────────────────────────────────
  const calcAverageSince = (now, days) => {
    const since = new Date(now);
    since.setDate(now.getDate() - days);
    const recent = predictionHistory.filter((p) => new Date(p.timestamp) >= since);
    if (!recent.length) return null;
    return recent.reduce((acc, p) => acc + p.prediction, 0) / recent.length;
  };

  const now = new Date();
  const todayAvg = calcAverageSince(now, 1);
  const weekAvg = calcAverageSince(now, 7);
  const monthAvg = calcAverageSince(now, 30);

  // chart data (kept for possible future use)
  const chartData = [...filteredHistory]
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
    .map((p) => ({ time: new Date(p.timestamp).toLocaleTimeString(), value: p.prediction }));



  const diff = prevPrediction !== null ? +(prediction - prevPrediction).toFixed(4) : 0;
  const diffColor = diff > 0 ? 'text-green-500' : diff < 0 ? 'text-red-500' : 'text-gray-400';
  const diffIcon = diff > 0 ? '🔺' : diff < 0 ? '🔻' : '⭘';

  // filter helpers -----------------------------------------------------------
  const applyFilter = (type) => {
    setFilter(type);
    const now = new Date();
    let filtered;
    if (type === 'today') {
      filtered = predictionHistory.filter((item) => new Date(item.timestamp).toDateString() === now.toDateString());
    } else if (type === '7days') {
      const sevenDaysAgo = new Date(now);
      sevenDaysAgo.setDate(now.getDate() - 7);
      filtered = predictionHistory.filter((item) => new Date(item.timestamp) >= sevenDaysAgo);
    } else {
      filtered = predictionHistory;
    }
    setFilteredHistory(filtered);
  };

  const handleSearchDate = (e) => {
    const selected = e.target.value;
    setSearchDate(selected);
    if (!selected) return applyFilter(filter);
    const filtered = predictionHistory.filter((item) => new Date(item.timestamp).toISOString().split('T')[0] === selected);
    setFilteredHistory(filtered);
  };

  // copy & csv helpers -------------------------------------------------------
  const handleCopyHistory = () => {
    const text = filteredHistory.map((p) => `${new Date(p.timestamp).toLocaleString()} - ${p.prediction.toFixed(4)}`).join('\n');
    navigator.clipboard.writeText(text).then(() => alert('History copied!')).catch(() => alert('Copy failed'));
  };

  const handleDownloadCSV = () => {
    const csv = `Timestamp,Prediction\n${filteredHistory
      .map((p) => `"${new Date(p.timestamp).toLocaleString('ru-RU').replace(',', '')}",${p.prediction.toFixed(4)}`)
      .join('\n')}`;
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
    link.download = 'prediction_history.csv';
    link.click();
  };

  const buildSvgPath = (data, w, h, pad = 40) => {
  if (!data.length) return { path: '', points: [] };

  const xs = data.map((_, i) =>
    pad + ((w - 2 * pad) * i) / (data.length - 1 || 1)
  );
  const values = data.map((d) => d.value);
  const minY = Math.min(...values);
  const maxY = Math.max(...values);
  const ys = values.map(
    (v) => pad + ((h - 2 * pad) * (1 - (v - minY) / (maxY - minY || 1)))
  );

  const points = xs.map((x, i) => [x, ys[i]]);
  const path = points
    .map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`)
    .join(' ');

  return { path, points };
};

  const catmullRom2bezier = (points) => {
  // возвращает строку «C … C …» для вставки в path
  if (points.length < 2) return '';
  const d = [];
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[i - 1] || points[i];
    const p1 = points[i];
    const p2 = points[i + 1];
    const p3 = points[i + 2] || p2;
    const cp1x = p1[0] + (p2[0] - p0[0]) / 6;
    const cp1y = p1[1] + (p2[1] - p0[1]) / 6;
    const cp2x = p2[0] - (p3[0] - p1[0]) / 6;
    const cp2y = p2[1] - (p3[1] - p1[1]) / 6;
    d.push(
      `C${cp1x.toFixed(1)},${cp1y.toFixed(1)} ` +
        `${cp2x.toFixed(1)},${cp2y.toFixed(1)} ` +
        `${p2[0].toFixed(1)},${p2[1].toFixed(1)}`
    );
  }
  return d.join(' ');
};



  // ────────────────────────────────────────────────────────────────────────────
  // RENDER
  // ────────────────────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      {/* ─── NAVBAR ───────────────────────────────────────────────────────────*/}
      <nav className="bg-white dark:bg-gray-800 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-xl sm:text-2xl font-bold">ML Prediction Service</h1>

            <div className="flex items-center gap-3">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="px-3 py-1 text-sm rounded-md bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
              >
                {darkMode ? '☀️ Light' : '🌙 Dark'}
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-1 text-sm rounded-md text-white bg-red-600 hover:bg-red-700 transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* ─── MAIN CONTENT ─────────────────────────────────────────────────────*/}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 space-y-6">
        {/* error banner */}
        {error && (
          <div className="bg-red-100 dark:bg-red-700/30 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* cards grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Current prediction */}
          <section className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8 flex flex-col items-center">
          <h2 className="text-xl font-semibold mb-6 text-gray-900 dark:text-gray-100">
            Current Prediction
          </h2>

          {prediction !== null ? (
            <>
              {/* само значение */}
              <p className={`text-5xl font-bold mb-1 ${predictionColor}`}>
                {prediction.toFixed(4)}
              </p>

              {/* дельта */}
              <p className={`text-sm font-medium ${diffColor}`}>
                {diffIcon}{' '}
                {diff === 0 ? '0' : Math.abs(diff).toFixed(4)}
              </p>

              <span className="mt-1 text-xs text-gray-600 dark:text-gray-400">
                Last updated: {timestamp ? new Date(timestamp).toLocaleString() : 'N/A'}
              </span>
            </>
          ) : (
            <p className="text-lg text-gray-600 dark:text-gray-400">
              {isLoading ? 'Loading…' : 'No data'}
            </p>
          )}
        </section>

          {/* Averages */}
          <section className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8">
            <h2 className="text-xl font-semibold mb-6 text-gray-900 dark:text-gray-100">Averages</h2>
            <div className="grid grid-cols-3 text-center gap-4">
              {[
                { label: 'Today', value: todayAvg },
                { label: 'Last 7 Days', value: weekAvg },
                { label: 'Last 30 Days', value: monthAvg },
              ].map(({ label, value }) => (
                <div key={label}>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">{label}</p>
                  <p className="text-2xl font-bold text-indigo-600">{value !== null ? value.toFixed(4) : '—'}</p>
                </div>
              ))}
            </div>
          </section>
        </div>

        {/* History card */}
        <section className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Prediction History</h2>

          {/* filters */}
          <div className="flex flex-wrap items-center gap-3 mb-4">
            {[
              { id: 'today', label: 'Today' },
              { id: '7days', label: 'Last 7 Days' },
              { id: 'all', label: 'All' },
            ].map(({ id, label }) => (
              <button
                key={id}
                onClick={() => applyFilter(id)}
                className="px-3 py-1 text-sm rounded bg-blue-100 dark:bg-blue-800 text-blue-900 dark:text-blue-100 hover:bg-blue-200 dark:hover:bg-blue-700"
              >
                {label}
              </button>
            ))}
            <input
              type="date"
              value={searchDate}
              onChange={handleSearchDate}
              className="ml-auto p-1 text-sm bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded"
            />
            <button
              onClick={handleCopyHistory}
              className="px-3 py-1 text-sm rounded bg-green-500 hover:bg-green-600 text-white"
            >
              Copy
            </button>
            <button
              onClick={handleDownloadCSV}
              className="px-3 py-1 text-sm rounded bg-blue-500 hover:bg-blue-600 text-white"
            >
              Download CSV
            </button>
          </div>

          {/* table */}
          <div className="overflow-y-auto max-h-[400px] rounded-md">
            <table className="w-full text-sm">
              <thead className="bg-gray-200 dark:bg-gray-700 sticky top-0">
                <tr>
                  <th className="px-4 py-2 text-left font-medium">Time</th>
                  <th className="px-4 py-2 text-left font-medium">Value</th>
                </tr>
              </thead>
              <tbody>
                {filteredHistory.map((pred, idx) => (
                  <tr
                    key={idx}
                    className={idx % 2 === 0 ? 'bg-white dark:bg-gray-900' : 'bg-gray-50 dark:bg-gray-800'}
                  >
                    <td className="px-4 py-2 text-gray-700 dark:text-gray-300 whitespace-nowrap">
                      {new Date(pred.timestamp).toLocaleString()}
                    </td>
                    <td className="px-4 py-2 font-semibold text-gray-900 dark:text-gray-100 whitespace-nowrap">
                      {pred.prediction.toFixed(4)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <LineChartCard data={chartData} />

      </main>
    </div>
  );
}

export default Dashboard;
