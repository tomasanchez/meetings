#
# Build stage
#
FROM eclipse-temurin:17-jdk-alpine as build

ARG APP_DIR=/workspace/app

# Deploy Application
WORKDIR $APP_DIR
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
ADD src $APP_DIR/src

## Install Dependencies
RUN ./mvnw install -DskipTests
RUN mkdir -p target/dependency && (cd target/dependency; jar -xf ../*.jar)


#
# Package stage
#
FROM eclipse-temurin:17-jdk-alpine
VOLUME /tmp
ARG DEPENDENCY=/workspace/app/target/dependency
COPY --from=build ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY --from=build ${DEPENDENCY}/META-INF /app/META-INF
COPY --from=build ${DEPENDENCY}/BOOT-INF/classes /app
EXPOSE 8080
ENTRYPOINT ["java","-cp","app:app/lib/*","com.grupo3.meetings.MeetingsApplication"]