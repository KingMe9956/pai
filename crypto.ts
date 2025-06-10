
export async function deriveKey(seed: string): Promise<CryptoKey> {
  return window.crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(seed),
    'PBKDF2',
    false,
    ['deriveKey']
  ).then(baseKey => {
    return window.crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: new Uint8Array(16),
        iterations: 600000,
        hash: 'SHA-512'
      },
      baseKey,
      { name: 'AES-GCM', length: 256 },
      true,
      ['encrypt', 'decrypt']
    );
  });
}

export async function encryptData(key: CryptoKey, data: string): Promise<{ iv: Uint8Array, data: ArrayBuffer }> {
  const iv = window.crypto.getRandomValues(new Uint8Array(12));
  const encoded = new TextEncoder().encode(data);
  return {
    iv,
    data: await window.crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      key,
      encoded
    )
  };
} 
