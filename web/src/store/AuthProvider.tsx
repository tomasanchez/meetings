import { ReactNode, useState } from "react";
import AuthContext from "./auth-context";
import { LoginRequest, RegisterRequest } from "../api/models/dataApi";

interface AuthProvProps {
  children: ReactNode;
}

const url = import.meta.env.VITE_URL


export const AuthProvider = (props: AuthProvProps) => {
  const [user, setUser] = useState(null);

  const login = async (userData: LoginRequest) => {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    };

    const response = await fetch(
      url+"auth/token",
      requestOptions
    );
    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("user", data.data.token);
      setUser(data.data);
      return;
    }
    throw new Error(response.status.toString());
  };

  const logout = () => {
    localStorage.removeItem("user");
    setUser(null);
  };

  const register = async (userData: RegisterRequest) => {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    };

    const response = await fetch(
      url+"users/",
      requestOptions
    );
    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("user", data.data.token);
      setUser(data.data);
      return;
    }

    throw new Error(response.status.toString());
  };
  const authContext = { user, login, logout, register };

  return (
    <AuthContext.Provider value={authContext}>
      {props.children}
    </AuthContext.Provider>
  );
};
