package com.schedutn.scheduler;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@OpenAPIDefinition(
        info = @io.swagger.v3.oas.annotations.info.Info(
                title = "Scheduler Service",
                version = "0.1.2",
                description = "Scheduler manages the workflow of meetings scheduling",
                license = @io.swagger.v3.oas.annotations.info.License(
                        name = "MIT",
                        url = "https://mit-license.org/"
                ),
                contact = @io.swagger.v3.oas.annotations.info.Contact(
                        name = "Tomas Sanchez",
                        url = "https://tomasanchez.github.io",
                        email = "tosanchez@frba.utn.edu.ar")
        )
)
@SpringBootApplication
public class SchedulerApplication {

    public static void main(String[] args) {
        SpringApplication.run(SchedulerApplication.class, args);
    }

}
