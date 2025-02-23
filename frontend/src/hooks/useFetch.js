import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

export const useFetch = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!url) return; // Avoid making API calls when URL is null
    const controller = new AbortController();
    const { signal } = controller;

    try {
      setLoading(true);
      setError(null);
      const response = await api({ url, ...options, signal }); // Dynamic HTTP method support
      setData(response.data);
    } catch (err) {
      if (!signal.aborted) {
        setError(err.response?.data?.error || 'An error occurred');
      }
    } finally {
      if (!signal.aborted) {
        setLoading(false);
      }
    }

    return () => controller.abort(); // Cleanup function to cancel API request
  }, [url, JSON.stringify(options)]); // Re-run when URL or options change

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
};
