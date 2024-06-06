// Detailed health tips array
const healthTips = [
    "Drink at least 8 cups of water daily. Staying hydrated is crucial for maintaining energy levels and overall health.",
    "Take a 5-minute break every hour to stretch. This helps reduce muscle tension and improve circulation.",
    "Incorporate more fruits and vegetables into your diet. They provide essential vitamins, minerals, and fiber.",
    "Practice deep breathing exercises to reduce stress. Inhale deeply through your nose, hold for a few seconds, and exhale slowly.",
    "Ensure you get 7-8 hours of sleep each night. Quality sleep is vital for mental and physical health.",
    "Take a walk for at least 30 minutes every day. Walking helps improve cardiovascular health and mood.",
    "Stay consistent with your medication schedule. Always take your medications as prescribed by your doctor.",
    "Visit your doctor for regular health check-ups. Early detection of health issues can lead to better outcomes.",
    "Monitor your blood pressure regularly. Keeping track of your blood pressure can help manage hypertension.",
    "Keep a gratitude journal to boost your mental health. Write down three things you are grateful for each day.",
    "Eat a balanced breakfast every morning. A healthy breakfast fuels your body and improves concentration.",
    "Limit your intake of sugary drinks. Opt for water, herbal teas, or natural fruit juices instead.",
    "Practice good posture. Sit and stand up straight to avoid back pain and improve breathing.",
    "Take time for mindfulness or meditation. Spend a few minutes each day in quiet reflection to reduce stress.",
    "Include lean proteins in your diet. Proteins are essential for muscle repair and immune function.",
    "Spend time outdoors in nature. Fresh air and sunlight can boost your mood and overall well-being.",
    "Avoid processed foods. Choose whole, unprocessed foods for better nutrition and health.",
    "Stay socially connected. Engage with friends and family regularly to support your mental health.",
    "Wash your hands frequently. Proper hand hygiene can prevent the spread of infections.",
    "Set realistic health goals. Break larger goals into smaller, achievable steps to stay motivated.",
    "Incorporate strength training exercises. Building muscle mass improves metabolism and bone density.",
    "Avoid smoking and limit alcohol consumption. Both can have serious long-term health effects.",
    "Practice safe sun exposure. Wear sunscreen and protective clothing to prevent skin damage.",
    "Stay informed about your health conditions. Educate yourself about managing any chronic illnesses you may have.",
    "Take breaks from screen time. Rest your eyes and stretch your body to prevent strain and fatigue.",
    "Incorporate healthy fats into your diet. Foods like avocados, nuts, and olive oil are beneficial.",
    "Stay positive and practice self-compassion. Be kind to yourself and focus on your progress, not perfection."
];

// Function to change the health tip displayed
function changeHealthTip() {
    const tipElement = document.getElementById('health-tip');
    if (tipElement) {
        const randomIndex = Math.floor(Math.random() * healthTips.length);
        tipElement.innerText = healthTips[randomIndex];
    } else {
        console.error('Element with id "health-tip" not found.');
    }
}

// Set an interval to change the health tip every 10 seconds
setInterval(changeHealthTip, 10000);

// Function to handle reminder form submission
function handleReminderForm(event) {
    event.preventDefault();

    const reminderType = document.getElementById('reminder-type').value;
    const interval = document.getElementById('interval').value;

    const reminders = JSON.parse(localStorage.getItem('reminders')) || [];
    const newReminder = { type: reminderType, interval: interval };
    reminders.push(newReminder);
    localStorage.setItem('reminders', JSON.stringify(reminders));

    displayReminder(newReminder);
    document.getElementById('reminder-form').reset(); // Reset form fields
}

// Function to display reminders on the page
function displayReminder(reminder) {
    const reminderList = document.querySelector('.reminder-list');
    if (reminderList) {
        const reminderItem = document.createElement('div');
        reminderItem.className = 'reminder-item';
        reminderItem.innerHTML = `
            <strong>Reminder:</strong> ${reminder.type} <br> 
            <strong>Interval:</strong> ${reminder.interval}
            <button onclick="markReminderAsCompleted(this)" class="btn">Mark as Completed</button>
            <button onclick="deleteReminder(this)" class="btn">Delete</button>
        `;
        reminderList.appendChild(reminderItem);
    } else {
        console.error('Element with class "reminder-list" not found.');
    }
}

// Function to mark reminder as completed
function markReminderAsCompleted(button) {
    const reminderItem = button.parentElement;
    reminderItem.classList.add('completed');
    button.remove(); // Remove the 'Mark as Completed' button after marking it as completed
}

// Function to delete reminder
function deleteReminder(button) {
    const reminderItem = button.parentElement;
    reminderItem.remove();
}

// Function to delete completed reminders
function deleteCompletedReminders() {
    const reminderList = document.querySelector('.reminder-list');
    const completedReminders = reminderList.querySelectorAll('.completed');
    completedReminders.forEach(reminder => reminder.remove());
}

// Example usage during fetch
document.addEventListener('DOMContentLoaded', function() {
    const reminderForm = document.getElementById('reminder-form');
    if (reminderForm) {
        reminderForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const reminderType = document.getElementById('reminder-type').value;
            const interval = document.getElementById('interval').value;

            const reminder = {
                type: reminderType,
                interval: interval
            };

            displayReminder(reminder);
            reminderForm.reset(); // Reset form fields
        });
    }

    // Example of pre-existing reminders fetched from an API
    fetch('/api/reminders')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const reminderList = document.querySelector('.reminder-list');
            if (reminderList) {
                data.reminders.forEach(reminder => {
                    displayReminder(reminder);
                });
            }
        })
        .catch(error => console.error('There was a problem with the fetch operation:', error));
});

// Function to validate form fields
function validateForm(form) {
    let isValid = true;
    const email = form.elements['email'];
    const password = form.elements['password'];
    const passwordVerify = form.elements['passwordVerify'];

    if (!email.value.includes('@')) {
        isValid = false;
        email.setCustomValidity('Please enter a valid email address.');
    } else {
        email.setCustomValidity('');
    }

    if (password.value.length < 8) {
        isValid = false;
        password.setCustomValidity('Password must be at least 8 characters long.');
    } else {
        password.setCustomValidity('');
    }

    if (passwordVerify) {
        if (password.value !== passwordVerify.value) {
            isValid = false;
            passwordVerify.setCustomValidity('Passwords do not match.');
        } else {
            passwordVerify.setCustomValidity('');
        }
    }

    return isValid;
}

// Example of attaching the validateForm function to a form's submit event
document.getElementById('signupForm').addEventListener('submit', function(event) {
    if (!validateForm(event.target)) {
        event.preventDefault();
    }
});
// Function to handle user signup
function handleSignup(event) {
    event.preventDefault();
    const userData = {
        name: event.target.elements['name'].value,
        email: event.target.elements['email'].value,
        password: event.target.elements['password'].value,
        birthday: event.target.elements['birthday'].value,
        sex: event.target.elements['sex'].value
    };

    let users = JSON.parse(localStorage.getItem('users')) || [];
    users.push(userData);
    localStorage.setItem('users', JSON.stringify(users));

    localStorage.setItem('currentUser', JSON.stringify(userData));
    window.location.href = './features.html'; // Redirect to features page
}

// Function to handle user login
function handleLogin(event) {
    event.preventDefault();
    const email = event.target.elements['email'].value;
    const password = event.target.elements['password'].value;

    let users = JSON.parse(localStorage.getItem('users')) || [];
    const user = users.find(user => user.email === email && user.password === password);
    if (user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
        window.location.href = './features.html'; // Redirect to features page
    } else {
        alert('Login failed: Invalid email or password');
    }
}

// Function to handle user logout
function handleLogout() {
    localStorage.removeItem('currentUser');
    window.location.href = '/index.html';
}

// Invoke initial functions on page load
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navList = document.querySelector('.nav-list');
    const reminderForm = document.getElementById('reminder-form');
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');
    const logoutButton = document.getElementById('logout');
    const userNameDisplay = document.getElementById('userName');

    if (navToggle && navList) {
        navToggle.addEventListener('click', function() {
            navList.classList.toggle('active');
        });
    }

    changeHealthTip(); // Immediately change the health tip when the page loads
    setInterval(changeHealthTip, 10000); // Change health tip every 10 seconds

    if (reminderForm) {
        reminderForm.addEventListener('submit', handleReminderForm);
        const reminders = JSON.parse(localStorage.getItem('reminders')) || [];
        reminders.forEach(displayReminder);
    }

    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            event.preventDefault();
            if (validateForm(signupForm)) {
                handleSignup(event);
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }

    if (userNameDisplay) {
        const user = JSON.parse(localStorage.getItem('currentUser'));
        if (user) {
            userNameDisplay.textContent = user.name;
        } else {
            window.location.href = './login.html';
        }
    }
});

const dailyQuotes = [
    "Health is wealth.",
    "Take care of your body. It's the only place you have to live.",
    "An apple a day keeps the doctor away.",
    "Your health is an investment, not an expense.",
    "The greatest wealth is health.",
];

function displayDailyQuote() {
    const quoteElement = document.getElementById('daily-quote');
    if (quoteElement) {
        const randomIndex = Math.floor(Math.random() * dailyQuotes.length);
        quoteElement.innerText = dailyQuotes[randomIndex];
    }
}

document.addEventListener('DOMContentLoaded', function() {
    displayDailyQuote();
});

function clearLocalStorage() {
    localStorage.clear();
    alert('All data cleared!');
    window.location.reload();
}

document.getElementById('clearDataButton').addEventListener('click', clearLocalStorage);


//bmi calculator
document.getElementById('bmiForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);

    if (weight > 0 && height > 0) {
        const bmi = weight / (height * height);
        let resultText = `Your BMI is ${bmi.toFixed(2)}.`;

        if (bmi < 18.5) {
            resultText += " You are underweight.";
        } else if (bmi >= 18.5 && bmi < 24.9) {
            resultText += " You have a normal weight.";
        } else if (bmi >= 25 && bmi < 29.9) {
            resultText += " You are overweight.";
        } else {
            resultText += " You are obese.";
        }

        document.getElementById('bmiResult').innerText = resultText;
    } else {
        document.getElementById('bmiResult').innerText = "Please enter valid weight and height.";
    }
});
//Hydration Tracker
let dailyWaterIntake = 0;

function addWaterIntake(amount) {
    dailyWaterIntake += amount;
    localStorage.setItem('dailyWaterIntake', dailyWaterIntake);
    displayWaterIntake();
}

function displayWaterIntake() {
    const waterElement = document.getElementById('water-intake');
    if (waterElement) {
        waterElement.innerText = `Daily Water Intake: ${dailyWaterIntake} ml`;
    }
}

document.getElementById('addWaterButton').addEventListener('click', function() {
    const amount = parseInt(prompt('Enter water intake in ml:'));
    addWaterIntake(amount);
});

document.addEventListener('DOMContentLoaded', function() {
    dailyWaterIntake = parseInt(localStorage.getItem('dailyWaterIntake')) || 0;
    displayWaterIntake();
});


//User Progress Dashboard
function displayUserProgress() {
    const progressElement = document.getElementById('user-progress');
    const dailySteps = localStorage.getItem('dailySteps') || 0;
    const dailyWaterIntake = localStorage.getItem('dailyWaterIntake') || 0;
    if (progressElement) {
        progressElement.innerHTML = `
            <p>Daily Steps: ${dailySteps}</p>
            <p>Daily Water Intake: ${dailyWaterIntake} ml</p>
        `;
    }
}

document.addEventListener('DOMContentLoaded', displayUserProgress);

//notification setting for in- browser
function showNotification(message) {
    if (Notification.permission === 'granted') {
        new Notification(message);
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                new Notification(message);
            }
        });
    }
}

document.getElementById('notifyButton').addEventListener('click', function() {
    showNotification('Time to drink water!');
});

//reminder completion
function markReminderAsCompleted(button) {
    const reminderItem = button.parentNode;
    reminderItem.style.textDecoration = 'line-through';
}

document.querySelectorAll('.reminder-item button').forEach(button => {
    button.addEventListener('click', function() {
        markReminderAsCompleted(button);
    });
});


//profile greenting
function displayGreeting() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    const greetingElement = document.getElementById('greeting');
    const hours = new Date().getHours();
    let greeting = 'Hello';

    if (hours < 12) {
        greeting = 'Good Morning';
    } else if (hours < 18) {
        greeting = 'Good Afternoon';
    } else {
        greeting = 'Good Evening';
    }

    if (user && greetingElement) {
        greetingElement.innerText = `${greeting}, ${user.name}!`;
    }
}

document.addEventListener('DOMContentLoaded', displayGreeting);