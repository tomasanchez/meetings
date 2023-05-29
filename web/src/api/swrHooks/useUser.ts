import useSWR from "swr";

interface Token {
  email: string;
  exp: number;
  id: string;
  role: string;
  username: string;
}

// mock the user api
const userFetcher = async () => {

  const data = localStorage.getItem('login')
  if (data) {

    const decodedToken: Token = JSON.parse(atob(data.split('.')[1])); // Decodifica los datos del token
    return decodedToken
  }

  // not authorized
  // throw new Error("Not authorized!")
};


export default function useUser() {
  const { data, mutate, error } = useSWR<Token | null>("/users/me", userFetcher);

  const loading = !data && !error;
  const loggedOut = error && error.status === 403;

  return {
    loading,
    loggedOut,
    user: data,
    mutate
  };
}
