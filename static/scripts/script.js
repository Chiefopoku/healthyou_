// reminders.js

document.addEventListener('DOMContentLoaded', function() {
    const reminderForm = document.getElementById('reminder-form');
    if (reminderForm) {
        reminderForm.addEventListener('submit', handleReminderForm);
        loadReminders(); // Load reminders from the server on page load
    }

    function handleReminderForm(event) {
        event.preventDefault();

        const reminderType = document.getElementById('reminder-type').value;
        const interval = document.getElementById('interval').value;

        const reminder = { 'reminder-type': reminderType, 'interval': interval };

        fetch('/set_reminder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams(reminder).toString()
        }).then(response => {
            if (response.ok) {
                loadReminders();
                document.getElementById('reminder-form').reset(); // Reset form fields
            } else {
                response.json().then(data => {
                    alert(`Failed to set reminder: ${data.message}`);
                });
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Failed to set reminder. Please try again.');
        });
    }

    function loadReminders() {
        fetch('/get_reminders')
            .then(response => response.json())
            .then(reminders => {
                const reminderList = document.querySelector('.reminder-list');
                reminderList.innerHTML = ''; // Clear the list first
                reminders.forEach(reminder => {
                    displayReminder(reminder);
                });
            }).catch(error => {
                console.error('Error:', error);
                alert('Failed to load reminders. Please try again.');
            });
    }

    function displayReminder(reminder) {
        const reminderList = document.querySelector('.reminder-list');
        if (reminderList) {
            const reminderItem = document.createElement('div');
            reminderItem.className = 'reminder-item';
            reminderItem.innerHTML = `
                <strong>Reminder:</strong> ${reminder.reminder_type} <br> 
                <strong>Interval:</strong> ${reminder.interval}
                <button onclick="completeReminder(${reminder.id})" class="btn">Completed</button>
                <button onclick="deleteReminder(${reminder.id})" class="btn">Delete</button>
            `;
            reminderList.appendChild(reminderItem);
        } else {
            console.error('Element with class "reminder-list" not found.');
        }
    }

    window.completeReminder = function(reminderId) {
        fetch(`/complete_reminder/${reminderId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                loadReminders(); // Refresh the list of reminders
            } else {
                response.json().then(data => {
                    alert(`Failed to mark reminder as completed: ${data.message}`);
                });
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Failed to mark reminder as completed. Please try again.');
        });
    };

    window.deleteReminder = function(reminderId) {
        fetch(`/delete_reminder/${reminderId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                loadReminders(); // Refresh the list of reminders
            } else {
                response.json().then(data => {
                    alert(`Failed to delete reminder: ${data.message}`);
                });
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Failed to delete reminder. Please try again.');
        });
    };
});


// notifications.js

// Function to show browser notifications
function showNotification(message) {
    if (Notification.permission === 'granted') {
        new Notification(message);
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                new Notification(message);
            }
        }).catch(error => {
            console.error('Notification permission request failed:', error);
        });
    }
}

// Function to clear local storage
function clearLocalStorage() {
    localStorage.clear();
    alert('All data cleared!');
    window.location.reload();
}

// Add event listeners on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // Adding event listener for the notify button
    const notifyButton = document.getElementById('notifyButton');
    if (notifyButton) {
        notifyButton.addEventListener('click', function() {
            showNotification('Time to drink water!');
        });
    }

    // Adding event listener for the clear data button
    const clearDataButton = document.getElementById('clearDataButton');
    if (clearDataButton) {
        clearDataButton.addEventListener('click', clearLocalStorage);
    }
});

// navToggle.js

document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navList = document.getElementById('navList');

    if (navToggle && navList) {
        navToggle.addEventListener('click', function() {
            const isExpanded = navToggle.getAttribute('aria-expanded') === 'true' || false;
            navToggle.setAttribute('aria-expanded', !isExpanded);
            navList.classList.toggle('active');
        });

        // Optional: Close the nav menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!navToggle.contains(event.target) && !navList.contains(event.target)) {
                navToggle.setAttribute('aria-expanded', 'false');
                navList.classList.remove('active');
            }
        });
    }
});


// auth.js 

document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            event.preventDefault();
            if (validateForm(signupForm)) {
                handleSignup(event);
            }
        });
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const logoutButton = document.getElementById('logout');
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }

    function validateForm(form) {
        let isValid = true;
        const email = form.elements['email'];
        const password = form.elements['password'];
        const passwordVerify = form.elements['passwordVerify'];

        if (email && !email.value.includes('@')) {
            isValid = false;
            email.setCustomValidity('Please enter a valid email address.');
        } else if (email) {
            email.setCustomValidity('');
        }

        if (password.value.length < 8) {
            isValid = false;
            password.setCustomValidity('Password must be at least 8 characters long.');
        } else {
            password.setCustomValidity('');
        }

        if (passwordVerify && password.value !== passwordVerify.value) {
            isValid = false;
            passwordVerify.setCustomValidity('Passwords do not match.');
        } else if (passwordVerify) {
            passwordVerify.setCustomValidity('');
        }

        return isValid;
    }

    function handleSignup(event) {
        event.preventDefault();
        const userData = {
            name: document.getElementById('name').value,
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            passwordVerify: document.getElementById('passwordVerify').value,
            birthday: document.getElementById('birthday').value,
            sex: document.getElementById('sex').value
        };

        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(userData).toString()
        }).then(response => {
            if (response.ok) {
                window.location.href = '/features'; // Redirect to features page
            } else {
                response.json().then(data => {
                    alert(`Signup failed: ${data.message}`);
                });
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Signup failed. Please try again.');
        });
    }

    function handleLogin(event) {
        event.preventDefault();

        const loginIdentity = document.getElementById('login_identity').value;
        const password = document.getElementById('password').value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ login_identity: loginIdentity, password: password })
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(data => {
                    throw new Error(data.message);
                });
            }
        }).then(data => {
            alert(data.message);
            if (data.message === "Login successful!") {
                window.location.href = '/features'; // Redirect to features page on successful login
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Failed to login. Please try again.');
        });
    }

    function handleLogout(event) {
        event.preventDefault(); // Prevent form from submitting
        fetch('/logout', {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                window.location.href = '/'; // Redirect to the home page
            } else {
                alert('Logout failed. Please try again.');
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Logout failed. Please try again.');
        });
    }
});

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