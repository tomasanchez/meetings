export const fetcher = async (input: RequestInfo | URL, init?: RequestInit | undefined) => {
    const url = import.meta.env.VITE_URL
    fetch(url+input, init).then(res => res.json())
}