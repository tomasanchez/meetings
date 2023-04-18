package com.grupo3.meetings.repository;

import com.grupo3.meetings.domain.Event;
import com.grupo3.meetings.domain.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
public class UserRepository {
        List<User> db ;
    public Optional<User> findUserById(String userId) {
        return Optional.empty();
    }
    public UserRepository() {
        this.db = new ArrayList<User>();
    }
}
