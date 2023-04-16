package com.grupo3.meetings.exceptions.event;

public class UnauthorizedUserException extends RuntimeException {
    public UnauthorizedUserException() {
        super("You are not authorized to perform this action.");
    }
}
