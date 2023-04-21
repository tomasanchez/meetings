package com.schedutn.scheduler.domain.models

import jakarta.validation.constraints.NotBlank

/**
 * Meeting.
 *
 * @property title name of the meeting
 * @property description brief description of the meeting
 * @property location where this meeting will be held
 */
data class Meeting(

  @field:NotBlank(message = "Schedule title must not be blank")
  val title: String,

  val description: String?,

  val location: String?,
)