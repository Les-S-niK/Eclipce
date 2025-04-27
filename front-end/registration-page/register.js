import {
    importPublicKey,
    generateAESKey,
    exportAESKey,
    encryptWithAES,
    decryptWithAES,
    base64ToArrayBuffer,
    arrayBufferToBase64
} from '../encrypting.js';

import {
    getCookie
} from "../utils.js"

document.addEventListener('DOMContentLoaded', async () => {
    async function decryptUserRefreshToken() {
        const refreshUrl = "http://0.0.0.0:8080/api_v1/token_auth/refresh/"
        const refreshEncryptedToken = localStorage.getItem("refresh_token")
        const symmetricKeyId = localStorage.getItem("symmetric_key_id")
        if (refreshEncryptedToken) {
            const refreshResponse = await fetch(refreshUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${refreshEncryptedToken}`
                },
                body: JSON.stringify({
                    key_id: symmetricKeyId,
                })
            })
            const jsonResponse = await refreshResponse.json()
            const accessToken = jsonResponse.access_token
            console.log(accessToken)
            if (accessToken){
                sessionStorage.setItem("access_token", accessToken)
                window.location.href = "iLoveDicks.cum"
            }
        }
    }
    await decryptUserRefreshToken()
    
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

    loginInput.parentNode.insertBefore(loginError, loginInput.nextSibling);
    loginInput.parentNode.insertBefore(conflictError, loginError.nextSibling);
    passwordInputs[0].parentNode.insertBefore(passwordError, passwordInputs[0].nextSibling);
    passwordInputs[1].parentNode.insertBefore(passwordMatchError, passwordInputs[1].nextSibling);

    function isValidlogin(login) {
        return /^[a-zA-Z0-9_-]+$/.test(login) &&
            login.length >= 4 &&
            login.length <= 24;
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

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errors = [];
        const loginErrorText = "Логин может содержать от 4 до 24 символов и состоять из латинских букв, цифр и \"_\" или \"-\" .";
        const passwordsNotMatchError = "Пароли не совпадают.";
        const passwordNotStrongError = "Пароль должен содержать минимум 8 символов, заглавную букву и цифру.";
        const responseError = "Произошла ошибка: ";
        const conflictErrorText = "Пользователь с таким логином уже существует.";
        const registrationUrl = "http://0.0.0.0:8080/api_v1/sign_up/";
        const createAsymKeysUrl = "http://0.0.0.0:8080/api_v1/keys/asym_keys/create/";
        const sendAESKeyUrl = "http://0.0.0.0:8080/api_v1/keys/sym_key/save/";

        let isValid = true;
        
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
            let serverPublicKey = sessionStorage.getItem("server_public_key");
            let serverKeysId = sessionStorage.getItem("server_keys_id")
            let keyId = sessionStorage.getItem("symmetric_key_id")

            if (!serverPublicKey || !serverKeysId || !keyId) {
                try {
                    const response = await fetch(createAsymKeysUrl, {
                        method: "GET", 
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    const data = await response.json();
                    serverPublicKey = data.public_key;
                    serverKeysId = data.keys_id;
                    keyId = crypto.randomUUID();

                    sessionStorage.setItem("server_public_key", serverPublicKey);
                    sessionStorage.setItem("server_keys_id", serverKeysId);
                    sessionStorage.setItem("symmetric_key_id", keyId)
                } catch (error) {
                    console.error("Can't get the public key.");
                    return;
                }
            }
            await encryptAndSend(serverPublicKey, serverKeysId, keyId);
        }

        async function getAESKeyFromStorage() {
            try {
                const aesKeyBase64 = sessionStorage.getItem("symmetric_key");
                const ivBase64 = sessionStorage.getItem("symmetric_key_iv");
                
                if (!aesKeyBase64 || !ivBase64) return null;
                
                const rawKey = base64ToArrayBuffer(aesKeyBase64);
                const iv = base64ToArrayBuffer(ivBase64);
                
                const aesKey = await window.crypto.subtle.importKey(
                    "raw",
                    rawKey,
                    { name: "AES-CBC", length: 256 },
                    true,
                    ["encrypt", "decrypt"]
                );
                
                return { key: aesKey, iv };
            } catch (error) {
                console.error("Failed to load key:", error);
                return null;
            }
        }

        async function encryptAndSend(serverPublicKeyPem, serverKeysId, keyId) {
            try {
                const cryptoKey = await importPublicKey(serverPublicKeyPem);
                const aesKey = await generateAESKey();
                const rawAESKey = await exportAESKey(aesKey);
                const iv = window.crypto.getRandomValues(new Uint8Array(16));
                const combinedKeyAndIv = new Uint8Array(rawAESKey.byteLength + iv.byteLength);

                combinedKeyAndIv.set(new Uint8Array(rawAESKey), 0);
                combinedKeyAndIv.set(iv, rawAESKey.byteLength);
                
                const encryptedAESKeyAndIv = await window.crypto.subtle.encrypt(
                    { name: "RSA-OAEP" },
                    cryptoKey,
                    combinedKeyAndIv
                );
                
                sessionStorage.setItem("symmetric_key_iv", arrayBufferToBase64(iv))
                sessionStorage.setItem("symmetric_key", arrayBufferToBase64(rawAESKey))
                sessionStorage.removeItem("server_public_key")
                sessionStorage.removeItem("server_keys_id")

                const encryptedAESKeyBase64 = arrayBufferToBase64(encryptedAESKeyAndIv);
                await fetch(sendAESKeyUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        asym_keys_id: serverKeysId,
                        key_id: keyId,
                        sym_key: encryptedAESKeyBase64
                    })
                });

                const encryptedUserLogin = await encryptWithAES(aesKey, iv, loginInput.value);
                const encryptedUserPassword = await encryptWithAES(aesKey, iv, passwordInputs[0].value);
                
                const dataToSend = {
                    encrypted_login: arrayBufferToBase64(encryptedUserLogin),
                    encrypted_password: arrayBufferToBase64(encryptedUserPassword),
                    key_id: keyId
                };

                const response = await fetch(registrationUrl, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(dataToSend)
                });

                if (!response.ok) {
                    if (response.status === 409) {
                        loginInput.classList.add('error');
                        conflictError.textContent = conflictErrorText;
                    }
                    throw new Error(responseError + response.statusText);
                }
                const tokenResponse = await response.json()
                const accessToken = tokenResponse.access_token
                const refreshEncryptedToken = tokenResponse.refresh_token
                
                sessionStorage.setItem("access_token", accessToken)
                localStorage.setItem("refresh_token", refreshEncryptedToken)
                localStorage.setItem("symmetric_key_id", keyId)
                
                window.location.href = "iLoveDicks.cum"
            } catch (error) {
                console.error("Encoding error.", error);
            }
        }
    });
});