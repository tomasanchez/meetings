import Swal from "sweetalert2";
import { EventRequest, ToggleVotingRequest, VoteRequest } from "../models/dataApi";

const url = import.meta.env.VITE_URL


export async function addEvent(urlInput: string, { arg }: { arg: EventRequest }) {
    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('login')}`
        },
        body: JSON.stringify(arg)
    };

    const response = await fetch(url+urlInput, requestOptions)
    const data = await response.json()
    
    if (!response.ok) {
        Swal.fire({
            title: 'Error',
            text: data.detail,
            icon: 'error',
            confirmButtonText: 'OK'
          });
        throw new Error(data.detail);
    }
    return data;
}

export async function joinEvent(urlEvent: string,  { arg }: { arg: string }) {

    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('login')}`
        },
        body: JSON.stringify({username: arg})
    };

    const response = await fetch(url+`${urlEvent}/relationships/guests`, requestOptions)
    const data = await response.json()
    
    if (!response.ok) {
        Swal.fire({
            title: 'Error',
            text: data.detail,
            icon: 'error',
            confirmButtonText: 'OK'
          });
        throw new Error(data.detail);
    }
    return data;
}

export async function voteOption(urlEvent: string, { arg }: { arg: VoteRequest }) {

    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('login')}`
        },
        body: JSON.stringify(arg)
    };

    const response = await fetch(url+`${urlEvent}/options`, requestOptions)
    const data = await response.json()
    
    if (!response.ok) {
        Swal.fire({
            title: 'Error',
            text: data.detail,
            icon: 'error',
            confirmButtonText: 'OK'
          });
        throw new Error(data.detail);
    }
    return data;
}


export async function toggleVoting(urlEvento: string, { arg }: {arg: ToggleVotingRequest}) {

    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('login')}`
        },
        body: JSON.stringify(arg)
    };

    const response = await fetch(url+`${urlEvento}/voting`, requestOptions)
    const data = await response.json()
    
    if (!response.ok) {
        Swal.fire({
            title: 'Error',
            text: data.detail,
            icon: 'error',
            confirmButtonText: 'OK'
          });
        throw new Error(data.detail);
    }
    return data;
}