package com.grupo3.meetings.users.infrastructure
import org.mindrot.jbcrypt.BCrypt
import com.grupo3.meetings.users.core.domain.HashService

class BcryptHashService : HashService {
    override suspend fun hash(password: String): String {
        var salt = BCrypt.gensalt()
        return BCrypt.hashpw(password, salt)
    }

    override suspend fun areEqual(password: String, hashedPassword: String): Boolean {
        return BCrypt.checkpw(password, hashedPassword)
    }
}