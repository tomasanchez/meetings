package com.schedutn.scheduler.api.v1


import com.schedutn.scheduler.api.DataWrapper
import com.schedutn.scheduler.api.v1.SchedulesEntryPoint.Companion.SCHEDULES_ENTRY_POINT_URL
import com.schedutn.scheduler.domain.events.MeetingScheduled
import com.schedutn.scheduler.domain.events.OptionVoted
import com.schedutn.scheduler.domain.models.Meeting
import com.schedutn.scheduler.domain.models.MeetingOption
import com.schedutn.scheduler.domain.models.Schedule
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import java.time.LocalDate

@RestController
@RequestMapping(SCHEDULES_ENTRY_POINT_URL)
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

  @GetMapping("/")
  @Operation(
    summary = "Query Schedules",
    description = "Retrieves available schedules"
  )
  fun querySchedules(): DataWrapper<Collection<MeetingScheduled>> {
    log.info("Querying schedules")

    val schedules = repository.values.map { schedule ->
      MeetingScheduled(
        id = schedule.id!!,
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


}