import React from "react";
import classes from "./Modal.module.css";
import reactDom from "react-dom";

const Backdrop = (props) => {
  return <div className={classes.backdrop}> </div>;
};

const ModalOverlay = (props) => {
  return (
    <div className={classes.modal}>
      <div className={classes.scrollbox} >
      <p className=" text-end ">
        <button onClick={props.onClose} className={classes.close}>
          X
        </button>
      </p>
      <div className={classes.content}>{props.children}</div>
      </div>

    </div>
  );
};

const portalElement = document.getElementById("overlay");

export const Modal = (props) => {
  return (
    <>
      {reactDom.createPortal(<Backdrop />, portalElement)}
      {reactDom.createPortal(
        <ModalOverlay onClose={props.onClose}> {props.children} </ModalOverlay>,
        portalElement
      )}
    </>
  );
};
