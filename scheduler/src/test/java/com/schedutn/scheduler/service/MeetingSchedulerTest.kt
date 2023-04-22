package com.schedutn.scheduler.service

import com.schedutn.scheduler.domain.commands.ProposeOption
import com.schedutn.scheduler.domain.commands.ScheduleMeeting
import com.schedutn.scheduler.domain.commands.ToggleVoting
import com.schedutn.scheduler.domain.commands.VoteForOption
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import java.time.LocalDate
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

internal class MeetingSchedulerTest {

  private lateinit var meetingScheduler: MeetingScheduler
  private lateinit var scheduleCommand: ScheduleMeeting
  private lateinit var option1: ProposeOption
  private lateinit var option2: ProposeOption

  @BeforeEach
  fun setUp() {
    meetingScheduler = MeetingScheduler()

    option1 = ProposeOption(
      date = LocalDate.now(),
      hour = 10,
      minute = 0,
    )

    option2 = ProposeOption(
      date = LocalDate.now(),
      hour = 11,
      minute = 0,
    )

    scheduleCommand = ScheduleMeeting(
      organizer = "user1",
      title = "Meeting",
      description = "A meeting",
      location = "A location",
      options = setOf(
        option1,
        option2,
      ),
      guests = setOf("user2", "user3"),
    )
  }

  @Test
  fun `a meeting can be scheduled`() {
    // Given a command to schedule a meeting

    // When
    val event = meetingScheduler.scheduleMeeting(scheduleCommand)

    // Then
    assertTrue { event.id.isNotBlank() }
    assertTrue { event.organizer == scheduleCommand.organizer }
    assertTrue { event.title == scheduleCommand.title }
    assertTrue { event.description == scheduleCommand.description }
    assertTrue { event.location == scheduleCommand.location }
    assertTrue { event.options.size == scheduleCommand.options.size }
    assertTrue { event.guests.size == scheduleCommand.guests!!.size }
  }

  @Test
  fun `a meeting can be found by its id`() {
    // Given
    val event = meetingScheduler.scheduleMeeting(scheduleCommand)

    // When
    val schedule = meetingScheduler.scheduleById(event.id)

    // Then
    assertEquals(schedule.id, event.id)
  }

  @Test
  fun `an exception is thrown when a meeting is not found`() {
    // Given
    val id = "not-found"

    // Throws when
    assertThrows<ScheduleNotFoundException> {
      meetingScheduler.scheduleById(id)
    }
  }

  @Test
  fun `a user can join a meeting`() {
    // Given
    val newJoiner = "user4"
    val event = meetingScheduler.scheduleMeeting(scheduleCommand)

    // When
    val joined = meetingScheduler.joinAMeeting(id = event.id, username = newJoiner)

    // Then
    assertTrue { newJoiner in joined.guests }
  }

  @Test
  fun `organizer can toggle voting`() {
    // Given
    val organizer = "organizer"
    val event = meetingScheduler.scheduleMeeting(
      scheduleCommand.copy(organizer = organizer)
    )

    // When
    val toggled = meetingScheduler.toggleVoting(
      id = event.id,
      command = ToggleVoting(
        username = organizer,
        voting = true,
      )
    )

    // Then
    assertFalse { event.voting }
    assertTrue { toggled.voting }
  }

  @Test
  fun `others than the organizer cannot toggle voting`() {
    // Given
    val organizer = "organizer"
    val event = meetingScheduler.scheduleMeeting(
      scheduleCommand.copy(organizer = organizer)
    )

    // Throws When
    assertThrows<ScheduleAuthorizationException> {
      meetingScheduler.toggleVoting(
        id = event.id,
        command = ToggleVoting(
          username = "other",
          voting = true,
        )
      )
    }
  }

  @Test
  fun `user can vote for option`() {
    // Given
    val owner = "owner"
    val voter = "voter"
    val event = meetingScheduler.scheduleMeeting(
      scheduleCommand.copy(organizer = owner, guests = setOf(voter)))
    meetingScheduler.toggleVoting(
      id = event.id,
      command = ToggleVoting(
        username = owner,
        voting = true,
      )
    )

    // When
    val voted = meetingScheduler.voteForAnOption(
      id = event.id,
      VoteForOption(
        username = voter,
        option = option1,
      )
    )

    // Then
    assertTrue { voted.options.any { it.votes.contains(voter) } }
  }

  @Test
  fun `user cannot vote for option if voting is not enabled`() {
    // Given
    val owner = "owner"
    val voter = "voter"
    val event = meetingScheduler.scheduleMeeting(
      scheduleCommand.copy(organizer = owner, guests = setOf(voter)))
    meetingScheduler.toggleVoting(
      id = event.id,
      command = ToggleVoting(
        username = owner,
        voting = false,
      )
    )

    // Throws When
    assertThrows<ScheduleAuthorizationException> {
      meetingScheduler.voteForAnOption(
        id = event.id,
        VoteForOption(
          username = voter,
          option = option1,
        )
      )
    }
  }

  @Test
  fun `user cannot vote for option if not a guest`() {
    // Given
    val owner = "owner"
    val voter = "voter"
    val event = meetingScheduler.scheduleMeeting(
      scheduleCommand.copy(organizer = owner, guests = setOf(voter)))
    meetingScheduler.toggleVoting(
      id = event.id,
      command = ToggleVoting(
        username = owner,
        voting = true,
      )
    )

    // Throws When
    assertThrows<ScheduleAuthorizationException> {
      meetingScheduler.voteForAnOption(
        id = event.id,
        VoteForOption(
          username = "other",
          option = option1,
        )
      )
    }
  }

  @Test
  fun `user cannot vote for option not registered`() {
    // Given
    val owner = "owner"
    val voter = "voter"
    val event = meetingScheduler.scheduleMeeting(
      scheduleCommand.copy(organizer = owner, guests = setOf(voter)))
    meetingScheduler.toggleVoting(
      id = event.id,
      command = ToggleVoting(
        username = owner,
        voting = true,
      )
    )

    // Throws When
    assertThrows<ScheduleAuthorizationException> {
      meetingScheduler.voteForAnOption(
        id = event.id,
        VoteForOption(
          username = voter,
          option = ProposeOption(
            date = option1.date.plusDays(100),
            hour = 12,
            minute = 0,
          ),
        )
      )
    }
  }

}