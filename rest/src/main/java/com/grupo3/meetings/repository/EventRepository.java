package com.grupo3.meetings.repository;

import com.grupo3.meetings.api.DTO.AttendeeDTO;
import com.grupo3.meetings.api.DTO.EventDTO;
import com.grupo3.meetings.domain.Event;
import com.grupo3.meetings.domain.Option;
import com.grupo3.meetings.domain.Statistics;
import com.grupo3.meetings.exceptions.event.EventNotFoundException;
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
        // se guarda en arrayList de eventos
        this.db.add(nuevo);
        //asigno id
        int id= this.db.indexOf(nuevo);
        nuevo.setId(String.valueOf(id));
        return nuevo;
    }

    public Event addAttendee(Long eventId, AttendeeDTO attendeeDTO) {
        return (Event) null;
    }

    public Event getEvent(Long eventId) {
        String id= String.valueOf(eventId);
        return this.db.stream().filter(e -> e.getId().equals(id)).findFirst().orElse(null);
    }

    public Event closeEventVoting(Long eventId) {
        Event event= this.db.stream().filter(e -> e.getId().equals(eventId)).findFirst().orElseThrow(() -> new EventNotFoundException(eventId));
        event.closeEvent2();
        return event;
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

    public Event addOption(String eventId, Option option) {
//        Event event = this.db.stream().filter(e -> e.getId().equals(eventId)).findFirst().get();
        Event event= this.db.stream().filter(e -> e.getId().equals(eventId)).findFirst().orElse(null);
        event.addOption(option);
        return event;
    }
}
