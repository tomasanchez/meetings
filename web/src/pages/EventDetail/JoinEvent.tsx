import { Button } from "../../components/UI";
import { joinEventService } from "../../api/services/joinEventService";
import useJoinEvent from "../../api/swrHooks/useJoinEvent";

interface JoinEventProps {
  idUrl: string,
  user: string
}

export const JoinEvent = (props: JoinEventProps) => {
  const { mutate } = useJoinEvent(props.idUrl);

  
  const joinEvent = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    await joinEventService(props.idUrl, props.user!);
    mutate();

    window.location.reload();
  }


  return (
    <Button onClick={joinEvent} >
      JoinEvent
    </Button>
  )
}