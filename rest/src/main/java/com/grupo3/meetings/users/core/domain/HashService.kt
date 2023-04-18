package com.grupo3.meetings.users.core.domain

import com.grupo3.meetings.users.infrastructure.BcryptHashService

interface HashService {
    fun hash(password: String): String
    fun areEqual(password: String, hashedPassword: String): Boolean
}

val hashService =  BcryptHashService()