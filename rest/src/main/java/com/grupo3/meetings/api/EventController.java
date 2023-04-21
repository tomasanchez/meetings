package com.grupo3.meetings.api;

import com.grupo3.meetings.domain.dto.EventDTO;
import com.grupo3.meetings.domain.dto.NewGuestInEventDTO;
import com.grupo3.meetings.domain.dto.VoteOptionDTO;
import com.grupo3.meetings.domain.models.Event;
import com.grupo3.meetings.domain.models.Option;
import com.grupo3.meetings.domain.models.Statistics;
import com.grupo3.meetings.exceptions.event.EventNotFoundException;
import com.grupo3.meetings.exceptions.event.OptionNotFoundException;
import com.grupo3.meetings.exceptions.event.UnauthorizedUserException;
import com.grupo3.meetings.service.EventService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import java.util.List;
import java.util.NoSuchElementException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = {"api/v1/events/"})
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
      return ResponseEntity.status(HttpStatus.NOT_FOUND)
          .body("Event with id " + eventId + " does not exist");
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
      return ResponseEntity.status(HttpStatus.NOT_FOUND)
          .body("Event with id " + eventId + " does not exist");
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
      return ResponseEntity.status(HttpStatus.NOT_FOUND)
          .body("Event with id " + eventId + " does not exist");
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


  @Operation(summary = "Vote on an Event", description = "Allows a user to vote on a specified event")
  @PostMapping("/{eventId}/attendees")
  public ResponseEntity<?> voteOnEvent(@PathVariable Long eventId,
      @RequestBody NewGuestInEventDTO voteOptionDTO) {
    try {
      Event event = eventService.voteOnEvent(eventId, voteOptionDTO);
      return ResponseEntity.ok(event);
    } catch (EventNotFoundException e) {
      return ResponseEntity.status(HttpStatus.NOT_FOUND)
          .body("Event with id " + eventId + " does not exist");
    } catch (OptionNotFoundException e) {
      return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Invalid option selected");
    }
  }


}

