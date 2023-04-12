import React, {useState} from 'react'
import AuthContext from './auth-context'

export const AuthProvider = (props) => {

    const [user, setUser] = useState(null)

    const login = (userData) => {

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
