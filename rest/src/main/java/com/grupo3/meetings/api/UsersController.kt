package com.grupo3.meetings.api

import com.grupo3.meetings.domain.dto.UpdateUserParams
import com.grupo3.meetings.domain.dto.UserDTO
import com.grupo3.meetings.domain.models.User
import com.grupo3.meetings.domain.models.UserId
import com.grupo3.meetings.service.user.UserService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "Users", description = "The Users API")
class UsersController(
  @Autowired
  private val service: UserService
) {

  @Operation(
    summary = "Creates a User",
    description = "Creates a new user in the system",
  )
  @PostMapping
  fun createUser(@RequestBody userDTO: UserDTO): User {
    return service.create(userDTO)
  }

  @Operation(
    summary = "Find All Users",
    description = "Gets all users in the system",
  )
  @GetMapping
  fun getAllUsers(): List<User> {
    return service.getAll()
  }

  @Operation(
    summary = "Find User by Id",
    description = "Get user by Id",
  )
  @GetMapping("/{id}")
  fun getUserById(@PathVariable id: UserId): User {
    return service.getById(id)
  }

  @Operation(
    summary = "Updates a User",
    description = "Updates a user in the system",
  )
  @PatchMapping("/{id}")
  fun updateUser(@PathVariable id: UserId, @RequestBody userParams: UpdateUserParams): User? {
    return service.update(id, userParams)
  }
}