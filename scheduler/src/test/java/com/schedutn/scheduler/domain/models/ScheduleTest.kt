package com.schedutn.scheduler.domain.models

import com.schedutn.scheduler.domain.IllegalScheduleException
import com.schedutn.scheduler.domain.IllegalVoteException
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import java.time.LocalDate
import kotlin.test.assertFalse
import kotlin.test.assertNotNull
import kotlin.test.assertTrue

internal class ScheduleTest {

  private val options = setOf(
    MeetingOption(
      date = LocalDate.now(),
    ),
    MeetingOption(
      date = LocalDate.now().plusDays(1),
    ),
  )

  @Test
  fun `a schedule can be vote by a guest`() {
    // Given
    val username = "guest"
    val guests = setOf(username)
    val schedule = Schedule(
      organizer = "organizer",
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      guests = guests,
      voting = true,
    )

    val vote = MeetingOption(
      date = LocalDate.now().plusDays(1))

    // When
    val votedSchedule = schedule.vote(username = username, option = vote)

    // Then
    assertTrue {
      votedSchedule.options.any { it.votes.contains(username) }
    }
  }

  @Test
  fun `a schedule can be vote by a organizer`() {
    // Given
    val organizer = "organizer"
    val schedule = Schedule(
      organizer = organizer,
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      voting = true,
    )

    val vote = MeetingOption(
      date = LocalDate.now().plusDays(1))

    // When
    val votedSchedule = schedule.vote(username = organizer, option = vote)

    // Then
    assertTrue {
      votedSchedule.options.any { it.votes.contains(organizer) }
    }
  }

  @Test
  fun `a schedule cannot be voted if not enabled`() {

    val schedule = Schedule(
      organizer = "organizer",
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      voting = false,
    )

    assertThrows<IllegalVoteException> {
      schedule.vote(username = "guest", option = MeetingOption(date = LocalDate.now()))
    }
  }

  @Test
  fun `a schedule cannot be voted if user is not invited`() {

    val schedule = Schedule(
      organizer = "organizer",
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      voting = true,
    )

    assertThrows<IllegalVoteException> {
      schedule.vote(username = "not a guest", option = MeetingOption(date = LocalDate.now()))
    }
  }

  @Test
  fun `a schedule cannot be voted for an option not included in options`() {
    val schedule = Schedule(
      organizer = "organizer",
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      voting = true,
    )

    assertThrows<IllegalVoteException> {
      schedule.vote(username = "guest",
        option = MeetingOption(date = LocalDate.now().plusDays(2)))
    }
  }

  @Test
  fun `a schedule can be toggled by its organizer`() {
    // Given
    val userOrganizer = "organizer"
    val schedule = Schedule(
      organizer = userOrganizer,
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      voting = false,
    )

    // When
    val enabledSchedule = schedule.toggleVoting(userOrganizer, true)

    // Then
    assertTrue { enabledSchedule.voting }
  }

  @Test
  fun `a schedule cannot be toggled by others than the organizer`() {
    // Given
    val schedule = Schedule(
      organizer = "organizer",
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      voting = false,
    )

    // Throws when
    assertThrows<IllegalScheduleException> {
      schedule.toggleVoting("not the organizer", true)
    }
  }

  @Test
  fun `a schedule can be scheduled by its organizer`() {
    // Given
    val organizer = "organizer"

    val schedule = Schedule(
      organizer = organizer,
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      voting = true,
      date = null,
    )

    // When
    val scheduled = schedule.schedule(organizer)

    // Then
    assertFalse { scheduled.voting }
    assertNotNull(scheduled.date)
    assertTrue {
      scheduled.options.any { it.dateTime() == scheduled.date }
    }
  }

  @Test
  fun `a schedule cannot be scheduled by other than organizer`() {
    // Given
    val organizer = "organizer"
    val username = "guest"
    val schedule = Schedule(
      organizer = organizer,
      event = Meeting(
        title = "title",
        location = "location",
        description = "description",
      ),
      options = options,
      voting = true,
      date = null,
    )

    // Throws When

    assertThrows<IllegalScheduleException> {
      schedule.schedule(username)
    }
  }
}