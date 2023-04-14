package com.grupo3.meetings.exceptions.option;

public class OptionDoesntExistException extends RuntimeException {
    public OptionDoesntExistException() {
        super("Option does not exist");
    }
}
