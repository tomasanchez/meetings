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
  const repeatPassword = useRef();
  const [isLogin, setisLogin] = useState(true);
  const [errorLogin, seterrorLogin] = useState(false);
  const [errorRegister, seterrorRegister] = useState(false);

  const handleLogin = (event) => {
    event.preventDefault()
    if (passwordInput.current.value == "" || loginInput.current.value == "") {
      seterrorLogin(true);
      return;
    }

    authCtx.login(loginInput.current.value);
    navigate("/");
  };

  const resetErrors = () => {
    if (errorLogin) seterrorLogin(false);
    if (errorRegister) seterrorLogin(false);
  };

  const loginForm = (
    <form className="my-3" onSubmit={handleLogin} >
      <div className="mb-4">
        <label htmlFor="username" className="form-label opacity-75 mb-0">
          Usuario
        </label>
        <input
          type="text"
          className={`${classes["form-control-login"]} form-control`}
          id="username"
          name="username"
          required
          onBlur={resetErrors}
          ref={loginInput}
        />
      </div>
      <div className="mb-4">
        <label htmlFor="password" className="form-label opacity-75 mb-0">
          Contraseña
        </label>
        <input
          type="password"
          className={`${classes["form-control-login"]} form-control`}
          id="password"
          name="password"
          required
          onBlur={resetErrors}
          ref={passwordInput}
        />
        <span>
          ¿Eres nuevo?{" "}
          <span
            onClick={() => {
              setisLogin(false);
            }}
            className={`${classes["link_register"]}`}
          >
            Registrate acá
          </span>
        </span>
      </div>
      {errorLogin && (
        <p className=" text-danger ">
          *El usuario y/o contraseña son incorrectos
        </p>
      )}
      <div className="d-flex justify-content-center ">
        <Button type='submit'>Ingresar</Button>
      </div>
    </form>
  );

  const handleRegister = (event) => {
    event.preventDefault();
    if (passwordInput.current.value !== repeatPassword.current.value) {
      seterrorRegister(true);
      return;
    }

    authCtx.login(loginInput.current.value);
    navigate("/");
  };

  const registerForm = (
    <form className="my-3" onSubmit={handleRegister} >
      <div className="mb-4">
        <label htmlFor="username" className="form-label opacity-75 mb-0">
          Usuario
        </label>
        <input
          type="email"
          required
          placeholder="Ej: tacs@utn.edu.ar"
          className={`${classes["form-control-login"]} form-control`}
          id="username"
          name="username"
          ref={loginInput}
        />
      </div>
      <div className="mb-4">
        <label htmlFor="password" className="form-label opacity-75 mb-0">
          Contraseña
        </label>
        <input
          type="password"
          required
          className={`${classes["form-control-login"]} form-control`}
          id="password"
          name="password"
          ref={passwordInput}
        />
      </div>
      <div className="mb-4">
        <label htmlFor="repeatpassword" className="form-label opacity-75 mb-0">
          Repetí la contraseña
        </label>
        <input
          type="password"
          className={`${classes["form-control-login"]} form-control`}
          id="repeatpassword"
          required
          name="repeatpassword"
          ref={repeatPassword}
        />
        {errorRegister && (
          <span className="text-danger"> Las contraseñas no coinciden </span>
        )}
      </div>
      <div className="d-flex justify-content-center ">
        <Button type='submit'>Registrarse</Button>
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
          {isLogin && loginForm}
          {!isLogin && registerForm}
        </div>
      </div>
    </>
  );
};
