import { OverlayTrigger, ToggleButton, Tooltip } from "react-bootstrap";
import { Event, VoteRequest } from "../../api/models/dataApi";
import classes from "./EventDetails.module.css";
import { voteOption } from "../../api/services/eventService";

interface EventOptionsProps {
  event: Event,
  idUrl: string,
  user: string,
  mutate: any
}

export const EventOptions = (props: EventOptionsProps) => {

  const getDatesFromOptions = () => {
    return props.event!.options.reduce<string[]>((acc: any, option: any) => {
      if(!acc.includes(option.date.split("T")[0])) {
        acc.push(`${option.date.split("T")[0]}`);
      }
      return acc;
    }, []);
  }

  const toggleVote = async (date: string) => {
  const request: VoteRequest = {
    username: props.user!,
    option: {
      date: date.split("T")[0],
      hour: +date.split("T")[1].split(":")[0],
      minute: +date.split("T")[1].split(":")[1]
    }
  }

    const response = await voteOption(
      `scheduler-service/schedules/${props.idUrl}`,
      { arg: request }
    );
    props.mutate(response);
  };

  return (
    <div className="col">
    {props.event!.options &&
      <>
      <h3>Options</h3>
      {getDatesFromOptions().map((date: string) => {
        return (
          <div key={date}>
            <div> {date} </div>
            <ul className={classes.list}>
              {props.event!.options.map((option: any, index: number) => {
                if(option.date.split('T')[0] === date) {
                  return (
                      <ToggleButton 
                        key={index}
                        variant="primary"
                        disabled={!(props.event.guests.indexOf(props.user) !== -1) || !props.event.voting}
                        value={option.date}
                        onClick={() => {toggleVote(option.date)}} >
                          {option.date.split('T')[1]}
                          {option.votes.length > 0 &&
                          <OverlayTrigger
                            placement="bottom"
                            overlay={
                              <Tooltip id="button-tooltip-2" style={{position: "absolute"}}>
                                {option.votes.map((vote: string) => {
                                  return (<div>{vote}</div>)
                                })}
                              </Tooltip>}
                          >
                            <span> x{option.votes.length}</span>
                          </OverlayTrigger>
                        }
                      </ToggleButton>
                  )
                }
              })}
            </ul>
          </div>
        )
      })
      } 
      </>
    }
    </div>
  )
}