package com.grupo3.meetings.controller;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.grupo3.meetings.api.DTO.EventDTO;
import com.grupo3.meetings.api.EventController;
import com.grupo3.meetings.domain.Event;
import com.grupo3.meetings.service.EventService;
import org.junit.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;
import java.util.List;

import static net.bytebuddy.matcher.ElementMatchers.is;
import static org.hamcrest.Matchers.hasSize;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;


@RunWith(SpringRunner.class)
@WebMvcTest(EventController.class)
public class EventControllerTest {

    @Autowired
    private MockMvc mvc;

    @MockBean
    private EventService service;

    // write test cases here
    ObjectMapper objectMapper;

    @BeforeEach
    public void setUp() {
//        objectMapper = new ObjectMapper();
    }

    @Test
    public void givenEmployees_whenGetEmployees_thenReturnJsonArray()
            throws Exception {

        Event alex = new Event("Reunion de discord");

        List<Event> allEmployees = Arrays.asList(alex);

        given(service.getAllEvents()).willReturn(allEmployees);


        mvc.perform(get("/api/events/")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().string(getJSON(allEmployees)));
    }


//    @Test
////    @Transactional
////    @WithUserDetails(USER_CREDENTIALS)
//    public void  whenPost_User_aValidDTO_then_isCreated() throws Exception {
//        EventDTO evento = new EventDTO("Reunion de discord");
//
//        Mockito.when(service.createEvent(evento)).thenReturn(new Event(evento));
//
//        mvc
//                .perform(MockMvcRequestBuilders.post("/api/events").content(getJSON(evento))
//                        .contentType(MediaType.APPLICATION_JSON))
//                .andExpect(MockMvcResultMatchers.status().isCreated())
//                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
//                .andExpect(MockMvcResultMatchers.content().string(getJSON(evento)));
//    }

    private String getJSON(List<Event> contactDTO) throws JsonProcessingException {
        objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(contactDTO);
    }

    private String getJSON(Event contactDTO) throws JsonProcessingException {
        objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(contactDTO);
    }
    private String getJSON(EventDTO contactDTO) throws JsonProcessingException {
        objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(contactDTO);
    }

}
