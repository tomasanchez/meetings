package com.grupo3.meetings.repository

import com.grupo3.meetings.domain.dto.UserDTO
import com.grupo3.meetings.domain.models.User
import com.grupo3.meetings.domain.models.UserId
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.stereotype.Service

@Service
@Qualifier("userRepository")
class InMemoryUserRepository : UserRepository {

  private val users = mutableListOf<User>()
  private var id = 1

  override fun createUser(user: UserDTO): User {
    val newUser = User(id++.toString(), user.email, user.password)
    users.add(newUser)
    return newUser
  }

  override fun updateUser(user: User): User {
    val index = users.indexOfFirst { it.id == user.id }
    if (index != -1) {
      users[index] = user
    }
    return user
  }

  override fun getByEmail(email: String): User? {
    return users.find { it.email == email }
  }

  override fun getById(id: UserId): User? {
    return users.find { it.id == id }
  }

  override fun getAll(): List<User> {
    return users.toList()
  }
}