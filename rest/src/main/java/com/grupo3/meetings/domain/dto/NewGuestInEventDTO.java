package com.grupo3.meetings.domain.dto;

public class NewGuestInEventDTO {

  private String guest;

  public NewGuestInEventDTO() {
  }

  public NewGuestInEventDTO(String guest) {
    this.guest = guest;
  }

  public String getGuest() {
    return guest;
  }

  public void setGuest(String guest) {
    this.guest = guest;
  }
}
