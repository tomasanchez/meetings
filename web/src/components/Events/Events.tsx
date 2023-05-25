import { useState } from "react";
import { EventGenerator } from "./EventGenerator";
import { EventForm } from "./EventForm";
import { AvailableEvent } from "./AvailableEvent";
import { ProtectedRoute } from '../Guards/ProtectedRoute';

export const Events = () => {
  const [createEventIsShown, setcreateEventIsShown] = useState(false);

  const openEventForm = () => {
    setcreateEventIsShown(true);
  };

  const closeEventForm = () => {
    setcreateEventIsShown(false);
  };

  return (
    <>
      {createEventIsShown &&  <ProtectedRoute><EventForm onClose={closeEventForm} /></ProtectedRoute> }
      <EventGenerator onCreate={openEventForm} />
      <AvailableEvent />
    </>
  );
};
