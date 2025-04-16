document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const loginInput = document.querySelector('input[type="login"]');
    const passwordInputs = document.querySelectorAll('input[type="password"]');

    const loginError = document.createElement('div');
    const passwordError = document.createElement('div');
    const passwordMatchError = document.createElement('div');
    const conflictError = document.createElement('div');

    loginError.className = 'error-message';
    passwordError.className = 'error-message';
    passwordMatchError.className = 'error-message';
    conflictError.className = 'error-message';

    // Вставляем элементы ошибок в DOM
    loginInput.parentNode.insertBefore(loginError, loginInput.nextSibling);
    loginInput.parentNode.insertBefore(conflictError, loginError.nextSibling); // Конфликтная ошибка под логином
    passwordInputs[0].parentNode.insertBefore(passwordError, passwordInputs[0].nextSibling);
    passwordInputs[1].parentNode.insertBefore(passwordMatchError, passwordInputs[1].nextSibling);

    function isValidlogin(login) {
        return /^[a-zA-Z0-9]+$/.test(login) &&
            login.length >= 4 &&
            login.length <= 16;
    }

    function passwordsMatch() {
        return passwordInputs[0].value === passwordInputs[1].value;
    }

    function isPasswordStrong(password) {
        return password.length >= 8 && 
            password.length <= 128 &&
            /[a-zA-Z]/.test(password) && 
            /[0-9]/.test(password);
    }

    form.addEventListener('submit', (e) => {
        const errors = [];
        const loginErrorText = "Логин может содержать от 4 до 24 символов и состоять из латинских букв и цифр.";
        const passwordsNotMatchError = "Пароли не совпадают.";
        const passwordNotStrongError = "Пароль должен содержать минимум 8 символов, заглавную букву и цифру.";
        const responseError = "Произошла ошибка: ";
        const conflictErrorText = "Пользователь с таким логином уже существует.";
        const registrationUrl = "http://127.0.0.1:8000/api_v1/sign_up/";
        
        let isValid = true;
        
        e.preventDefault();
        
        loginError.textContent = '';
        passwordError.textContent = '';
        passwordMatchError.textContent = '';
        conflictError.textContent = '';
        
        if (!isValidlogin(loginInput.value)) {
            errors.push(loginErrorText);
            isValid = false;
            loginInput.classList.add('error');
            loginError.textContent = loginErrorText;
        } else {
            loginInput.classList.remove('error');
        }
        
        if (!passwordsMatch()) {
            errors.push(passwordsNotMatchError);
            isValid = false;
            passwordInputs.forEach(input => input.classList.add('error'));
            passwordMatchError.textContent = passwordsNotMatchError;
        } else {
            passwordInputs.forEach(input => input.classList.remove('error'));
        }
        
        if (!isPasswordStrong(passwordInputs[0].value)) {
            errors.push(passwordNotStrongError);
            isValid = false;
            passwordInputs.forEach(input => input.classList.add('error'));
            passwordError.textContent = passwordNotStrongError;
        }
        
        if (isValid) {
            const userData = {
                login: loginInput.value,
                password: passwordInputs[0].value
            };
            
            fetch(registrationUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 409) {
                        loginInput.classList.add('error');
                        conflictError.textContent = conflictErrorText;
                    }
                    throw new Error(responseError + response.statusText);
                }
                return response.json();
            })
            .then(data => console.log(data))
            .catch(error => console.error(responseError, error));
        }
    });
});
