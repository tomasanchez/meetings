import React from 'react'
import { LoginRequest, RegisterRequest } from '../api/models/dataApi'

export interface AuthContextType  {
    user: string | null,
    login: ( user : LoginRequest ) => Promise<any>,
    logout: () => void,
    register: (user : RegisterRequest) => any,
}

const AuthContext = React.createContext<AuthContextType | null>(null)

export default AuthContext