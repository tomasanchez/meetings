package com.grupo3.meetings.controller;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.grupo3.meetings.api.EventController;
import com.grupo3.meetings.domain.Event;
import com.grupo3.meetings.service.EventService;
import org.junit.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
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
    void setUp() {
//    contactDTO = new ContactDTO();
//    contactDTO.setName("name test contact");
//    contactDTO.setEmail("email test contact");
//    contactDTO.setPhone(Long.valueOf(1133448899));
//    contactDTO.setMessage("message test contact");
//
//    baseUrl = ServletUriComponentsBuilder.fromCurrentContextPath().toUriString();
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


    // --------------------------------------------------------------------------------------------
    // Internal Methods
    // --------------------------------------------------------------------------------------------

    private String getJSON(List<Event> contactDTO) throws JsonProcessingException {
          objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(contactDTO);
    }

}
