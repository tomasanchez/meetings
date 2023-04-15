package com.grupo3.meetings.users.infrastructure

import com.grupo3.meetings.users.core.domain.User
import com.grupo3.meetings.users.core.domain.UserId
import com.grupo3.meetings.users.core.domain.UserRepository

class InMemoryUserRepository : UserRepository {
    private val users = mutableListOf<User>()
    private var id = 0

    override suspend fun createUser(user: User): User {
        val newUser = user.copy(id = id++)
        users.add(newUser)
        return newUser
    }

    override suspend fun updateUser(user: User): User {
        val index = users.indexOfFirst { it.id == user.id }
        if (index != -1) {
            users[index] = user
        }
        return user
    }

    override suspend fun getByEmail(email: String): User? {
        return users.find { it.email == email }
    }

    override suspend fun getById(id: UserId): User? {
        return users.find { it.id == id }
    }

    override suspend fun getAll(): List<User> {
        return users.toList()
    }

    override suspend fun deleteUser(id: UserId): User? {
        val userToRemove = getById(id)
        users.remove(userToRemove)
        return userToRemove
    }
}