package com.grupo3.meetings.users.core.actions

import com.grupo3.meetings.users.core.domain.*

class UpdateUser (userService: UserService, userRepository: UserRepository){
    suspend fun invoke ( userId: UserId, updatedUser: User) : User? {
        val user = userRepository.getById(userId)
        if (user == null){
            //error no hay user
        }
        return userService.update(updatedUser)
    }
}

val updateUser = UpdateUser(userService, userRepository)