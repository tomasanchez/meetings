package com.schedutn.scheduler.service

import com.schedutn.scheduler.domain.IllegalScheduleException
import com.schedutn.scheduler.domain.IllegalVoteException
import com.schedutn.scheduler.domain.commands.ScheduleMeeting
import com.schedutn.scheduler.domain.commands.ToggleVoting
import com.schedutn.scheduler.domain.commands.VoteForOption
import com.schedutn.scheduler.domain.events.MeetingScheduled
import com.schedutn.scheduler.domain.events.OptionVoted
import com.schedutn.scheduler.domain.models.Meeting
import com.schedutn.scheduler.domain.models.MeetingOption
import com.schedutn.scheduler.domain.models.Schedule
import com.schedutn.scheduler.repository.ScheduleRepositoryMongo
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service

@Service
class MeetingScheduler : ScheduleService {
  @Autowired
  private lateinit var schedules : ScheduleRepositoryMongo

  override fun scheduleMeeting(command: ScheduleMeeting): MeetingScheduled {

    val schedule = Schedule(
      organizer = command.organizer,
      event = Meeting(
        title = command.title,
        description = command.description,
        location = command.location,
      ),
      options = command.options.map {
        MeetingOption(
          date = it.date,
          hour = it.hour,
          minute = it.minute,
        )
      }.toSet(),
      guests = command.guests ?: emptySet(),
    )

    return modelToEvent(schedules.save(schedule))
  }

  override fun joinAMeeting(id: String, username: String): MeetingScheduled {
    if(schedules.findById(id).isPresent) {
      val schedule = schedules.findById(id).get()

      val joined = schedule.join(username = username)

      return modelToEvent(schedules.save(joined))
    }
    throw ScheduleNotFoundException(id)
  }

  override fun toggleVoting(id: String, command: ToggleVoting): MeetingScheduled {
    if(schedules.findById(id).isPresent) {
      val schedule = schedules.findById(id).get()

      try {
        val toggled = schedule.toggleVoting(username = command.username,
          enabledVotes = command.voting)

        return modelToEvent(schedules.save(toggled))
      } catch (e: IllegalScheduleException) {

        throw ScheduleAuthorizationException(e)
      }
    }
    throw ScheduleNotFoundException(id)
  }

  override fun voteForAnOption(id: String, command: VoteForOption): MeetingScheduled {
    if(schedules.findById(id).isPresent) {
      val schedule = schedules.findById(id).get()

      val option = MeetingOption(
        date = command.option.date,
        hour = command.option.hour,
        minute = command.option.minute,
      )

      try {

        val voted: Schedule = schedule.vote(option = option, username = command.username)
        return modelToEvent(schedules.save(voted))

      } catch (e: IllegalVoteException) {

        throw ScheduleAuthorizationException(e)
      }
    }
    throw ScheduleNotFoundException(id)
  }

  override fun scheduleById(id: String): MeetingScheduled {
    if(schedules.findById(id).isPresent) {
      return modelToEvent(schedules.findById(id).get())
    }
    throw ScheduleNotFoundException(id)
  }

  override fun findAll(): Collection<MeetingScheduled> {
    return schedules.findAll().map(::modelToEvent)
  }

  /**
   * Converts a Schedule to a MeetingScheduled
   *
   * @param schedule to be translated
   * @return an Event with the corresponding JSON representation
   */
  private fun modelToEvent(schedule: Schedule): MeetingScheduled {
    return MeetingScheduled(
      id = schedule.id!!,
      voting = schedule.voting,
      options = schedule
        .options
        .map {
          OptionVoted(date = it.dateTime(),
            votes = it.votes
          )
        }
        .toSet(),
      guests = schedule.guests,
      organizer = schedule.organizer,
      title = schedule.event.title,
      description = schedule.event.description,
      location = schedule.event.location,
    )
  }
}