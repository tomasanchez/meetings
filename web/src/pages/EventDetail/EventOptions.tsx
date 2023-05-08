import { OverlayTrigger, ToggleButton, Tooltip } from "react-bootstrap";
import useEventVote from "../../api/swrHooks/useEventVote";
import { VoteRequest } from "../../api/models/dataApi";
import { voteOption } from "../../api/services/voteService";
import classes from "./EventDetails.module.css";

interface EventOptionsProps {
  event: Event,
  idUrl: string,
  user: string
}

interface Event {
  id: string
  organizer: string
  voting: boolean
  title: string
  description: string
  location: string
  date: string
  guests: string[]
  options: Option[]
}

interface Option {
  date: string
  votes: string[]
}

export const EventOptions = (props: EventOptionsProps) => {
  const { mutate } = useEventVote(props.idUrl);

  const getDatesFromOptions = () => {
    return props.event!.options.reduce<string[]>((acc: any, option: any) => {
      if(!acc.includes(option.date.split("T")[0])) {
        acc.push(`${option.date.split("T")[0]}`);
      }
      return acc;
    }, []);
  }

  const toggleVote = async (date: string, e: React.MouseEvent<HTMLButtonElement>) => {
  e.preventDefault();
  const request: VoteRequest = {
    username: props.user!,
    option: {
      date: date.split("T")[0],
      hour: +date.split("T")[1].split(":")[0],
      minute: +date.split("T")[1].split(":")[1]
    }
  }

    await voteOption(props.idUrl, request);
    mutate();

    window.location.reload();
  };

  return (
    <div className="col">
    {props.event!.options &&
      <>
      <h3>Options</h3>
      {getDatesFromOptions().map((date: string) => {
        return (
          <div>
            <div> {date} </div>
            <ul className={classes.list}>
              {props.event!.options.map((option: any, index: number) => {
                if(option.date.split('T')[0] === date) {
                  return (
                      <ToggleButton 
                        key={index}
                        variant="primary"
                        disabled={props.event.guests.indexOf(props.user) !== -1 || !props.event.voting}
                        value={option.date}
                        onClick={(e: React.MouseEvent<HTMLButtonElement>) => {toggleVote(option.date, e)}} >
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