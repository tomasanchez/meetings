package com.schedutn.scheduler.api.jsonapi.response

import com.fasterxml.jackson.annotation.JsonIgnore
import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty
import com.schedutn.scheduler.api.jsonapi.AbstractJsonApiData
import com.schedutn.scheduler.api.jsonapi.AbstractJsonApiResources
import com.schedutn.scheduler.api.jsonapi.JsonApiRelationShip
import com.schedutn.scheduler.domain.events.MeetingScheduled
import com.schedutn.scheduler.domain.models.Schedule
import io.swagger.v3.oas.annotations.media.Schema


@JsonInclude(JsonInclude.Include.NON_NULL)
class ScheduleJsonApiRelationShips(
  @JsonIgnore
  private val schedule: Schedule,
) : JsonApiRelationShip {

  @Schema(description = "Organizer")
  @JsonProperty("organizer")
  @JsonIgnore
  val organizer: JsonApiRelationShip? = null

  @Schema(description = "Options for the meeting to be scheduled")
  @JsonProperty("options")
  val options: OptionJsonApiResources = OptionJsonApiResources(schedule.options)

  @Schema(description = "Users invited to the meeting")
  @JsonProperty("guests")
  val guests: UserJsonApiResources = UserJsonApiResources(schedule.guests)
}

@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Represents a Meeting Schedule")
class ScheduleJsonApiData(
  @JsonIgnore
  private val schedule: Schedule,
) : AbstractJsonApiData<MeetingScheduled>() {

  @JsonProperty("id")
  @Schema(description = "Unique Identifier", example = "6442ee3291a1304d4c88ffc9", required = true)
  override val id: String = schedule.id!!

  @JsonProperty("type")
  @Schema(description = "Schedule's type", example = "schedule", required = true)
  override val type: String = schedule.javaClass.simpleName.lowercase()

  @JsonProperty("attributes")
  @Schema(description = "Schedule's attributes", required = true)
  override val attributes: MeetingScheduled = MeetingScheduled(
    id = schedule.id!!,
    organizer = schedule.organizer,
    title = schedule.event.title,
    description = schedule.event.description,
    location = schedule.event.location,
    date = schedule.date

  )

  @JsonProperty("relationships")
  @Schema(description = "Schedule's relationships")
  override val relationships: ScheduleJsonApiRelationShips = ScheduleJsonApiRelationShips(schedule)
}

/**
 * JSON:API Schedules format
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "JSON:API Response format for Multiple Schedules")
class ScheduleJsonApiResources(schedules: Collection<Schedule>)
  : AbstractJsonApiResources<MeetingScheduled>() {

  @JsonProperty("data")
  @Schema(description = "Schedules' data", required = true)
  override val data: Collection<ScheduleJsonApiData> = schedules.map { schedule ->
    ScheduleJsonApiData(schedule)
  }
}