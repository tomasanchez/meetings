package com.grupo3.meetings.service;

import com.grupo3.meetings.domain.dto.AttendeeDTO;
import com.grupo3.meetings.domain.dto.EventDTO;
import com.grupo3.meetings.domain.dto.NewGuestInEventDTO;
import com.grupo3.meetings.domain.dto.VoteOptionDTO;
import com.grupo3.meetings.domain.models.Event;
import com.grupo3.meetings.domain.models.Option;
import com.grupo3.meetings.domain.models.Statistics;
import com.grupo3.meetings.exceptions.event.EventNotFoundException;
import com.grupo3.meetings.repository.EventRepository;
import com.grupo3.meetings.repository.UserRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class EventService {

  @Autowired
  EventRepository repoEventos;
  @Autowired
  UserRepository userRepository;

  public Event createEvent(EventDTO eventDTO) {
    return this.repoEventos.createEvent(eventDTO);
  }


  public Event addAttendee(Long eventId, AttendeeDTO attendeeDTO) {
    return this.repoEventos.addAttendee(eventId, attendeeDTO);
  }

  public Event getEvent(Long eventId) {
    return this.repoEventos.getEvent(eventId);
  }

  public Event closeEventVoting(Long eventId) {
    return this.repoEventos.closeEventVoting(eventId);
  }

  public Statistics getStatistics() {
    return this.repoEventos.getStatistics();
  }

  public List<Event> getAllEvents() {
    return this.repoEventos.getAllEvents();
  }

  public Event addAttendeeAndVote(String eventId, VoteOptionDTO attendeeAndVoteDTO) {
    Event event = repoEventos.findEventById(eventId)
        .orElseThrow(() -> new EventNotFoundException(eventId));
    // Save changes and return updated event
    repoEventos.save(event);
    return event;
  }

  public boolean existsById(String eventId) {
    return repoEventos.existsById(eventId);
  }

  public Event addOption(String eventId, Option option) {
    return this.repoEventos.addOption(eventId, option);
  }

  public Event findEventById(Long eventId) {
    return repoEventos.findEventById(String.valueOf(eventId))
        .orElseThrow(() -> new EventNotFoundException(String.valueOf(eventId)));
  }

  public Event save(Event evento) {
    this.repoEventos.save(evento);
    return evento;
  }

  public Event addOptionForUser(String eventId, Option option, String userId) {
    Event event = repoEventos.findEventById(eventId)
        .orElseThrow(() -> new EventNotFoundException(eventId));
    Option opcionAVotar = event.getListOfOptions().stream().filter(o -> o.equals(option))
        .findFirst().orElse(null);
    if (opcionAVotar == null) {
      this.addOption(eventId, option);
    } else {
      opcionAVotar.toggleVote(userId);
    }
    return event;
  }

  public Event updateEvent(Long eventId, EventDTO eventDTO) {
    Event event = repoEventos.findEventById(String.valueOf(eventId))
        .orElseThrow(() -> new EventNotFoundException(String.valueOf(eventId)));
    event.setTitle(eventDTO.getNombreDeEvento());
    event.setDescription(eventDTO.getDescripcion());
    event.setLocation(eventDTO.getUbicacion());
    return event;
  }

  public Event voteOnEvent(Long eventId, NewGuestInEventDTO voteOptionDTO) {
    Event event = repoEventos.findEventById(String.valueOf(eventId))
        .orElseThrow(() -> new EventNotFoundException(String.valueOf(eventId)));
    event.vote(voteOptionDTO.getGuest());
    return event;
  }
}
