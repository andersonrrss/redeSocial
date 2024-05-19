CREATE TABLE users (
        id                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        socket_id            TEXT DEFAULT NULL,
        nome                 VARCHAR(45) NOT NULL,
        email                VARCHAR(100) NOT NULL,
        senha_hash           VARCHAR(255) NOT NULL,
        profile_pic          TEXT NOT NULL DEFAULT '/images/profile/default.jpg',
        bio                  VARCHAR(150) DEFAULT 'Olá! Tudo bem?',
        followers_ids        TEXT,
        following_ids        TEXT,
        creation             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT unq_users_nome UNIQUE (nome),
        CONSTRAINT unq_users_email UNIQUE (email)
);

CREATE TABLE posts (
        id                   INTEGER NOT NULL PRIMARY KEY,
        user_id              INTEGER NOT NULL,
        content              VARCHAR(500) NOT NULL,
        image_path           TEXT,
        likes_ids            LONGTEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE comments (
        id                   INTEGER NOT NULL PRIMARY KEY,
        user_id              INTEGER NOT NULL,
        post_id              INTEGER NOT NULL,
        parent_id            INTEGER NOT NULL DEFAULT 0,
        content              VARCHAR(500),
        likes                INTEGER DEFAULT 0,
        timestamp            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (parent_id) REFERENCES comments(id)
);

CREATE TABLE messages (
        id                   INTEGER NOT NULL PRIMARY KEY,
        receiver_id          INTEGER NOT NULL,
        sender_id            INTEGER NOT NULL,
        message              TEXT,
        timestamp            DATETIME,
        view                 BOOLEAN DEFAULT 0, --Not Viewed
        parent_id            INTEGER DEFAULT 0,
        FOREIGN KEY (receiver_id) REFERENCES users(id),
        FOREIGN KEY (sender_id) REFERENCES users(id),
        FOREIGN KEY (parent_id) REFERENCES messages(id)
);

CREATE TABLE notifications (
        user_id              INTEGER NOT NULL,
        content              TEXT NOT NULL,
        notification_type    VARCHAR(50) NOT NULL,
        view                 BOOLEAN NOT NULL DEFAULT 0, --Not viewed
        timestamp            DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Criação de índices
CREATE INDEX idx_users_id ON users (id);
CREATE INDEX idx_user_socket_id ON users (socket_id);
CREATE INDEX idx_nome ON users (nome);
CREATE INDEX idx_email ON users (email);
CREATE INDEX idx_senha ON users (senha_hash);

CREATE INDEX idx_posts_id ON posts (id);
CREATE INDEX idx_posts_user_id ON posts (user_id);

CREATE INDEX idx_comments_id ON comments (id);
CREATE INDEX idx_comments_post_id ON comments (post_id);

CREATE INDEX idx_messages_id ON messages (id);
CREATE INDEX idx_messages_sender_id ON messages (sender_id);
CREATE INDEX idx_messages_receiver_id ON messages (receiver_id);

CREATE INDEX idx_notifications_user_id ON notifications (user_id);
