package com.schedutn.scheduler.domain.commands

import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema
import jakarta.validation.constraints.NotBlank

/**
 * Join meeting command.
 *
 * @property username
 */
@Schema(description = "Command to Join a meeting")
data class JoinMeeting(

  @JsonProperty("username")
  @Schema(description = "User's username", example = "johndoe", required = true)
  @field:NotBlank
  val username: String,
) : Command
