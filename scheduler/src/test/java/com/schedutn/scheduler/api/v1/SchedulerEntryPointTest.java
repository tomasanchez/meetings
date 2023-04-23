package com.schedutn.scheduler.api.v1;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.schedutn.scheduler.BaseIntegrationTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

@AutoConfigureMockMvc
public class SchedulerEntryPointTest extends BaseIntegrationTest {

  private final String BASE_URL = SchedulesEntryPoint.SCHEDULES_ENTRY_POINT_URL;

  @Autowired
  private MockMvc mvc;

  @Test
  public void whenQuerySchedules_then_isOk() throws Exception {
    mvc.perform(get(BASE_URL))
        .andExpect(status().isOk());
  }
  
}
