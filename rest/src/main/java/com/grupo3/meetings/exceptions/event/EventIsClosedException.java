package com.grupo3.meetings.exceptions.event;

public class EventIsClosedException extends RuntimeException {
    public EventIsClosedException(String error) {
        super(error);
    }
}
