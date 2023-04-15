package com.grupo3.meetings.users.core.domain

class UserService (hashService: HashService, userRepository: UserRepository) {
    suspend fun create (user: User): User {
        val existingUser: User? = userRepository.getByEmail(user.email)
        if(existingUser == null){
//            mandar error
        }
        val hashedPassword = hashService.hash(user.password)
        var hashedUser = user.copy(password = hashedPassword)
        return userRepository.createUser(user)
    }

    suspend fun update(user: User): User {
        val existingUser: User? = userRepository.getByEmail(user.email)
        if(existingUser == null){
//            mandar error
        }
        return userRepository.updateUser(user)
    }

    suspend fun delete(userId: UserId): User? {
        val existingUser: User? = userRepository.getById(userId)
        if(existingUser == null){
//            mandar error
        }
        return userRepository.deleteUser(userId)
    }
}

var userService = UserService(hashService, userRepository)