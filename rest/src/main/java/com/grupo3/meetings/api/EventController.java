package com.grupo3.meetings.api;

import com.grupo3.meetings.api.DTO.AttendeeAndVoteDTO;
import com.grupo3.meetings.api.DTO.EventDTO;
import com.grupo3.meetings.api.DTO.OptionDTO;
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

import java.util.HashMap;
import java.util.List;
import java.util.Map;
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
            @RequestBody OptionDTO optionRequest
    ) {
        try {
            Option option = new Option(optionRequest);
            Event evento = eventService.getEvent(Long.parseLong(eventId));
            eventService.addOption(eventId, option);
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

    @Operation(summary = "Add Attendee and Vote", description = "Adds an attendee to the specified event with the specified availability options and votes for them")
    @PostMapping("/{eventId}/attendees")
    public ResponseEntity<?> addAttendeeAndVote(@PathVariable String eventId, @RequestBody AttendeeAndVoteDTO attendeeAndVoteDTO) {
        if (validateEventExists(eventId)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Event " + eventId + " not found");
        }
//        catch (EventNotFoundException e) {
//            Map<String, String> error = new HashMap<>();
//            error.put("message", "Event not found");
//            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
//        } catch (UserNotFoundException e) {
//            Map<String, String> error = new HashMap<>();
//            error.put("message", "User not found");
//            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
//        } catch (OptionNotFoundException e) {
//            Map<String, String> error = new HashMap<>();
//            error.put("message", "Option not found");
//            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
//        }
        Event event = eventService.addAttendeeAndVote(eventId, attendeeAndVoteDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(event);
    }


    private boolean validateEventExists(String eventId) {
//        if (!eventService.existsById(eventId)) {
//            throw new EventNotFoundException(eventId);
//        }
        return eventService.existsById(eventId);
    }


}

