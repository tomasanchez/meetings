import {ReactNode, useState} from 'react'
import AuthContext from './auth-context'

interface AuthProvProps {
    children: ReactNode
}

export const AuthProvider = (props: AuthProvProps) => {

    const [user, setUser] = useState(null)

    const login = (userData: any) => {

        localStorage.setItem('user',userData)
        setUser(userData)
    }

    const logout = () =>  {
        localStorage.removeItem('user')
        setUser(null);
    }

    const authContext = {user, login, logout}

  return (
    <AuthContext.Provider value={ authContext }>
    {props.children}
    </AuthContext.Provider>  )
}
