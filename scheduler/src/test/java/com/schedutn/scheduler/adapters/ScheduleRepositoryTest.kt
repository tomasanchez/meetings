package com.schedutn.scheduler.adapters

import com.schedutn.scheduler.domain.models.Meeting
import com.schedutn.scheduler.domain.models.MeetingOption
import com.schedutn.scheduler.domain.models.Schedule
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import java.time.LocalDate
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotNull

internal class ScheduleRepositoryTest {

  private lateinit var repository: ScheduleRepository

  private lateinit var schedule: Schedule

  @BeforeEach
  fun setUp() {
    repository = ScheduleRepository()

    schedule = Schedule(
      version = 0,
      organizer = "organizer",
      event = Meeting(
        title = "title",
        description = "description",
        location = "location",
      ),
      guests = setOf("attendee"),
      options = setOf(
        MeetingOption(
          date = LocalDate.now(),
          hour = 12,
          minute = 30,
        )
      ),
    )
  }

  @Test
  fun `when a schedule is save, an id is generated`() {
    // When
    val saved = repository.save(schedule)

    // Then
    assertNotNull(saved.id)
  }

  @Test
  fun `when a schedule is saved, version is incremented `() {
    // Given
    val previousVersion = schedule.version

    // When
    val saved = repository.save(schedule)

    // Then
    assertEquals(previousVersion + 1, saved.version)
  }

  @Test
  fun `a schedule cannot be saved if it has been modified`() {
    // Given
    val old = repository.save(schedule)
    repository.save(old.copy(organizer = "newOrganizer"))

    // Throws When
    assertThrows<IllegalStateException> {
      repository.save(old)
    }
  }

  @Test
  fun `a repository lists all saved schedules`() {
    // Given
    repository.save(schedule)

    // When
    val schedules = repository.findAll()

    // Then
    assertEquals(1, schedules.size)
  }

  @Test
  fun `a repository can find a saved schedule by its id`() {
    // Given
    val saved = repository.save(schedule)

    // When
    val found = repository.findById(saved.id!!)

    // Then
    assertEquals(saved, found)
  }

  @Test
  fun `a repository can delete a saved schedule by its id`() {
    // Given
    val saved = repository.save(schedule)

    // When
    repository.deleteById(saved.id!!)

    // Then
    assertFalse { repository.findAll().contains(saved) }
  }

}