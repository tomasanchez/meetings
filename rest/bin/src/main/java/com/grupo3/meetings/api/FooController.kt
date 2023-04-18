package com.grupo3.meetings.api

import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

data class Foo(val id: Long, val name: String)


@RestController
@RequestMapping("/api/v1/foo")
@Tag(name = "Foo", description = "The Foo API")
class FooController {

    companion object {
        private val log = org.slf4j.LoggerFactory.getLogger(FooController::class.java)
    }

    @Operation(summary = "Find All Foo",
                description = "Gets all foo resources in the system",)
    @GetMapping
    fun getAllFoo(): List<Foo>{
        log.debug("Requested Foo list")
        return listOf(Foo(1, "foo"), Foo(2, "foo"))
    }

    @Operation(summary = "Foo by ID",
        description = "Gets a single Foo resource by its unique ID")
    @GetMapping("/{id}")
    fun getFoo(@PathVariable id: Long): Foo {
        log.debug("Requested Foo with id: $id")
        return Foo(id, "foo")
    }
}