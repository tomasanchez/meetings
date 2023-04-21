package com.grupo3.meetings.domain.dto;

import com.grupo3.meetings.domain.models.Option;
import java.time.LocalDate;
import java.time.LocalTime;

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
