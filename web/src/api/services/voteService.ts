import { VoteRequest } from "../models/dataApi";

const url = import.meta.env.VITE_URL


export async function voteOption(id: string, vote: VoteRequest) {
    
    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(vote)
    };

    return fetch(url+`scheduler-service/schedules/${id}/options`,requestOptions ).then(res => res.json())
  }