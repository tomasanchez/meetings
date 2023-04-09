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

  return (
    <AuthContext.Provider value={ {user,login,logout} }>
    {props.children}
    </AuthContext.Provider>  )
}
