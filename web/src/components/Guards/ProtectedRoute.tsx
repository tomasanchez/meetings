import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import useUser from "../../api/swrHooks/useUser";
import { useEffect } from "react";

type Props = {
  redirectTo?: string;
  children?: React.ReactNode;
};

export const ProtectedRoute = ({ children }: Props) => {
  const navigate = useNavigate();
  const { user } = useUser();

  useEffect(() => {
    if (!user) {
      Swal.fire({
        title: "Error",
        text: "Por favor inicie sesion",
        icon: "error",
        confirmButtonText: "OK",
      });
      navigate("/login");

    }
  }, [user]);

  return <> {children} </>;
};
