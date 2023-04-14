package com.grupo3.meetings.exceptions.option;

public class NoOptionVotedException extends RuntimeException{
    public NoOptionVotedException() {
        super("No option voted");
    }
}
