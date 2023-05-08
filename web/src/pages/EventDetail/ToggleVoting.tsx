import { Button } from "../../components/UI";
import { toggleVotingService } from "../../api/services/toggleVotingService"
import useToggleVoting from "../../api/swrHooks/userToggleVoting"

interface ToggleVotingProps {
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

export const ToggleVoting = (props: ToggleVotingProps) => {
  const { mutate } = useToggleVoting(props.idUrl);

  const toggleVoting = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    await toggleVotingService(props.idUrl, props.user, !props.event.voting);
    mutate();

    window.location.reload();
  }

  return (
    <div>
      <Button onClick={toggleVoting} >
        {!(props.event.voting) ? "Enable voting" : "Close event"}
      </Button>
    </div>
  )
}