import { ReactNode } from "react";
import classes from "./Card.module.css";

interface cardProps {
  className?: string;
  children: ReactNode;
}

const Card = (props: cardProps) => {
  return (
    <div className={`${classes.card} ${props.className}`}>{props.children}</div>
  );
};

export default Card;
