import React from 'react';

export default function RecommendationCard({ recommendation, loading }) {
  if (loading && !recommendation) return (
    <div className="flex items-center justify-center p-8 text-muted text-sm bg-slate-900/50 rounded-lg border border-slate-800">
      <span className="animate-pulse">Analyzing market data...</span>
    </div>
  );

  if (!recommendation) return (
    <div className="flex flex-col items-center justify-center p-8 text-muted text-sm bg-slate-900/50 rounded-lg border border-slate-800">
      <span>No AI recommendation available at this time.</span>
      <span className="text-xs mt-2 opacity-70">Try searching for a different stock or check back later.</span>
    </div>
  );

  const aiRec = recommendation.ai_recommendation || {};
  const action = aiRec.recommendation || 'Hold';
  const confidence = aiRec.confidence;
  const reasoning = aiRec.reasoning;

  const isBuy = action.toUpperCase().includes('BUY');
  const isSell = action.toUpperCase().includes('SELL');

  const borderColor = isBuy ? 'border-emerald-500/30' : isSell ? 'border-red-500/30' : 'border-amber-500/30';
  const bgColor = isBuy ? 'bg-emerald-500/10' : isSell ? 'bg-red-500/10' : 'bg-amber-500/10';

  return (
    <div className="flex flex-col gap-4">
      <div className={`flex flex-col items-center justify-center p-6 rounded-lg border ${borderColor} ${bgColor}`} style={{
        background: isBuy ? 'rgba(16, 185, 129, 0.1)' : isSell ? 'rgba(239, 68, 68, 0.1)' : 'rgba(245, 158, 11, 0.1)',
        borderColor: isBuy ? 'rgba(16, 185, 129, 0.3)' : isSell ? 'rgba(239, 68, 68, 0.3)' : 'rgba(245, 158, 11, 0.3)',
        borderWidth: '1px',
        borderStyle: 'solid'
      }}>
        <div className="text-sm text-muted mb-1">AI Verdict</div>
        <div className={`text-3xl font-bold tracking-wide`} style={{
          color: isBuy ? '#34d399' : isSell ? '#f87171' : '#fbbf24'
        }}>
          {action}
        </div>
        {confidence && (
          <div className="text-xs text-muted mt-2">Confidence: {(confidence * 100).toFixed(1)}%</div>
        )}
      </div>

      <div className="flex flex-col gap-2">
        <div className="text-xs font-bold text-muted">Reasoning</div>
        <p className="text-sm text-secondary leading-relaxed">
          {reasoning || "No detailed reasoning available."}
        </p>
      </div>
    </div>
  );
}
