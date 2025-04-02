document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const loginInput = document.querySelector('input[type="login"]');
    const passwordInputs = document.querySelectorAll('input[type="password"]');

    function isValidlogin(login) {
        return /^[a-zA-Z0-9]+$/.test(login);
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
        const loginErrorText = "Некорректный login."
        const passwordsNotMatchErorr = "Пароли не совпадают."
        const passwordNotStrongError = "Пароль должен содержать минимум 8 символов, заглавную букву и цифру."
        const responseError = "Произошла ошибка: "
        const registrationUrl = "http://127.0.0.1:8000/api_v1/sign_up/"
        
        let isValid = true;
        
        e.preventDefault();
        if (!isValidlogin(loginInput.value)) {
            errors.push(loginErrorText);
            isValid = false;
            loginInput.classList.add('error');
        } else {
            loginInput.classList.remove('error');
        }
        
        if (!passwordsMatch()) {
            errors.push(passwordsNotMatchErorr);
            isValid = false;
            passwordInputs.forEach(input => input.classList.add('error'));
        } else {
            passwordInputs.forEach(input => input.classList.remove('error'));
        }
        if (!isPasswordStrong(passwordInputs[0].value)) {
            errors.push(passwordNotStrongError);
            isValid = false;
            passwordInputs.forEach(input => input.classList.add('error'));
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