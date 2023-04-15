package com.grupo3.meetings.users.core.domain

import com.grupo3.meetings.users.infrastructure.InMemoryUserRepository

interface UserRepository {
    suspend fun createUser(user: User): User
    suspend fun updateUser(user: User): User
    suspend fun getByEmail(email: String): User?
    suspend fun getById(id: UserId): User?
    suspend fun getAll(): List<User>
    suspend fun deleteUser(id: UserId): User?
}

var userRepository = InMemoryUserRepository()
