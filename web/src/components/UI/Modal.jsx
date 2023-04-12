import React from 'react'
import classes from './Modal.module.css'
import reactDom from 'react-dom'


const Backdrop = (props) => {
    return <div onClick={props.onClose} className={classes.backdrop}> </div>;
  };
  
  const ModalOverlay = (props) => {
    return (
      <div className={classes.modal}>
        <div className={classes.content}>{props.children}</div>
      </div>
    );
  };
  
  const portalElement = document.getElementById('overlay');
  
  export const Modal = (props) => {
    return(
    <>
    {reactDom.createPortal(<Backdrop onClose={props.onClose}/>, portalElement)}
    {reactDom.createPortal(<ModalOverlay> {props.children} </ModalOverlay>, portalElement)}
    </>);
  };
  