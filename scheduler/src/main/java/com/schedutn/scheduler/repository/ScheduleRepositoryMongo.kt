package com.schedutn.scheduler.repository

import com.schedutn.scheduler.domain.models.Schedule
import org.springframework.data.mongodb.repository.MongoRepository

interface ScheduleRepositoryMongo : MongoRepository<Schedule, String> {
}