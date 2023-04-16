package com.grupo3.meetings.service;

import com.grupo3.meetings.api.DTO.AttendeeAndVoteDTO;
import com.grupo3.meetings.api.DTO.AttendeeDTO;
import com.grupo3.meetings.api.DTO.EventDTO;
import com.grupo3.meetings.domain.Event;
import com.grupo3.meetings.domain.Option;
import com.grupo3.meetings.domain.Statistics;
import com.grupo3.meetings.domain.User;
import com.grupo3.meetings.exceptions.event.EventNotFoundException;
import com.grupo3.meetings.exceptions.event.OptionNotFoundException;
import com.grupo3.meetings.exceptions.event.UserNotFoundException;
import com.grupo3.meetings.repository.EventRepository;
import com.grupo3.meetings.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

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

    public Event addAttendeeAndVote(String eventId, AttendeeAndVoteDTO attendeeAndVoteDTO)
             {
        Event event = repoEventos.findEventById(eventId).orElseThrow(() -> new EventNotFoundException(eventId));
        // Save changes and return updated event
        repoEventos.save(event);
        return event;
    }

    public boolean existsById(String eventId) {
        return repoEventos.existsById(eventId);
    }

    public void addOption(String eventId, Option option) {
        this.repoEventos.addOption(eventId, option);
    }

    public Event findEventById(Long eventId) {
        return repoEventos.findEventById(String.valueOf(eventId)).orElseThrow(() -> new EventNotFoundException(String.valueOf(eventId)));
//        String id= String.valueOf(eventId);
//        return repoEventos.findEventById(id).get();
    }
}
