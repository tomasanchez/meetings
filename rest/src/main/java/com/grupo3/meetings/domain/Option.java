package com.grupo3.meetings.domain;

import java.time.DayOfWeek;
import java.time.LocalTime;
import java.util.HashSet;

public class Option {
    private DayOfWeek day;
    private LocalTime time;
    private HashSet<String> votes;

    public Option(DayOfWeek day, LocalTime time) {
        this.day = day;
        this.time = time;
        this.votes = new HashSet<String>();
    }

    public DayOfWeek getDay() {
        return day;
    }

    public void setDay(DayOfWeek day) {
        this.day = day;
    }

    public LocalTime getTime() {
        return time;
    }

    public void setTime(LocalTime time) {
        this.time = time;
    }

    public Integer getVotes() {
        return votes.size();
    }

    public void toggleVote(String userId) {
        if(this.votes.contains(userId))
            this.votes.remove(userId);
        else
            this.votes.add(userId);
    }
}
