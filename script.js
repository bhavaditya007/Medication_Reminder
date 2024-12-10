document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get login credentials
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Send login request to backend
    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Login successful, show reminder form
            document.getElementById('reminderForm').style.display = 'block';
            userId = data.user_id;  // Store user ID for reminder setting
            alert('Login Successful!');
        } else {
            alert('Login Failed!');
        }
    })
    .catch(error => alert('Error: ' + error));
});

document.getElementById('setReminderButton').addEventListener('click', function() {
    const medication = document.getElementById('medication').value;
    const reminderTime = document.getElementById('reminderTime').value;
    const sound = document.getElementById('sound').value;

    // Send reminder data to backend
    fetch('/set-reminder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ medication, reminderTime, sound, user_id: userId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Reminder set successfully!") {
            alert('Reminder has been set!');
            checkReminderTime(reminderTime, sound);
        }
    })
    .catch(error => alert('Error: ' + error));
});

document.getElementById('viewRemindersButton').addEventListener('click', function() {
    // Fetch stored reminders for the user
    fetch(`/get-reminders?user_id=${userId}`)
    .then(response => response.json())
    .then(reminders => {
        const remindersList = document.getElementById('remindersList');
        remindersList.innerHTML = '';
        reminders.forEach(reminder => {
            const li = document.createElement('li');
            li.textContent = `${reminder.medication} at ${reminder.reminder_time} (Sound: ${reminder.sound})`;
            remindersList.appendChild(li);
        });
    });
});

function playSound(sound) {
    let audio;
    if (sound === 'beep') {
        audio = new Audio('beep_sound.mp3');  // Replace with your own beep sound file
    } else if (sound === 'alert') {
        audio = new Audio('alert_sound.mp3'); // Replace with your own alert sound file
    } else if (sound === 'chime') {
        audio = new Audio('chime_sound.mp3'); // Replace with your own chime sound file
    }
    audio.play();
}

function showNotification(medication) {
    if (Notification.permission === "granted") {
        new Notification("Medication Reminder", {
            body: `It's time to take your medication: ${medication}`,
            icon: "medication_icon.png" // Optional: add an icon for the notification
        });
    }
}

function checkReminderTime(reminderTime, sound) {
    const reminderDate = new Date(reminderTime);
    const currentDate = new Date();

    const timeDifference = reminderDate - currentDate;

    if (timeDifference <= 0) {
        alert('The reminder time has already passed!');
        return;
    }

    setTimeout(function() {
        showNotification("Your Medication"); // Display notification
        playSound(sound); // Play the selected sound
    }, timeDifference); // Set reminder at the correct time
}

// Request notification permission when the page loads
if (Notification.permission !== "granted") {
    Notification.requestPermission();
}
