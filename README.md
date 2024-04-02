# Wise Dental
#### Video Demo:  <https://www.youtube.com/watch?v=tzHIBoyS884>
#### Description:
A basic dental office system for reservation and info

## Design debate:
I Kept going back and forth between 4 different palettes (until right before the submission), but stayed with this white/cream/dark gray/soft pink palette as it seemed more modern and fitting

## File Descriptions :
### website_data.db:
Contains two databases (users and reservations)

### requirements.txt :
Contains all libraries used

### helpers.py :
Contains all helper methods used

### app.py :
Contains the brains of the website from sql queries to all routes used like:
* "/" : Main route (index)
* "/login" : User login route
* "/logout" : User logout route
* "/register" User register route
* "/forgot": Password resetting route for user
* "/reserve" : User can reserve an appointment at the dental office
* "/history" : User can see past records of appointments and can cancel an pending ones
* "/admin" : Admin route to access admin page
* "/info_general" : Access information about general dental information
* "/info_cosmetic" : Access information about cosmetic dental information
* "/info_surgical" : Access information about surgical dental information

## HTML file descriptions :
> These files are the implemented features I made, but I am planning to do much more features than these

### admin.html
Admin page that just appears when an admin accounted is detected

### forgot.html
User can reset there password at an time they want

### history.html
Preview all your previous appointments reserved

### index.html
Shows main page with all its info

### info_cosmetic.html
Shows placeholder for information about cosmetic dental

### info_general.html
Shows placeholder for information about general dental

### info_surgical.html
Shows placeholder for information about surgical dental

### layout.html
This contains the header and the footer for the website

### layyout_2.html
Has custom features for the index and extends layout.html

### laout_3.html
Has custom features for the 3 info pages and extends layout_2.html

### login.html
Normal login page for user.

All conditions are checked, for example: email already used, password is incorrect, fields aren't empty and saves the user id in the session

### register.html
Normal register page for user

All conditions are checked, for example: email already is in database, password is too short, passsword and confirmation match, mobile number is too short, fields aren't empty and saves the user id in the session

### reserve.html
User can reserve for any procedure and can write an optional comment for the doctor before the appointment and select a date

## styles.css:
> This is a css file that is 600 lines long that has all of the design components of the site (except for a few exception that are written withen the html files them selves)

> There are custom color codes and nested loops for the header

> Imported font awsome css lines to put the social media icons below in the footer with a copywrite symbol as well just to be fancy

> Wrote code for custom headers for each page

> Wrote code for the three sections of information in the main page, as when you hover above it, a box smoothly appears.
