package com.schedutn.scheduler.domain.events

import com.schedutn.scheduler.domain.Message

/**
 * An event is an occurrence in the system, usually triggered as a result of executing a command.
 *
 * Events are immutable, serializable and should contain all the relevant data related to the
 * occurrence.
 *
 * Events are produced by command handlers, or even other Event handlers as a result of an
 * execution, and they represent the source of truth about the system state. Once an event
 * has been created, it cannot be changed or deleted.
 *
 */
interface Event : Message