export const fetcher = async (input: RequestInfo | URL, init?: RequestInit | undefined) :Promise<any> => {
    const url = import.meta.env.VITE_URL 
    return fetch(url+input, init).then(res => res.json())
}