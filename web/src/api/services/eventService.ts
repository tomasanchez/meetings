import { EventRequest } from "../models/dataApi";

const url = import.meta.env.VITE_URL


export async function addEvent(urlInput: string, { arg }: {arg: EventRequest} ) {
    
    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(arg)
    };

    return fetch(url+urlInput,requestOptions ).then(res => res.json())
  }