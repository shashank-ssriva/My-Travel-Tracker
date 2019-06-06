CREATE DATABASE IF NOT EXISTS MyTravelTracker;
USE MyTravelTracker;

CREATE TABLE `MyTravelTracker`.`TravelDetails` (
  `travel_id` BIGINT UNIQUE AUTO_INCREMENT,
  `source_airport` VARCHAR(45) NULL,
  `destination_airport` VARCHAR(45) NULL,
  `travel_date` VARCHAR(10) NULL,
  `trip_type` VARCHAR(15)
  PRIMARY KEY (travel_id)
);
