import classes from "./AvailableEvent.module.css";
import Card from "../UI/Card";
import { EventItem } from "./EventItem/EventItem";

export const DUMMY_EVENTS = [
  {
    id: "m1",
    name: "Birras en el bar",
    description: "Birras en el bar de siempre, yo invito.",
    eventLocation: "Medrano 951",
    month: "MARZO",
    day: "3",
    organizer: "tomas_sanchez",
    options: [
      {
        day: "3",
        month: "MARZO",
        hora: "20:00",
        votes: ["tomas_sanchez", "matias_yogui", "renzo_de_matteo"],
      },
      {
        day: "4",
        month: "MARZO",
        hora: "20:00",
        votes: [],
      },
      {
        day: "4",
        month: "MARZO",
        hora: "21:00",
        votes: ["renzo_de_matteo"],
      }
    ],
    guests: ["tomas_sanchez", "matias_yogui", "renzo_de_matteo"],
  }
];

export const AvailableEvent = () => {
  const eventList = DUMMY_EVENTS.map((event) => (
    <EventItem
      key={event.id}
      id={event.id}
      name={event.name}
      description={event.description}
      month={event.month}
      day={event.day}
      organizer={event.organizer}
      options={event.options}
      guests={event.guests}
      eventLocation={event.eventLocation}
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
