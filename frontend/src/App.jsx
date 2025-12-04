import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar.jsx';
import Home from './pages/Home.jsx';
import StockList from './pages/StockList.jsx';
import Learn from './pages/Learn.jsx';
import About from './pages/About.jsx';
import Dashboard from './pages/Dashboard.jsx';
import './styles.css';
import './autocomplete.css';

export default function App() {
  return (
    <Router>
      <div className="app-root">
        <Navbar />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/stocklist" element={<StockList />} />
            <Route path="/learn" element={<Learn />} />
            <Route path="/about" element={<About />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
        <footer className="app-footer">
          <div className="flex flex-col gap-2">
            <span>Data provided by Alpha Vantage & NewsAPI</span>
            <span className="text-muted">AI predictions are for demonstration only</span>
            <span className="text-muted">&copy; 2025 StockLife AI</span>
          </div>
        </footer>
      </div>
    </Router>
  );
}

