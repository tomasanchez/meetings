import { useContext, useState } from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";
import { DUMMY_EVENTS } from "../../components/Events/AvailableEvent";
import { Button, Modal } from "../../components/UI";
import AuthContext, { AuthContextType } from "../../store/auth-context";
import { ErrorPage } from "../ErrorPage";
import classes from "./EventDetails.module.css";

interface Option {
  day: string;
  month: string;
  hora: string;
  votes: string[];
}

interface EventDetailsProps {
  name: string;
  description: string;
  mes: string;
  dia: string;
  id: string;
  organizer: string;
  eventLocation: string;
  guests: string[];
  options: Option[];
}

export const EventDetails = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { name, description, mes, dia, id, organizer, eventLocation, options, guests } = location.state.event as EventDetailsProps;
  const [showDetails, setshowDetails] = useState(true);
  const authCtx = useContext(AuthContext) as AuthContextType;

  const goBack = () => {
    navigate("/");
    setshowDetails(false);
  }

  const getDatesFromOptions = () => {
    return options.reduce<string[]>((acc, option) => {
      if(!acc.includes(`${option.day} de ${option.month}`)) {
        acc.push(`${option.day} de ${option.month}`);
      }
      return acc;
    }, []);
  }

  const toggleVotes = () => {
    console.log("togvotes");
  }

  const joinEvent = () => {
    console.log(authCtx.user);
  }

  return (
    <>
      {!DUMMY_EVENTS.find((event) => event.id === id) && (<ErrorPage/>)}
      {showDetails &&
        <Modal onClose={goBack}>
          <div className="container">
            <div className="row">
              <div className="col">
                <div className={classes.organizer}> Organizer: {organizer} </div>
                <h3> {name} </h3>
                <div> {eventLocation} </div>
                <div> {description} </div>
                <hr/>
                <div> {mes} {dia} </div>
                <div>Guest List: </div>
                <ul>
                  {guests.map((guest: string) => <li>{guest}</li>)}
                </ul>
              </div>
              
              <div className="col">
                {getDatesFromOptions().map((date: string) => {
                  return (
                    <div>
                      <div> {date} </div>
                      <ul className={classes.list}>
                        {options.map((option: any, index: number) => {
                          if(`${option.day} de ${option.month}` === date) {
                            return (
                              <li key={index} className={classes.option}>
                                <input type="checkbox" className="btn-check" id={`btn-check-outlined checkbox-${index}`} defaultChecked={option.votes.indexOf(authCtx.user) !== -1}/>
                                <label className="btn btn-outline-primary" for={`btn-check-outlined checkbox-${index}`}>{option.hora}
                                  {option.votes.length > 0 &&
                                    <OverlayTrigger
                                      placement="bottom"
                                      overlay={
                                        <Tooltip id="button-tooltip-2" style={{position: "absolute"}}>
                                          {option.votes.map((vote: string) => {
                                            return (
                                              <div>{vote}</div>
                                            )
                                          })}
                                        </Tooltip>}
                                    >
                                      <span> x{option.votes.length}</span>
                                    </OverlayTrigger>
                                  }
                                </label>
                              </li>
                            )
                          }
                        })}
                      </ul>
                    </div>
                  )
                })
                } 
              </div>
            </div>
          </div>
          {authCtx.user !== null && 
            guests.indexOf(authCtx.user) !== -1 ?
              <div className={classes.button}>
                <Button onClick={toggleVotes}>Votar</Button>
              </div>
              :
              <div className={classes.button}>
                <Button onClick={joinEvent}>Confirmar Asistencia</Button>
              </div>
          }
        </Modal>
      }
    </>
  )
};