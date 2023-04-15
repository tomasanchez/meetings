package com.grupo3.meetings.users.core.actions

import com.grupo3.meetings.users.core.domain.User
import com.grupo3.meetings.users.core.domain.UserService
import com.grupo3.meetings.users.core.domain.userService

class CreateUser (userService: UserService) {
    suspend fun invoke (email: String, password: String) : User? {
        val newUser = User(0, email, password)
        return userService.create(newUser)
    }
}

val createUser = CreateUser(userService)