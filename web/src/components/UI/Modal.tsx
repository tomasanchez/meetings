import { ReactNode } from "react";
import classes from "./Modal.module.css";
import reactDom from "react-dom";

interface modalOverlayProps {
  onClose: () => any;
  children: ReactNode;
}

interface modalProps {
  onClose: () => any;
  children: ReactNode;
}

const Backdrop = () => {
  return <div className={classes.backdrop}> </div>;
};

const ModalOverlay = (props: modalOverlayProps) => {
  return (
    <div className={classes.modal}>
      <div className={classes.scrollbox}>
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

export const Modal = (props: modalProps) => {
  return (
    <>
      {reactDom.createPortal(<Backdrop />, portalElement!)}
      {reactDom.createPortal(
        <ModalOverlay onClose={props.onClose}> {props.children} </ModalOverlay>,
        portalElement!
      )}
    </>
  );
};
