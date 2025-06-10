
import { deriveKey, encrypt, decrypt } from './crypto';
import { IndexedDBWrapper } from './indexedDB';

const SCHEMA_VERSION = 1;
const USER_DB_NAME = 'userKnowledgeBase';

export class PersonalKnowledgeBase {
  private db: IndexedDBWrapper;
  private cryptoKey: CryptoKey | null = null;

  constructor(userId: string, imei: string, email: string) {
    this.db = new IndexedDBWrapper(`${USER_DB_NAME}_${userId}`, SCHEMA_VERSION);
    this.initializeCrypto(imei, email);
  }

  private async initializeCrypto(imei: string, email: string) {
    this.cryptoKey = await deriveKey(imei + email);
  }

  async addData(table: 'events'|'notes'|'context', data: any) {
    if (!this.cryptoKey) throw new Error('Crypto not initialized');
   
    const encrypted = await encrypt(this.cryptoKey, JSON.stringify(data));
    return this.db.put(table, encrypted);
  }

  async query(table: string, queryFn: (item: any) => boolean) {
    if (!this.cryptoKey) return [];
   
    const all = await this.db.getAll(table);
    return Promise.all(all.map(async (encrypted) => {
      const decrypted = await decrypt(this.cryptoKey!, encrypted);
      return JSON.parse(decrypted);
    })).then(data => data.filter(queryFn));
  }
}

// Initialize in main app component
export const initUserDB = (user: User) => {
  const knowledgeBase = new PersonalKnowledgeBase(
    user.id,
    user.imei,
    user.email
  );
 
  // Schema initialization
  knowledgeBase.db.createStore('events', 'id');
  knowledgeBase.db.createStore('notes', 'id');
  knowledgeBase.db.createStore('context', 'key');
 
  return knowledgeBase;
}; 
