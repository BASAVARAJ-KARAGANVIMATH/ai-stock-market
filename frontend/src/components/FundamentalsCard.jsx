export default function FundamentalsCard({ fundamentals, analysis, loading }) {
  if (loading && !fundamentals) return <div className="text-muted text-sm">Loading…</div>;
  if (!fundamentals) return <div className="text-muted text-sm">No fundamentals available.</div>;

  return (
    <div className="flex flex-col gap-4">
      {/* Analysis Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-700">
        <div>
          <div className="text-sm text-muted">Fundamental Rating</div>
          <div className="text-xs text-secondary mt-1">{analysis?.explanation}</div>
        </div>
        <div className="text-right">
          <span className={badgeClass(analysis?.classification)}>{analysis?.classification || 'N/A'}</span>
          {typeof analysis?.total_score === 'number' && (
            <div className="text-xs text-muted mt-1">Score: {analysis.total_score}/14</div>
          )}
        </div>
      </div>

      {/* Detailed Scores */}
      {analysis?.scores && (
        <div>
          <div className="text-xs font-bold text-muted mb-2">
            Scoring Breakdown
          </div>
          <div className="grid grid-cols-2 gap-2" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr' }}>
            {Object.entries(analysis.scores).map(([metric, score]) => (
              <div key={metric} className="flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800">
                <span className="text-xs text-secondary">{metric}</span>
                <span className={`text-xs font-bold ${score === 2 ? 'text-emerald-400' : score === 1 ? 'text-amber-400' : 'text-red-400'}`}>
                  {score}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Raw Metrics */}
      <div className="pt-4 border-t border-slate-700">
        <div className="text-xs font-bold text-muted mb-3">
          Key Metrics Data
        </div>
        <div className="grid grid-cols-2 gap-3" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr' }}>
          <MetricRow label="Market Cap" value={fundamentals.market_cap} format="compact" />
          <MetricRow label="P/E Ratio" value={fundamentals.pe_ratio} />
          <MetricRow label="P/B Ratio" value={fundamentals.price_to_book} />
          <MetricRow label="ROE" value={fundamentals.return_on_equity} format="percent" />
          <MetricRow label="Debt/Eq" value={fundamentals.debt_to_equity} />
          <MetricRow label="EPS (TTM)" value={fundamentals.eps} />
          <MetricRow label="Book Val" value={fundamentals.book_value} />
          <MetricRow label="Div Yield" value={fundamentals.dividend_yield} format="percent" />
        </div>
      </div>
    </div>
  );
}

const MetricRow = ({ label, value, format }) => (
  <div className="flex justify-between items-center">
    <span className="text-xs text-muted">{label}</span>
    <span className="text-sm text-primary font-medium">
      {format === 'percent' && value ? `${(value * 100).toFixed(2)}%` :
        format === 'compact' ? formatValue(value) :
          formatValue(value)}
    </span>
  </div>
);

const badgeClass = (rating) => {
  if (!rating) return 'badge warning';
  const r = rating.toLowerCase();
  if (r === 'strong') return 'badge success';
  if (r === 'weak') return 'badge danger';
  return 'badge warning';
};

const formatValue = (val) => {
  if (val === null || val === undefined) return '-';
  if (typeof val === 'number') {
    if (val >= 1000000000000) return `${(val / 1000000000000).toFixed(2)}T`;
    if (val >= 1000000000) return `${(val / 1000000000).toFixed(2)}B`;
    if (val >= 1000000) return `${(val / 1000000).toFixed(2)}M`;
    if (val >= 1000) return `${(val / 1000).toFixed(2)}K`;
    return val.toFixed(2);
  }
  return val;
};

