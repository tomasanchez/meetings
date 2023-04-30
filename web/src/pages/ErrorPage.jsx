import React from "react";
import {Card, BrandIcon} from "../components/UI";
import { Link } from "react-router-dom";
import classes from "./ErrorPage.module.css";

export const ErrorPage = () => {
  return (
    <Card className={`${classes.card_error_page}`}>
      <BrandIcon />
      <h1>Ups. Surgió un error.</h1>
      <Link className="btn bg-danger mt-4 " to={"/"}>
        Ir al home
      </Link>
    </Card>
  );
};
