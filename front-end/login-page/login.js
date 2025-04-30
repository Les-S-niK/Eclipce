import {
    importPublicKey,
    generateAESKey,
    exportAESKey,
    encryptWithAES,
    decryptWithAES,
    base64ToArrayBuffer,
    arrayBufferToBase64,
    importAESKey,
} from '../encrypting.js';

import {
    getCookie
} from "../utils.js"

document.addEventListener('DOMContentLoaded', async () => {
    const form = document.querySelector('form');
    const loginInput = document.querySelector('input[type="login"]');
    const passwordInput = document.querySelector('input[type="password"]');

    const loginError = document.createElement('div');
    const passwordError = document.createElement('div');

    loginError.className = 'error-message';
    passwordError.className = 'error-message';

    loginInput.parentNode.insertBefore(loginError, loginInput.nextSibling);
    passwordInput.parentNode.insertBefore(passwordError, passwordInput.nextSibling);

    const responseError = "Произошла ошибка: ";
    const authErrorText = "Не удалось авторизовать пользователя. Проверьте правильность пароля и логина.";
    const validationErrorText = "Переданы недопустимые данные. Проверьте длину логина и пароля, а также их содержимое.";
    const authorizationUrl = "http://127.0.0.1:8080/api_v1/sign_in/";
    const createAsymKeysUrl = "http://0.0.0.0:8080/api_v1/keys/asym_keys/create/";
    const sendAESKeyUrl = "http://0.0.0.0:8080/api_v1/keys/sym_key/save/";
    const refreshUrl = "http://0.0.0.0:8080/api_v1/token_auth/refresh/";

    async function getRSAKey() {
        try {
            const response = await fetch(createAsymKeysUrl, {
                method: "GET", 
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            let serverPublicKey = data.public_key;
            let serverKeysId = data.keys_id;
            let keyId = crypto.randomUUID();
            sessionStorage.setItem("symmetric_key_id", keyId);

            return [serverPublicKey, serverKeysId, keyId];
        } catch (error) {
            console.error("Can't get the public key.");
            return;
        }
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

    async function encryptAndSendAES(serverPublicKeyPem, serverKeysId, keyId) {
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
            sessionStorage.setItem("symmetric_key_iv", arrayBufferToBase64(iv));
            sessionStorage.setItem("symmetric_key", arrayBufferToBase64(rawAESKey));

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
        } catch (error) {
            console.error("Encoding error.", error);
        }
    }

    async function decryptUserRefreshToken() {
        const refreshEncryptedToken = localStorage.getItem("refresh_token");
        const symmetricKeyId = localStorage.getItem("symmetric_key_id");
        
        if (refreshEncryptedToken) {
            try {
                const refreshResponse = await fetch(refreshUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${refreshEncryptedToken}`
                    },
                    body: JSON.stringify({
                        key_id: symmetricKeyId,
                    })
                });
                
                if (refreshResponse.ok) {
                    const jsonResponse = await refreshResponse.json();
                    const accessToken = jsonResponse.access_token;
                    
                    if (accessToken) {
                        sessionStorage.setItem("access_token", accessToken);
                        // window.location.href = "iLoveDicks.cum"
                    }
                }
            } catch (error) {
                console.error("Error refreshing token:", error);
            }
        }
    }

    const RSAKeyData = await getRSAKey();
    await encryptAndSendAES(
        RSAKeyData[0],
        RSAKeyData[1],
        RSAKeyData[2]
    );
    await decryptUserRefreshToken();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        loginError.textContent = '';
        passwordError.textContent = '';

        try {
            const rawKey = base64ToArrayBuffer(sessionStorage.getItem("symmetric_key"));
            const aesKey = await importAESKey(rawKey);
            const iv = base64ToArrayBuffer(sessionStorage.getItem("symmetric_key_iv"));
            
            const encryptedUserLogin = await encryptWithAES(aesKey, iv, loginInput.value);
            const encryptedUserPassword = await encryptWithAES(aesKey, iv, passwordInput.value);
            const keyId = sessionStorage.getItem("symmetric_key_id");

            const dataToSend = {
                encrypted_login: arrayBufferToBase64(encryptedUserLogin),
                encrypted_password: arrayBufferToBase64(encryptedUserPassword),
                key_id: keyId
            };

            const response = await fetch(authorizationUrl, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend)
            });

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
                
                const tokenResponse = await response.json();
                const accessToken = tokenResponse.access_token;
                const refreshEncryptedToken = tokenResponse.refresh_token;
                
                sessionStorage.setItem("access_token", accessToken);
                localStorage.setItem("refresh_token", refreshEncryptedToken);
                localStorage.setItem("symmetric_key_id", keyId);
                
                // window.location.href = "iLoveDicks.cum"
            }
        } catch (error) {
            console.error(responseError + error);
        }
    });
});