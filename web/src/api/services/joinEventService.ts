const url = import.meta.env.VITE_URL


export async function joinEventService(id: string, username: string) {
    
    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({"username": username})
    };

    return fetch(url+`scheduler-service/schedules/${id}/relationships/guests`,requestOptions ).then(res => res.json())
  }