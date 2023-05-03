import { useState } from "react";
import { EventGenerator } from "./EventGenerator";
import { EventForm } from "./EventForm";
import { AvailableEvent } from "./AvailableEvent";

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
      {createEventIsShown && <EventForm onClose={closeEventForm} />}
      <EventGenerator onCreate={openEventForm} />
      <AvailableEvent />
    </>
  );
};
