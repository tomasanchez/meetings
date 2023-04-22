package com.schedutn.scheduler.api.errors

import io.swagger.v3.oas.annotations.media.Schema

@Schema(description = "Error response")
data class UnAuthorizedScheduleOperation(

  @Schema(description = "Error code", example = "403")
  val code: String,

  @Schema(description = "Error message",
    example = "User has no permission to perform this operation")
  val message: String,
)
