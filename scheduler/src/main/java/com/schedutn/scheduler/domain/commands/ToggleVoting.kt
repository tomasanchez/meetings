package com.schedutn.scheduler.domain.commands

import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema
import jakarta.validation.constraints.NotBlank

/**
 * Toggle voting command.
 *
 * @property username Username of the user who toggled voting
 * @property voting Whether voting is enabled or not
 */
@Schema(description = "Command to toggle voting")
data class ToggleVoting(

  @JsonProperty("username")
  @Schema(description = "Username of the user who toggled voting", required = true)
  @field:NotBlank
  val username: String,

  @JsonProperty("voting")
  @Schema(description = "Meeting ID", required = true)
  val voting: Boolean = true,
) : Command
