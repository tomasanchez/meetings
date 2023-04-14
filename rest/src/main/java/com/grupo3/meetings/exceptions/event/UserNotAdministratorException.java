package com.grupo3.meetings.exceptions.event;

public class UserNotAdministratorException extends RuntimeException{
    public UserNotAdministratorException(String error) {
        super(error);
    }
}
