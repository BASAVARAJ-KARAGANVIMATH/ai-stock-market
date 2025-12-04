import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_URL = "https://newsapi.org/v2/everything"


def clean_company_name(name: str) -> str:
    """
    Remove common legal suffixes from company name to get a cleaner search term.
    """
    if not name:
        return ""
    
    # Common suffixes to remove (case insensitive)
    suffixes = [
        " limited", " ltd", " public limited company", " pvt ltd", " private limited",
        " inc", " corp", " corporation", " sa", " ag", " nv", " plc"
    ]
    
    clean_name = name.lower()
    for suffix in suffixes:
        if clean_name.endswith(suffix):
            clean_name = clean_name[:-len(suffix)]
            break
            
    return clean_name.strip()

def fetch_news(symbol: str, company_name: str = None):
    """
    Fetch news articles for a specific stock symbol.
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE.BSE", "TCS.NS")
        company_name: Optional company name for better search results (e.g., "Reliance Industries Limited")
    
    Returns:
        List of news articles filtered for relevance to the specific company
    """
    if not NEWS_API_KEY:
        raise ValueError("NewsAPI key not set. Please set NEWS_API_KEY environment variable.")
    
    # Extract base company name from symbol (e.g., "RELIANCE.BSE" -> "RELIANCE")
    # Remove common suffixes like .BSE, .NSE, .NS, .BO
    clean_symbol = symbol.upper()
    for suffix in ['.BSE', '.NSE', '.NS', '.BO']:
        if clean_symbol.endswith(suffix):
            clean_symbol = clean_symbol[:-len(suffix)]
            break
    
    # Create a more specific search query using company name if available
    if company_name:
        # Use the cleaned company name OR the symbol for broader results
        cleaned_name = clean_company_name(company_name)
        # Query: ("Wipro" OR WIPRO) AND stock
        search_query = f'("{cleaned_name}" OR {clean_symbol}) AND stock'
    else:
        # Fallback to symbol-based search
        search_query = f"{clean_symbol} stock"
    
    params = {
        "q": search_query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "pageSize": 50,  # Fetch more to filter for relevance
    }
    r = requests.get(NEWS_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    
    # Check for API errors
    if data.get("status") == "error":
        error_msg = data.get("message", "Unknown error from NewsAPI")
        raise ValueError(f"NewsAPI error: {error_msg}")
    
    articles = data.get("articles", [])
    
    # Filter articles for relevance to the specific company
    filtered_articles = []
    search_terms = set()
    
    # Build search terms for filtering
    if company_name:
        # Add company name and variations
        search_terms.add(company_name.lower())
        cleaned_name = clean_company_name(company_name)
        search_terms.add(cleaned_name.lower())
        # Add individual words from company name (for partial matches)
        search_terms.update(word.lower() for word in cleaned_name.split() if len(word) > 3)
    
    # Add the clean symbol
    search_terms.add(clean_symbol.lower())
    
    for a in articles:
        if not a.get("title") or not a.get("url"):
            continue
            
        # Check if article mentions the company
        title = (a.get("title") or "").lower()
        description = (a.get("description") or "").lower()
        content = title + " " + description
        
        # Article is relevant if it mentions any of our search terms
        is_relevant = any(term in content for term in search_terms)
        
        if is_relevant:
            filtered_articles.append({
                "title": a.get("title"),
                "description": a.get("description"),
                "url": a.get("url"),
                "source": {"name": (a.get("source") or {}).get("name")},
                "publishedAt": a.get("publishedAt"),
            })
            
            # Limit to top 20 most recent relevant articles
            if len(filtered_articles) >= 20:
                break
    
    return filtered_articles


