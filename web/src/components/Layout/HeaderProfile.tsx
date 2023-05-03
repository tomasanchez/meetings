import { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext, { AuthContextType } from "../../store/auth-context";

export const HeaderProfile = () => {
  const authCtx = useContext(AuthContext) as AuthContextType;

  return (
    <>
      {!authCtx.user && <Link to={`/login`}>Iniciar sesión</Link>}
      {authCtx.user && <Link to={'/'} onClick={authCtx.logout}>Cerrar sesión</Link>}
    </>
  );
};
