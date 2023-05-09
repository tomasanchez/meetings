import classes from "./AvailableEvent.module.css";
import Card from "../UI/Card";
import { EventItem } from "./EventItem/EventItem";
import useEvent from "../../api/swrHooks/useEvent";


export const AvailableEvent = () => {
  const { events, error, isLoading } = useEvent();


  if (error) return <div>error</div>;
  if (isLoading) return <div>loading</div>;
  if (!events?.data) {
    <div>Aún no hay eventos!</div>
  }
  
  return (  <section className={classes.event}>
      <Card>
        <ul>
          {events!.data.map((event: any) => (
              <EventItem
                key={event.id}
                event={event}
              ></EventItem>
            ))}
        </ul>
      </Card>
    </section>
  )
};
