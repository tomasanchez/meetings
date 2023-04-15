package com.grupo3.meetings.users.core.actions

import com.grupo3.meetings.users.core.domain.User
import com.grupo3.meetings.users.core.domain.UserRepository
import com.grupo3.meetings.users.core.domain.userRepository

class GetAllUsers (userRepository: UserRepository){
    suspend fun invoke () : List<User> {
        return userRepository.getAll()
    }
}

val getAllUsers = GetAllUsers(userRepository)