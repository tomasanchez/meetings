package com.grupo3.meetings.domain;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.grupo3.meetings.api.UsersController;
import com.grupo3.meetings.users.core.domain.*;
import com.grupo3.meetings.users.core.domain.User;
import org.junit.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;

import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.util.Arrays;
import java.util.List;

import static org.mockito.BDDMockito.given;

@RunWith(SpringRunner.class)
@WebMvcTest(UsersController.class)
public class UserControllerTests {
    private static final String route = "/api/v1/users";
    private String baseUrl;
    private UserDTO userDTO;
    ObjectMapper objectMapper;
    @Autowired
    private UsersController usersController;


    @MockBean
    private UserService service;

    @MockBean
    private UserRepository repository;

    @Autowired
    private MockMvc mockMvc;
    User mario = new User(1, "mario@mail.com", "password");
    @BeforeEach
    void setUp(){
        baseUrl = ServletUriComponentsBuilder.fromCurrentContextPath().toUriString();
    }
    @Test
    public void whenGet_AllUsers_thenOk() throws Exception {
        List<User> allUsers = Arrays.asList(mario);
        given(service.getAll()).willReturn(allUsers);
        mockMvc.perform(MockMvcRequestBuilders.get(route))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.content().string(getJSON(allUsers)));
    }

    @Test
    public void canRetrieveByIdWhenExists() throws Exception{
        given(service.getById(1)).willReturn(mario);
        mockMvc.perform(MockMvcRequestBuilders.get(route+"/1"))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.content().string(getJSON(mario)));
    }

    @Test
    public void createusertest() throws Exception{
        UserDTO dto = new UserDTO(mario.getEmail(), mario.getPassword());
        given(service.create(dto)).willReturn(mario);

        mockMvc.perform(MockMvcRequestBuilders
                        .post(route)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(getJSON(dto))
                )
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.content().string(getJSON(mario)));
    }

    @Test
    public void updateusertest() throws Exception{
        User newUser = new User(mario.getId(), mario.getEmail(), "new_password");
        UpdateUserParams params = new UpdateUserParams(newUser.getPassword());
        given(service.update(newUser.getId(), params)).willReturn(newUser);

        mockMvc.perform(MockMvcRequestBuilders
                        .patch(route + "/" + newUser.getId())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(getJSON(params))
                )
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.content().string(getJSON(newUser)));
    }


    private String getJSON(List<User> users) throws JsonProcessingException {
        objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(users);
    }

    private String getJSON(User user) throws JsonProcessingException {
        objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(user);
    }

    private String getJSON(UserDTO dto) throws JsonProcessingException {
        objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(dto);
    }

    private String getJSON(UpdateUserParams params) throws JsonProcessingException {
        objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(params);
    }
}
