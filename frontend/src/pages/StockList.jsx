import React from 'react';

export default function StockList() {
    const stocks = [
        // Banking & Financial Services
        { symbol: "HDFCBANK.NS", name: "HDFC Bank Ltd.", sector: "Banking" },
        { symbol: "ICICIBANK.NS", name: "ICICI Bank Ltd.", sector: "Banking" },
        { symbol: "SBIN.NS", name: "State Bank of India", sector: "Banking" },
        { symbol: "KOTAKBANK.NS", name: "Kotak Mahindra Bank Ltd.", sector: "Banking" },
        { symbol: "AXISBANK.NS", name: "Axis Bank Ltd.", sector: "Banking" },
        { symbol: "BAJFINANCE.NS", name: "Bajaj Finance Ltd.", sector: "Financial Services" },
        { symbol: "HDFCLIFE.NS", name: "HDFC Life Insurance Company Ltd.", sector: "Insurance" },
        { symbol: "SBILIFE.NS", name: "SBI Life Insurance Company Ltd.", sector: "Insurance" },

        // Information Technology
        { symbol: "TCS.NS", name: "Tata Consultancy Services Ltd.", sector: "IT Services" },
        { symbol: "INFY.NS", name: "Infosys Ltd.", sector: "IT Services" },
        { symbol: "WIPRO.NS", name: "Wipro Ltd.", sector: "IT Services" },
        { symbol: "HCLTECH.NS", name: "HCL Technologies Ltd.", sector: "IT Services" },
        { symbol: "TECHM.NS", name: "Tech Mahindra Ltd.", sector: "IT Services" },

        // Energy & Oil
        { symbol: "RELIANCE.NS", name: "Reliance Industries Ltd.", sector: "Oil & Gas" },
        { symbol: "ONGC.NS", name: "Oil and Natural Gas Corporation Ltd.", sector: "Oil & Gas" },
        { symbol: "BPCL.NS", name: "Bharat Petroleum Corporation Ltd.", sector: "Oil & Gas" },
        { symbol: "IOC.NS", name: "Indian Oil Corporation Ltd.", sector: "Oil & Gas" },
        { symbol: "POWERGRID.NS", name: "Power Grid Corporation of India Ltd.", sector: "Power" },
        { symbol: "NTPC.NS", name: "NTPC Ltd.", sector: "Power" },

        // Automobile
        { symbol: "TATAMOTORS.NS", name: "Tata Motors Ltd.", sector: "Automobile" },
        { symbol: "MARUTI.NS", name: "Maruti Suzuki India Ltd.", sector: "Automobile" },
        { symbol: "M&M.NS", name: "Mahindra & Mahindra Ltd.", sector: "Automobile" },
        { symbol: "BAJAJ-AUTO.NS", name: "Bajaj Auto Ltd.", sector: "Automobile" },
        { symbol: "HEROMOTOCO.NS", name: "Hero MotoCorp Ltd.", sector: "Automobile" },
        { symbol: "EICHERMOT.NS", name: "Eicher Motors Ltd.", sector: "Automobile" },

        // Consumer Goods & FMCG
        { symbol: "HINDUNILVR.NS", name: "Hindustan Unilever Ltd.", sector: "FMCG" },
        { symbol: "ITC.NS", name: "ITC Ltd.", sector: "FMCG" },
        { symbol: "NESTLEIND.NS", name: "Nestle India Ltd.", sector: "FMCG" },
        { symbol: "BRITANNIA.NS", name: "Britannia Industries Ltd.", sector: "FMCG" },
        { symbol: "DABUR.NS", name: "Dabur India Ltd.", sector: "FMCG" },
        { symbol: "GODREJCP.NS", name: "Godrej Consumer Products Ltd.", sector: "FMCG" },
        { symbol: "TITAN.NS", name: "Titan Company Ltd.", sector: "Consumer Durables" },
        { symbol: "ASIANPAINT.NS", name: "Asian Paints Ltd.", sector: "Paints" },

        // Pharmaceuticals & Healthcare
        { symbol: "SUNPHARMA.NS", name: "Sun Pharmaceutical Industries Ltd.", sector: "Pharma" },
        { symbol: "DRREDDY.NS", name: "Dr. Reddy's Laboratories Ltd.", sector: "Pharma" },
        { symbol: "CIPLA.NS", name: "Cipla Ltd.", sector: "Pharma" },
        { symbol: "DIVISLAB.NS", name: "Divi's Laboratories Ltd.", sector: "Pharma" },
        { symbol: "APOLLOHOSP.NS", name: "Apollo Hospitals Enterprise Ltd.", sector: "Healthcare" },

        // Telecommunication & Media
        { symbol: "BHARTIARTL.NS", name: "Bharti Airtel Ltd.", sector: "Telecom" },
        { symbol: "ZEEL.NS", name: "Zee Entertainment Enterprises Ltd.", sector: "Media" },

        // Infrastructure & Construction
        { symbol: "LT.NS", name: "Larsen & Toubro Ltd.", sector: "Construction" },
        { symbol: "ULTRACEMCO.NS", name: "UltraTech Cement Ltd.", sector: "Cement" },
        { symbol: "GRASIM.NS", name: "Grasim Industries Ltd.", sector: "Cement" },
        { symbol: "ADANIPORTS.NS", name: "Adani Ports and Special Economic Zone Ltd.", sector: "Infrastructure" },

        // Metals & Mining
        { symbol: "TATASTEEL.NS", name: "Tata Steel Ltd.", sector: "Metals" },
        { symbol: "HINDALCO.NS", name: "Hindalco Industries Ltd.", sector: "Metals" },
        { symbol: "COALINDIA.NS", name: "Coal India Ltd.", sector: "Mining" },
        { symbol: "VEDL.NS", name: "Vedanta Ltd.", sector: "Mining" },

        // E-commerce & Technology
        { symbol: "ZOMATO.NS", name: "Zomato Ltd.", sector: "Food Tech" },
        { symbol: "NYKAA.NS", name: "FSN E-Commerce Ventures Ltd. (Nykaa)", sector: "E-commerce" },

        // Others
        { symbol: "ADANIENT.NS", name: "Adani Enterprises Ltd.", sector: "Conglomerate" },
        { symbol: "INDIGO.NS", name: "InterGlobe Aviation Ltd. (IndiGo)", sector: "Aviation" },
    ];

    return (
        <div className="page-container">
            <section className="stock-container">
                <h1>Indian Stock Market - Top Companies</h1>
                <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
                    A comprehensive list of {stocks.length} popular stocks across various sectors in the Indian market.
                </p>

                <table className="stock-table">
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Company Name</th>
                            <th>Sector</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stocks.map((stock) => (
                            <tr key={stock.symbol}>
                                <td className="stock-ticker">{stock.symbol}</td>
                                <td>{stock.name}</td>
                                <td>{stock.sector}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                <div style={{ marginTop: '2rem', padding: '1rem', background: 'rgba(0, 210, 255, 0.1)', borderRadius: '0.5rem', borderLeft: '3px solid var(--primary-color)' }}>
                    <p style={{ margin: 0, fontSize: '0.9rem' }}>
                        💡 <strong>Note:</strong> These stocks are available for analysis on our platform.
                        Use the Dashboard to search for any stock and get AI-powered recommendations.
                    </p>
                </div>
            </section>
        </div>
    );
}
