package com.grupo3.meetings.exceptions.event;

import com.grupo3.meetings.domain.Option;

public class OptionNotFoundException extends RuntimeException {
    public OptionNotFoundException(String message) {
        super(message);
    }

    public OptionNotFoundException(Option option) {
        super("Option not found : " + option.getDate() + " " + option.getTime());
    }
}
