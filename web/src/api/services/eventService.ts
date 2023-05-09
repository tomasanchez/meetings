import { EventRequest, ToggleVotingRequest, VoteRequest } from "../models/dataApi";

const url = import.meta.env.VITE_URL


export async function addEvent(urlInput: string, { arg }: { arg: EventRequest }) {

    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(arg)
    };

    return fetch(url + urlInput, requestOptions).then(res => res.json())
}

export async function joinEvent(urlEvent: string,  { arg }: { arg: string }) {

    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({username: arg})
    };

    return fetch(url + `${urlEvent}/relationships/guests`, requestOptions).then(res => res.json())
}

export async function voteOption(urlEvent: string, { arg }: { arg: VoteRequest }) {

    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(arg)
    };

    return fetch(url + `${urlEvent}/options`, requestOptions).then(res => res.json())
}


export async function toggleVoting(urlEvento: string, { arg }: {arg: ToggleVotingRequest}) {

    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(arg)
    };

    return fetch(url + `${urlEvento}/voting`, requestOptions).then(res => res.json())
}