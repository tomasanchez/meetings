import { Link } from "react-router-dom";
import useUser from "../../api/swrHooks/useUser";
import { logout } from "../../api/services/authService";

export const HeaderProfile = () => {

  const { user, mutate } = useUser();
  const handleLogOut = () => {
    logout();
    mutate(null)
  }
  return (
    <>
      {!user && <Link to={`/login`}>Iniciar sesión</Link>}
      {user && <Link to={'/'} onClick={handleLogOut}>Cerrar sesión</Link>}
    </>
  );
};
