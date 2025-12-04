import axios from 'axios';

const client = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' });

export async function getNews(symbol) {
  const { data } = await client.get(`/api/news/${encodeURIComponent(symbol)}`);
  return data;
}

