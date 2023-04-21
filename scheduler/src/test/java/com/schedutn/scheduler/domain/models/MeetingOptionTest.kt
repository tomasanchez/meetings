package com.schedutn.scheduler.domain.models

import org.junit.jupiter.api.Test
import java.time.LocalDate
import kotlin.test.assertEquals
import kotlin.test.assertNotEquals
import kotlin.test.assertTrue

internal class MeetingOptionTest {


    @Test
    fun `options with same date, hour and minute are equals `() {

        val option1 = MeetingOption(date = LocalDate.now(), hour = 0, minute = 0, votes = setOf("user1"))
        val option2 = MeetingOption(date = LocalDate.now(), hour = 0, minute = 0, votes = setOf("user2"))

        assertEquals(option1, option2)
    }

    @Test
    fun `options with different date, hour and minute are not equals `() {

        val option1 = MeetingOption(
                date = LocalDate.now(),
                hour = 0,
                minute = 0,
                votes = setOf("user1"))

        val option2 = MeetingOption(
                date = LocalDate.now().plusDays(1),
                hour = 0,
                minute = 0,
                votes = setOf("user1")
        )

        assertNotEquals(option1, option2)
    }

    @Test
    fun `an option can be voted`() {
        // Given
        val username = "user1"
        val option = MeetingOption(date = LocalDate.now(), hour = 0, minute = 0)

        // When
        val votedOption = option.vote(username)

        // Then
        assertEquals(setOf(username), votedOption.votes)
    }

    @Test
    fun `an option can have voting revoked`() {
        // Given
        val username = "user1"
        val option = MeetingOption(date = LocalDate.now(), hour = 0, minute = 0, votes = setOf(username))

        // When
        val votedOption = option.vote(username)

        // Then
        assertTrue { votedOption.votes.isEmpty() }
    }

}