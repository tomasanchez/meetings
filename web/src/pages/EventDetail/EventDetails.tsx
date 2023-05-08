import { useLocation, useNavigate } from "react-router-dom";
import { Button, Modal } from "../../components/UI";
import classes from "./EventDetails.module.css";
import useEventWithId from "../../api/swrHooks/useEventWithId";
import { EventOptions } from "./EventOptions";
import useToggleVoting from "../../api/swrHooks/userToggleVoting";
import useJoinEvent from "../../api/swrHooks/useJoinEvent";

export const EventDetails = () => {
  const location = useLocation();
  const idUrl = location.pathname.split("/")[1];
  const navigate = useNavigate();
  const user = localStorage.getItem("username");
  
  const { mutate } = useToggleVoting(idUrl);
  const { mutate: mutateJoin } = useJoinEvent(idUrl);
  const { event, error, isLoading } = useEventWithId(idUrl);


  const goBack = () => {
    navigate("/");
  };

  if (error) return <div>failed to load</div>;
  if (isLoading) return <div>loading...</div>;

  const toggleVoting = async () => {
    await toggleVotingService(idUrl, user!, !event?.data.voting);
    mutate();
  };

  const joinEvent = async () => {
    await joinEventService(idUrl, user!);
    mutateJoin();
  };

  return (
    <>
      <Modal onClose={goBack}>
        <>
          <div className="container">
            <div className="row">
              <div className="col">
                <div className={classes.organizer}>
                  {" "}
                  Organizer: {event!.data.organizer}{" "}
                </div>
                <h3> {event!.data.title} </h3>
                <div> {event!.data.location} </div>
                <div> {event!.data.description} </div>
                {event!.data.guests.length > 0 && (
                  <>
                    <hr />
                    <div>Guest List: </div>
                    <ul>
                      {event!.data.guests.map((guest: string) => (
                        <li>{guest}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
              <EventOptions event={event!.data} idUrl={idUrl} user={user!} />
            </div>
          </div>

          <div className={classes.button}>
            {user !== null && (
              <>
                {!(event!.data.guests.indexOf(user) !== -1) && (
                  <Button onClick={joinEvent}>JoinEvent
                  </Button>
                )}

                {user === event!.data.organizer && (
                  <Button onClick={toggleVoting}>
                    {!event!.data.voting ? "Enable voting" : "Close event"}
                  </Button>
                )}
              </>
            )}
          </div>
        </>
      </Modal>
    </>
  );
};
function toggleVotingService(idUrl: string, arg1: string, arg2: boolean) {
  throw new Error("Function not implemented.");
}

function joinEventService(idUrl: string, arg1: string) {
  throw new Error("Function not implemented.");
}

