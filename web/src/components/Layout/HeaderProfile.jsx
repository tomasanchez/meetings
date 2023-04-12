import React, { useContext } from "react";
import {Link} from 'react-router-dom'
import AuthContext from "../../store/auth-context";

export const HeaderProfile = () => {
  const authCtx = useContext(AuthContext);

  return <>{!authCtx.user && <Link to={`/login`}>Iniciar sesión</Link>}
  {authCtx.user && <Link onClick={authCtx.logout} >Cerrar sesión</Link>}
  </>;
};
