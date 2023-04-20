package com.grupo3.meetings.api.DTO;

import com.grupo3.meetings.domain.Option;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

public class OptionDTO {
//    private DayOfWeek day;
    private LocalDate date;
    private LocalTime time;
//    private Set<String> votes;

    public OptionDTO(LocalDate day, LocalTime time) {
        this.time = time;
        this.date = day;
//        this.votes = new HashSet<>();
    }
    public LocalTime getTime() {
        return time;
    }

    public void setTime(LocalTime time) {
        this.time = time;
    }


    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public Option toOptionForEvent() {
        return new Option(this.date, this.time);
    }

}
