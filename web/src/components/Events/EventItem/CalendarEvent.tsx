import classes from "./CalendarEvent.module.css";

interface CalendarEventProp {
  mes: string,
  dia: string
}

export const CalendarEvent = (props: CalendarEventProp) => {
  return (
    <div className={`d-flex flex-column ${classes.calendar}`}>
      <p className="m-0" > {props.mes} </p>
      <p className={`m-0 ${classes.date} `} > {props.dia} </p>
    </div>
  );
};
