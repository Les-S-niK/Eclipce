export async function importPublicKey(pem) {
    const pemHeader = "-----BEGIN PUBLIC KEY-----";
    const pemFooter = "-----END PUBLIC KEY-----";
    const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
    const binaryDerString = window.atob(pemContents.replace(/\s+/g, ''));
    const binaryDer = new Uint8Array(binaryDerString.length);
    for (let i = 0; i < binaryDerString.length; i++) {
        binaryDer[i] = binaryDerString.charCodeAt(i);
    }
    return await window.crypto.subtle.importKey(
        "spki",
        binaryDer.buffer,
        {
            name: "RSA-OAEP",
            hash: "SHA-256"
        },
        false,
        ["encrypt"]
    );
}

export async function generateAESKey() {
    return await window.crypto.subtle.generateKey(
        {
            name: "AES-CBC",
            length: 256,
        },
        true,
        ["encrypt", "decrypt"]
    );
}

export async function exportAESKey(key) {
    return await window.crypto.subtle.exportKey("raw", key);
}

export async function encryptWithAES(key, iv, data) {
    const encoder = new TextEncoder();
    const dataBytes = encoder.encode(data);
    return await window.crypto.subtle.encrypt(
        { name: "AES-CBC", iv },
        key,
        dataBytes
    );
}

export async function decryptWithAES(key, iv, encryptedData) {
    try {
        const decrypted = await window.crypto.subtle.decrypt(
            { name: "AES-CBC", iv },
            key,
            encryptedData
        );
        return new TextDecoder().decode(decrypted);
    } catch (error) {
        console.error("Decryption error:", error);
        throw error;
    }
}

export async function getAESKeyFromStorage() {
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

export function base64ToArrayBuffer(base64) {
    const binaryString = atob(base64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
}

export function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

export async function encryptDataForServer(publicKeyPem, data) {
    const cryptoKey = await importPublicKey(publicKeyPem);
    const aesKey = await generateAESKey();
    const rawAESKey = await exportAESKey(aesKey);
    const iv = window.crypto.getRandomValues(new Uint8Array(16));
    
    const combined = new Uint8Array(rawAESKey.byteLength + iv.byteLength);
    combined.set(new Uint8Array(rawAESKey), 0);
    combined.set(iv, rawAESKey.byteLength);
    
    const encryptedKey = await window.crypto.subtle.encrypt(
        { name: "RSA-OAEP" },
        cryptoKey,
        combined
    );
    
    const encryptedData = await encryptWithAES(aesKey, iv, data);
    
    return {
        encryptedKey: arrayBufferToBase64(encryptedKey),
        encryptedData: arrayBufferToBase64(encryptedData),
        iv: arrayBufferToBase64(iv)
    };
}