HealthYou is a web application designed to help users maintain their daily health routines through personalized reminders and tips. The app focuses on simplicity and user customization to ensure an engaging and user-friendly experience.

Table of Contents

	•	Features
	•	Installation
	•	Usage
	•	Contributing
	•	License
	•	Detailed Documentation
	•	Future Enhancements

Features

	1.	Health Tips
	•	Displays changing health tips to keep users informed and motivated.
	•	Tips include hydration, nutrition, exercise, mindfulness, and more.
	2.	Set Your Reminders
	•	Allows users to set various health-related reminders such as hydration, medication, exercise, etc.
	•	Users can select the type of reminder and set the interval.
	3.	Current Reminders
	•	Lists all the current reminders set by the user.
	•	Provides options to edit or delete reminders.
	4.	Responsive Design
	•	The application is designed to be fully responsive and works on various devices and screen sizes.
	5.	BMI Calculator
	•	Allows users to calculate their Body Mass Index (BMI) by entering their weight and height.

Installation

To get started with HealthYou, follow these steps:

	1.	Clone the Repository
    git clone https://github.com/Chiefopoku/healthyou_

    2. Navigate to the Project Directory
    cd healthyou_

    3.	Open the Project
	•	You can open the index.html file in your browser to view the landing page.
	•	You can use a local server for a better development experience.

Usage

Health Tips

Health tips are displayed at the top of the features page and change every 10 seconds. These tips provide valuable information and motivation to help users maintain their health routines.

Setting Reminders

	1.	Navigate to the “Features” page.
	2.	Use the form under the “Set Your Reminders” section.
	3.	Select the type of reminder and the interval.
	4.	Click the “Set Reminder” button to add the reminder to your list.

Managing Reminders

	1.	The “Current Reminders” section lists all the reminders you have set.
	2.	Each reminder includes “Edit” and “Delete” buttons.
	3.	Click “Edit” to modify the reminder details.
	4.	Click “Delete” to remove the reminder from the list.

Calculating BMI

	1.	Navigate to the “Features” page.
	2.	Use the form under the “Calculate Your BMI” section.
	3.	Enter your weight in kilograms and height in meters.
	4.	Click the “Calculate BMI” button to see your BMI and related health information.

Contributing

We welcome contributions to improve HealthYou. To contribute:

	1.	Fork the Repository
	2.	Create a New Branch
    git checkout -b feature/your-feature-name

    3.	Make Your Changes
	4.	Commit Your Changes
    git commit -m "Add feature: your-feature-name"

    5. Push to Your Branch
    git push origin feature/your-feature-name

    6. **Open a Pull Request**
    Please ensure your code adheres to the company's coding standards and includes tests where applicable.

## License

This project is yet to be licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

Detailed Documentation

### HTML Structure

- **Header**
    - Contains the HealthYou logo and navigation links.
- **Hero Section**
    - Welcome message with a call-to-action button linking to the sign-up page.
- **Health Tips Section**
    - Displays dynamically changing health tips.
- **Reminder Setup Section**
    - Form to set new reminders with options for type and interval.
- **Current Reminders Section**
    - Lists current reminders with options to edit and delete each reminder.
- **BMI Calculator Section**
    - Form to calculate the Body Mass Index (BMI) based on user input for weight and height.
- **Footer**
    - Contains links to Terms of Service, Privacy Policy, and social media icons.

CSS Styling

- **General Styles**
    - Applied to body, headings, and general elements to ensure a cohesive look and feel.
- **Header Styles**
    - Flexbox layout for alignment and spacing.
    - Includes hover effects for navigation links.
- **Hero Section Styles**
    - Background image and text styles for visual appeal.
    - Call-to-action button styling.
- **Section Styles**
    - Padding and text alignment for consistency.
- **Feature Section Styles**
    - Flexbox layout for horizontal alignment.
    - Individual feature item styling with hover effects.
- **How It Works Section Styles**
    - Flexbox layout similar to the feature section.
    - Unique background color and hover effects.
- **Testimonials Section Styles**
    - Flexbox layout for alignment.
    - Unique border styling and hover effects.
- **BMI Calculator Section Styles**
    - Form styling for user inputs and result display.
- **Footer Styles**
    - Flexbox layout for alignment.
    - Links and social media icon styling.

JavaScript Functionality

- **changeHealthTip**
    - Dynamically updates the health tip every 10 seconds.
- **handleReminderForm**
    - Handles form submission to add new reminders.
    - Adds edit and delete buttons to each reminder.
- **editReminder**
    - Allows users to edit the details of an existing reminder.
- **deleteReminder**
    - Removes a reminder from the list.
- **calculateBMI**
    - Calculates and displays the user's BMI based on input weight and height.

---

Future Enhancements

- **User Authentication**
    - Implement user sign-up, login, and authentication.
- **Data Persistence**
    - Save user reminders and preferences to a database.
- **Notification System**
    - Integrate push notifications for reminders.
- **Advanced Customization**
    - Allow users to set more detailed preferences for reminders.

---

We hope you find HealthYou helpful in maintaining your daily health routines. For any questions or support, feel free to contact us at healthyou@gmail.com.

Inspiration and Team

HealthYou was inspired by the need to maintain daily health routines in a busy lifestyle. Our team, consisting of health enthusiasts and tech experts, aimed to create a solution that is both simple and effective. This project was developed as a Portfolio Project for Holberton School.

Meet the Team

- **Emmanuel Opoku-Adjei**
  - LinkedIn: [Emmanuel Opoku-Adjei](https://www.linkedin.com/in/emmanuel-opoku-adjei)
  - GitHub: [Chiefopoku](https://github.com/Chiefopoku)
  - Twitter: [@Chiefopoku](https://x.com/chieffzz)

Project Repository

You can find the project repository on GitHub: [HealthYou Repository](https://github.com/Chiefopoku/healthyou_)
