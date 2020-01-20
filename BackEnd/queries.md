### Evaluation Influx (Car Rental Platform)

Create a database
```sql
CREATE DATABASE carRental
```

Use the database created
```sql
USE carRental;
```

Create the user table
```sql
CREATE TABLE user (user_id INT NOT NULL auto_increment, user_name VARCHAR(255) NOT NULL, user_email VARCHAR(255) NOT NULL, user_password VARCHAR(255) NOT NULL, user_salt VARCHAR(255) NOT NULL, user_number VARCHAR(255), user_license VARCHAR(255) NOT NULL, primary key(user_id));
```

Create the Car table
```sql
CREATE TABLE Cars (car_id INT NOT NULL auto_increment, car_model VARCHAR(255) NOT NULL, car_type VARCHAR(255) NOT NULL, car_seats INT(255) NOT NULL, car_color VARCHAR(255) NOT NULL, car_booked INT(10) NOT NULL, primary key(car_id));
```

Create the Booking table
```sql
CREATE TABLE Booking (booking_id INT NOT NULL auto_increment, user_id INT, car_id INT, booking_date VARCHAR(255) NOT NULL, booking_days VARCHAR(255) NOT NULL, primary key(booking_id), foreign key(user_id) REFERENCES user(user_id), foreign key(car_id) REFERENCES Cars(car_id));
```

Inserting Cars
```sql
INSERT INTO Cars (car_model, car_type, car_seats, car_color) VALUES(%s, %s, %s, %s);
```