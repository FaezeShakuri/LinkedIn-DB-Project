import sqlite3

conn = sqlite3.connect('linkedin.db')
curs = conn.cursor()

curs.execute(""" CREATE TABLE users (
                user_id integer PRIMARY KEY AUTOINCREMENT,
                email text NOT NULL,
                password text NOT NULL,
                profile_id integer NOT NULL,

                FOREIGN KEY (profile_id) REFERENCES profiles (profile_id)
                ) """)

curs.execute(""" CREATE TABLE profiles (
                profile_id integer PRIMARY KEY AUTOINCREMENT,
                first_name text NOT NULL,
                last_name text NOT NULL,
                day int NOT NULL,
                month int NOT NULL,
                year int NOT NULL,
                country text NOT NULL,
                intro text NOT NULL,
                about text NOT NULL,
                featured text NOT NULL,
                background text NOT NULL,
                accomplishments text NOT NULL,
                additional_information text NOT NULL,
                job_status text NOT NULL,
                company text NOT NULL,
                skills text NOT NULL,
                language_support_id integer NOT NULL,

                FOREIGN KEY (language_support_id) REFERENCES language_supports (language_support_id)
                ) """)

curs.execute(""" CREATE TABLE language_supports (
                language_support_id integer PRIMARY KEY AUTOINCREMENT,
                support_persian integer NOT NULL,
                support_english integer NOT NULL,
                support_chinese integer NOT NULL,
                support_russian integer NOT NULL,
                support_german integer NOT NULL,
                support_french integer NOT NULL,
                support_japanese integer NOT NULL,
                support_italian integer NOT NULL
                ) """)

curs.execute(""" CREATE TABLE networks (
                network_id integer PRIMARY KEY AUTOINCREMENT,
                sender_id integer NOT NULL,
                receiver_id integer NOT NULL,
                network_status integer NOT NULL,

                FOREIGN KEY (sender_id) REFERENCES users (user_id)
                FOREIGN KEY (receiver_id) REFERENCES users (user_id)
                ) """)

curs.execute(""" CREATE TABLE conversations (
                conversation_id integer PRIMARY KEY AUTOINCREMENT,
                sender_id integer NOT NULL,
                receiver_id integer NOT NULL,

                FOREIGN KEY (sender_id) REFERENCES users (user_id)
                FOREIGN KEY (receiver_id) REFERENCES users (user_id)
                ) """)

curs.execute(""" CREATE TABLE messages (
                message_id integer PRIMARY KEY AUTOINCREMENT,
                content text NOT NULL,
                sender_id integer NOT NULL,
                conversation_id integer NOT NULL,

                FOREIGN KEY (sender_id) REFERENCES users (user_id)
                FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
                ) """)

curs.execute(""" CREATE TABLE posts (
                post_id integer PRIMARY KEY AUTOINCREMENT,
                content text NOT NULL,
                sender_id integer NOT NULL,
                repost_id integer NOT NULL,

                FOREIGN KEY (sender_id) REFERENCES users (user_id)
                FOREIGN KEY (repost_id) REFERENCES posts (post_id)
                ) """)

curs.execute(""" CREATE TABLE comments (
                comment_id integer PRIMARY KEY AUTOINCREMENT,
                post_id integer NOT NULL,
                sender_id integer NOT NULL,
                content text NOT NULL,
                reply_id integer NOT NULL,

                FOREIGN KEY (sender_id) REFERENCES users (user_id)
                FOREIGN KEY (reply_id) REFERENCES comments (comment_id)
                FOREIGN KEY (post_id) REFERENCES posts (post_id)
                ) """)

curs.execute(""" CREATE TABLE post_likes (
                like_id integer PRIMARY KEY AUTOINCREMENT,
                sender_id integer NOT NULL,
                post_id integer NOT NULL,

                FOREIGN KEY (sender_id) REFERENCES users (user_id)
                FOREIGN KEY (post_id) REFERENCES posts (post_id)
                ) """)

curs.execute(""" CREATE TABLE comment_likes (
                like_id integer PRIMARY KEY AUTOINCREMENT,
                sender_id integer NOT NULL,
                comment_id integer NOT NULL,

                FOREIGN KEY (sender_id) REFERENCES users (user_id)
                FOREIGN KEY (comment_id) REFERENCES comments (comment_id)
                ) """)

curs.execute(""" CREATE TABLE notifications (
                notification_id integer PRIMARY KEY AUTOINCREMENT,
                notification_type integer NOT NULL,
                content integer NOT NULL,
                receiver_id integer NOT NULL,

                FOREIGN KEY (receiver_id) REFERENCES users (receiver_id)
                ) """)


conn.commit()
conn.close()
