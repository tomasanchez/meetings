package com.grupo3.meetings.users.core.domain

import com.grupo3.meetings.exceptions.user.UserAlreadyExists
import com.grupo3.meetings.exceptions.user.UserNotFound
import org.assertj.core.api.BDDAssertions
import org.junit.Test
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.assertThrows
import org.junit.runner.RunWith
import org.mockito.BDDMockito.given
import org.mockito.Mockito.mock
import org.springframework.test.context.junit4.SpringRunner


@RunWith(SpringRunner::class)
class UserServiceTest {
    private val hashService: HashService = mock()
    private val userRepository: UserRepository = mock()
    private val userService = UserService(hashService, userRepository)

    private val mario = User(1, "mario@mail.com", "password")

    @Test
    fun `should create user from DTO`() {
        val dto = UserDTO("email@email.com", "password")
        val hashedPassword = "mysecretpassword"
        val expectedUser = User(1, dto.email, hashedPassword)

        given(hashService.hash(dto.password)).willReturn(hashedPassword)
        given(userRepository.createUser(dto.copy(password = hashedPassword))).willReturn(expectedUser)

        val createdUser = userService.create(dto)

        BDDAssertions.assertThat(createdUser).isEqualTo(expectedUser)
    }

    @Test
    fun `should fail if email is in use`() {
        val dto = UserDTO("email@email.com", "password")

        given(userRepository.getByEmail(dto.email))
                .willReturn(User(3, dto.email, "other_password"))

        val result = assertThrows<UserAlreadyExists> {
            userService.create(dto)
        }

        assertEquals(result.message, "User already exists")
    }

    @Test
    fun `get all users`() {
        given(userRepository.getAll()).willReturn(listOf(mario))

        val users = userService.getAll()

        BDDAssertions.assertThat(users).containsExactly(mario)
    }

    @Test
    fun `get user by id`() {
        given(userRepository.getById(mario.id)).willReturn(mario)

        val users = userService.getById(mario.id)

        BDDAssertions.assertThat(users).isEqualTo(mario)
    }

    @Test
    fun `should fail get by id if user does not exist`() {
        assertThrows<UserNotFound> {
            userService.getById(mario.id)
        }
    }

    @Test
    fun `should update existing user`() {
        val params = UpdateUserParams("pwd")
        val hashedPassword = "dwp"
        val expectedUser = mario.copy(password = hashedPassword)

        given(userRepository.getById(mario.id)).willReturn(mario)
        given(hashService.hash(params.password!!)).willReturn(hashedPassword)
        given(userRepository.updateUser(expectedUser)).willReturn(expectedUser)

        val updatedUser = userService.update(mario.id, params)

        BDDAssertions.assertThat(updatedUser).isEqualTo(expectedUser)
    }

    @Test
    fun `should fail update if user does not exist`() {
        assertThrows<UserNotFound> {
            userService.update(mario.id, UpdateUserParams(""))
        }
    }
}