package com.grupo3.meetings.domain;

import lombok.Getter;
import lombok.Setter;

import java.time.DayOfWeek;
import java.time.LocalTime;
import java.util.HashSet;
import java.util.Set;

@Getter @Setter
public class Option {
    private DayOfWeek day;
    private LocalTime time;
    private Set<String> votes;

    public Option(DayOfWeek day, LocalTime time) {
        this.day = day;
        this.time = time;
        this.votes = new HashSet<>();
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
