// This script can be run on first initialization and on subsequent starts.
// It ensures the application user exists and idempotently seeds the "items" collection.

// Connect to the "test" database.
db = db.getSiblingDB('test');

// Ensure app user exists
if (!db.getUser('test')) {
  db.createUser({
    user: 'test',
    pwd: 'test',
    roles: [
      { role: 'readWrite', db: 'test' }
    ]
  });
}

// Seed or update item with ObjectId _id
// Use upsert to ensure the document exists with expected fields
// Note: the API exposes this ID as a readable hex string
const seedId = ObjectId("507f1f77bcf86cd799439011");
db.items.updateOne(
  { _id: seedId },
  { $set: { name: 'Sample Item', price: 107.99 } },
  { upsert: true }
);

print('Mongo seed complete: ensured user "test" and upserted items["507f1f77bcf86cd799439011"]');
