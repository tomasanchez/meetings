package com.grupo3.meetings.domain;

import com.grupo3.meetings.api.DTO.OptionDTO;
import com.grupo3.meetings.api.DTO.VoteOptionDTO;
import lombok.Getter;
import lombok.Setter;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

@Getter @Setter
public class Option {
//    private DayOfWeek day;
    private LocalTime time;
    private Set<String> votes;

    private LocalDate date;

    public Option(LocalDate date, LocalTime time) {
        this.date = date;
        this.time = time;
        this.votes = new HashSet<>();
    }

    public Option(OptionDTO optionRequest) {
        this.time = optionRequest.getTime();
        this.date = optionRequest.getDate();
        this.votes= new HashSet<>();
    }

    public Option(VoteOptionDTO optionRequest) {
        this.time = optionRequest.getOption().getTime();
        this.votes= new HashSet<>();
        this.votes.add(optionRequest.getUsername());
        this.date = optionRequest.getOption().getDate();
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



    public LocalTime getTime() {
        return time;
    }

    public void setTime(LocalTime time) {
        this.time = time;
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

    public boolean equals(Option obj) {
        return this.date.equals(obj.getDate()) && this.time.equals(obj.getTime());
    }
}
