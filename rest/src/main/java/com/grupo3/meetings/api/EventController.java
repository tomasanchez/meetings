package com.grupo3.meetings.api;

import com.grupo3.meetings.api.DTO.EventDTO;
import com.grupo3.meetings.api.DTO.NewGuestInEventDTO;
import com.grupo3.meetings.api.DTO.VoteOptionDTO;
import com.grupo3.meetings.domain.Event;
import com.grupo3.meetings.domain.Option;
import com.grupo3.meetings.domain.Statistics;
import com.grupo3.meetings.exceptions.event.*;
import com.grupo3.meetings.service.EventService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.NoSuchElementException;

@RestController
//@RequestMapping("/api/events")
@RequestMapping(value = {"/api/events", "api/events/"})
@Tag(name = "Events", description = "API URLs Events")
public class EventController {


    @Autowired
    private EventService eventService;

    @Operation(summary = "Create Event", description = "Creates a new event with the specified options")
    @PostMapping("")
    public ResponseEntity<Event> createEvent(@RequestBody EventDTO eventDTO) {
        Event event = eventService.createEvent(eventDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(event);
    }

    @Operation(summary = "Get Event", description = "Returns the specified event with its associated availability options and votes")
    @GetMapping("/{eventId}")
    public ResponseEntity<?> getEvent(@PathVariable Long eventId) {
        Event event = eventService.getEvent(eventId);
        if (event == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Event with id " + eventId + " does not exist");
        }
        return ResponseEntity.ok(event);
    }

    @Operation(summary = "Update Event", description = "Updates the specified event with new information")
    @PatchMapping("/{eventId}")
    public ResponseEntity<?> updateEvent(@PathVariable Long eventId, @RequestBody EventDTO eventDTO) {
        try {
            Event event = eventService.updateEvent(eventId, eventDTO);
            return ResponseEntity.ok(event);
        } catch (EventNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Event with id " + eventId + " does not exist");
        } catch (UnauthorizedUserException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
    }

    @Operation(summary = "Get All Events", description = "Returns a list of all events created")
    @GetMapping("")
    public ResponseEntity<List<Event>> getAllEvents() {
        List<Event> events = eventService.getAllEvents();
        return ResponseEntity.ok(events);
    }

    @Operation(summary = "Add Option to Event", description = "Adds a new option to the specified event")
    @PostMapping("/{eventId}/options")
    public ResponseEntity<?> addOption(
            @PathVariable String eventId,
            @RequestBody VoteOptionDTO optionRequest
    ) {
        try {
            Option option = new Option(optionRequest);
            Event evento = eventService.addOptionForUser(eventId, option, optionRequest.getUserId());

            return ResponseEntity.ok(evento);
        } catch (NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Event with id " + eventId + " does not exist");
        } catch (EventNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(e.getMessage());
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
        }
    }


    @Operation(summary = "Close Event Voting", description = "Closes the voting period for the specified event (if the event was created by the authenticated user)")
    @PutMapping("/{eventId}")
    public ResponseEntity<Event> closeEventVoting(@PathVariable Long eventId) {
        try {
            Event event = eventService.closeEventVoting(eventId);
            return ResponseEntity.ok(event);
        } catch (EventNotFoundException e) {
            return ResponseEntity.notFound().build();
        } catch (UnauthorizedUserException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
    }

    @Operation(summary = "Get Statistics", description = "Returns statistics on the number of events and votes cast in the last 2 hours")
    @GetMapping("/statistics")
    public ResponseEntity<Statistics> getStatistics() {
        Statistics statistics = eventService.getStatistics();
        return ResponseEntity.ok(statistics);
    }

//    @Operation(summary = "Add Attendee and Vote", description = "Adds an attendee to the specified event with the specified availability options and votes for them")
//    @PostMapping("/{eventId}/attendees")
//    public ResponseEntity<?> addAttendeeAndVote(@PathVariable String eventId, @RequestBody VoteOptionDTO attendeeAndVoteDTO) {
//        if (validateEventExists(eventId)) {
//            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Event " + eventId + " not found");
//        }
//
//        Event event = eventService.addAttendeeAndVote(eventId, attendeeAndVoteDTO);
//        return ResponseEntity.status(HttpStatus.CREATED).body(event);
//    }
//
//
//    private boolean validateEventExists(String eventId) {
//        return eventService.existsById(eventId);
//    }

    @Operation(summary = "Vote on an Event", description = "Allows a user to vote on a specified event")
    @PostMapping("/{eventId}/attendees")
    public ResponseEntity<?> voteOnEvent(@PathVariable Long eventId, @RequestBody NewGuestInEventDTO voteOptionDTO) {
        try {
            Event event = eventService.voteOnEvent(eventId, voteOptionDTO);
            return ResponseEntity.ok(event);
        } catch (EventNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Event with id " + eventId + " does not exist");
        }
//        catch (UserNotFoundException e) {
//            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User with id " + userId + " does not exist");
//        }
        catch (OptionNotFoundException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Invalid option selected");
        }
//        catch (DuplicateVoteException e) {
//            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("User has already voted on this event");
//        } catch (VotingClosedException e) {
//            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Voting period for this event has ended");
//        }
    }


}

