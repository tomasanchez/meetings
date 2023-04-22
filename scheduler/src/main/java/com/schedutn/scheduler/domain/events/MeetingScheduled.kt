package com.schedutn.scheduler.domain.events

import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema
import jakarta.validation.constraints.NotEmpty
import java.time.LocalDateTime

/**
 * Event for when a Meeting is Scheduled
 *
 * @property id Event Id
 * @property organizer The username of responsible for the event
 * @property voting Whether mode voting is enabled
 * @property title Event name
 * @property description More details about the event
 * @property location Where the event takes place
 * @property date When the event takes place
 * @property guests Invited users' usernames
 * @property options Options to schedule the event
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

  @JsonProperty("voting")
  @Schema(description = "Whether mode voting is enabled", example = "true")
  val voting: Boolean = false,

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