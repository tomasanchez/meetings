package com.schedutn.scheduler.api.jsonapi.response

import com.fasterxml.jackson.annotation.JsonIgnore
import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty
import com.schedutn.scheduler.api.jsonapi.AbstractJsonApiData
import com.schedutn.scheduler.api.jsonapi.AbstractJsonApiResource
import com.schedutn.scheduler.api.jsonapi.AbstractJsonApiResources
import com.schedutn.scheduler.api.jsonapi.JsonApiRelationShip
import com.schedutn.scheduler.domain.events.UserReferred
import io.swagger.v3.oas.annotations.media.Schema

@Schema(description = "Represents a user")
@JsonInclude(JsonInclude.Include.NON_NULL)
class UserJsonApiData(
  @JsonIgnore
  private val username: String,
) : AbstractJsonApiData<UserReferred>() {

  @Schema(description = "Unique identifier", example = "6443dd50fea3c96e4eb4853b", required = true)
  @JsonProperty("id")
  override val id: String = username

  @Schema(description = "User type", example = "user", required = true)
  @JsonProperty("type")
  override val type: String = "user"

  @Schema(description = "Data attributes", example = "null", required = true)
  @JsonProperty("attributes")
  @JsonIgnore
  override val attributes: UserReferred? = null

  @JsonIgnore
  override val relationships: JsonApiRelationShip? = null
}

@Schema(description = "Represents a User resource using JSON:API specification")
@JsonInclude(JsonInclude.Include.NON_NULL)
class UserJsonApiResource(
  @JsonIgnore
  private val username: String,
) : AbstractJsonApiResource<UserReferred>() {

  @Schema(description = "User data", required = true)
  @JsonProperty("data")
  override val data: UserJsonApiData = UserJsonApiData(username)
}

@Schema(description = "Represents a user resource collection using JSON:API specification")
@JsonInclude(JsonInclude.Include.NON_NULL)
class UserJsonApiResources(
  @JsonIgnore
  private val users: Collection<String>,
) : AbstractJsonApiResources<UserReferred>() {

  @JsonProperty("data")
  override val data: Collection<UserJsonApiData> = users.map { UserJsonApiData(it) }
}