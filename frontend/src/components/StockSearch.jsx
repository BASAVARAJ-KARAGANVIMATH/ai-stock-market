import React, { useState, useEffect, useRef } from 'react';
import { searchStock } from '../api/stockApi';

export default function StockSearch({ defaultValue, onSearch, loading }) {
  const [val, setVal] = useState(defaultValue || '');
  const [suggestions, setSuggestions] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [error, setError] = useState(null);
  const wrapperRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = async (e) => {
    const value = e.target.value;
    setVal(value);
    setError(null);

    if (value.length >= 1) {
      try {
        const results = await searchStock(value);
        setSuggestions(results);
        setShowDropdown(true);
      } catch (err) {
        console.error(err);
        setSuggestions([]);
      }
    } else {
      setSuggestions([]);
      setShowDropdown(false);
    }
  };

  const handleSelect = (symbol) => {
    setVal(symbol);
    setShowDropdown(false);
    onSearch(symbol);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (val) {
      onSearch(val);
    }
  };

  return (
    <div className="autocomplete-wrapper" ref={wrapperRef}>
      <form onSubmit={handleSubmit} className="search-container">
        <div className="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <input
          type="text"
          className="search-input"
          value={val}
          onChange={handleInputChange}
          placeholder="Enter stock symbol (e.g., RELIANCE.BSE)"
          disabled={loading}
          onFocus={() => val.length >= 1 && setShowDropdown(true)}
        />
        <button type="submit" className="analyze-btn" disabled={loading}>
          {loading ? 'Loading...' : 'ANALYZE'}
        </button>
      </form>
      {showDropdown && suggestions.length > 0 && (
        <div className="autocomplete-dropdown">
          {suggestions.map((s) => (
            <div
              key={s.symbol}
              className="autocomplete-item"
              onClick={() => handleSelect(s.symbol)}
            >
              <span className="symbol">{s.symbol}</span>
              <span className="name">{s.name}</span>
            </div>
          ))}
        </div>
      )}
      {error && <div className="search-error">{error}</div>}
    </div>
  );
}

