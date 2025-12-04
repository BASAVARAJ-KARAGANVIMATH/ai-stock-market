import axios from 'axios';

const client = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' });

export async function getPrediction(symbol) {
  const { data } = await client.get(`/api/predict/${encodeURIComponent(symbol)}`);
  return data;
}

