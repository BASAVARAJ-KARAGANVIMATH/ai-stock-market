import React, { useMemo, useState } from 'react';
import Plot from 'react-plotly.js';

const TIMEFRAMES = [
  { label: '1D', days: 1 },
  { label: '7D', days: 7 },
  { label: '15D', days: 15 },
  { label: '30D', days: 30 },
  { label: '6M', days: 180 },
  { label: '1Y', days: 365 },
  { label: '5Y', days: 1825 },
];

export default function StockChart({ data, loading }) {
  const [timeframe, setTimeframe] = useState('1Y');

  const filteredData = useMemo(() => {
    if (!data || data.length === 0) return [];
    const days = TIMEFRAMES.find(t => t.label === timeframe)?.days || 365;
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - days);
    return data.filter(d => new Date(d.date) >= cutoff);
  }, [data, timeframe]);

  if (loading && (!data || data.length === 0)) {
    return (
      <div className="flex items-center justify-center h-64 text-muted text-sm bg-slate-900/50 rounded-lg">
        Loading chart data...
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-muted text-sm bg-slate-900/50 rounded-lg">
        No chart data available.
      </div>
    );
  }

  const dates = data.map(d => d.date);
  const closes = data.map(d => d.close);
  const opens = data.map(d => d.open);
  const highs = data.map(d => d.high);
  const lows = data.map(d => d.low);

  return (
    <div className="w-full h-full min-h-[400px] rounded-lg overflow-hidden border border-slate-800 bg-slate-900">
      <Plot
        data={[
          {
            x: dates,
            close: closes,
            decreasing: { line: { color: '#ef4444' } },
            high: highs,
            increasing: { line: { color: '#10b981' } },
            line: { color: 'rgba(31,119,180,1)' },
            low: lows,
            open: opens,
            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y',
            name: 'Price'
          }
        ]}
        layout={{
          dragmode: 'zoom',
          margin: { r: 40, t: 20, b: 40, l: 60 },
          showlegend: false,
          xaxis: {
            showgrid: true,
          },
          yaxis: {
            gridcolor: '#243044',
            tickprefix: '₹',
            showgrid: true,
          },
          height: 450,
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          font: {
            color: '#94a3b8',
            family: 'Inter, sans-serif'
          }
        }}
        config={{
          responsive: true,
          displayModeBar: true,
          displaylogo: false,
          modeBarButtonsToRemove: ['select2d', 'lasso2d']
        }}
        style={{ width: '100%' }}
        useResizeHandler
      />
    </div>
  );
}
