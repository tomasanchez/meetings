import React, { useRef, useState, useContext } from "react";
import classes from "./LoginPage.module.css";
import { Button, BrandIcon } from "../components/UI";
import { useNavigate } from "react-router-dom";
import AuthContext from "../store/auth-context";

export const LoginPage = () => {
  const authCtx = useContext(AuthContext);
  const navigate = useNavigate();
  const loginInput = useRef();
  const passwordInput = useRef();
  const [errorLogin, seterrorLogin] = useState(false);

  const handleLogin = () => {
    if (passwordInput.current.value == "" || loginInput.current.value == "") {
      seterrorLogin(true);
      return;
    }

    authCtx.login(loginInput.current.value);
    navigate("/");
  };

  const resetErrors = () => {
    if (errorLogin) seterrorLogin(false);
  };

  const loginForm = (
    <form className="my-3">
      <div className="mb-4">
        <label htmlFor="username" className="form-label opacity-75 mb-0">
          Usuario
        </label>
        <input
          type="text"
          className={`${classes["form-control-login"]} form-control`}
          id="username"
          name="username"
          onBlur={resetErrors}
          ref={loginInput}
        />
      </div>
      <div className="mb-4">
        <label
          htmlFor="exampleInputPassword1"
          className="form-label opacity-75 mb-0"
        >
          Contraseña
        </label>
        <input
          type="password"
          className={`${classes["form-control-login"]} form-control`}
          id="password"
          name="password"
          onBlur={resetErrors}
          ref={passwordInput}
        />
      </div>
      {errorLogin && (
        <p className=" text-danger ">
          *El usuario y/o contraseña son incorrectos
        </p>
      )}
      <div className="d-flex justify-content-center ">
        <Button onClick={handleLogin}>Ingresar</Button>
      </div>
    </form>
  );

  return (
    <>
      <div className={`${classes.containerLogin} d-flex flex-column`}>
        <nav className={`${classes["nav-login"]} position-absolute nav-login`}>
          <BrandIcon />
        </nav>

        <div className={`${classes["background-max"]} d-none d-md-block`}></div>

        <div
          className={`${classes["login-card"]} d-flex flex-column bg-white rounded flex-grow-1 flex-md-grow-0`}
        >
          <h3 className="h3">
            ¡Hola! Para seguir, ingresá tu usuario y contraseña
          </h3>

          {loginForm}
        </div>
      </div>
    </>
  );
};
