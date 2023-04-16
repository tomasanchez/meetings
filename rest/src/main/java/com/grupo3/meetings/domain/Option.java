package com.grupo3.meetings.domain;

import com.grupo3.meetings.api.DTO.OptionDTO;
import lombok.Getter;
import lombok.Setter;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.HashSet;
import java.util.Set;

@Getter @Setter
public class Option {
//    private DayOfWeek day;
    private LocalTime time;
    private Set<String> votes;

    private LocalDate date;

    public Option(LocalDate date, LocalTime time, Set<String> votes) {
        this.date = date;
        this.time = time;
        this.votes = votes;
    }
//    /**
//     * Default Option constructor.
//     * @param day Day of the week
//     * @param time Time of the day
//     */
//    public Option(DayOfWeek day, LocalTime time) {
//        this.day = day;
//        this.time = time;
//        this.votes = new HashSet<>();
//    }

//    public Option(OptionDTO optionRequest) {
//        this.day = optionRequest.getDay();
//        this.time = optionRequest.getTime();
//        this.votes = new HashSet<>();
//    }
    public Option(OptionDTO optionRequest) {
        this.date = optionRequest.getDate();
        this.time = optionRequest.getTime();
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


//    public String getDay() {
//        switch (day) {
//            case MONDAY:
//                return "lunes";
//            case TUESDAY:
//                return "martes";
//            case WEDNESDAY:
//                return "miércoles";
//            case THURSDAY:
//                return "jueves";
//            case FRIDAY:
//                return "viernes";
//            case SATURDAY:
//                return "sábado";
//            case SUNDAY:
//                return "domingo";
//            default:
//                return "error";
//        }
//    }

//    public void setDay(DayOfWeek day) {
//        this.day = day;
//    }

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
}
