package com.schedutn.scheduler.domain.commands

import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema
import jakarta.validation.constraints.Max
import jakarta.validation.constraints.Min
import java.time.LocalDate

@Schema(description = "Command to propose a meeting option")
data class ProposeOption(

  @Schema(description = "Proposed Date", required = true)
  @JsonProperty("date")
  val date: LocalDate,

  @Schema(description = "Proposed Hour", required = true)
  @JsonProperty("hour")
  @field:Max(value = 23, message = "Hour must be between 0 and 23")
  @field:Min(value = 0, message = "Hour must be between 0 and 23")
  val hour: Int,

  @Schema(description = "Proposed Minute", required = true)
  @JsonProperty("minute")
  @field:Max(value = 59, message = "Minute must be between 0 and 59")
  @field:Min(value = 0, message = "Minute must be between 0 and 59")
  val minute: Int,
) : Command
