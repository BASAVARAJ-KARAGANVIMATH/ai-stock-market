import React from 'react';

export default function Learn() {
    return (
        <div className="page-container">
            <section className="hero" style={{ padding: '2rem 0' }}>
                <h1>Stock Market Basics</h1>
                <p>Master the fundamentals of investing and understand how AI-powered analysis works.</p>
            </section>

            <div className="learn-grid">
                <article className="learn-card">
                    <h2>📊 What Are Stocks?</h2>
                    <p><strong>Stocks are tiny pieces of a company.</strong></p>
                    <p>When you buy a stock, you're not gambling — you're literally buying a share of that business.</p>
                    <ul>
                        <li>If the company grows, earns more money, and becomes more valuable, the stock price usually goes up.</li>
                        <li>If the company struggles, the stock price usually drops.</li>
                    </ul>
                    <p style={{ marginTop: '1rem', fontWeight: 600 }}>Simple rule:</p>
                    <p>✅ Good companies → usually higher stock prices.</p>
                    <p>❌ Bad companies → usually lower stock prices.</p>
                </article>

                <article className="learn-card">
                    <h2>📈 What Are Fundamentals?</h2>
                    <p><strong>Fundamentals tell you if a company is strong or weak.</strong></p>
                    <p>They're basically the company's "health report."</p>
                    <p style={{ marginTop: '1rem', marginBottom: '0.5rem', fontWeight: 600 }}>The main fundamentals beginners should know:</p>
                    <ul>
                        <li><strong>Revenue:</strong> How much money the company brings in. More is better.</li>
                        <li><strong>Profit (Net Income):</strong> What's left after expenses. If this keeps growing, that's good.</li>
                        <li><strong>EPS (Earnings Per Share):</strong> Profit divided by number of shares. Rising EPS means the company is improving.</li>
                        <li><strong>Debt:</strong> How much the company owes. Too much debt = risky.</li>
                        <li><strong>PE Ratio:</strong> Price compared to earnings. High PE often means expensive. Low PE can mean cheap or declining.</li>
                        <li><strong>Free Cash Flow:</strong> Actual cash the company has leftover. More cash = more stability.</li>
                        <li><strong>Growth Rate:</strong> How fast revenue and profits are increasing.</li>
                    </ul>
                    <p style={{ marginTop: '1rem', fontStyle: 'italic' }}>If these fundamentals look strong, the stock is usually safer long-term.</p>
                </article>

                <article className="learn-card">
                    <h2>💰 What Does Buy / Sell Mean?</h2>
                    <p><strong>Buy:</strong></p>
                    <ul>
                        <li>You purchase a stock because you expect the price to rise.</li>
                        <li>You enter at a price you believe is lower than future value.</li>
                    </ul>
                    <p style={{ marginTop: '1rem' }}><strong>Sell:</strong></p>
                    <ul>
                        <li>You sell a stock when you think the price will fall, you want to take profit, or you want to limit losses.</li>
                    </ul>
                    <p style={{ marginTop: '1rem', fontWeight: 600 }}>The basic formula is simple:</p>
                    <p style={{ fontSize: '1.1rem', color: 'var(--primary-color)' }}>Buy low, sell high.</p>
                    <p style={{ color: 'var(--text-muted)' }}>Most people mess it up by letting emotions control them.</p>
                </article>

                <article className="learn-card">
                    <h2>🎯 How Buy/Sell Signals Work</h2>
                    <p>Buy/Sell signals are based on patterns in price, volume, trends, and momentum.</p>
                    <p style={{ marginTop: '1rem', fontWeight: 600 }}>A Buy signal usually appears when:</p>
                    <ul>
                        <li>The price is rising with strong momentum</li>
                        <li>Volume is increasing</li>
                        <li>Trends show upward direction</li>
                        <li>Risk indicators look stable</li>
                    </ul>
                    <p style={{ marginTop: '1rem', fontWeight: 600 }}>A Sell signal usually appears when:</p>
                    <ul>
                        <li>Momentum weakens</li>
                        <li>Price breaks downward</li>
                        <li>Volume spikes on selling</li>
                        <li>Risk indicators turn negative</li>
                    </ul>
                    <p style={{ marginTop: '1rem', fontStyle: 'italic' }}>The AI looks at these patterns faster than a human ever could.</p>
                </article>

                <article className="learn-card">
                    <h2>🤖 Why AI Helps Beginners</h2>
                    <p><strong>Beginners struggle because they:</strong></p>
                    <ul>
                        <li>Overthink</li>
                        <li>Trade emotionally</li>
                        <li>Don't understand trends</li>
                        <li>Don't know when to exit</li>
                        <li>React too slow</li>
                    </ul>
                    <p style={{ marginTop: '1rem', fontWeight: 600 }}>AI doesn't do any of that.</p>
                    <p>It reads market data, detects real patterns, and gives simple direction: <strong>Buy / Sell / Hold</strong>.</p>
                    <p style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(0, 210, 255, 0.1)', borderRadius: '0.5rem', borderLeft: '3px solid var(--primary-color)' }}>
                        💡 <strong>Pro Tip:</strong> Use AI as your guide, but always do your own research before investing real money.
                    </p>
                </article>

                <article className="learn-card">
                    <h2>⚠️ Important Disclaimer</h2>
                    <p style={{ color: 'var(--text-muted)' }}>
                        This platform is for <strong>educational and demonstration purposes only</strong>.
                        AI predictions are not guaranteed to be accurate. Always consult with a financial advisor
                        before making investment decisions. Past performance does not guarantee future results.
                    </p>
                </article>
            </div>
        </div>
    );
}
