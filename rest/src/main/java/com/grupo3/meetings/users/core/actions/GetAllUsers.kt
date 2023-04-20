package com.grupo3.meetings.users.core.actions

import com.grupo3.meetings.users.core.domain.User
import com.grupo3.meetings.users.core.domain.UserRepository
import com.grupo3.meetings.users.core.domain.userRepository
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.stereotype.Repository


class GetAllUsers (private val userRepository: UserRepository){
    suspend operator fun invoke () : List<User> {
        return userRepository.getAll()
    }
}

val getAllUsers = GetAllUsers(userRepository)