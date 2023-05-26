import { useNavigate, useParams } from "react-router-dom";
import { Button, Modal } from "../../components/UI";
import classes from "./EventDetails.module.css";
import { EventOptions } from "./EventOptions";
import { joinEvent, toggleVoting } from "../../api/services/eventService";
import useUser from "../../api/swrHooks/useUser";
import { EventWrapper, ToggleVotingRequest } from "../../api/models/dataApi";
import useSWR from "swr";
import { fetcher } from "../../api/fetcher";
import Swal from "sweetalert2";


export const EventDetails = () => {
  const navigate = useNavigate();
  const {idEvent} = useParams<{idEvent: string}>()
  const { user } = useUser();
  const {
    data: event,
    error,
    isLoading,
    mutate,
  } = useSWR<EventWrapper>(`schedules/${idEvent}`, fetcher);

  const goBack = () => {
    navigate("/");
  };

  if (error) {
    Swal.fire({
      title: 'Error',
      text: error.detail,
      icon: 'error',
      confirmButtonText: 'OK'
    });
    throw new Error(error);
  }
  if (isLoading) return <div>loading...</div>;
  if (!user) {navigate("/login")};


  const toggleVotingHandler = async () => {
    const toggleVotingRequest: ToggleVotingRequest = {
      username: user?.username,
      voting: !event?.data.voting,
    };

    const response = await toggleVoting(
      `schedules/${idEvent}`,
      { arg: toggleVotingRequest }
    );
    mutate(response);
  };

  const joinEventHandler = async () => {
    const response = await joinEvent(`schedules/${idEvent}`, {
      arg: user?.username,
    });
    mutate(response);
  };

  return (
    <>
      <Modal onClose={goBack}>
        <>
          <div className="container">
            <div className="row">
              <div className="col">
                <div className={classes.organizer}>
                  Organizer: {event?.data.organizer}{" "}
                </div>
                <h3> {event?.data.title} </h3>
                <div> {event?.data.location} </div>
                <div> {event?.data.description} </div>
                {event?.data.guests.length > 0 && (
                  <>
                    <hr />
                    <div>Guest List: </div>
                    <ul>
                      {event?.data.guests.map((guest: string) => (
                        <li>{guest}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
              <EventOptions
                event={event?.data}
                idEvent={idEvent}
                user={user?.username}
                mutate={mutate}
              />
            </div>
          </div>

          <div className={classes.button}>
            {user?.username !== null && (
              <>
                {!(event?.data.guests.indexOf(user?.username) !== -1) && user?.username !== event?.data.organizer && (
                  <Button onClick={joinEventHandler}>Join Event & Vote</Button>
                )}

                {user?.username === event?.data.organizer && (
                  <Button onClick={toggleVotingHandler}>
                    {!event?.data.voting ? "Enable voting" : "Close event"}
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
