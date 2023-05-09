import classes from "./AvailableEvent.module.css";
import Card from "../UI/Card";
import { EventItem } from "./EventItem/EventItem";
import useEvent from "../../api/swrHooks/useEvent";
import Swal from "sweetalert2";


export const AvailableEvent = () => {
  const { events, error, isLoading } = useEvent();


  if (error){
    Swal.fire({
      title: 'Error',
      text: error.detail,
      icon: 'error',
      confirmButtonText: 'OK'
    });
    throw new Error(error);
  }

  if (isLoading) return <div>loading</div>;
  
  return ( <section className={classes.event}>
      <Card>
        { events?.data.length == 0 && <div className="text-center" >No hay eventos próximos</div> }
        { events?.data.length != 0 && <ul>
          {events!.data.map((event: any) => (
              <EventItem
                key={event.id}
                event={event}
              ></EventItem>
            ))}
        </ul>}
      </Card>
    </section>
  )
};
