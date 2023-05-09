import { LoginRequest, RegisterRequest } from "../models/dataApi";
import Swal from 'sweetalert2';

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
        Swal.fire({
            title: 'Error',
            text: data.detail,
            icon: 'error',
            confirmButtonText: 'OK'
          });
        throw new Error(data.detail);
    }
    localStorage.setItem(LOCALSTORAGE_NAME, data.data.token)
};

export const logout = () => {
    localStorage.removeItem(LOCALSTORAGE_NAME)
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
    await login({username: userData.username, password: userData.password})
};
