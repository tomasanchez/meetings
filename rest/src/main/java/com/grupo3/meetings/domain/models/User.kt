package com.grupo3.meetings.domain.models


typealias UserId = String

data class User(val id: UserId, val email: String, val password: String)