DROP TABLE IF EXISTS "sensors";

CREATE TABLE "sensors" (
  ID INTEGER PRIMARY KEY,
  SENSOR integer NULL,
  DATA integer NULL,
  DATA_DATE date,
  DATA_TIME time
);
