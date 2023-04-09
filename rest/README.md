# Meetings REST API

This project contains Meetings Application REST API Service.
This service was built using `Springboot` with `JDK 17` and `Maven`,
also includes support for `Kotlin`.

## Table of Contents

<!-- TOC -->
* [Meetings REST API](#meetings-rest-api)
  * [Table of Contents](#table-of-contents)
  * [Development Environment](#development-environment)
    * [Install Java and Kotlin](#install-java-and-kotlin)
    * [Install Maven](#install-maven)
    * [Running Local](#running-local)
      * [Step 1: Create module from existing source](#step-1--create-module-from-existing-source)
      * [Step 2: Rebuild all packages](#step-2--rebuild-all-packages)
      * [Step 3: Launch the REST service](#step-3--launch-the-rest-service)
<!-- TOC -->

## Development Environment

### Install Java and Kotlin

Install a `Java 17 SDK` from IntelliJ.

### Install Maven

This package uses Maven for dependency management.

Download Maven for the [official website](https://maven.apache.org/download.cgi).

### Running Local

#### Step 1: Create module from existing source

1. From the File menu, choose `File->New->Module from existing sources`
2. In the resulting dialog, select `grupo-3-tacs/rest/pom.xml`
3. Click Ok

Note that Intellij may take some time rebuilding package indexes.
When you open any file, if prompted to _"Trust"_ the package, then do so.


#### Step 2: Rebuild all packages

1. In the project explorer, right-click `grupo-3-tacs/rest`
2. Choose `Rebuild Module 'rest'`

#### Step 3: Launch the REST service

1. In the project explorer, choose `rest`
2. Drill down through the folders until you find `MeetingsApplication`
3. Right-click `MeetingsApplication` and choose `Run 'MeetingsApplication'`
4. Verify that the service is running by opening a browser and navigating to http://localhost:8080/docs
5. If you see the Swagger UI, then the service is running.
