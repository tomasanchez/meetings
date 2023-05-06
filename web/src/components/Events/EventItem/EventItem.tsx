import classes from "./EventItem.module.css";
import { CalendarEvent } from "./CalendarEvent";
import { Link, Outlet } from "../../../../node_modules/react-router-dom/dist/index";

interface EventItemProps {
  name: string;
  description: string;
  month: string;
  day: string;
  id: string;
  organizer: string;
  eventLocation: string;
  options: {
    day: string;
    month: string;
    hora: string;
    votes: string[];
  }[];
  guests: string[];
}

export const EventItem = (props: EventItemProps) => {  return (
    <>
      <li className={classes.event}>
        <div className="d-flex flex-column justify-content-center align-items-center ">
          <h3> {props.name} </h3>
          <div className={classes.description}> {props.organizer} </div>
        </div>

        <div>
          <CalendarEvent mes={props.month} dia={props.day} />
          <Link to={{pathname: `/${props.id}`}} state={{event: props}}>VER JUNTADA</Link>
        </div>
      </li>

      <Outlet />
    </>
  );
};
