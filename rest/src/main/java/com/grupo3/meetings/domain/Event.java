package com.grupo3.meetings.domain;

import com.grupo3.meetings.api.DTO.EventDTO;
import com.grupo3.meetings.api.DTO.OptionDTO;
import com.grupo3.meetings.exceptions.event.EventIsClosedException;
import com.grupo3.meetings.exceptions.event.UserNotAdministratorException;
import com.grupo3.meetings.exceptions.option.NoOptionVotedException;
import com.grupo3.meetings.exceptions.event.UserNotInGuestListException;
import com.grupo3.meetings.exceptions.option.OptionDoesntExistException;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.*;
import java.util.stream.Collectors;

@Getter @Setter @NoArgsConstructor
public class Event {
    private String id;
    private String title;
    private String description;
    private String location;
    private User administrator;
    private Set<String> listOfGuests;
    private Option votedOption;
    private Set<Option> listOfOptions;
    private Boolean isClosed;

    /**
     * Default Event construtor.
     *
     * @param title Name of the event
     * @param description Description of the event
     * @param location Where the event will take place
     * @parma administrator User that created the event
     * @param listOfOptions List of options for the event
     * */
    public Event(String title, String description, String location, User administrator, Set<Option> listOfOptions) {
        this.title = title;
        this.description = description;
        this.location = location;
        this.administrator = administrator;
        this.listOfOptions = listOfOptions;
        this.isClosed = false;
        this.listOfGuests = new HashSet<>();
        this.addUserToGuestList(administrator);
    }

    public Event(EventDTO eventDTO) {
        this.title = eventDTO.getNombreDeEvento();
        this.description = eventDTO.getDescripcion();
        this.location = eventDTO.getUbicacion();
        this.listOfOptions=eventDTO.getOptions().stream().map(dto->dto.toOptionForEvent()).collect(Collectors.toSet());
        this.listOfGuests= new HashSet<>();
        this.isClosed=false;
    }

    public Event(String reunionDeDiscord) {
        this.title = reunionDeDiscord;
    }

    public Set<String> getListOfGuests() {
        return listOfGuests;
    }

    public Set<Option> getListOfOptions() {
        return listOfOptions;
    }

    public Option getVotedOption() {
        return votedOption;
    }

    public Boolean getIsClosed() {
        return isClosed;
    }

    /**
     * Validates if the event is open.
     *
     * @throws EventIsClosedException if the event is closed
     * */
    private void validateIfEventIsOpen() {
        if(this.isClosed)
            throw new EventIsClosedException("Event is closed");
    }

    /**
     * Validates if the user is the administrator of the event.
     *
     * @param user User to be validated
     * @throws UserNotAdministratorException if the user is not the administrator
     * */
    private void validateIfUserIsAdministrator(User user) {
        if(!this.administrator.equals(user))
            throw new UserNotAdministratorException("Only the administrator can modify the event");
    }

    /**
     * Adds an option to the event.
     *
     * @param option Option to be added
     * @throws EventIsClosedException if the event is closed
     * @throws UserNotAdministratorException if the user is not the administrator
     * */
    public void addOption(Option option) {

        this.listOfOptions.add(option);
    }

    /**
     * Removes an option from the event.
     *
     * @param option Option to be removed
     * @throws EventIsClosedException if the event is closed
     * @throws UserNotAdministratorException if the user is not the administrator
     * @throws OptionDoesntExistException if the option doesn't exist
     * */
    public void removeOption(Option option, User administrator) {
        validateIfEventIsOpen();
        validateIfUserIsAdministrator(administrator);
        if(!this.listOfOptions.contains(option))
            throw new OptionDoesntExistException();
        this.listOfOptions.remove(option);
    }

    /**
     * Votes for an option.
     * @param option Option to be voted
     * @param user User that votes
     * @throws EventIsClosedException if the event is closed
     * @throws UserNotInGuestListException if the user is not in the guest list of the event
     */
    public void vote(Option option, User user) {
        validateIfEventIsOpen();
        if(!this.listOfGuests.contains(user.getId()))
            throw new UserNotInGuestListException();
        option.toggleVote(user.getId());
    }

    /**
     * Adds a user to the guest list of the event.
     * @param user User to be added
     * @throws EventIsClosedException if the event is closed
     */
    public void addUserToGuestList(User user) {
        validateIfEventIsOpen();
        this.listOfGuests.add(user.getId());
    }

    /**
     * Close the event from voting and chooses the option with the most votes.
     * @param user User that closes the event
     * @throws EventIsClosedException if the event is already closed
     * @throws UserNotAdministratorException if the user is not the administrator
     * @throws NoOptionVotedException if there is no votes on any option
     */
    public void closeEvent(User user) {
        validateIfEventIsOpen();
        validateIfUserIsAdministrator(user);

        // When there is a tie, the first option is chosen
        this.votedOption = this.listOfOptions.
                stream()
                .max(Comparator.comparing(Option::getVotes))
                .orElseThrow(NoOptionVotedException::new);

        if(votedOption.getVotes() == 0)
            throw new NoOptionVotedException();

        this.isClosed = true;
    }

    /**
     * Reopens the event for voting.
     * @param user User that reopens the event
     * @throws EventIsClosedException if the event is already open
     */
    public void openEvent(User user) {
        validateIfUserIsAdministrator(user);
        this.isClosed = false;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
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

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public User getAdministrator() {
        return administrator;
    }

    public void setAdministrator(User administrator) {
        this.administrator = administrator;
    }

    public void setListOfGuests(Set<String> listOfGuests) {
        this.listOfGuests = listOfGuests;
    }

    public void setVotedOption(Option votedOption) {
        this.votedOption = votedOption;
    }

    public void setListOfOptions(Set<Option> listOfOptions) {
        this.listOfOptions = listOfOptions;
    }

    public void setIsClosed(Boolean isClosed) {
        this.isClosed = isClosed;
    }

    public void closeEvent2() {
        this.isClosed = true;
    }

    public void vote(String username) {
        this.listOfGuests.add(username);
    }
}
