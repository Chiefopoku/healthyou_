

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
            body: new URLSearchParams(reminder)
        }).then(response => {
            if (response.ok) {
                loadReminders();
                document.getElementById('reminder-form').reset(); // Reset form fields
            } else {
                alert('Failed to set reminder. Please try again.');
            }
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
                <button onclick="deleteReminder(${reminder.id})" class="btn">Delete</button>
            `;
            reminderList.appendChild(reminderItem);
        } else {
            console.error('Element with class "reminder-list" not found.');
        }
    }

    function deleteReminder(reminderId) {
        fetch(`/delete_reminder/${reminderId}`, {
            method: 'DELETE'
        }).then(response => {
            if (response.ok) {
                loadReminders();
            } else {
                alert('Failed to delete reminder. Please try again.');
            }
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
            });
    }
});

//auth.js

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

        if (!email.value.includes('@')) {
            isValid = false;
            email.setCustomValidity('Please enter a valid email address.');
        } else {
            email.setCustomValidity('');
        }

        if (password.value.length <= 8) {
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
            body: new URLSearchParams(userData)
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
        const email = event.target.elements['email'].value;
        const password = event.target.elements['password'].value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        }).then(response => {
            if (response.ok) {
                window.location.href = '/features'; // Redirect to features page
            } else {
                alert('Login failed: Invalid email or password');
            }
        });
    }

    function handleLogout(event) {
        event.preventDefault(); // Prevent form from submitting
        fetch('/logout', {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                window.location.href = '/'; // Redirect to the home page
            }
        });
    }
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
    const navToggle = document.querySelector('.nav-toggle');
    const navList = document.querySelector('.nav-list');

    if (navToggle && navList) {
        navToggle.addEventListener('click', function() {
            navList.classList.toggle('active');
        });
    }
});
