package com.schedutn.scheduler.domain.events

import io.swagger.v3.oas.annotations.media.Schema
import java.time.LocalDateTime

@Schema(description = "Option Voted for a Schedule")
data class OptionVoted(

  @Schema(description = "Tentative date", required = true)
  val date: LocalDateTime,

  @Schema(description = "Voters' usernames", example = "[user1, user2]")
  val votes: Set<String> = emptySet(),
)
