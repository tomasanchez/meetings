import classes from "./EventItem.module.css";
import {
  Link,
  Outlet,
} from "../../../../node_modules/react-router-dom/dist/index";
import { Event } from "../../../api/models/dataApi";

interface EventItem {
  event: Event
}

export const EventItem = (props: EventItem) => {
  return (
    <>
      <li className={classes.event + " gap-3"}>
        <div className="d-flex flex-column justify-content-center align-items-center ">
          <h3> {props.event.title} </h3>
          <div className={classes.description}> {props.event.organizer} </div>
        </div>
        <div className=" align-self-center text-center " >
          {props.event.voting && (
            <div className={`d-flex flex-column ${classes.calendar}`}>
              <p className="mb-2 fs-6 "> Participa en la votación  y elegí una fecha! </p>
            </div>
          )}
          <Link to={{ pathname: `/${props.event.id}` }}>VER JUNTADA</Link>
        </div>
      </li>

      <Outlet />
    </>
  );
};
