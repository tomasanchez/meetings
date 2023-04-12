import React, { useRef, useState } from "react";
import { Button, Modal } from "../UI/";

import classes from "./EventForm.module.css";

const today = new Date().toISOString().split("T")[0];
const isEmpty = (value) => value.trim() === "";

export const EventForm = (props) => {
  const nameInput = useRef();
  const descInput = useRef();
  const placeInput = useRef();
  const dateInput = useRef();
  const hourInput = useRef();
  const [formIsValid, setformIsValid] = useState({
    name: true,
    desc: true,
    place: true,
    date: true,
    hour: true,
  });

  const resetErrors = (prop) => {
    if (
      formIsValid.place &&
      formIsValid.name &&
      formIsValid.desc &&
      formIsValid.hour &&
      formIsValid.date
    )
      return;
    setformIsValid((value) => ({ ...value, [prop]: true }));
  };

  const confirmHandler = (event) => {
    event.preventDefault();

    const nameEvent = nameInput.current.value;
    const descEvent = descInput.current.value;
    const placeEvent = placeInput.current.value;
    const dateEvent = dateInput.current.value;
    const hourEvent = hourInput.current.value;

    const nameValid = !isEmpty(nameEvent);
    const descValid = !isEmpty(descEvent);
    const placeValid = !isEmpty(placeEvent);
    const dateValid = !isEmpty(dateEvent);
    const hourValid = !isEmpty(hourEvent);

    const formValid =
      nameValid && descValid && placeValid && dateValid && hourValid;

    setformIsValid({
      name: nameValid,
      desc: descValid,
      place: placeValid,
      date: dateValid,
      hour: hourValid,
    });

    if (!formValid) return;
  };

  return (
    <Modal onClose={props.onClose}>
      <h3 className=" text-center ">CREA TU EVENTO</h3>

      <form className="my-3" onSubmit={confirmHandler}>
        <div className={classes.control}>
          <label htmlFor="nameEvent">Nombre del evento</label>
          <input
            type="text"
            placeholder="Ej: Estudiar tacs..."
            id="nameEvent"
            autoComplete="off"
            ref={nameInput}
            onBlur={() => {
              resetErrors("name");
            }}
          />
          {!formIsValid.name && (
            <p className=" text-danger ">Ingresa un nombre!</p>
          )}
        </div>
        <div className={classes.control}>
          <label htmlFor="nameEvdescEventent">Descripción</label>
          <input
            type="text"
            placeholder="Ej: Nos juntamos para repasar primer parcial"
            id="descEvent"
            autoComplete="off"
            ref={descInput}
            onBlur={() => {
              resetErrors("desc");
            }}
          />
          {!formIsValid.desc && (
            <p className=" text-danger ">Ingresa la descripción!</p>
          )}
        </div>
        <div className={classes.control}>
          <label htmlFor="placeEvent">Lugar</label>
          <input
            type="text"
            placeholder="Ej: Biblioteca medrano"
            autoComplete="off"
            id="placeEvent"
            ref={placeInput}
            onBlur={() => {
              resetErrors("place");
            }}
          />
          {!formIsValid.place && (
            <p className=" text-danger ">Ingresa un lugar para la juntada!</p>
          )}
        </div>
        <div className="d-flex gap-4">
          <div className={classes.control}>
            <label htmlFor="dateEvent">Fecha</label>
            <input
              type="date"
              id="dateEvent"
              min={today}
              defaultValue={today}
              ref={dateInput}
            />
            {(!formIsValid.date || !formIsValid.hour) && (
              <p className=" text-danger ">Ingresa una fecha y horario!</p>
            )}
          </div>
          <div className={classes.control}>
            <label htmlFor="hourEvent">Hora</label>
            <input
              onBlur={() => {
                resetErrors("hour");
              }}
              type="time"
              id="hourEvent"
              ref={hourInput}
            />
          </div>
        </div>

        <Button type="submit"> Crear Evento </Button>
      </form>
    </Modal>
  );
};
