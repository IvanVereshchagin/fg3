import React from 'react';
import {
  ResponsiveContainer,
  ComposedChart,   
  Area,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts';

export default function LineChartCard({ data }) {
  if (!data.length) return null;

  return (
    <section className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8">
      <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">
        Линейный график
      </h2>

      <ResponsiveContainer width="100%" height={300}>
      
        <ComposedChart
          data={data}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
     
          <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6366f1" stopOpacity={0.25} />
              <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.15} />
          <XAxis dataKey="time" tick={{ fill: '#9ca3af', fontSize: 12 }} minTickGap={40} />
          <YAxis tick={{ fill: '#9ca3af', fontSize: 12 }} width={60} domain={['auto', 'auto']} />
          <Tooltip
            contentStyle={{ background: '#1f2937', border: 'none', borderRadius: 8 }}
            labelStyle={{ color: '#d1d5db' }}
            itemStyle={{ color: '#fbbf24' }}
          />

          {/* area-подложка */}
          <Area type="monotone" dataKey="value" fill="url(#colorUv)" stroke="none" />
          {/* сама линия */}
          <Line
            type="monotone"
            dataKey="value"
            stroke="#6366f1"
            strokeWidth={2}
            dot={{ r: 3 }}
            activeDot={{ r: 5 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </section>
  );
}
