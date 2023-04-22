package com.schedutn.scheduler.api

import com.schedutn.scheduler.api.errors.InvalidSchedule
import com.schedutn.scheduler.api.errors.UnAuthorizedScheduleOperation
import com.schedutn.scheduler.service.ScheduleAuthorizationException
import com.schedutn.scheduler.service.ScheduleNotFoundException
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpStatus
import org.springframework.http.HttpStatusCode
import org.springframework.http.ResponseEntity
import org.springframework.validation.FieldError
import org.springframework.validation.ObjectError
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.ResponseStatus
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.context.request.WebRequest
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler

@RestControllerAdvice
class GlobalControllerExceptionHandler : ResponseEntityExceptionHandler() {

  companion object {

    private val log = org.slf4j.LoggerFactory.getLogger(
      GlobalControllerExceptionHandler::class.java)
  }

  @ResponseStatus(HttpStatus.NOT_FOUND)
  @ExceptionHandler(ScheduleNotFoundException::class)
  fun handleScheduleNotFound(
    ex: ScheduleNotFoundException): ResponseEntity<InvalidSchedule> {

    val details = InvalidSchedule(
      code = "404",
      message = ex.message ?: "Not found"
    )

    log.error("404: $details")
    return ResponseEntity(details, HttpStatus.NOT_FOUND)
  }

  @ResponseStatus(HttpStatus.FORBIDDEN)
  @ExceptionHandler(ScheduleAuthorizationException::class)
  fun handleScheduleAuthorization(
    ex: ScheduleAuthorizationException): ResponseEntity<UnAuthorizedScheduleOperation> {

    val bodyOfResponse = UnAuthorizedScheduleOperation(
      code = "403",
      message = ex.message ?: "Forbidden"
    )
    
    return ResponseEntity(bodyOfResponse, HttpStatus.FORBIDDEN)
  }

  /**
   * Handles Unprocessable Entity Exceptions.
   *
   * @param ex The runtime exception
   * @return a response entity with the occurred errors and an unprocessable entity status
   */
  override fun handleMethodArgumentNotValid(ex: MethodArgumentNotValidException,
    headers: HttpHeaders,
    status: HttpStatusCode,
    request: WebRequest): ResponseEntity<Any> {

    val errors: MutableMap<String, String?> = HashMap()

    ex.bindingResult.allErrors.forEach { error: ObjectError ->
      val fieldName = (error as FieldError).field
      val message = error.getDefaultMessage()
      errors[fieldName] = message
    }

    val bodyOfResponse = mapOf<String, Any?>(
      "message" to "Cannot process Entity, please check the errors.",
      "detail" to errors
    )

    log.error("Cannot process Entity, please check the errors.")

    return ResponseEntity(bodyOfResponse, HttpStatus.UNPROCESSABLE_ENTITY)
  }
}