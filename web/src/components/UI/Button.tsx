import { ReactNode } from "react";
import classes from "./Button.module.css";

interface buttonProps {
  type?: "button" | "submit" | "reset";
  onClick?: () => any;
  children: ReactNode;
}

export const Button = (props: buttonProps) => {
  return (
    <button
      className={classes.button}
      type={props.type || "button"}
      onClick={props.onClick}
    >
      {props.children}
    </button>
  );
};
