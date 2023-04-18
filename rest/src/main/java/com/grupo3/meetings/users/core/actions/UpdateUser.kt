package com.grupo3.meetings.users.core.actions

import com.grupo3.meetings.users.core.domain.UpdateUserParams
import com.grupo3.meetings.users.core.domain.*

class UpdateUser (userService: UserService, userRepository: UserRepository){
    suspend fun invoke ( userId: UserId, userParams: UpdateUserParams) : User? {
        val user = userRepository.getById(userId)
        if (user == null){
            //error no hay user
        }
        return userService.update(userId, userParams)
    }
}

val updateUser = UpdateUser(userService, userRepository)