import React from 'react';

export default function NewsFeed({ news = [], loading }) {
  if (loading && (!news || news.length === 0)) return <div className="muted">Loading news…</div>;
  if (!news || news.length === 0) return <div className="muted">No recent news.</div>;

  return (
    <div className="news-list">
      {news.map((n, idx) => (
        <div key={idx} className="news-item">
          <a href={n.url} target="_blank" rel="noreferrer">{n.title}</a>
          {n.source?.name && <div className="muted">{n.source.name}</div>}
          {n.publishedAt && <div className="muted">{new Date(n.publishedAt).toLocaleString()}</div>}
        </div>
      ))}
    </div>
  );
}

