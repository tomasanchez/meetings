package com.grupo3.meetings.users.core.domain

import com.grupo3.meetings.api.UserDTO
import com.grupo3.meetings.users.infrastructure.InMemoryUserRepository

interface UserRepository {
    fun createUser(user: UserDTO): User
    fun updateUser(user: User): User?
    fun getByEmail(email: String): User?
    fun getById(id: UserId): User?
    fun getAll(): List<User>
    fun deleteUser(id: UserId): User?
}

var userRepository = InMemoryUserRepository()
