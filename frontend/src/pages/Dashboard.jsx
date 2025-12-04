import React, { useCallback, useEffect, useMemo, useState } from 'react';
import StockSearch from '../components/StockSearch.jsx';
import StockChart from '../components/StockChart.jsx';
import FundamentalsCard from '../components/FundamentalsCard.jsx';
import RecommendationCard from '../components/RecommendationCard.jsx';
import NewsFeed from '../components/NewsFeed.jsx';
import { getStock } from '../api/stockApi.js';
import { getPrediction } from '../api/predictApi.js';
import { getNews } from '../api/newsApi.js';

export default function Dashboard() {
  const [symbol, setSymbol] = useState('RELIANCE.BSE');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [stockData, setStockData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [news, setNews] = useState([]);

  const fetchAll = useCallback(async (sym) => {
    if (!sym) return;
    setLoading(true);
    setError('');
    try {
      const [s, p, n] = await Promise.all([
        getStock(sym),
        getPrediction(sym),
        getNews(sym)
      ]);
      setStockData(s);
      setPrediction(p);
      setNews(n?.articles || n?.news || []);

      // Backend now returns single clean error or null
      if (s?.error) {
        setError(s.error);
      } else if (p?.error) {
        setError(p.error);
      } else if (n?.error) {
        setError(n.error);
      } else {
        setError('');
      }
    } catch (e) {
      // Clean error message for network/unexpected errors
      setError("Unable to load stock data. Please try again or select a different stock.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchAll(symbol); }, [fetchAll, symbol]);

  const chartData = useMemo(() => {
    if (!stockData?.prices) return { fullData: [] };
    // Prices come sorted descending (latest first), reverse for chronological order
    const fullData = [...stockData.prices].reverse();
    return { fullData };
  }, [stockData]);

  return (
    <div className="flex-col gap-4">
      <div className="grid-layout">
        {/* Search Section */}
        <div className="card" style={{ gridColumn: '1 / -1' }}>
          <StockSearch
            defaultValue={symbol}
            onSearch={(val) => setSymbol(val.trim())}
            loading={loading}
          />
          {error && (
            <div className="badge danger" style={{ marginTop: '1rem', width: '100%', justifyContent: 'center', padding: '1rem' }}>
              <span>⚠️ {error}</span>
              {error.includes('rate limit') && (
                <div className="text-xs" style={{ marginTop: '0.5rem', opacity: 0.8 }}>
                  Tip: Alpha Vantage free tier allows 5 calls per minute. Please wait 60 seconds.
                </div>
              )}
            </div>
          )}
        </div>

        {/* Main Chart Area */}
        <div className="card" style={{ gridColumn: 'span 8' }}>
          <div className="card-header">
            <div className="flex flex-col">
              <h3>{stockData?.company_name || symbol}</h3>
              <div className="flex items-center gap-2">
                {stockData?.prices && stockData.prices.length > 0 ? (
                  <span className="text-xl font-bold">₹{Number(stockData.prices[0].close).toFixed(2)}</span>
                ) : stockData?.price ? (
                  <span className="text-xl font-bold">₹{Number(stockData.price).toFixed(2)}</span>
                ) : null}
              </div>
            </div>
          </div>
          <StockChart data={chartData.fullData} loading={loading} />
        </div>

        {/* Fundamentals Side Panel */}
        <div className="card" style={{ gridColumn: 'span 4' }}>
          <div className="card-header">
            <h3>Fundamentals</h3>
          </div>
          <FundamentalsCard fundamentals={stockData?.fundamentals} analysis={stockData?.fundamental_analysis} loading={loading} />
        </div>

        {/* AI Recommendation */}
        <div className="card" style={{ gridColumn: 'span 4' }}>
          <div className="card-header">
            <h3>AI Recommendation</h3>
          </div>
          <RecommendationCard recommendation={prediction} loading={loading} />
        </div>

        {/* News Feed */}
        <div className="card" style={{ gridColumn: 'span 8' }}>
          <div className="card-header">
            <h3>Latest News</h3>
          </div>
          <NewsFeed news={news} loading={loading} />
        </div>
      </div>

      {/* Mandatory Disclaimer Section */}
      <div className="disclaimer-section">
        <h4 className="text-sm font-bold" style={{ marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>DISCLAIMER</h4>
        <p>
          This Share Market Analysis and Recommendation system does NOT provide financial advice.
          All insights, predictions, and recommendations generated here are strictly for educational and research purposes only.
          Do your own due diligence before making investment decisions.
        </p>
      </div>
    </div>
  );
}

