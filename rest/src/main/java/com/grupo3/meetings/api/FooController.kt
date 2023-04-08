package com.grupo3.meetings.api

import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.media.ArraySchema
import io.swagger.v3.oas.annotations.media.Content
import io.swagger.v3.oas.annotations.media.Schema
import io.swagger.v3.oas.annotations.responses.ApiResponse
import io.swagger.v3.oas.annotations.responses.ApiResponses
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

data class Foo(val id: Long, val name: String)


@RestController
@RequestMapping("/api/v1/foo")
class FooController {


    @Operation(summary = "Get all foo")
    @ApiResponses(value = [
        ApiResponse(responseCode = "200",
                description = "Found Foos",
                content = [(Content(mediaType = "application/json",
                        array = (ArraySchema(schema = Schema(implementation = Foo::class)))))])])
    @GetMapping
    fun getAllFoo(): ResponseEntity<List<Foo>> {
        return ResponseEntity
                .ok()
                .body(listOf(Foo(1, "foo"), Foo(2, "bar"), Foo(3, "baz")))
    }

    @Operation(summary = "Get a foo by id")
    @ApiResponses(value = [
        ApiResponse(responseCode = "200", description = "Found Foo", content = [
            (Content(
                    mediaType = "application/json",
                    schema = (Schema(implementation = Foo::class))
            ))]),
        ApiResponse(responseCode = "404", description = "Did not find any Foo", content = [Content()])]
    )
    @GetMapping("/{id}", "")
    fun getFoo(@PathVariable id: Long): Foo {
        return Foo(id, "foo")
    }
}