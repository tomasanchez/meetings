import React from "react";
import classes from "./BrandIcon.module.css";
import calendarIcon from "../../assets/calendar.png";
import {Link} from 'react-router-dom'


export const BrandIcon = (props) => {
  return (
    <div className={`${classes.brand} ${props.className}`}>
      <Link to={"/"}>
        <h1>Meetings</h1>
      </Link>
      <img
        src={calendarIcon}
        className={classes.icon}
        alt="A beautyfull calendar Icon "
      />
    </div>
  );
};
