import classes from './EventItem.module.css'
import { CalendarEvent } from './CalendarEvent'

interface EventItemProps {
  name: string,
  description: string,
  mes?: string,
  dia?: string,
  id: string
}

export const EventItem = (props: EventItemProps) => {
  return (
    <li className={classes.event}>
      <div className='d-flex flex-column justify-content-center align-items-center ' >
        <h3> {props.name} </h3>
        <div className={classes.description} > {props.description} </div>
      </div>

      <div>
        <CalendarEvent mes={props.mes || ''} dia={props.dia || 'A DEFINIR'} />
        <a href="">VER JUNTADA</a>
      </div>
    </li>
  )
}
