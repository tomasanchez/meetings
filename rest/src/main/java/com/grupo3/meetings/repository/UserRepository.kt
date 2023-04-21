package com.grupo3.meetings.repository

import com.grupo3.meetings.domain.dto.UserDTO
import com.grupo3.meetings.domain.models.User
import com.grupo3.meetings.domain.models.UserId

interface UserRepository {

  fun createUser(user: UserDTO): User
  fun updateUser(user: User): User?
  fun getByEmail(email: String): User?
  fun getById(id: UserId): User?
  fun getAll(): List<User>
}

var userRepository = InMemoryUserRepository()
