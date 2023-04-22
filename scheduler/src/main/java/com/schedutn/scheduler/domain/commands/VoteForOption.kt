package com.schedutn.scheduler.domain.commands

import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema
import jakarta.validation.Valid
import jakarta.validation.constraints.NotEmpty

@Schema(description = "Command to vote for a meeting option")
data class VoteForOption(

  @JsonProperty("username")
  @Schema(description = "Username of the voter", required = true)
  @field:NotEmpty
  val username: String,

  @JsonProperty("option")
  @Schema(description = "Option to vote for", required = true)
  @field:Valid
  val option: ProposeOption
) : Command
