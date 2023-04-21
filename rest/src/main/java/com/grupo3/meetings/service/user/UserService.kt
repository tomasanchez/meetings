package com.grupo3.meetings.service.user

import com.grupo3.meetings.domain.dto.UpdateUserParams
import com.grupo3.meetings.domain.dto.UserDTO
import com.grupo3.meetings.domain.models.User
import com.grupo3.meetings.domain.models.UserId
import com.grupo3.meetings.exceptions.user.UserAlreadyExists
import com.grupo3.meetings.exceptions.user.UserNotFound
import com.grupo3.meetings.repository.UserRepository
import com.grupo3.meetings.repository.userRepository
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.stereotype.Service

@Service
class UserService(
  @Autowired @Qualifier("hashService") private val hashService: HashService,
  @Autowired @Qualifier("userRepository") private val userRepository: UserRepository
) {

  fun create(user: UserDTO): User {
    val existingUser: User? = userRepository.getByEmail(user.email)
    if (existingUser != null) {
      throw UserAlreadyExists()
    }
    val hashedPassword = hashService.hash(user.password)
    var hashedUser = user.copy(password = hashedPassword)
    return userRepository.createUser(hashedUser)
  }

  fun update(userId: UserId, userParams: UpdateUserParams): User? {
    val existingUser: User = userRepository.getById(userId) ?: throw UserNotFound()
    val hashedPassword: String
    if (userParams.password != null) {
      hashedPassword = hashService.hash(userParams.password)
    } else {
      hashedPassword = existingUser.password
    }

    val updatedUser = User(userId, existingUser.email, hashedPassword)
    return userRepository.updateUser(updatedUser)
  }

  fun getAll(): List<User> {
    return userRepository.getAll()
  }

  fun getById(userId: UserId): User {
    return userRepository.getById(userId) ?: throw UserNotFound()
  }

}

var userService = UserService(hashService, userRepository)