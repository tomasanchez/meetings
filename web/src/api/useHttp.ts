import { useState, useCallback } from 'react';

interface RequestConfig {
    url: string,
    method?: string,
    headers?: any,
    body?: any
}

export const useHttp = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null)

  const sendRequest = useCallback(async (requestConfig: RequestConfig) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(requestConfig.url, {
        method: requestConfig.method ? requestConfig.method : 'GET',
        headers: requestConfig.headers ? requestConfig.headers : {},
        body: requestConfig.body ? JSON.stringify(requestConfig.body) : null,
      });

      if (!response.ok) {
        throw new Error('Algo falló');
      }

      const data = await response.json();
      setData(data)
    } catch (err: any ) {
      setError(err.message || 'Algo falló!');
    }
    setIsLoading(false);
  }, []);

  return {
    isLoading,
    error,
    data,
  };
};