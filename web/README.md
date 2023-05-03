
# Meetings WEB APP

This project contains Meetings Application WEB APP.
This app was built using `REACT` with `VITE` and `BOOTSTRAP`,
also includes `DOCKER`.

The FRONTEND project its not finished yet

## Table of Contents

<!-- TOC -->

 * [Development Environment](#development-environment)
 * [Running Local](#running-local)
 * [Running Dockerl](#running-local)


<!-- TOC -->

## Development Environment

## Tech Stack

-   **React:** We chose React as our frontend framework for several reasons. Firstly, none of us had extensive experience with it, so we wanted to use this project as an opportunity to learn React. Secondly, React has a large and supportive community, which makes it easier to find resources and solve problems. Finally, React's component-based architecture allows us to build reusable UI elements and manage complex user interfaces with ease.
    
-   **Vite:** We opted for Vite as our build tool and development server due to its fast and efficient performance. Vite's instant hot module replacement and lightning-fast cold start speed make our development process more productive and enjoyable.
    
-   **TypeScript:** We decided to use TypeScript for its strong typing and code predictability. TypeScript allows us to catch errors at compile-time rather than runtime, which improves our code quality and helps us avoid common mistakes.
    
-   **Bootstrap CSS:** We decided to use Bootstrap CSS for its comprehensive CSS utilities and responsive design system. We only used the CSS part of Bootstrap, without relying on any pre-built UI components. This allowed us to create a unique and custom UI design without the need for extensive custom styling.

## State Management

For state management in our React application, we'll be using context instead of Redux. Since our application isn't large-scale, we believe that context will simplify our code and reduce the amount of boilerplate we need to write. By using context, we can avoid the setup and maintenance overhead of Redux and focus on building our application features.


## Running Local

#### instructions: Clone the project, install dependencies and run the APP

1. The first step is to clone the project, which means that you will create a local copy of the source code repository in your computer. This is a common practice when working with version control systems like Git.

2. The second step is to install the dependencies of the project by running the `yarn install` command in the folder of the web application. This command will download and install all the required packages and libraries listed in the project's `package.json` file. If you don't have yarn installed, the instructions recommend installing it with NPM (Node Package Manager).

3. The third step is to start the project by running the `yarn dev` command. This will launch the development server and the React application will be available in your web browser at the specified URL.

Note that the terminal will say where the project is ready to be accesed

Example: 
```
  VITE v4.2.1  ready in 643 ms

  ➜  Local:   http://127.0.0.1:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```
## Running Docker

#### instructions: Clone the project, open Docker and run it.

1. The first step is to clone the project, which means that you will create a local copy of the source code repository in your computer. This is a common practice when working with version control systems like Git.

2. The second step is building the Docker image: This step creates a Docker image based on the project code and the instructions in the `Dockerfile` located in the project's web folder. The image includes all the necessary components and dependencies required to run the project in a container. Run the command `docker build .`  

3. The third step is running the Docker container: This step starts a new Docker container from the image created in step 2, run the command `docker run --rm -p 5173:5173 <image_id>`   .
The `--rm` flag ensures that the container is removed after it exits, while the `-p` flag maps the container's port 5173 to the same port on the host computer. The `<image_id>` refers to the ID of the Docker image created in step 2. 

4. Open the app in "http://localhost:5173/"