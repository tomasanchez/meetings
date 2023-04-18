package com.grupo3.meetings.exceptions.event;

public class UserNotInGuestListException extends RuntimeException {
    public UserNotInGuestListException() {
        super("User is not in the guest list");
    }
}
