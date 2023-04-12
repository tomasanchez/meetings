import React from "react";
import classes from "./AvailableEvent.module.css";
import Card from "../UI/Card";
import { EventItem } from "./EventItem/EventItem";

const DUMMY_EVENTS = [
  {
    id: "m1",
    name: "Birras en el bar",
    description: "Sanchez, Tomas",
    mes: "MARZO",
    dia: "3",
  },
  {
    id: "m2",
    name: "Bowling en Boedo",
    description: "Yogui, Matias",
    mes: "FEBRERO",
    dia: "14",
  },
  {
    id: "m3",
    name: "Asado en lo de tito",
    description: "De Matteo, Renzo",
    mes: "ABRIL",
    dia: "20",
  },
];

export const AvailableEvent = () => {
  const eventList = DUMMY_EVENTS.map((event) => (
    <EventItem
      key={event.id}
      id={event.id}
      name={event.name}
      description={event.description}
      mes={event.mes}
      dia={event.dia}
    ></EventItem>
  ));
  return (
    <section className={classes.event}>
      <Card>
        <ul>{eventList}</ul>
      </Card>
    </section>
  );
};
