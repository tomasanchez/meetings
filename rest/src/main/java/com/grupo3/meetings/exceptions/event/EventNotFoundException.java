package com.grupo3.meetings.exceptions.event;

public class EventNotFoundException extends RuntimeException {
    public EventNotFoundException(String eventId) {
        super("Event not found with id: " + eventId);
    }

    public EventNotFoundException(Long eventId) {
        super("Event not found with id: " + eventId);
    }
}
