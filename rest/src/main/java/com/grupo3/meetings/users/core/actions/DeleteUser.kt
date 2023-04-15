package com.grupo3.meetings.users.core.actions

import com.grupo3.meetings.users.core.domain.User
import com.grupo3.meetings.users.core.domain.UserId
import com.grupo3.meetings.users.core.domain.UserService
import com.grupo3.meetings.users.core.domain.userService

class DeleteUser (userService: UserService){
    suspend fun invoke(id: UserId): User? {
        return userService.delete(id)
    }
}

val deleteUser = DeleteUser(userService)