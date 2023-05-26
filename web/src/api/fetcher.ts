import ResponseError from "./models/dataApi"

export const fetcher = async (input: RequestInfo | URL, init?: RequestInit | undefined) :Promise<any> => {
    const url = import.meta.env.VITE_URL 

    const res = await fetch(url+input, init)
 
    if (!res.ok) {
      const error = new ResponseError('An error occurred while fetching the data.')
      // Attach extra info to the error object.
      error.info = await res.json()
      error.status = res.status
      throw error
    }
   
    return res.json()
  }