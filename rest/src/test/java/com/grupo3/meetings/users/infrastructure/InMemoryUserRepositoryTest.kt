package com.grupo3.meetings.users.infrastructure

import com.grupo3.meetings.users.core.domain.User
import com.grupo3.meetings.users.core.domain.UserDTO
import org.assertj.core.api.BDDAssertions
import org.junit.Test
import org.junit.jupiter.api.Assertions.*

class InMemoryUserRepositoryTest {
    private val userRepository = InMemoryUserRepository()

    private val dto = UserDTO( "mario@mail.com", "password")

    @Test
    fun `should create new user`() {
        val user = userRepository.createUser(dto)

        val expectedUser = User(user.id, dto.email, dto.password)

        BDDAssertions.assertThat(expectedUser).isEqualTo(expectedUser)
    }

    @Test
    fun `should get user by id after created`() {
        val user = userRepository.createUser(dto)
        val expectedUser = User(user.id, dto.email, dto.password)

        val retrievedUser = userRepository.getById(user.id)

        BDDAssertions.assertThat(retrievedUser).isEqualTo(expectedUser)
    }

    @Test
    fun `should get user by email after created`() {
        val user = userRepository.createUser(dto)
        val expectedUser = User(user.id, dto.email, dto.password)

        val retrievedUser = userRepository.getByEmail(user.email)

        BDDAssertions.assertThat(retrievedUser).isEqualTo(expectedUser)
    }

    @Test
    fun `should get all users`() {
        val user = userRepository.createUser(dto)
        val expectedUser = User(user.id, dto.email, dto.password)

        val user2 = userRepository.createUser(dto)
        val expectedUser2 = User(user2.id, dto.email, dto.password)

        val retrievedUsers = userRepository.getAll()

        BDDAssertions.assertThat(retrievedUsers).containsExactly(expectedUser, expectedUser2)
    }
}