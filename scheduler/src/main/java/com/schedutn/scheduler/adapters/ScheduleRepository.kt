package com.schedutn.scheduler.adapters

import com.schedutn.scheduler.domain.models.Schedule
import java.util.*

class ScheduleRepository(
  private val db: MutableMap<String, Schedule> = mutableMapOf()
) {

  fun save(schedule: Schedule): Schedule {

    val id: String = schedule.id ?: UUID.randomUUID().toString()

    val saved = schedule.copy(id = id, version = schedule.version + 1)

    if (schedule.id == null) {
      db[id] = saved
      return saved
    }

    val current = db[id]!!

    if (schedule.version >= current.version) {
      db[id] = saved
      return saved
    }

    throw IllegalStateException("Schedule with id $id is not up to date")
  }

  fun findById(id: String): Schedule? {
    return db[id]
  }

  fun findAll(): Collection<Schedule> {
    return db.values
  }

  fun deleteById(id: String) {
    db.remove(id)
  }
}
