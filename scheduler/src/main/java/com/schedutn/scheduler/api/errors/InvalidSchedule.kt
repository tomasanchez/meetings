package com.schedutn.scheduler.api.errors

import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema

@Schema(description = "Error response")
data class InvalidSchedule(

  @Schema(description = "Error code", example = "404")
  @JsonProperty("code")
  val code: String,

  @Schema(description = "Error message", example = "Not found")
  @JsonProperty("message")
  val message: String,
)