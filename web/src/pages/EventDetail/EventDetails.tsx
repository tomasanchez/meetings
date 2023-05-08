import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button, Modal } from "../../components/UI";
import classes from "./EventDetails.module.css";
import useEventWithId from "../../api/swrHooks/useEventWithId";
import { EventOptions } from "./EventOptions";
import { ToggleVoting } from "./ToggleVoting";
import { JoinEvent } from "./JoinEvent";

export const EventDetails = () => {
  const location = useLocation();
  const idUrl = location.pathname.split("/")[1];
  const navigate = useNavigate();
  const [showDetails, setshowDetails] = useState(true);
  const { event, error, isLoading } = useEventWithId(idUrl);
  const user = localStorage.getItem("username");

  const goBack = () => {
    navigate("/");
    setshowDetails(false);
  }

  if (error) return <div>failed to load</div>
  if (isLoading) return <div>loading...</div>

  return (
    <>
      {showDetails &&
        <Modal onClose={goBack}>
          <>
            <div className="container">
              <div className="row">
                <div className="col">
                  <div className={classes.organizer}> Organizer: {event!.data.organizer} </div>
                  <h3> {event!.data.title} </h3>
                  <div> {event!.data.location} </div>
                  <div> {event!.data.description} </div>
                  {event!.data.guests.length > 0 &&
                    <>
                      <hr/>
                      <div>Guest List: </div>
                      <ul>
                        {event!.data.guests.map((guest: string) => <li>{guest}</li>)}
                      </ul>
                    </>
                  }
                </div>
                <EventOptions event={event!.data} idUrl={idUrl} user={user!} />
              </div>
            </div>

            <div className={classes.button}>
              {user !== null && 
                (
                  <>
                    {!(event!.data.guests.indexOf(user) !== -1) &&
                      <JoinEvent idUrl={idUrl} user={user!} />
                    }
                    
                    {(user === event!.data.organizer) &&
                      <ToggleVoting event={event!.data} idUrl={idUrl} user={user!}  />
                    }
                  </>
                )
              }
            </div>
          </>
        </Modal>
      }
    </>
  )
}