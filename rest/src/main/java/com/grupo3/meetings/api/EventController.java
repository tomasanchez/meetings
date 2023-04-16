package com.grupo3.meetings.api;

import com.grupo3.meetings.api.DTO.AttendeeAndVoteDTO;
import com.grupo3.meetings.api.DTO.EventDTO;
import com.grupo3.meetings.domain.Event;
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


    @Operation(summary = "Add Attendee and Vote", description = "Adds an attendee to the specified event with the specified availability options and votes for them")
    @PostMapping("/{eventId}/attendees")
    public ResponseEntity<?> addAttendeeAndVote(@PathVariable String eventId, @RequestBody AttendeeAndVoteDTO attendeeAndVoteDTO) {
        if(validateEventExists(eventId)){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Event "+eventId+" not found");
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

//    private void validateUserExists(String userId) {
//        if (!userService.existsById(userId)) {
//            throw new NotFoundException("User not found");
//        }
//    }

//    private void validateOptionExists(String eventId, String optionId) {
//        if (!eventService.optionExists(eventId, optionId)) {
//            throw new NotFoundException("Option not found");
//        }
//    }


    @Operation(summary = "Get Event", description = "Returns the specified event with its associated availability options and votes")
    @GetMapping("/{eventId}")
    public ResponseEntity<Event> getEvent(@PathVariable Long eventId) {
        try {
            Event event = eventService.getEvent(eventId);
            return ResponseEntity.ok(event);
        } catch (EventNotFoundException e) {
            return ResponseEntity.notFound().build();
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

    @Operation(summary = "Get All Events", description = "Returns a list of all events created")
    @GetMapping("")
    public ResponseEntity<List<Event>> getAllEvents() {
        List<Event> events = eventService.getAllEvents();
        return ResponseEntity.ok(events);
    }
}

