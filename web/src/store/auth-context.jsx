import React from 'react'

const AuthContext = React.createContext({
    user: '',
    login: () => {},
    logout: () => {}
})

export default AuthContext