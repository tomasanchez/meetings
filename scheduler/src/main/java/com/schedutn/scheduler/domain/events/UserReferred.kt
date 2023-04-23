package com.schedutn.scheduler.domain.events

import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty
import io.swagger.v3.oas.annotations.media.Schema

@Schema(description = "User")
@JsonInclude(JsonInclude.Include.NON_NULL)
data class UserReferred(

  @Schema(description = "Unique identifier", example = "6443dd50fea3c96e4eb4853b", required = true)
  @JsonProperty("id")
  val id: String,

  @Schema(description = "Resource type", example = "user", required = true)
  @JsonProperty("username")
  val username: String,

  @Schema(description = "Resource type", example = "user@mail.org")
  @JsonProperty("email")
  val email: String? = null,

  @Schema(description = "User first name", example = "John")
  @JsonProperty("name")
  val name: String? = null,

  @Schema(description = "User last name", example = "Doe")
  @JsonProperty("lastName")
  val lastName: String? = null,

  @Schema(description = "User profile picture", example = "https://example.com/profile.jpg")
  @JsonProperty("profilePicture")
  val profilePicture: String? = null,
) : Event