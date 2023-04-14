package com.grupo3.meetings.domain;

import java.util.*;

public class Event {
    private String id;
    private String title;
    private String description;
    private String location;
    private User administrator;
    private HashSet<String> listOfGuests;
    private Option votedOption;
    private HashSet<Option> listOfOptions;
    private boolean isClosed;

    public Event(String title, String description, String location, User administrator, HashSet<Option> listOfOptions) {
        this.title = title;
        this.description = description;
        this.location = location;
        this.administrator = administrator;
        this.listOfOptions = listOfOptions;
        this.isClosed = false;
        this.listOfGuests = new HashSet<String>();
        this.addUserToGuestList(administrator);
    }

    public Event() {
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public User getAdministrator() {
        return administrator;
    }

    public void setAdministrator(User administrator) {
        this.administrator = administrator;
    }

    public Set<String> getListOfGuests() {
        return listOfGuests;
    }

    public void setListOfGuests(HashSet<String> listOfGuests) {
        this.listOfGuests = listOfGuests;
    }

    public Option getVotedOption() {
        return votedOption;
    }

    public void setVotedOption(Option finalOption) {
        this.votedOption = finalOption;
    }

    public HashSet<Option> getListOfOptions() {
        return listOfOptions;
    }

    public void setListOfOptions(HashSet<Option> listOfOptions) {
        this.listOfOptions = listOfOptions;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public boolean getIsClosed() {
        return isClosed;
    }

    public void validateIfEventIsOpen() {
        if(this.isClosed)
            throw new RuntimeException("Event is closed");
    }

    public void validateIfUserIsAdministrator(User user) {
        if(!this.administrator.equals(user))
            throw new RuntimeException("Only the administrator can modify the event");
    }

    public void addOption(Option option) {
        validateIfEventIsOpen();
        if(listOfOptions.contains(option))
            throw new RuntimeException("Option already exists");
        this.listOfOptions.add(option);
    }

    public void removeOption(Option option, User administrator) {
        validateIfEventIsOpen();
        validateIfUserIsAdministrator(administrator);
        if(!this.listOfOptions.contains(option))
            throw new RuntimeException("Option does not exist");
        this.listOfOptions.remove(option);
    }

    public void vote(Option option, User user) {
        validateIfEventIsOpen();
        if(!this.listOfGuests.contains(user.getId()))
            throw new RuntimeException("User is not in the guest list");
        option.toggleVote(user.getId());
    }

    public void addUserToGuestList(User user) {
        validateIfEventIsOpen();
        this.listOfGuests.add(user.getId());
    }

    // When there is a tie, the first option is chosen
    public void closeEvent(User user) {
        validateIfEventIsOpen();
        validateIfUserIsAdministrator(user);

        this.votedOption = this.listOfOptions.
                stream()
                .max(Comparator.comparing(Option::getVotes))
                .orElseThrow(NoSuchElementException::new);

        if(votedOption.getVotes() == 0)
            throw new RuntimeException("No one voted for any option");

        this.isClosed = true;
    }

    public void openEvent(User user) {
        validateIfUserIsAdministrator(user);
        this.isClosed = false;
    }
}
