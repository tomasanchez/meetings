package com.grupo3.meetings.domain.dto;

public class VoteOptionDTO {

  private String username;
  private OptionDTO option;

  public VoteOptionDTO() {
  }

  public VoteOptionDTO(String username, OptionDTO option) {
    this.username = username;
    this.option = option;
  }

  public String getUsername() {
    return username;
  }

  public void setUsername(String username) {
    this.username = username;
  }

  public OptionDTO getOption() {
    return option;
  }

  public void setOption(OptionDTO option) {
    this.option = option;
  }

  public String getUserId() {
    return this.username;
  }
}
