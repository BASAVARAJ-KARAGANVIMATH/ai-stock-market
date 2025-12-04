import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path ? 'active' : '';
    };

    return (
        <nav className="navbar">
            <Link to="/" className="logo">StockLife AI</Link>
            <div className="nav-links">
                <Link to="/" className={isActive('/')}>Home</Link>
                <Link to="/stocklist" className={isActive('/stocklist')}>Stock List</Link>
                <Link to="/learn" className={isActive('/learn')}>Learn</Link>
                <Link to="/about" className={isActive('/about')}>About</Link>
                <Link to="/dashboard" className="btn-dashboard">Dashboard</Link>
            </div>
        </nav>
    );
}
