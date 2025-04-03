document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const loginInput = document.querySelector('input[type="login"]');
    const passwordInput = document.querySelector('input[type="password"]');

    const loginError = document.createElement('div');
    const passwordError = document.createElement('div');

    loginError.className = 'error-message';
    passwordError.className = 'error-message';

    loginInput.parentNode.insertBefore(loginError, loginInput.nextSibling);
    passwordInput.parentNode.insertBefore(passwordError, passwordInput.nextSibling);

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const authorizationUrl = "http://127.0.0.1:8000/api_v1/sign_in/";
        const responseError = "Произошла ошибка: ";
        const authErrorText = "Не удалось авторизовать пользователя. Проверьте правильность пароля и логина.";
        const validationErrorText = "Переданы неверные данные. Пожалуйста, проверьте введенные данные.";

        loginError.textContent = '';
        passwordError.textContent = '';

        const userData = {
            login: loginInput.value,
            password: passwordInput.value
        };

        localStorage.setItem('user', JSON.stringify(userData));

        fetch(authorizationUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    loginInput.classList.add('error');
                    loginError.textContent = authErrorText;
                } else if (response.status === 422) {
                    loginInput.classList.add('error');
                    loginError.textContent = validationErrorText;
                }
                throw new Error(responseError + response.statusText);
            } else {
                loginInput.classList.remove("error");
            }
            return response.json();
        })
        .catch(error => console.error(responseError + error));
    });
});