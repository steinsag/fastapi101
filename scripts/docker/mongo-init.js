// This script runs automatically on first container startup.
// It creates a non-admin user "test" with password "test" on the database "test".

// The official image runs this with the root user specified via MONGO_INITDB_ROOT_USERNAME/PASSWORD.

// Connect to the "test" database and create the application user.
db = db.getSiblingDB('test');

db.createUser({
  user: 'test',
  pwd: 'test',
  roles: [
    { role: 'readWrite', db: 'test' }
  ]
});

print('Initialized MongoDB: created user "test" with readWrite on db "test"');
