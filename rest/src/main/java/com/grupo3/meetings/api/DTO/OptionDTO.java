package com.grupo3.meetings.api.DTO;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Set;

public class OptionDTO {
//    private DayOfWeek day;
    private LocalDate date;
    private LocalTime time;
    private Set<String> votes;

//    public OptionDTO(DayOfWeek day, LocalTime time, Set<String> votes) {
//        this.day = day;
//        this.time = time;
//        this.votes = votes;
//    }
    public OptionDTO(LocalDate day, LocalTime time, Set<String> votes) {
        this.date  = day;
        this.time = time;
        this.votes = votes;
    }
    public LocalTime getTime() {
        return time;
    }

    public void setTime(LocalTime time) {
        this.time = time;
    }

    public Set<String> getVotes() {
        return votes;
    }

    public void setVotes(Set<String> votes) {
        this.votes = votes;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }
}
