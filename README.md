# CS50X - HOTEL BOOKING Flask app
#### Video Demo:  <URL HERE>
#### Description:

## Tools used
- Python, Flask, Flask-SQLAlchemy, SQLite3, Bootstrap, HTML, Jinja2, CSS, JavaScript, jQuerry

# This is my personal project for [CS50x](https://cs50.harvard.edu/x/2023/) programming course by Harvard.
This web app is developed for CS50x course in 2023. The web app is intendet for the hotel front end (client side) and backend (reception / hotel management).
This web app is designed with the purpose to automate reservations for the hotel.

## Backend
In the backend the hotel management staff executes the following operations:

- Create room type with specific criterias - total guests, adults and children capacity, total of that room type in existence in the hotel.
- Upload image for the given room or if left blank default img is shown
- View all created rooms or delete room

- Create Rate type - example: Double Room BB(Bed and Breakfast)
- Each Rate type can have up to 4 different rate plans with each having different prices and date ranges in which is valid
- Each rate plan can have different prices for adults, single adult accommodation, children under 2, 7, 12 or children on regular bed.
- View all created rate type/plans or delete them

- Availability
- Select from the created rooms, select from the created rate plans and select start and end date and quantity to list that room as available for booking's
- Check Availability - Select start and end date
- The calendar is loaded for the dates selected where you can see total rooms of given type, total added for bookings, available for bookings and booked.
- On each date in the calendar there is green indication with 'a' that this room is available for bookings.
- On the right side of each room in the calendar there is the option to stop sale the given room for selected period and the indication turns red for these dates and room is closed for bookings

- Reservations tab
- Here all reservations are displayed in a table with all the information needed for the staff
- The table is searchable and can be ordered and has pagination.
- The plugin iam using for this table is from [datatables.net](https://datatables.net/) 

## Frontend / Client side

- Client search for check-in and check-out dates with specific criteria - Total rooms, total adults and children. 
- Rooms are limited to 3, clients to 6 and children to two per search.
- If children are selected Client must input their age range.

- If the search is succesfull - There are room/s that meet the Client criteria
- All options are rendered on new page from where Client can select  with summary for the reservation - price per day per room, price per day all rooms, total price, number of  guests etc.
- Upon selecting from the options the Client is redirected to a new page with full summary for the reservation that is about to make and short form with Client's information.
- When submited email is send to the client email with the reservation number and check-in date.
- New page for succesfull reservation is rendered.

- Client and Reservation are stored in the hotel database and displayed in the reservation tab

## Database structure
![Model](https://github.com/Acrofil/cs50x-final-project/blob/main/sqltablesdesign.png)

## Flask structure
![Model](https://github.com/Acrofil/cs50x-final-project/blob/main/treestructure.png)

## Ways to improve the web app

- Use wtf-forms as more secure way
- Improve the security of the app
- let each room have gallery instead of just one image
- the names of the images stored for the room's can be uploaded like cdns or use uuid to change the name.
- Option to edit rate plans, rename rate types, edit rooms.
- Mobile expirience for hotel-managment can be improved as for now the back end is more intendet for desktop use.
- At the end of the process of making reservation can be generated pdf with the hotel logo and custom design for pdf printing.
- At the table with reservations can be included the option to download given reservation as csv, pdf or other format
- When sending mail for confirmation the reservation pdf can be included too.
- Overall expirience in the web app can be improved with using Ajax and limit page reloads and more easy data transfer
- If there are no rooms to accommodate the current search or not available for the selected dates - return suggested dates for when are gonna be available.
- Implement some paying service.
- Improve client side visuals
- Improve search

