# # Use Maven image to build the Spring Boot application
# FROM maven:3.8.4-openjdk-11 AS build

# # Set working directory
# WORKDIR /app

# # Copy the pom.xml file and install dependencies
# COPY pom.xml .
# RUN mvn dependency:go-offline -B

# # Copy the rest of the application code
# COPY src ./src

# # Package the application
# RUN mvn clean package -DskipTests

# # Use OpenJDK image to run the application
# FROM openjdk:11-jre-slim

# # Set working directory
# WORKDIR /app

# # Copy the packaged application from the build image
# COPY --from=build /app/target/app-0.0.1-SNAPSHOT.jar /app/app.jar

# # Expose port 8080
# EXPOSE 8080

# # Run the Spring Boot app
# CMD ["java", "-jar", "app.jar"]

FROM maven:3.8.3-openjdk-17 as build
WORKDIR ./src
COPY . .
RUN mvn install -DskipTests=true

FROM eclipse-temurin:17.0.8.1_1-jre-ubi9-minimal

RUN ls -la

COPY --from=build src/target/*.jar /run/app.jar

EXPOSE 8080

ENV JAVA_OPTIONS="-Xmx2048m -Xms256m"
ENTRYPOINT java -jar $JAVA_OPTIONS /run/app.jar
