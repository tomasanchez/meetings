import { useLocation, useNavigate } from "react-router-dom";
import { Button, Modal } from "../../components/UI";
import classes from "./EventDetails.module.css";
import useEventWithId from "../../api/swrHooks/useEventWithId";
import { EventOptions } from "./EventOptions";
import useSWRMutation from "swr/mutation";
import { joinEvent, toggleVoting } from "../../api/services/eventService";
import useUser from "../../api/swrHooks/useUser";
import { ToggleVotingRequest } from "../../api/models/dataApi";
import { useState } from "react";

export const EventDetails = () => {
  const location = useLocation();
  const idUrl = location.pathname.split("/")[1];
  const navigate = useNavigate();
  const { user } = useUser();
  const { event, error, isLoading } = useEventWithId(idUrl);
  const [eventState, setEventState] = useState<Event | null>(event!.data);
  const { trigger: triggerJoinEvent } = useSWRMutation(idUrl, joinEvent);
  const { trigger: triggerToggleVoting } = useSWRMutation(idUrl, toggleVoting);

  const goBack = () => {
    navigate("/");
  };

  if (error) return <div>failed to load</div>;
  if (isLoading) return <div>loading...</div>;

  const toggleVotingHandler = async () => {
    const toggleVotingRequest: ToggleVotingRequest = {
      username: user!.username,
      voting: !event!.data.voting
    }
    await console.log(triggerToggleVoting(toggleVotingRequest));
  };

  const joinEventHandler = async () => {
    await triggerJoinEvent(user!.username);
  };

  return (
    <>
      <Modal onClose={goBack}>
        <>
          <div className="container">
            <div className="row">
              <div className="col">
                <div className={classes.organizer}>
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
              <EventOptions event={event!.data} idUrl={idUrl} user={user!.username} />
            </div>
          </div>

          <div className={classes.button}>
            {user!.username !== null && (
              <>
                {!(event!.data.guests.indexOf(user!.username) !== -1) && (
                  <Button onClick={joinEventHandler}>
                    JoinEvent
                  </Button>
                )}

                {user!.username === event!.data.organizer && (
                  <Button onClick={toggleVotingHandler}>
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