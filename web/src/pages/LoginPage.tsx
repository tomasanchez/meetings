import { useRef, useState, FormEvent, useEffect } from "react";
import classes from "./LoginPage.module.css";
import { Button, BrandIcon } from "../components/UI";
import { useNavigate } from "react-router-dom";
import { LoginRequest, RegisterRequest } from "../api/models/dataApi";
import { login, register } from "../api/services/authService";
import useUser from "../api/swrHooks/useUser";

export const LoginPage = () => {
  const navigate = useNavigate();
  const userNameInput = useRef<HTMLInputElement>(null);
  const passwordInput = useRef<HTMLInputElement>(null);
  const repeatPassword = useRef<HTMLInputElement>(null);
  const [isLogin, setisLogin] = useState<boolean>(true);
  const [errorLogin, seterrorLogin] = useState<boolean>(false);
  const [errorRegister, seterrorRegister] = useState<boolean>(false);

  const { user, mutate } = useUser();

  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user]);

  const handleLogin = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (
      passwordInput.current?.value == "" ||
      userNameInput.current?.value == ""
    ) {
      seterrorLogin(true);
      return;
    }

    const user: LoginRequest = {
      password: passwordInput.current!.value,
      username: userNameInput.current!.value,
    };

    try {
      await login(user);
      mutate();
    } catch (error) {
      seterrorLogin(true);
    }
  };

  const resetErrors = () => {
    if (errorLogin) seterrorLogin(false);
    if (errorRegister) seterrorLogin(false);
  };

  const loginForm = (
    <form className="my-3" onSubmit={handleLogin}>
      <div className="mb-4">
        <label htmlFor="username" className="form-label opacity-75 mb-0">
          Usuario
        </label>
        <input
          type="text"
          className={`${classes["form-control-login"]} form-control`}
          id="username"
          name="username"
          autoComplete="off"
          required
          onBlur={resetErrors}
          ref={userNameInput}
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
          minLength={8}
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
        <Button type="submit">Ingresar</Button>
      </div>
    </form>
  );

  const handleRegister = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (passwordInput.current?.value !== repeatPassword.current?.value) {
      seterrorRegister(true);
      return;
    }

    const newUser: RegisterRequest = {
      email: userNameInput.current!.value+'@meetings.com.ar',
      username: userNameInput.current!.value,
      password: passwordInput.current!.value,
      role: "user",
    };

    try {
      await register(newUser);
      mutate();
    } catch (error) {
      seterrorRegister(true);
    }
  };

  const registerForm = (
    <form className="my-3" onSubmit={handleRegister}>
      <div className="mb-4">
        <label htmlFor="username" className="form-label opacity-75 mb-0">
          Usuario
        </label>
        <input
          required
          minLength={8}
          placeholder="Ej: MiUsuario1234"
          className={`${classes["form-control-login"]} form-control`}
          id="username"
          name="username"
          ref={userNameInput}
        />
      </div>
      <div className="mb-4">
        <label htmlFor="password" className="form-label opacity-75 mb-0">
          Contraseña
        </label>
        <input
          type="password"
          required
          minLength={8}
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
          minLength={8}
          required
          name="repeatpassword"
          ref={repeatPassword}
        />
        {errorRegister && (
          <span className="text-danger"> Las contraseñas no coinciden </span>
        )}
      </div>
      <div className="d-flex justify-content-center flex-column">
        <Button type="submit">Registrarse</Button>
        <Button onClick={() => {setisLogin(true)}}>Log In</Button>
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
