import { useRef } from "react";
import { Button, Modal } from "../UI";

import classes from "./EventForm.module.css";
import { FormEvent } from "react";
import { EventRequest } from "../../api/models/dataApi";
import useSWRMutation from "swr/mutation";
import { addEvent } from "../../api/services/eventService";

interface eventFormProps {
  onClose: () => any;
}

const today = new Date().toISOString().split("T")[0];

export const EventForm = (props: eventFormProps) => {
  const nameInput = useRef<HTMLInputElement>(null);
  const descInput = useRef<HTMLTextAreaElement>(null);
  const placeInput = useRef<HTMLInputElement>(null);
  const dateInput = useRef<HTMLInputElement>(null);
  const hourInput = useRef<HTMLInputElement>(null);

  const { trigger } = useSWRMutation("scheduler-service/schedules", addEvent);

  const confirmHandler = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const [hours, minutes] = hourInput.current!.value.split(":");

    const newEvent: EventRequest = {
      description: descInput.current!.value,
      location: placeInput.current!.value,
      organizer: "",
      title: nameInput.current!.value,
      options: [
        { date: dateInput.current!.value, hour: +hours, minute: +minutes },
      ],
      guests: [],
    };

    try {
      await trigger(newEvent);
      props.onClose()
    } catch (e) {
      console.log(e);
    }
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

        <div className="d-flex gap-4">
          <div className={classes.control}>
            <label htmlFor="dateEvent">
              Fecha<span>(*)</span>
            </label>
            <input
              ref={dateInput}
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
            <input type="time" id="hourEvent" ref={hourInput} required />
          </div>
        </div>

        <Button type="submit"> Crear Evento </Button>
      </form>
    </Modal>
  );
};
