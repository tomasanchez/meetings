import { LoginRequest, RegisterRequest, RegisterResponse } from "../models/dataApi";

const LOCALSTORAGE_NAME = 'login'
const url = import.meta.env.VITE_URL


export const login = async (userData: LoginRequest) => {

    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData)
    };

    const response = await fetch(url+'auth-service/auth/token', requestOptions)
    const data = await response.json()

    if (!response.ok) {
        throw new Error(response.status.toString())
    }
    localStorage.setItem(LOCALSTORAGE_NAME, data.data.token)
    localStorage.setItem('username', userData.username)
};

export const logout = () => {
    localStorage.removeItem(LOCALSTORAGE_NAME)
    localStorage.removeItem('username')
}

export const register = async (userData: RegisterRequest) => {

    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData)
    };

    const response = await fetch(url+'auth-service/users', requestOptions)
    if (!response.ok) {
        throw new Error(response.status.toString())
    }
    const data = await response.json() as Promise<RegisterResponse>

    try {
        await login({username: userData.username, password: userData.password})
    } catch (error) {
        throw new Error('Login ERROR')

    }

};
