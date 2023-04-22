package com.schedutn.scheduler.domain.events

import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema
import jakarta.validation.constraints.NotEmpty
import java.time.LocalDateTime

/**
 * Meeting scheduled Event
 *
 * @property id
 * @property organizer
 * @property title
 * @property description
 * @property location
 * @property date
 * @property guests
 * @property options
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Meeting Scheduled")
data class MeetingScheduled(

  @JsonProperty("id")
  @Schema(description = "Event Id", example = "6442ee3291a1304d4c88ffc9", required = true)
  val id: String,

  @JsonProperty("organizer")
  @Schema(description = "Owner's username of the event", example = "johndoe", required = true)
  val organizer: String,

  @JsonProperty("title")
  @Schema(description = "Event Name", example = "Event Name", required = true)
  val title: String,

  @JsonProperty("description")
  @Schema(description = "Description of the event", example = "We will discuss the new project")
  val description: String? = null,

  @JsonProperty("location")
  @Schema(description = "Location of the event", example = "Zoom")
  val location: String? = null,

  @JsonProperty("date")
  @Schema(description = "Date when event takes place")
  val date: LocalDateTime? = null,

  @JsonProperty("guests")
  @Schema(description = "Invited users' usernames", example = "[user1, user2]")
  val guests: Set<String> = emptySet(),

  @JsonProperty("options")
  @Schema(description = "Options to schedule the event", required = true)
  @field:NotEmpty
  val options: Set<OptionVoted> = emptySet(),
) : Event