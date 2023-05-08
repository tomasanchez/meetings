const url = import.meta.env.VITE_URL

export async function toggleVotingService(id: string, username: string, voting: boolean) {
    
    const requestOptions = {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({"username": username, "voting": voting})
    };

    return fetch(url+`scheduler-service/schedules/${id}/voting`,requestOptions ).then(res => res.json())
  }