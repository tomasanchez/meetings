import React from "react";
import classes from "./Header.module.css";
import friendsCafe from "../../assets/friends_cafe.jpg";
import { HeaderProfile } from "./HeaderProfile";
import {BrandIcon} from '../UI'


export const Header = () => {
  return (
    <>
      <header className={classes.header}>
        <BrandIcon/>
        <HeaderProfile/>
      </header>
      <div className={classes["main-image"]}>
        <img src={friendsCafe} alt="A meeting of friends" />
      </div>
    </>
  );
};
