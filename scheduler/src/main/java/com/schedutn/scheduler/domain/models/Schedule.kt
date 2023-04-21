package com.schedutn.scheduler.domain.models

import com.schedutn.scheduler.domain.IllegalScheduleException
import com.schedutn.scheduler.domain.IllegalVoteException
import jakarta.validation.Valid
import jakarta.validation.constraints.Min
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.NotEmpty
import java.time.LocalDateTime

/**
 * Schedule
 *
 * Aggregate all the information about a Schedule.
 *
 * @property version version of the schedule
 * @property organizer username of the organizer
 * @property voting whether voting is enabled or not
 * @property event meeting information
 * @property guests list of guests
 * @property options list of options
 * @property date voted date of the event
 */
data class Schedule(

  val id: String? = null,

  @field:Min(value = 0, message = "Version must be greater or equal to 0")
  val version: Int = 0,

  @field:NotBlank(message = "Organizer username must not be blank")
  val organizer: String,

  val voting: Boolean = false,

  @field:Valid
  val event: Meeting,

  val guests: Set<String> = setOf(),

  @field:NotEmpty
  @field:Valid
  val options: Set<MeetingOption>,

  val date: LocalDateTime? = null,
) : PersistentEntity {

  /**
   * Votes or revokes a vote for an option.
   *
   * @param username username of the guest
   * @param option option to vote
   * @return new schedule with the option voted
   * @throws IllegalVoteException if voting is not enabled, user is not a guest or option is not valid
   */
  fun vote(username: String, option: MeetingOption): Schedule {

    if (!voting)
      throw IllegalVoteException("Voting is not enabled")

    if (!guests.contains(username) && username != organizer)
      throw IllegalVoteException("User is not a guest")

    if (!options.contains(option))
      throw IllegalVoteException("Option is not valid")


    return copy(options = options.map { if (it == option) it.vote(username) else it }.toSet(),
      version = version + 1
    )
  }

  /**
   * Returns the option with the most votes.
   *
   * @return option with the most votes
   */
  private fun getMostVotedOption(): MeetingOption =
    options.maxByOrNull { it.votes.size } ?: options.first()

  /**
   * Sets the date of the event to the most voted option.
   *
   * @param username user who wants to set the date
   * @return new schedule with the date set
   */
  fun schedule(username: String): Schedule {

    if (username != organizer)
      throw IllegalScheduleException("Only the organizer can schedule the event")

    return copy(
      date = getMostVotedOption().dateTime(),
      voting = false,
      version = version + 1
    )
  }

  /**
   * Enables or disables voting.
   *
   * @param username user who wants to enable or disable voting
   * @param enabledVotes whether voting is enabled or not
   * @return new schedule with the new voting policy
   */
  fun toggleVoting(username: String, enabledVotes: Boolean): Schedule {

    if (username != organizer)
      throw IllegalScheduleException("Only the organizer can enable or disable voting")

    return copy(
      voting = enabledVotes,
      version = version + 1
    )
  }

  override fun getIdentifier(): String? = id

}
