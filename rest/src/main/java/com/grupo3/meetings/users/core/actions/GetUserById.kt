package com.grupo3.meetings.users.core.actions

import com.grupo3.meetings.users.core.domain.User
import com.grupo3.meetings.users.core.domain.UserId
import com.grupo3.meetings.users.core.domain.UserRepository
import com.grupo3.meetings.users.core.domain.userRepository

class GetUserById (userRepository: UserRepository) {
    suspend fun invoke(id: UserId): User? {
        val user = userRepository.getById(id)
        if(user == null){
            //error de no encontrado
        }
        return user
    }
}

val getUserById = GetUserById (userRepository)