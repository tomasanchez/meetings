package com.schedutn.scheduler.api.errors

import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema

@Schema(description = "Error wrapper")
@JsonInclude(JsonInclude.Include.NON_NULL)
class ErrorWrapper<T>(
  @Schema(description = "Error details")
  @JsonProperty("detail")
  val detail: T

) {
  @Schema(description = "Response metadata")
  @JsonProperty("meta")
  val meta: Map<String, Any>? = null
}