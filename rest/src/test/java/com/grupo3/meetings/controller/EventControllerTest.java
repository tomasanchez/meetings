package com.grupo3.meetings.controller;


import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.grupo3.meetings.api.EventController;
import com.grupo3.meetings.domain.models.Event;
import com.grupo3.meetings.service.EventService;
import java.util.List;
import org.junit.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;


@RunWith(SpringRunner.class)
@WebMvcTest(EventController.class)
public class EventControllerTest {

  // write test cases here
  ObjectMapper objectMapper;
  @Autowired
  private MockMvc mvc;
  @MockBean
  private EventService service;

  @BeforeEach
  public void setUp() {
//        objectMapper = new ObjectMapper();
  }

  @Test
  public void givenEmployees_whenGetEmployees_thenReturnJsonArray()
      throws Exception {

    Event alex = new Event("Reunion de discord");

    List<Event> allEmployees = List.of(alex);

    given(service.getAllEvents()).willReturn(allEmployees);

    mvc.perform(get("/api/v1/events/")
            .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk())
        .andExpect(MockMvcResultMatchers.content().string(getJSON(allEmployees)));
  }

  private String getJSON(List<Event> contactDTO) throws JsonProcessingException {
    objectMapper = new ObjectMapper();
    return objectMapper.writeValueAsString(contactDTO);
  }

}
