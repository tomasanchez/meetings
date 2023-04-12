import React from 'react'
import classes from './EventItem.module.css'
import { CalendarEvent } from './CalendarEvent'

export const EventItem = (props) => {
  return (
    <li className={classes.event}>
      <div className='d-flex flex-column justify-content-center align-items-center ' >
        <h3> {props.name} </h3>
        <div className={classes.description} > {props.description} </div>
      </div>

      <div>
        <CalendarEvent mes={props.mes} dia={props.dia} />
        <a href="">VER JUNTADA</a>
      </div>
    </li>
  )
}
