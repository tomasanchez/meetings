package com.grupo3.meetings;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@OpenAPIDefinition(
    info = @Info(
        title = "Meetings API",
        version = "0.1.0",
        description = "Meetings API allows you to manage meetings workflows," +
            " validate user credentials and obtain metrics about the system.",
        license = @License(name = "MIT License", url = "https://mit-license.org/")
    ))
@SpringBootApplication
public class MeetingsApplication {

  public static void main(String[] args) {
    SpringApplication.run(MeetingsApplication.class, args);
  }

}
