document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const loginInput = document.querySelector('input[type="login"]');
    const passwordInput = document.querySelectorAll('input[type="password"]');

    function isValidlogin(login) {
        return /^[a-zA-Z0-9]+$/.test(login);
    }

    function isPasswordStrong(password) {
        return password.length >= 8 && 
            /[a-zA-Z]/.test(password) && 
            /[0-9]/.test(password);
    }

    form.addEventListener('submit', (e) => {
        const errors = [];
        const loginErrorText = "Некорректный login."
        const passwordNotStrongError = "Пароль должен содержать минимум 8 символов, заглавную букву и цифру."
        const authorizationUrl = "http://127.0.0.1:8000/api_v1/sign_in/"
        
        let isValid = true;
        
        e.preventDefault();
        if (!isValidlogin(loginInput.value)) {
            errors.push(loginErrorText);
            isValid = false;
            loginInput.classList.add('error');
        } else {
            loginInput.classList.remove('error');
        }
        if (!isPasswordStrong(passwordInput[0].value)) {
            errors.push(passwordNotStrongError);
            isValid = false;
            passwordInput.forEach(input => input.classList.add('error'));
        }
        
        console.log(passwordInput[0].value);
        if (isValid) {
            const userData = {
                login: loginInput.value,
                password: passwordInput[0].value
            };
            console.log(userData.password);

            localStorage.setItem('user', JSON.stringify(userData));

            window.location.href = 'login.html';
            alert(userData);
            fetch(authorizationUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(responseError + response.statusText);
                }
                return response.json();
            })
            .then(data => console.log(data))
            .catch(error => console.error(responseError, error));

        } else {
            alert(errors.join('\n'));
        }
    });
});