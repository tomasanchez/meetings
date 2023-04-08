package com.grupo3.meetings.api

import org.apache.commons.lang3.concurrent.ConcurrentException
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
import org.springframework.web.client.HttpClientErrorException
import org.springframework.web.context.request.WebRequest
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler
import java.util.function.Consumer


@RestControllerAdvice
class GlobalControllerExceptionHandler: ResponseEntityExceptionHandler() {


    /**
     * Handles Concurrency Exceptions.
     *
     * @param ex The runtime exception
     * @return a response entity with the exception message and a bad request status
     */
    @ExceptionHandler(ConcurrentException::class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    fun handleConversion(ex: RuntimeException): ResponseEntity<String> {
        return ResponseEntity(ex.message, HttpStatus.BAD_REQUEST)
    }

    /**
     * Handles Unauthorized Exceptions.
     *
     * @param ex The runtime exception
     * @return a response entity with the exception message and an unauthorized status
     */
    @ExceptionHandler(HttpClientErrorException.Unauthorized::class)
    @ResponseStatus(HttpStatus.UNAUTHORIZED)
    fun handleUnAuthorizedException(ex: RuntimeException): ResponseEntity<String> {
        return ResponseEntity(ex.message, HttpStatus.UNAUTHORIZED)
    }

    /**
     * Handles Forbidden Exceptions.
     *
     * @param ex The runtime exception
     * @return a response entity with the exception message and a forbidden status
     */
    @ExceptionHandler(HttpClientErrorException.Forbidden::class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    fun handleForbiddenException(ex: RuntimeException): ResponseEntity<String> {
        return ResponseEntity(ex.message, HttpStatus.FORBIDDEN)
    }

    /**
     * Handles Not Found Exceptions.
     *
     * @param ex The runtime exception
     * @return a response entity with the exception message and a not found status
     */
    @ExceptionHandler(HttpClientErrorException.NotFound::class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    fun handleNotFoundException(ex: RuntimeException): ResponseEntity<String> {
        return ResponseEntity(ex.message, HttpStatus.NOT_FOUND)
    }

    /**
     * Handles Bad Request Exceptions.
     *
     * @param ex The runtime exception
     * @return a response entity with the exception message and a bad request status
     */
    @ExceptionHandler(HttpClientErrorException.BadRequest::class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    fun handleBadRequestException(ex: RuntimeException): ResponseEntity<String> {
        return ResponseEntity(ex.message, HttpStatus.BAD_REQUEST)
    }

    /**
     * Handles Conflict Exceptions.
     *
     * @param ex The runtime exception
     * @return a response entity with the exception message and a conflict status
     */
    @ExceptionHandler(HttpClientErrorException.Conflict::class)
    @ResponseStatus(HttpStatus.CONFLICT)
    fun handleConflictException(ex: RuntimeException): ResponseEntity<String> {
        return ResponseEntity(ex.message, HttpStatus.CONFLICT)
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

        ex.bindingResult.allErrors.forEach(Consumer { error: ObjectError ->
            val fieldName = (error as FieldError).field
            val message = error.getDefaultMessage()
            errors[fieldName] = message
        })

        return ResponseEntity(errors, HttpStatus.UNPROCESSABLE_ENTITY)
    }
}