package com.grupo3.meetings.domain;

import com.grupo3.meetings.exceptions.event.EventIsClosedException;
import com.grupo3.meetings.exceptions.event.UserNotAdministratorException;
import com.grupo3.meetings.exceptions.option.NoOptionVotedException;
import com.grupo3.meetings.exceptions.event.UserNotInGuestListException;
import com.grupo3.meetings.exceptions.option.OptionDoesntExistException;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.*;

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

    private void validateIfEventIsOpen() {
        if(this.isClosed)
            throw new EventIsClosedException("Event is closed");
    }

    private void validateIfUserIsAdministrator(User user) {
        if(!this.administrator.equals(user))
            throw new UserNotAdministratorException("Only the administrator can modify the event");
    }

    public void addOption(Option option) {
        validateIfEventIsOpen();
        validateIfUserIsAdministrator(administrator);
        this.listOfOptions.add(option);
    }

    public void removeOption(Option option, User administrator) {
        validateIfEventIsOpen();
        validateIfUserIsAdministrator(administrator);
        if(!this.listOfOptions.contains(option))
            throw new OptionDoesntExistException();
        this.listOfOptions.remove(option);
    }

    public void vote(Option option, User user) {
        validateIfEventIsOpen();
        if(!this.listOfGuests.contains(user.getId()))
            throw new UserNotInGuestListException();
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
                .orElseThrow(NoOptionVotedException::new);

        if(votedOption.getVotes() == 0)
            throw new NoOptionVotedException();

        this.isClosed = true;
    }

    public void openEvent(User user) {
        validateIfUserIsAdministrator(user);
        this.isClosed = false;
    }
}
