package com.schedutn.scheduler.api.jsonapi.response

import com.fasterxml.jackson.annotation.JsonIgnore
import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.annotation.JsonProperty
import com.schedutn.scheduler.api.jsonapi.AbstractJsonApiData
import com.schedutn.scheduler.api.jsonapi.AbstractJsonApiResource
import com.schedutn.scheduler.api.jsonapi.AbstractJsonApiResources
import com.schedutn.scheduler.api.jsonapi.JsonApiRelationShip
import com.schedutn.scheduler.domain.events.OptionVoted
import com.schedutn.scheduler.domain.models.MeetingOption
import io.swagger.v3.oas.annotations.media.Schema

@JsonInclude(JsonInclude.Include.NON_NULL)
class OptionJsonApiData(
  @JsonIgnore
  private val option: MeetingOption
) : AbstractJsonApiData<OptionVoted>() {

  @JsonProperty("id")
  @Schema(description = "Unique Identifier", example = "2020-10-10_0:0", required = true)
  override val id: String = "${option.date}_${option.hour}:${option.minute}"

  @JsonProperty("type")
  @Schema(description = "Option's type", example = "option", required = true)
  override val type: String = option.javaClass.simpleName.lowercase()

  @JsonProperty("attributes")
  @Schema(description = "Option's attributes", required = true)
  override val attributes: OptionVoted = OptionVoted(date = option.dateTime())

  @JsonProperty("relationships")
  @Schema(description = "Votes")
  override val relationships: JsonApiRelationShip? = null
}

@JsonInclude(JsonInclude.Include.NON_NULL)
class OptionJsonApiResource(
  @JsonIgnore
  private val option: MeetingOption
) : AbstractJsonApiResource<OptionVoted>() {

  @JsonProperty("data")
  @Schema(description = "Option's data", required = true)
  override val data: OptionJsonApiData = OptionJsonApiData(option)
}

@JsonInclude(JsonInclude.Include.NON_NULL)
class OptionJsonApiResources(
  @JsonIgnore
  private val options: Collection<MeetingOption>
) : AbstractJsonApiResources<OptionVoted>() {

  @JsonProperty("data")
  @Schema(description = "Options' data", required = true)
  override val data: Collection<OptionJsonApiData> = options.map { OptionJsonApiData(it) }
}