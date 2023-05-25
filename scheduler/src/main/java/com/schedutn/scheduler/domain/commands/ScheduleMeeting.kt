package com.schedutn.scheduler.domain.commands

import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema
import jakarta.validation.Valid
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.NotEmpty

/**
 * Schedule meeting command.
 *
 * @property organizer Meeting Organizer's username
 * @property title Meeting Title
 * @property description Meeting Description
 * @property location Meeting Location
 * @property options Meeting Options
 * @property guests Meeting Guests' usernames
 */
@Schema(description = "Command to schedule a meeting")
data class ScheduleMeeting(

  @Schema(description = "Meeting Organizer's username", example = "johndoe", required = true)
  @JsonProperty("organizer")
  @field:NotBlank
  val organizer: String,

  @Schema(description = "Meeting Title", example = "Meeting with the team", required = true)
  @JsonProperty("title")
  @field:NotBlank
  val title: String,

  @Schema(description = "Meeting Description", example = "We will discuss the new project")
  @JsonProperty("description")
  val description: String? = null,

  @Schema(description = "Meeting Location", example = "Zoom")
  @JsonProperty("location")
  val location: String? = null,

  @Schema(description = "Meeting Options", required = true)
  @JsonProperty("options")
  @field:NotEmpty
  @field:Valid
  val options: Set<ProposeOption>,

  @Schema(description = "Meeting Guests invited", example = "[]", deprecated = true)
  @JsonProperty("guests")
  val guests: Set<String>? = emptySet(),
) : Command
