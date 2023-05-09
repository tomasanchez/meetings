import { useRef } from "react";
import { Button, Modal } from "../UI";
import { useState } from 'react';

import classes from "./EventForm.module.css";
import { FormEvent } from "react";
import { EventRequest, optionVote } from "../../api/models/dataApi";
import useSWRMutation from "swr/mutation";
import { addEvent } from "../../api/services/eventService";
import useUser from "../../api/swrHooks/useUser";
import Swal from "sweetalert2";

interface eventFormProps {
  onClose: () => void;
}

const today = new Date().toISOString().split("T")[0];

export const EventForm = (props: eventFormProps) => {
  const nameInput = useRef<HTMLInputElement>(null);
  const descInput = useRef<HTMLTextAreaElement>(null);
  const placeInput = useRef<HTMLInputElement>(null);

  const { trigger } = useSWRMutation("scheduler-service/schedules", addEvent);
  const { user } = useUser();

  const [date, setDate] = useState<string>(today);
  const [hour, setHour] = useState<string>("");
  const [counterOptions, setCounterOptions] = useState<number>(1);

  const confirmHandler = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if(user == null) {
      Swal.fire({
        title: 'Error',
        text: "Por favor inicie sesion",
        icon: 'error',
        confirmButtonText: 'OK'
      });
      return
    }

    const formData = new FormData(event.currentTarget);
    const formFields: {}[] = [];
    const optionsToSend: optionVote[] = [];

    Object.entries(Object.fromEntries(formData)).forEach((e) => {
      formFields.push(e);
    });


    for(let i = 0; i < (formFields.length)/2; i++) {
      const date: string = formFields[i*2][1];
      const [hours, minutes] = formFields[(i*2+1)][1].split(":");
      optionsToSend.push({date, hour: +hours, minute: +minutes})
    }

    const newEvent: EventRequest = {
      description: descInput.current!.value,
      location: placeInput.current!.value,
      organizer: user!.username,
      title: nameInput.current!.value,
      options: optionsToSend,
      guests: [],
    };
    
    await trigger(newEvent);
    props.onClose()
  
  };

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDate(e.target.value);
  };

  const handleHourChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setHour(e.target.value);
  };
  
  const addOption = () => {
    setCounterOptions(counterOptions + 1);
    setDate(today);
    setHour("");
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

        {Array.from(Array(counterOptions).keys()).map((i) => {
          return (
            <div className="d-flex gap-4" key={i}>
              <div className={classes.control}>
                <label htmlFor="dateEvent">
                  Fecha<span>(*)</span>
                </label>
                <input
                  name={`eventDate${i}`}
                  type="date"
                  id="dateEvent"
                  min={today}
                  defaultValue={today}
                  required
                  onChange={(e) => {handleDateChange(e)}}
                />
              </div>
              <div className={classes.control}>
                <label htmlFor="hourEvent">
                  Hora<span>(*)</span>
                </label>
                <input type="time" id="hourEvent" required name={`eventTime${i}`} onChange={(e) => {handleHourChange(e)}}  />
              </div>
              
              {(i === counterOptions - 1 && date !== "" && hour !== "") && <Button onClick={() => {addOption()}}>+</Button>}
            </div>
          );
        })
        }
        <Button type="submit"> Crear Evento </Button>
      </form>
    </Modal>
  );
};
