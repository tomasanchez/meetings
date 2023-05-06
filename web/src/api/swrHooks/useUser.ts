import useSWR from "swr";

// mock the user api
const userFetcher = async () => {

    const data = localStorage.getItem('login')
    if (data) {
      // authorized
      return data
    }
  
    // not authorized
    const error = new Error("Not authorized!");
    throw error;
  };
  

export default function useUser() {
  const { data, mutate, error } = useSWR<string | null>("/users/me", userFetcher);

  const loading = !data && !error;
  const loggedOut = error && error.status === 403;

  return {
    loading,
    loggedOut,
    user: data,
    mutate
  };
}
