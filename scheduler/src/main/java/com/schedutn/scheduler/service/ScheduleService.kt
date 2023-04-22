package com.schedutn.scheduler.service

import com.schedutn.scheduler.domain.commands.ScheduleMeeting
import com.schedutn.scheduler.domain.commands.ToggleVoting
import com.schedutn.scheduler.domain.commands.VoteForOption
import com.schedutn.scheduler.domain.events.MeetingScheduled

/**
 * Manages workflow for scheduling meetings.
 *
 * Provides methods for scheduling, joining, toggling voting,
 * and voting for options of a meeting use cases.
 */
interface ScheduleService {

  /**
   * Enables a user to Schedules meeting with certain options.
   *
   * Fulfills the use case: As a user, I want to schedule a meeting with certain options.
   *
   * @param command to Schedule a Meeting
   * @return an event representing the meeting scheduled
   */
  fun scheduleMeeting(command: ScheduleMeeting): MeetingScheduled

  /**
   * Allows a user to join a meeting a guest.
   *
   * Fulfills the use case: As a user, I want to join a meeting as a guest.
   *
   * @param id of the meeting
   * @param username who commands to join a meeting
   * @return an event representing the meeting once user has joined
   * @throws ScheduleNotFoundException if the meeting is not found
   */
  fun joinAMeeting(id: String, username: String): MeetingScheduled

  /**
   * Allows the organizer to enable or disable votes for a Schedule.
   *
   * Fulfills the use case: As an organizer, I want to enable or disable votes for a Schedule.
   *
   * @param id of the meeting
   * @param command to toggle voting
   * @return an event representing the meeting once voting has been toggled
   */
  fun toggleVoting(id: String, command: ToggleVoting): MeetingScheduled

  /**
   * Allows a user to vote for an option.
   *
   * Fulfills the use case: As a user, I want to vote for an option.
   *
   * @param id of the meeting
   * @param command to vote for an option
   * @return an event representing the meeting once user has voted
   */
  fun voteForAnOption(id: String, command: VoteForOption): MeetingScheduled

  /**
   * Finds a meeting by its id.
   *
   * @param id of the meeting
   * @return a meeting scheduled
   */
  fun scheduleById(id: String): MeetingScheduled?

  /**
   * Finds all meetings.
   *
   * @return a collection of meetings scheduled
   */
  fun findAll(): Collection<MeetingScheduled>
}