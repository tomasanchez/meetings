package com.schedutn.scheduler.service

import com.schedutn.scheduler.domain.commands.ProposeOption
import com.schedutn.scheduler.domain.commands.ScheduleMeeting
import com.schedutn.scheduler.domain.commands.ToggleVoting
import com.schedutn.scheduler.domain.commands.VoteForOption
import com.schedutn.scheduler.domain.models.Meeting
import com.schedutn.scheduler.domain.models.Schedule
import com.schedutn.scheduler.repository.ScheduleRepositoryMongo
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import org.mockito.Mockito
import org.mockito.Mockito.verify
import java.time.LocalDate
import java.util.*
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

internal class MeetingSchedulerTest {

  private lateinit var meetingScheduler: MeetingScheduler
  private lateinit var scheduleCommand: ScheduleMeeting
  private lateinit var option1: ProposeOption
  private lateinit var option2: ProposeOption
  private lateinit var repository: ScheduleRepositoryMongo

  @BeforeEach
  fun setUp() {
    repository = Mockito.mock(ScheduleRepositoryMongo::class.java)
    meetingScheduler = MeetingScheduler(schedules = repository)
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
    Mockito.`when`(repository.save(Mockito.any())).thenReturn(eventFromCommand(scheduleCommand))


    // When
    meetingScheduler.scheduleMeeting(scheduleCommand)


    // Then
    verify(repository).save(Mockito.any())
  }

  @Test
  fun `a meeting can be found by its id`() {
    // Given
    val event = eventFromCommand(scheduleCommand)
    val id: String = event.id as String

    // Mocking
    Mockito.`when`(repository.findById(id)).thenReturn(Optional.of(event))

    // When
    val schedule = meetingScheduler.scheduleById(id)

    // Then
    assertEquals(schedule.id, event.id)
  }

  @Test
  fun `an exception is thrown when a meeting is not found`() {
    // Given
    val id = "not-found"

    // Mocking
    Mockito.`when`(repository.findById(id)).thenReturn(Optional.empty())

    // Throws when
    assertThrows<ScheduleNotFoundException> {
      meetingScheduler.scheduleById(id)
    }
  }

  @Test
  fun `a user can join a meeting`() {
    // Given
    val newJoiner = "user4"
    val event = eventFromCommand(scheduleCommand)
    val id = event.id!!

    // Mocking
    Mockito.`when`(repository.findById(id)).thenReturn(Optional.of(event))
    Mockito.`when`(repository.save(Mockito.any())).thenReturn(eventFromCommand(scheduleCommand).join(newJoiner))

    // When
    val joined = meetingScheduler.joinAMeeting(id = id, username = newJoiner)


    // Then
    assertTrue { newJoiner in joined.guests }
  }

  @Test
  fun `organizer can toggle voting`() {
    // Given
    val organizer = "organizer"
    val event = eventFromCommand(scheduleCommand.copy(organizer = organizer))
    val id = event.id!!

    // Mocking
    Mockito
      .`when`(repository.findById(id))
      .thenReturn(Optional.of(event))
    Mockito
      .`when`(repository.save(Mockito.any()))
      .thenReturn(event.toggleVoting(organizer, true))

    // When
    val toggled = meetingScheduler.toggleVoting(
      id = id,
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
    val event = eventFromCommand(scheduleCommand.copy(organizer = organizer))
    val id = event.id!!

    // Mocking
    Mockito
      .`when`(repository.findById(id))
      .thenReturn(Optional.of(event))

    // Throws When
    assertThrows<ScheduleAuthorizationException> {
      meetingScheduler.toggleVoting(
        id = id,
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
    val event =
      eventFromCommand(scheduleCommand.copy(organizer = owner, guests = setOf(voter)))
        .toggleVoting(owner, true)
    val id = event.id!!

    // Mocking
    Mockito
      .`when`(repository.findById(id))
      .thenReturn(Optional.of(event))
    Mockito
      .`when`(repository.save(Mockito.any()))
      .thenReturn(event)

    // When
    meetingScheduler.voteForAnOption(
      id = id,
      VoteForOption(
        username = voter,
        option = option1,
      )
    )

    // Then
    verify(repository).save(Mockito.any())
  }

  @Test
  fun `user cannot vote for option if voting is not enabled`() {
    // Given
    val owner = "owner"
    val voter = "voter"
    val event = eventFromCommand(scheduleCommand.copy(organizer = owner, guests = setOf(voter)))
      .toggleVoting(owner, false)
    val id = event.id!!

    // Mocking
    Mockito
      .`when`(repository.findById(id))
      .thenReturn(Optional.of(event))

    // Throws When
    assertThrows<ScheduleAuthorizationException> {
      meetingScheduler.voteForAnOption(
        id = id,
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
    val event = eventFromCommand(scheduleCommand.copy(organizer = owner, guests = setOf(voter)))
      .toggleVoting(owner, true)
    val id = event.id!!

    // Mocking
    Mockito
      .`when`(repository.findById(id))
      .thenReturn(Optional.of(event))

    // Throws When
    assertThrows<ScheduleAuthorizationException> {
      meetingScheduler.voteForAnOption(
        id = id,
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
    val event = eventFromCommand(scheduleCommand.copy(organizer = owner, guests = setOf(voter)))
      .toggleVoting(owner, true)
    val id = event.id!!

    // Mocking
    Mockito
      .`when`(repository.findById(id))
      .thenReturn(Optional.of(event))

    // Throws When
    assertThrows<ScheduleAuthorizationException> {
      meetingScheduler.voteForAnOption(
        id = id,
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

  /**
   * Event from command
   *
   * @param command to create event
   * @return a new event instance
   */
  private fun eventFromCommand(command: ScheduleMeeting): Schedule = Schedule(
    id = UUID.randomUUID().toString(),
    organizer = command.organizer,
    event = Meeting(
      title = command.title,
      description = command.description,
      location = command.location,
    ),
    options = command.options.map {
      com.schedutn.scheduler.domain.models.MeetingOption(
        date = it.date,
        hour = it.hour,
        minute = it.minute,
      )
    }.toSet(),
    guests = command.guests ?: emptySet(),
  )


}