import axios from 'axios';

const client = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' });

export async function getStock(symbol) {
  const { data } = await client.get(`/api/stock/${encodeURIComponent(symbol)}`);
  return data;
}

export async function searchStock(query) {
  const { data } = await client.get(`/api/stock/search?query=${encodeURIComponent(query)}`);
  return data;
}


