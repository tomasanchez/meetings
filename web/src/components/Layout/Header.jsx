import React from "react";
import classes from "./Header.module.css";
import calendarIcon from "../../assets/calendar.png";
import friendsCafe from "../../assets/friends_cafe.jpg";
import { HeaderProfile } from "./HeaderProfile";


export const Header = () => {
  return (
    <>
      <header className={classes.header}>
        <div className={classes.brand}>
          <h1>Meetings</h1>
          <img
            src={calendarIcon}
            className={classes.icon}
            alt="A beautyfull calendar Icon "
          />
        </div>
        <HeaderProfile/>
      </header>
      <div className={classes["main-image"]}>
        <img src={friendsCafe} alt="A meeting of friends" />
      </div>
    </>
  );
};
