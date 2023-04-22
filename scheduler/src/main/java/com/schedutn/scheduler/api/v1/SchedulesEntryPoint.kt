package com.schedutn.scheduler.api.v1


import com.schedutn.scheduler.api.DataWrapper
import com.schedutn.scheduler.api.v1.SchedulesEntryPoint.Companion.SCHEDULES_ENTRY_POINT_URL
import com.schedutn.scheduler.domain.commands.ScheduleMeeting
import com.schedutn.scheduler.domain.events.MeetingScheduled
import com.schedutn.scheduler.domain.events.OptionVoted
import com.schedutn.scheduler.domain.models.Meeting
import com.schedutn.scheduler.domain.models.MeetingOption
import com.schedutn.scheduler.domain.models.Schedule
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import jakarta.validation.Valid
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import org.springframework.web.servlet.support.ServletUriComponentsBuilder
import java.net.URI
import java.time.LocalDate

@RestController
@RequestMapping(SCHEDULES_ENTRY_POINT_URL, produces = [MediaType.APPLICATION_JSON_VALUE])
@Tag(name = "Schedules", description = "Schedules Entry Point")
class SchedulesEntryPoint {

  companion object {

    const val SCHEDULES_ENTRY_POINT_URL = "/api/v1/schedules"
    private val log = org.slf4j.LoggerFactory.getLogger(SchedulesEntryPoint::class.java)
    private val repository: MutableMap<String, Schedule> = mutableMapOf(
      "1" to Schedule(
        id = "1",
        options = setOf(
          MeetingOption(
            date = LocalDate.now(),
          ),
          MeetingOption(
            date = LocalDate.now().minusDays(2),
          ),
          MeetingOption(
            date = LocalDate.now().plusDays(2),
          ),
        ),
        organizer = "admin",
        event = Meeting(
          title = "Meeting with the team",
          description = "We will discuss the new project",
          location = "Zoom",
        )
      ),
    )
  }

  @GetMapping
  @ResponseStatus(org.springframework.http.HttpStatus.OK)
  @Operation(
    summary = "Query Schedules",
    description = "Retrieves available schedules"
  )
  fun querySchedules(): DataWrapper<Collection<MeetingScheduled>> {
    log.info("Querying schedules")

    val schedules = repository.values.map { schedule ->
      MeetingScheduled(
        id = schedule.id!!,
        voting = schedule.voting,
        options = schedule.options.map { OptionVoted(date = it.dateTime()) }.toSet(),
        guests = schedule.guests,
        organizer = schedule.organizer,
        title = schedule.event.title,
        description = schedule.event.description,
        location = schedule.event.location,
      )
    }.toSet()

    return DataWrapper(data = schedules)
  }

  @GetMapping("/{id}")
  @ResponseStatus(org.springframework.http.HttpStatus.OK)
  @Operation(
    summary = "Query Schedule",
    description = "Retrieves a schedule by id"
  )
  fun querySchedule(@PathVariable id: String): DataWrapper<MeetingScheduled> {
    log.info("Querying schedule with id: $id")

    val schedule = repository[id] ?: throw IllegalArgumentException(
      "Schedule with id: $id not found")

    val meetingScheduled = MeetingScheduled(
      id = schedule.id!!,
      voting = schedule.voting,
      options = schedule
        .options
        .map {
          OptionVoted(date = it.dateTime(),
            votes = it.votes
          )
        }
        .toSet(),
      guests = schedule.guests,
      organizer = schedule.organizer,
      title = schedule.event.title,
      description = schedule.event.description,
      location = schedule.event.location,
    )

    return DataWrapper(data = meetingScheduled)
  }

  @PostMapping
  @ResponseStatus(org.springframework.http.HttpStatus.CREATED)
  @Operation(
    summary = "Commands to Schedule a Meeting",
    description = "Creates a new meeting proposal"
  )
  fun scheduleMeeting(
    @Valid @RequestBody command: ScheduleMeeting): ResponseEntity<DataWrapper<MeetingScheduled>> {
    log.info("Scheduling meeting: $command")

    val schedule = Schedule(
      id = (repository.values.count() + 1).toString(),
      organizer = command.organizer,
      event = Meeting(
        title = command.title,
        description = command.description,
        location = command.location,
      ),
      options = command
        .options
        .map {
          MeetingOption(date = it.date, hour = it.hour, minute = it.minute)
        }.toSet(),
      guests = command.guests ?: emptySet(),
    )

    repository[schedule.id!!] = schedule

    val uri = URI.create(
      ServletUriComponentsBuilder
        .fromCurrentContextPath()
        .path("$SCHEDULES_ENTRY_POINT_URL/{id}")
        .buildAndExpand(schedule.id)
        .toUriString()
    )

    return ResponseEntity.created(uri)
      .body(DataWrapper(data = scheduleToMeetingScheduled(schedule)))
  }

  /**
   * Converts a Schedule to a MeetingScheduled
   *
   * @param schedule to be translated
   * @return an Event with the corresponding JSON representation
   */
  private fun scheduleToMeetingScheduled(schedule: Schedule): MeetingScheduled {
    return MeetingScheduled(
      id = schedule.id!!,
      voting = schedule.voting,
      options = schedule
        .options
        .map {
          OptionVoted(date = it.dateTime(),
            votes = it.votes
          )
        }
        .toSet(),
      guests = schedule.guests,
      organizer = schedule.organizer,
      title = schedule.event.title,
      description = schedule.event.description,
      location = schedule.event.location,
    )
  }
}