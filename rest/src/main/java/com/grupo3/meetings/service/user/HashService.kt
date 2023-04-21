package com.grupo3.meetings.service.user

interface HashService {

  fun hash(password: String): String
  fun areEqual(password: String, hashedPassword: String): Boolean
}

val hashService = BcryptHashService()