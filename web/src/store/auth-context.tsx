import React from 'react'

export interface AuthContextType  {
    user: string | null,
    login: ( _: string ) => void,
    logout: () => void
}

const AuthContext = React.createContext<AuthContextType | null>(null)

export default AuthContext