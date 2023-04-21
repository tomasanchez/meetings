package com.schedutn.scheduler.domain.models

import jakarta.validation.constraints.Max
import jakarta.validation.constraints.Min
import java.time.LocalDate
import java.time.LocalDateTime

/**
 * Event option is a possible date for a Schedule to be held.
 *
 * @property date tentative date for the event
 * @property hour tentative hour for the event
 * @property minute tentative minute for the event
 */
data class MeetingOption(

  val date: LocalDate,

  @field:Max(value = 23, message = "Hour must be less than 24")
  @field:Min(value = 0, message = "Hour must be greater or equal to 0")
  val hour: Int = 0,

  @field:Max(value = 59, message = "Minute must be less than 60")
  @field:Min(value = 0, message = "Minute must be greater or equal to 0")
  val minute: Int = 0,

  val votes: Set<String> = setOf(),
) {

  /**
   * Adds or removes a vote from the option.
   *
   * @param username username of the user that voted
   * @return a new instance of [MeetingOption] with the vote added or removed
   */
  fun vote(username: String): MeetingOption {

    val newVotes = votes.toMutableSet()

    if (newVotes.contains(username)) {
      newVotes.remove(username)
    } else {
      newVotes.add(username)
    }

    return copy(votes = newVotes)
  }

  /**
   * Obtains the date time of the option.
   *
   * @return date time of the option
   */
  fun dateTime(): LocalDateTime = LocalDateTime.of(date, java.time.LocalTime.of(hour, minute))

  override fun equals(other: Any?): Boolean {
    if (other == null) return false

    if (other !is MeetingOption) return false

    return date == other.date && hour == other.hour && minute == other.minute
  }

  override fun hashCode(): Int {
    var result = date.hashCode()
    result = 31 * result + hour
    result = 31 * result + minute
    return result
  }
}