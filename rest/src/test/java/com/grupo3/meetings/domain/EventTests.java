package com.grupo3.meetings.domain;

import com.grupo3.meetings.exceptions.event.EventIsClosedException;
import com.grupo3.meetings.exceptions.event.UserNotAdministratorException;
import com.grupo3.meetings.exceptions.option.NoOptionVotedException;
import com.grupo3.meetings.exceptions.event.UserNotInGuestListException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Arrays;
import java.util.HashSet;

public class EventTests {
    private Event event;
    private Option option1;
    private Option option2;
    private Option option3;
    private User mario;
    private User luigi;
    private User peach;

    @BeforeEach
    public void setUp() {
        mario = new User("m1", "Mario");
        luigi = new User("l1", "Luigi");
        peach = new User("p1", "Peach");

        option1 = new Option(LocalDate.of(2023, 4, 5), LocalTime.of(10, 0));
        option2 = new Option(LocalDate.of(2023, 4, 5), LocalTime.of(11, 0));
        option3 = new Option(LocalDate.of(2023, 4, 5), LocalTime.of(12, 0));

        event = new Event("Pelicula Mario",
                "Juntada pelicula Mario",
                "Abasto",
                mario,
                new HashSet<Option>(Arrays.asList(option1, option2, option3))
        );

        event.addUserToGuestList(luigi);
        event.addUserToGuestList(peach);
    }

    @Test
    void cantAddSameUser() {
        event.addUserToGuestList(mario);
        Assertions.assertEquals(3, event.getListOfGuests().size());
    }

    @Test
    void userCanVote() {
        event.vote(option1, mario);
        Assertions.assertEquals(1, option1.getVotes());
    }

    @Test
    void userNotInvitedCantVote() {
        User toad = new User("t1", "Toad");
        Assertions.assertThrows(UserNotInGuestListException.class, () -> event.vote(option1, toad));
    }

    @Test
    void userCanAddOptions() {
        Option option4 = new Option(LocalDate.of(2023, 4, 5), LocalTime.of(13, 0));
        event.addOption(option4);
        Assertions.assertEquals(4, event.getListOfOptions().size());
    }

    @Test
    void administratorCanRemoveOptions() {
        event.removeOption(option1, mario);
        Assertions.assertEquals(2, event.getListOfOptions().size());
    }

    @Test
    void guestsCantRemoveOptions() {
        Assertions.assertThrows(UserNotAdministratorException.class, () -> event.removeOption(option1, luigi));
    }

    @Test
    void cantVoteOnAClosedEvent() {
        event.vote(option1, mario);
        event.closeEvent(mario);
        Assertions.assertThrows(EventIsClosedException.class, () -> event.vote(option1, mario));
    }

    @Test
    void cantAddUserOnAClosedEvent() {
        event.vote(option1, mario);
        event.closeEvent(mario);
        Assertions.assertThrows(EventIsClosedException.class, () -> event.addUserToGuestList(luigi));
    }

    @Test
    void administratorCanCloseEvent() {
        event.vote(option1, mario);
        event.closeEvent(mario);
        Assertions.assertTrue(event.getIsClosed());
        Assertions.assertEquals(option1, event.getVotedOption());
    }

    @Test
    void normalUserCantCloseEvent() {
        Assertions.assertThrows(UserNotAdministratorException.class, () -> event.closeEvent(luigi));
    }

    @Test
    void cantClosedAnEventWithoutAWinningOption() {
        Assertions.assertThrows(NoOptionVotedException.class, () -> event.closeEvent(mario));
    }

    @Test
    void administratorCanOpenAnEvent() {
        event.vote(option1, mario);
        event.closeEvent(mario);
        event.openEvent(mario);
        Assertions.assertFalse(event.getIsClosed());
    }

    @Test
    void normalUserCantOpenAnEvent() {
        event.vote(option1, mario);
        event.closeEvent(mario);
        Assertions.assertThrows(UserNotAdministratorException.class, () -> event.openEvent(luigi));
    }

    @Test
    void optionGetsVoted() {
        event.vote(option1, mario);
        event.vote(option2, mario);
        event.vote(option3, luigi);
        event.vote(option1, peach);
        event.closeEvent(mario);
        Assertions.assertEquals(option1, event.getVotedOption());
    }
}
