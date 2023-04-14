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

    /**
     * Default Option constructor.
     * @param day Day of the week
     * @param time Time of the day
     */
    public Option(DayOfWeek day, LocalTime time) {
        this.day = day;
        this.time = time;
        this.votes = new HashSet<>();
    }

    /**
     * Returns the number of votes for this option.
     * @return Number of votes
     */
    public Integer getVotes() {
        return votes.size();
    }

    /**
     * Toggles the vote of a user for this option.
     * @param userId Id of the user that wants to vote or unvote
     */
    public void toggleVote(String userId) {
        if(this.votes.contains(userId))
            this.votes.remove(userId);
        else
            this.votes.add(userId);
    }
}
