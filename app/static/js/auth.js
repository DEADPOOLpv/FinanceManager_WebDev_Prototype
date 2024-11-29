// Signup Event Listener
document.getElementById('signupSubmitBtn').addEventListener('click', async (event) => {
    event.preventDefault();  // Prevent the form from submitting normally
    const username = document.getElementById('signupUsername').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;

    const data = {
        username: username,
        email: email,
        password: password,
        confirm_password: confirmPassword
    };

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || 'Signup successful');
            window.location.href = '/login';
        } else {
            alert(result.message || 'Signup failed');
        }
    } catch (error) {
        console.error('Error during signup:', error);
        alert('An error occurred. Please try again.');
    }
});

// Login Event Listener
document.getElementById('loginSubmitBtn').addEventListener('click', async (event) => {
    event.preventDefault();  // Prevent the form from submitting normally
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const data = {
        username: username,
        password: password
    };

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || 'Login successful');
            window.location.href = homepageUrl;
        } else {
            alert(result.message || 'Login failed');
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again.');
    }
});

