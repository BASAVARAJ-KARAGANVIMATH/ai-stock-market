import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
    return (
        <div className="page-container">
            <section className="hero">
                <h1>Master the Market with AI</h1>
                <p>Get real-time analysis, fundamental insights, and AI-powered recommendations for Indian stocks.</p>
                <div className="cta-buttons">
                    <Link to="/dashboard" className="btn-primary">Go to Dashboard</Link>
                    <Link to="/learn" className="btn-secondary">Learn More</Link>
                </div>
            </section>
        </div>
    );
}
