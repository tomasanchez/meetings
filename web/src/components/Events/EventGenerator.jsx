import React from "react";
import classes from "./EventGenerator.module.css";
import { Button } from "../UI/Button";

export const EventGenerator = (props) => {
  return (
    <div className={` ${classes.summary} p-5 pb-3`}>
      <p className={`${classes.quote} mb-2 mb-lg-4`}>
        "Te reís un rato con tus amigos, y la vida se te reinicia"
      </p>
      <p className="mb-2 mb-lg-4">
        Con nuestra APP es todo más facil, vas a poder crear un evento, tus
        amigos unirse a él y entre todos acordar una fecha. Nunca más el "Vamos
        hablando".
      </p>

      <Button onClick={props.onCreate}> Crear evento </Button>
    </div>
  );
};
