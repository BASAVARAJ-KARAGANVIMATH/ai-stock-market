import React from 'react';

export default function About() {
    return (
        <div className="page-container">
            <section className="about-section">
                <h1>About StockLife AI</h1>
                <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Empowering investors with data-driven insights.</p>

                <div className="about-content">
                    <p>StockLife AI is an advanced stock analysis platform designed to help for beginner investors make informed decisions. By combining real-time market data with powerful AI algorithms, we provide actionable insights and recommendations.</p>

                    <div className="feature-list">
                        <div className="feature-item">
                            <span className="feature-icon">🚀</span>
                            <div>
                                <h3>AI Recommendations</h3>
                                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Smart buy/sell signals based on technical and fundamental analysis.</p>
                            </div>
                        </div>
                        <div className="feature-item">
                            <span className="feature-icon">📊</span>
                            <div>
                                <h3>Real-time Data</h3>
                                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Live stock prices and market updates.</p>
                            </div>
                        </div>
                        <div className="feature-item">
                            <span className="feature-icon">📈</span>
                            <div>
                                <h3>Company Fundamentals</h3>
                                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Comprehensive financial data including P/E ratio, Market Cap, and more.</p>
                            </div>
                        </div>
                        <div className="feature-item">
                            <span className="feature-icon">📰</span>
                            <div>
                                <h3>Latest News</h3>
                                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Stay updated with the latest market news and trends affecting your stocks.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
