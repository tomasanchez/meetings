package com.grupo3.meetings.users.core.domain

import com.grupo3.meetings.api.UpdateUserParams
import com.grupo3.meetings.api.UserDTO
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.stereotype.Service

@Service
class UserService (
        @Autowired @Qualifier("hashService") private val hashService: HashService,
        @Autowired @Qualifier("userRepository") private val userRepository: UserRepository
) {
    fun create (user: UserDTO): User {
        val existingUser: User? = userRepository.getByEmail(user.email)
        if(existingUser != null){
            throw Exception("Ya existe un usuario con este mail")
        }
        val hashedPassword = hashService.hash(user.password)
        var hashedUser = user.copy(password = hashedPassword)
        return userRepository.createUser(hashedUser)
    }

    fun update(userId: UserId, userParams: UpdateUserParams): User? {
        val existingUser: User = userRepository.getById(userId) ?: throw Exception("Usuario no encontrado")
        val hashedPassword : String
        if(userParams.password != null){
            hashedPassword = hashService.hash(userParams.password)
        }else{
            hashedPassword = existingUser.password
        }

        val updatedUser = User(userId, existingUser.email, hashedPassword)
        return userRepository.updateUser(updatedUser)
    }

    fun delete(userId: UserId): User? {
        val existingUser: User = userRepository.getById(userId) ?: throw Exception("Usuario no encontrado")
        return userRepository.deleteUser(userId)
    }

    fun getAll(): List<User> {
        return userRepository.getAll()
    }

    fun getById(userId: UserId): User? {
        val user = userRepository.getById(userId) ?: throw Exception("Usuario no encontrado")
        return user
    }

}

var userService = UserService(hashService, userRepository)