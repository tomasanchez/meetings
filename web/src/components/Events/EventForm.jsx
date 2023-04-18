import React, { useRef, useState } from "react";
import { Button, Modal } from "../UI/";

import classes from "./EventForm.module.css";

const today = new Date().toISOString().split("T")[0];

export const EventForm = (props) => {
  const [inputDates, setinputDates] = useState(1);
  const nameInput = useRef();
  const descInput = useRef();
  const placeInput = useRef();
  const dateInput = useRef([]);
  const hourInput = useRef([]);

  const addDatesHandler = () => {
    if (inputDates > 3) {
      alert("No seas complicado, solo 4 opciones podes darles a tus amigos");
      return;
    }
    setinputDates((prevValue) => prevValue + 1);

  };

  const removeDatesHandler = () => {
    if (inputDates == 1) {
      alert("Pone un horario por lo menos!!");
      return;
    }

    dateInput.current = dateInput.current.slice(0,-1);
    setinputDates((prevValue) => prevValue - 1);
  };

  const confirmHandler = (event) => {
    event.preventDefault();
  };

  return (
    <Modal onClose={props.onClose}>
      <h3 className=" text-center ">CREA TU EVENTO</h3>

      <form className="my-3" onSubmit={confirmHandler}>
        <div className={classes.control}>
          <label htmlFor="nameEvent">
            Nombre del evento <span>(*)</span>{" "}
          </label>
          <input
            type="text"
            placeholder="Ej: Estudiar tacs..."
            id="nameEvent"
            autoComplete="off"
            ref={nameInput}
            required
          />
        </div>
        <div className={classes.control}>
          <label htmlFor="nameEvdescEventent">
            Descripción <span>(*)</span>
          </label>
          <textarea
            placeholder="Ej: Nos juntamos para repasar primer parcial"
            id="descEvent"
            autoComplete="off"
            ref={descInput}
            required
          />
        </div>
        <div className={classes.control}>
          <label htmlFor="placeEvent">
            Lugar <span>(*)</span>
          </label>
          <input
            type="text"
            placeholder="Ej: Biblioteca medrano"
            autoComplete="off"
            id="placeEvent"
            ref={placeInput}
          />
        </div>

        {[...Array(inputDates)].map((_, index) => (
          <div key={index} className="d-flex gap-4">
            <div className={classes.control}>
              <label htmlFor="dateEvent">
                Fecha<span>(*)</span>
              </label>
              <input
                ref={(el) => (dateInput.current[index] = el)}
                type="date"
                id="dateEvent"
                min={today}
                defaultValue={today}
                required
              />
            </div>
            <div className={classes.control}>
              <label htmlFor="hourEvent">
                Hora<span>(*)</span>
              </label>
              <input
                type="time"
                id="hourEvent"
                ref={(el) => (hourInput.current[index] = el)}
                required
              />
            </div>

            {index == 0 && (
              <div className=" align-self-end pb-2 " >
                <button
                  type="button"
                  onClick={addDatesHandler}
                  className={classes.button}
                >
                  +
                </button>

                <button
                  type="button"
                  onClick={removeDatesHandler}
                  className={classes.button}
                >
                  -
                </button>
              </div>
            )}
          </div>
        ))}

        <Button type="submit"> Crear Evento </Button>
      </form>
    </Modal>
  );
};
