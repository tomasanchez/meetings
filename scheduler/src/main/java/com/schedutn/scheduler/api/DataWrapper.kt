package com.schedutn.scheduler.api

import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema
import org.springframework.validation.annotation.Validated

@Schema(description = "Data wrapper")
@JsonInclude(JsonInclude.Include.NON_NULL)
class DataWrapper<T>(

  @Schema(description = "Response status", example = "success")
  @JsonProperty("status")
  val status: String? = "success",

  @Schema(description = "Message of the response", example = "OK")
  @JsonProperty("message")
  val message: String? = null,

  @Schema(description = "Data of the response")
  @JsonProperty("data")
  @Validated
  val data: T? = null,

  @Schema(description = "Metadata of the response", example = "{ \"total\": 1 }")
  @JsonProperty("meta")
  val meta: Map<String, Any>? = null,
)
