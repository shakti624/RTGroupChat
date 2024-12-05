-- Table for storing user information
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL, 
    password TEXT NOT NULL, -- Store hashed passwords
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing chatrooms
CREATE TABLE chatrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL, -- Chatroom name
    description TEXT,          -- Optional description of the chatroom
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for managing user memberships in chatrooms (many-to-many relationship)
CREATE TABLE memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    chatroom_id INTEGER NOT NULL,
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE, -- delete cascade ensure deletion of parent deletes all children
    FOREIGN KEY (chatroom_id) REFERENCES chatrooms (id) ON DELETE CASCADE,
    UNIQUE (user_id, chatroom_id) -- Ensure a user can join a chatroom only once
);

-- Table for storing messages sent in chatrooms
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chatroom_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,           -- Message content
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chatroom_id) REFERENCES chatrooms (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
