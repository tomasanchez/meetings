package com.grupo3.meetings.exceptions.user;

public class UserAlreadyExists extends RuntimeException{
    public UserAlreadyExists () { super("User already exists"); }
}
