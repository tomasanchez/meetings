package com.schedutn.scheduler.domain

import java.io.Serializable

/**
 * Message is an object that carries information from one part of a program to another.
 *
 * It is a means of communication between different components of a system, and it can be used to
 * trigger actions or update the state of the system.
 *
 * They can be passed synchronously or asynchronously and may be sent between different threads,
 * processes, or even across different systems.
 *
 * By using messages to communicate between components, the system becomes more modular and easier
 * to maintain, as each component only needs to understand the message format and not the
 * implementation details of other components.
 */
interface Message : Serializable