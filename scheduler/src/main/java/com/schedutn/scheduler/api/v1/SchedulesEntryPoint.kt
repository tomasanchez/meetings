package com.schedutn.scheduler.api.v1


import com.schedutn.scheduler.api.DataWrapper
import com.schedutn.scheduler.api.v1.SchedulesEntryPoint.Companion.SCHEDULES_ENTRY_POINT_URL
import com.schedutn.scheduler.domain.commands.JoinMeeting
import com.schedutn.scheduler.domain.commands.ScheduleMeeting
import com.schedutn.scheduler.domain.commands.ToggleVoting
import com.schedutn.scheduler.domain.commands.VoteForOption
import com.schedutn.scheduler.domain.events.MeetingScheduled
import com.schedutn.scheduler.service.ScheduleService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import jakarta.validation.Valid
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import org.springframework.web.servlet.support.ServletUriComponentsBuilder
import java.net.URI

@RestController
@RequestMapping(SCHEDULES_ENTRY_POINT_URL, produces = [MediaType.APPLICATION_JSON_VALUE])
@Tag(name = "Schedules", description = "Schedules Entry Point")
class SchedulesEntryPoint {

  @Autowired
  lateinit var service: ScheduleService

  companion object {

    const val SCHEDULES_ENTRY_POINT_URL = "/api/v1/schedules"
    private val log = org.slf4j.LoggerFactory.getLogger(SchedulesEntryPoint::class.java)
  }

  @GetMapping
  @ResponseStatus(org.springframework.http.HttpStatus.OK)
  @Operation(
    summary = "Query Schedules",
    description = "Retrieves available schedules",
    tags = ["Queries"]
  )
  fun querySchedules(): DataWrapper<Collection<MeetingScheduled>> {
    log.info("Querying schedules")
    return DataWrapper(data = service.findAll())
  }

  @GetMapping("/{id}")
  @ResponseStatus(org.springframework.http.HttpStatus.OK)
  @Operation(
    summary = "Query Schedule",
    description = "Retrieves a schedule by id",
    tags = ["Queries"]
  )
  fun querySchedule(@PathVariable id: String): DataWrapper<MeetingScheduled> {
    log.info("Querying schedule with id: $id")

    val schedule = service.scheduleById(id)

    return DataWrapper(data = schedule)
  }

  @PostMapping
  @ResponseStatus(org.springframework.http.HttpStatus.CREATED)
  @Operation(
    summary = "Commands to Schedule a Meeting",
    description = "Creates a new meeting proposal",
    tags = ["Commands"]
  )
  fun scheduleMeeting(
    @Valid @RequestBody command: ScheduleMeeting): ResponseEntity<DataWrapper<MeetingScheduled>> {
    log.info("Scheduling meeting: $command")

    val scheduled = service.scheduleMeeting(command)

    val uri = URI.create(
      ServletUriComponentsBuilder
        .fromCurrentContextPath()
        .path("$SCHEDULES_ENTRY_POINT_URL/{id}")
        .buildAndExpand(scheduled.id)
        .toUriString()
    )

    return ResponseEntity.created(uri)
      .body(DataWrapper(data = scheduled))
  }

  @PatchMapping("/{id}/voting")
  @ResponseStatus(org.springframework.http.HttpStatus.OK)
  @Operation(
    summary = "Commands to Toggle Voting",
    description = "Enables or disables voting for a schedule",
    tags = ["Commands"]
  )
  fun toggleVoting(@PathVariable id: String,
                   @Valid @RequestBody command: ToggleVoting
  ): DataWrapper<MeetingScheduled> {
    log.info("Toggling voting for schedule with id: $id")

    val schedule = service.toggleVoting(id, command)

    return DataWrapper(data = schedule)
  }

  @PatchMapping("/{id}/options")
  @ResponseStatus(org.springframework.http.HttpStatus.OK)
  @Operation(
    summary = "Commands to Vote for an Option",
    description = "Adds or Revokes a vote for an option",
    tags = ["Commands"]
  )
  fun voteForOption(@PathVariable id: String,
                    @Valid @RequestBody command: VoteForOption
  ): DataWrapper<MeetingScheduled> {
    log.info("Voting for option for schedule with id: $id")

    val schedule = service.voteForAnOption(id = id, command = command)
    return DataWrapper(data = schedule)
  }

  @PatchMapping("/{id}/relationships/guests")
  @ResponseStatus(org.springframework.http.HttpStatus.OK)
  @Operation(
    summary = "Commands to Join a Meeting",
    description = "Adds a guest to a meeting",
    tags = ["Commands"]
  )
  fun joinMeeting(@PathVariable id: String, @Valid @RequestBody command: JoinMeeting): DataWrapper<MeetingScheduled> {
    log.info("Joining meeting for schedule with id: $id")


    val joined = service.joinAMeeting(id = id, username = command.username)

    log.info("${command.username} joined meeting for schedule with id: $id")

    return DataWrapper(data = joined)
  }
}