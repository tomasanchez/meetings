package com.schedutn.scheduler.service

/**
 * Meeting not found exception.
 *
 * @param id Meeting id not found
 */
class ScheduleNotFoundException(id: String) : RuntimeException("No Schedule with id=$id.")

class ScheduleAuthorizationException(error: Throwable) : RuntimeException(error)