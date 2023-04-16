package com.grupo3.meetings.repository;

import com.grupo3.meetings.api.DTO.AttendeeDTO;
import com.grupo3.meetings.api.DTO.EventDTO;
import com.grupo3.meetings.domain.Event;
import com.grupo3.meetings.domain.Statistics;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
public class EventRepository {

    List<Event> db ;
    EventRepository(){
        this.db = new ArrayList<Event>();
    }
    public Event createEvent(EventDTO eventDTO) {
        Event nuevo= new  Event(eventDTO);
        this.db.add(nuevo);
        int id= this.db.indexOf(nuevo);
        nuevo.setId(String.valueOf(id));
        return nuevo;
    }

    public Event addAttendee(Long eventId, AttendeeDTO attendeeDTO) {
        return (Event) null;
    }

    public Event getEvent(Long eventId) {
        Optional<Event> evento= this.db.stream().filter(e -> e.getId().equals(eventId)).findFirst();
        if(evento.isPresent()){
            return evento.get();
        }
        return (Event) null;
    }

    public Event closeEventVoting(Long eventId) {
        return (Event) null;
    }

    public Statistics getStatistics() {
        return (Statistics) null;
    }

    public List<Event> getAllEvents() {
        return this.db;
    }


    public Optional<Event> findEventById(String eventId) {
        return this.db.stream().filter(e -> e.getId().equals(eventId)).findFirst();
    }

    public void save(Event event) {
    }

    public boolean existsById(String eventId) {
//        return this.db.stream().filter(e -> e.getId().equals(eventId)).findFirst().isEmpty();
        return this.db.stream().anyMatch(e -> e.getId().equals(eventId));
    }
}
