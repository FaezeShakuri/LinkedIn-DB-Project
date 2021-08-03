import sqlite3
from exeptions import *

conn = sqlite3.connect('linkedin.db')
curs = conn.cursor()


def create_birthday_notifications(day, month):
    curs.execute("""SELECT user_id FROM users, profiles
    WHERE users.profile_id = profiles.profile_id AND day = ? AND month = ?""", (day, month))
    bday_users = curs.fetchall()
    bday_users = [user[0] for user in bday_users]

    for bday_user in bday_users:
        curs.execute("""SELECT user_id FROM users WHERE EXISTS (SELECT network_id FROM networks
        WHERE user_id IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id) AND user_id != ? AND network_status = 1)""", (bday_user, bday_user))
        users = curs.fetchall()
        users = [user[0] for user in users]

        for user in users:
            curs.execute("SELECT email FROM users WHERE user_id = ?", (bday_user, ))
            email = curs.fetchone()[0]
            create_notification(user, 1, "Today is the birthday of " + str(email))


def send_view_profile_notification(user_id, target_id):
    # notification
    curs.execute("SELECT email FROM users WHERE user_id = ?", (user_id, ))
    email = curs.fetchone()[0]
    create_notification(target_id, 2, str(email)+" viewed your profile.")

def read_all_notifications(user_id):
    curs.execute("DELETE FROM notifications WHERE receiver_id = ?", (user_id, ))
    conn.commit()
    return

def get_user_id(email):
    curs.execute("SELECT user_id FROM users WHERE email = ?", (email, ))
    user_id = curs.fetchone()[0]
    return user_id

def get_post_email(post_id):
    curs.execute("""SELECT email FROM posts, users
    WHERE posts.sender_id = users.user_id AND post_id = ?""", (post_id, ))
    email = curs.fetchone()[0]
    return email

def get_user_posts(user_id):
    curs.execute("""SELECT post_id, email, content, repost_id FROM posts, users
    WHERE posts.sender_id = users.user_id AND posts.sender_id = ? ORDER BY post_id""", (user_id, ))
    user_posts = curs.fetchall()
    user_posts = [[post[0], post[1]+(" posted: " if post[3]==-1 else (" reposted from " + str(get_post_email(post[3]))) + ": ")+post[2]] for post in user_posts]

    return user_posts # [ [post_id, text], [post_id, text], ... ]

def create_post(user_id, content):
    curs.execute("INSERT INTO posts(content, sender_id, repost_id) VALUES (?, ?, -1)", (content, user_id))
    conn.commit()
    return

def share_post(user_id, post_id):
    curs.execute("SELECT content FROM posts WHERE post_id = ?", (post_id, ))
    content = curs.fetchone()[0]
    curs.execute("INSERT INTO posts(content, sender_id, repost_id) VALUES (?, ?, ?)", (content, user_id, post_id))
    conn.commit()
    return

def comment_on_post(user_id, post_id, content):
    curs.execute("INSERT INTO comments(post_id, sender_id, content, reply_id) VALUES (?, ?, ?, -1)", (post_id, user_id, content))
    conn.commit()

    # notification
    curs.execute("SELECT sender_id FROM posts WHERE post_id = ?", (post_id, ))
    target_id = curs.fetchone()[0]
    curs.execute("SELECT email FROM users WHERE user_id = ?", (user_id, ))
    email = curs.fetchone()[0]
    create_notification(target_id, 4, str(email)+" commented on your post.")
    return

def comment_on_comment(user_id, post_id, content, comment_id):
    curs.execute("SELECT comment_id FROM comments WHERE comment_id = ? AND reply_id != -1", (comment_id, ))
    if (len(curs.fetchall()) > 0):
        return
    curs.execute("INSERT INTO comments(post_id, sender_id, content, reply_id) VALUES (?, ?, ?, ?)", (post_id, user_id, content, comment_id))
    conn.commit()

    # notification
    curs.execute("SELECT sender_id FROM comments WHERE comment_id = ?", (comment_id, ))
    target_id = curs.fetchone()[0]
    curs.execute("SELECT email FROM users WHERE user_id = ?", (user_id, ))
    email = curs.fetchone()[0]
    create_notification(target_id, 5, str(email)+" replied to your comment.")
    return

def like_post(user_id, post_id):
    curs.execute("SELECT like_id FROM post_likes WHERE sender_id = ? AND post_id = ?", (user_id, post_id))
    if (len(curs.fetchall()) == 0):
        curs.execute("INSERT INTO post_likes(sender_id, post_id) VALUES (?, ?)", (user_id, post_id))
        conn.commit()

        # notification
        curs.execute("SELECT sender_id FROM posts WHERE post_id = ?", (post_id, ))
        target_id = curs.fetchone()[0]
        curs.execute("SELECT email FROM users WHERE user_id = ?", (user_id, ))
        email = curs.fetchone()[0]
        create_notification(target_id, 3, str(email)+" liked your post.")
    return

def like_comment(user_id, comment_id):
    curs.execute("SELECT like_id FROM comment_likes WHERE sender_id = ? AND comment_id = ?", (user_id, comment_id))
    if (len(curs.fetchall()) == 0):
        curs.execute("INSERT INTO comment_likes(sender_id, comment_id) VALUES (?, ?)", (user_id, comment_id))
        conn.commit()

        # notification
        curs.execute("SELECT sender_id FROM comments WHERE comment_id = ?", (comment_id, ))
        target_id = curs.fetchone()[0]
        curs.execute("SELECT email FROM users WHERE user_id = ?", (user_id, ))
        email = curs.fetchone()[0]
        create_notification(target_id, 5, str(email)+" liked your comment.")
    return

def get_number_of_post_likes(post_id):
    curs.execute("SELECT like_id FROM post_likes WHERE post_id = ?", (post_id, ))
    number_of_likes = len(curs.fetchall())
    return number_of_likes

def get_number_of_comment_likes(comment_id):
    curs.execute("SELECT like_id FROM comment_likes WHERE comment_id = ?", (comment_id, ))
    number_of_likes = len(curs.fetchall())
    return number_of_likes

def get_number_of_post_comments(post_id):
    curs.execute("SELECT comment_id FROM comments WHERE post_id = ?", (post_id, ))
    number_of_comments = len(curs.fetchall())
    return number_of_comments

def get_posts(user_id, network_posted_posts, network_liked_posts, network_commented_posts):

    curs.execute("""SELECT user_id FROM users WHERE user_id != ? AND EXISTS (SELECT network_id FROM networks
    WHERE user_id IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id) AND network_status=1)""", (user_id, user_id, ))
    network_users = curs.fetchall()
    network_users = tuple([user[0] for user in network_users])
    network_users_c = "(" + ", ".join(["?" for user in network_users]) + ")"

    network_posts = set()

    if (network_posted_posts):
        curs.execute(f"SELECT post_id FROM posts WHERE sender_id IN {network_users_c}", [user for user in network_users])
        network_posts = curs.fetchall()
        network_posts = set([user[0] for user in network_posts])

    if (network_liked_posts):
        curs.execute(f"""SELECT distinct(posts.post_id) FROM posts, post_likes
        WHERE posts.post_id = post_likes.post_id AND post_likes.sender_id IN {network_users_c}""", [user for user in network_users])
        network_liked_posts = curs.fetchall()
        network_liked_posts = set([user[0] for user in network_liked_posts])
        network_posts = network_posts.union(network_liked_posts)

    if (network_commented_posts):
        curs.execute(f"""SELECT distinct(posts.post_id) FROM posts, comments
        WHERE posts.post_id = comments.post_id AND comments.sender_id IN {network_users_c}""", [user for user in network_users])
        network_commented_posts = curs.fetchall()
        network_commented_posts = set([user[0] for user in network_commented_posts])
        network_posts = network_posts.union(network_commented_posts)


    network_posts = list(network_posts)
    network_posts_c = "(" + ", ".join(["?" for post in network_posts]) + ")"

    curs.execute(f"""SELECT post_id, email, content, repost_id FROM posts, users WHERE
    posts.sender_id = users.user_id AND post_id in {network_posts_c} ORDER BY post_id""", [user for user in network_posts])
    network_posts = curs.fetchall()
    network_posts = [[post[0], post[1]+(" posted: " if post[3]==-1 else (" reposted from " + str(get_post_email(post[3]))) + ": ")+post[2]] for post in network_posts]

    return network_posts # [ [post_id, text], [post_id, text], ... ]

def get_post_comments(post_id):
    curs.execute("""SELECT comment_id, email, content FROM comments, users
    WHERE users.user_id = comments.sender_id AND post_id = ? AND reply_id=-1 ORDER BY comment_id""", (post_id, ))
    comments = curs.fetchall()
    comments = [[comment[0], comment[1]+": "+comment[2]] for comment in comments]
    return comments # [ [comment_id, text], [comment_id, text], ... ]

def get_comment_comments(comment_id):
    curs.execute("""SELECT comment_id, email, content FROM comments, users
    WHERE users.user_id = comments.sender_id AND reply_id=? ORDER BY comment_id""", (comment_id, ))
    comments = curs.fetchall()
    comments = [[comment[0], comment[1]+": "+comment[2]] for comment in comments]
    return comments # [ [comment_id, text], [comment_id, text], ... ]


def create_notification(receiver_id, notification_type, content):
    curs.execute("INSERT INTO notifications(notification_type, content, receiver_id) VALUES (?, ?, ?)", (notification_type, content, receiver_id))
    conn.commit()
    return

def get_notifications(user_id):
    curs.execute("SELECT notification_type, content FROM notifications WHERE receiver_id = ? ORDER BY notification_id", (user_id, ))
    notifications = curs.fetchall()
    notifications = [list(notification) for notification in notifications]
    return notifications # [ [notification_type, text], [notification_type, text], ... ]


def get_conversation_id(user_id, target_email):
    curs.execute("SELECT user_id FROM users WHERE email = ?", (target_email, ))
    target_id = curs.fetchone()[0]

    curs.execute("""SELECT conversation_id FROM conversations
    WHERE ? IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id)""", (user_id, target_id))
    conversation_id = curs.fetchone()[0]

    return conversation_id

def create_conversation(user_id, target_email):
    curs.execute("SELECT user_id FROM users WHERE email = ?", (target_email, ))
    target_id = curs.fetchone()[0]

    curs.execute("""SELECT conversation_id FROM conversations
    WHERE ? IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id)""", (user_id, target_id))

    if (len(curs.fetchall()) > 0):
        raise ConversationAlreadyExists()
    else:
        curs.execute("INSERT INTO conversations(sender_id, receiver_id) VALUES (?, ?)", (user_id, target_id))
        conn.commit()
    return

def get_conversations(user_id):
    curs.execute("""SELECT email FROM users WHERE user_id != ? AND EXISTS (SELECT conversation_id FROM conversations
    WHERE user_id IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id))""", (user_id, user_id, ))
    emails = curs.fetchall()
    emails = [email[0] for email in emails]
    return emails

def get_network_users_with_no_conversation(user_id):

    curs.execute("""SELECT email FROM users WHERE user_id != ? AND EXISTS (SELECT network_id FROM networks
    WHERE user_id IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id) AND network_status=1)""", (user_id, user_id, ))
    emails = curs.fetchall()
    network_users = set([email[0] for email in emails])

    other_users = set(get_conversations(user_id))

    user_emails = list(network_users.difference(other_users))

    return user_emails

def send_message(user_id, conversation_id, text):
    curs.execute("INSERT INTO messages(content, sender_id, conversation_id) VALUES (?, ?, ?)", (text, user_id, conversation_id))
    conn.commit()
    return

def get_messages(conversation_id):
    curs.execute("SELECT sender_id, content FROM messages WHERE conversation_id = ? ORDER BY message_id", (conversation_id, ))
    contents = curs.fetchall()

    messages = []

    for content in contents:
        curs.execute("SELECT email FROM users WHERE user_id=?", (content[0], ))
        email = curs.fetchone()[0]
        messages.append(email + ": " + content[1])

    return messages

def get_user_name(email):
    curs.execute("SELECT first_name, last_name FROM users, profiles WHERE users.profile_id = profiles.profile_id and email = ?", (email, ))
    name = curs.fetchone()
    name = (str(name[0]) + " " + str(name[1]))
    return name

def get_users(user_id, country, langs, company, first_name, last_name):
    curs.execute("SELECT email FROM users WHERE user_id != ?", (user_id, ))
    qualified_users = curs.fetchall()
    qualified_users = set([x[0] for x in qualified_users])

    # filter by country
    if (country != None):
        curs.execute("SELECT email FROM users, profiles WHERE users.profile_id = profiles.profile_id and country = ?", (country, ))
        country_users = curs.fetchall()
        country_users = set([x[0] for x in country_users])
        qualified_users = qualified_users.intersection(country_users)

    # filter by supported language
    curs.execute("""SELECT email FROM users, profiles, language_supports WHERE users.profile_id = profiles.profile_id
    AND profiles.language_support_id = language_supports.language_support_id AND
    ((support_persian=1 AND ?=1) OR (support_english=1 AND ?=1) OR (support_chinese=1 AND ?=1) OR (support_russian=1 AND ?=1) OR
    (support_german=1 AND ?=1) OR (support_french=1 AND ?=1) OR (support_japanese=1 AND ?=1) OR (support_italian=1 AND ?=1))""",
                 [langs[i] for i in range(0, 8)])
    temp_users = curs.fetchall()
    lang_users = set([x[0] for x in temp_users])
    qualified_users = qualified_users.intersection(lang_users)

    # filter by company name
    if (company != ""):
        curs.execute("SELECT email FROM users, profiles WHERE users.profile_id = profiles.profile_id and company = ?", (company, ))
        company_users = curs.fetchall()
        company_users = set([x[0] for x in company_users])
        qualified_users = qualified_users.intersection(company_users)

    # filter by company name
    if (first_name != ""):

        curs.execute("SELECT email FROM users, profiles WHERE users.profile_id = profiles.profile_id and first_name = ?", (first_name, ))
        first_name_users = curs.fetchall()
        first_name_users = set([x[0] for x in first_name_users])
        qualified_users = qualified_users.intersection(first_name_users)

    # filter by company name
    if (last_name != ""):
        curs.execute("SELECT email FROM users, profiles WHERE users.profile_id = profiles.profile_id and last_name = ?", (last_name, ))
        last_name_users = curs.fetchall()
        last_name_users = set([x[0] for x in last_name_users])
        qualified_users = qualified_users.intersection(last_name_users)

    qualified_users = list(qualified_users)
    qualified_users = [[email, get_number_of_mutural_friends(user_id, email)] for email in qualified_users]
    qualified_users.sort(key=lambda x:x[1], reverse=True)
    qualified_users = [[user[0], get_user_name(user[0])] for user in qualified_users]
    if (len(qualified_users) == 0):
        pass
    else:
        return qualified_users # [ [email, full_name], [email, full_name], ... ]


def send_invitation(sender_id, receiver_email):
    curs.execute("SELECT * FROM users WHERE email = ?", (receiver_email, ))
    receivers = curs.fetchall()
    if len(receivers) == 0:
        raise InvitationErrorInvalidEmail()

    else:
        receiver_id = receivers[0][0]

        curs.execute("""SELECT * FROM networks
        WHERE ? IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id) AND network_status=1""", (sender_id, receiver_id))
        if (len(curs.fetchall()) > 0):
            raise InvitationErrorAlreadyFollow()

        curs.execute("""SELECT * FROM networks
        WHERE ? IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id) AND network_status=0""", (sender_id, receiver_id))
        if (len(curs.fetchall()) > 0):
            raise InvitationErrorAlreadySent()

        curs.execute("INSERT INTO networks(sender_id, receiver_id, network_status) VALUES (?, ?, 0)", (sender_id, receiver_id))
        conn.commit()
    return

def get_invitations(user_id):
    curs.execute("SELECT sender_id FROM networks WHERE receiver_id = ? AND network_status=0", (user_id, ))
    list_of_invitations = curs.fetchall()
    list_of_emails = []
    for invitaiton in list_of_invitations:
        curs.execute("SELECT email FROM users WHERE user_id = ?", (invitaiton[0], ))
        email = curs.fetchone()[0]
        list_of_emails.append(email)
    return list_of_emails

def decline_invitation(sender_email, receiver_id):
    curs.execute("SELECT * FROM users WHERE email = ?", (sender_email, ))
    sender_id = curs.fetchall()[0][0]
    curs.execute("DELETE FROM networks WHERE sender_id=? and receiver_id=?", (sender_id, receiver_id))
    conn.commit()
    return

def accept_invitation(sender_email, receiver_id):
    curs.execute("SELECT * FROM users WHERE email = ?", (sender_email, ))
    sender_id = curs.fetchall()[0][0]
    curs.execute("UPDATE networks SET network_status=1 WHERE sender_id=? AND receiver_id=?", (sender_id, receiver_id))
    conn.commit()
    return


def get_people_you_may_know(user_id):

    emails = []

    curs.execute("SELECT * FROM users")
    qualified_users = curs.fetchall()
    for user in qualified_users:
        if user[0] != user_id:
            curs.execute("SELECT * FROM networks WHERE ? IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id)", (user_id, user[0]))
            if len(curs.fetchall()) > 0:
                continue
            if get_number_of_mutural_friends(user_id, user[1]) > 0:
                emails.append(user[1])

    return emails

def get_number_of_mutural_friends(user_id, target_email):

    curs.execute("SELECT user_id FROM users WHERE email = ?", (target_email, ))
    target_id = curs.fetchone()[0]

    curs.execute("""SELECT count(user_id) FROM users WHERE
    EXISTS (SELECT network_id FROM networks WHERE user_id IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id) AND user_id != ? AND network_status=1) AND
    EXISTS (SELECT network_id FROM networks WHERE user_id IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id) AND user_id != ? AND network_status=1)""",
    (user_id, user_id, target_id, target_id))
    number_of_mutural_friends = curs.fetchone()[0]

    return number_of_mutural_friends


def get_information(user_id):
    curs.execute("SELECT * FROM profiles WHERE profile_id = (SELECT profile_id from users WHERE user_id = ?)", (user_id,))
    information = curs.fetchone()
    curs.execute("""SELECT * FROM language_supports WHERE language_support_id = (SELECT language_support_id from profiles
    WHERE profile_id = (SELECT profile_id from users WHERE user_id = ?))""", (user_id,))
    language_supports = curs.fetchone()

    intro = information[7]
    about = information[8]
    featured = information[9]
    background = information[10]
    accomplishments = information[11]
    additional_information = information[12]
    job_status = information[13]
    company = information[14]
    skills = information[15]
    supported_languages = [language_supports[i] for i in range(1, 9)]

    return [intro, about, featured, background, accomplishments, additional_information, supported_languages, job_status, company, skills]

def edit_information(user_id, intro, about, featured, background, accomplishments, additional_information, langs, job_status, company, skills):

    curs.execute("SELECT job_status FROM users, profiles WHERE users.profile_id = profiles.profile_id AND user_id = ?", (user_id,))
    prev_job_status = curs.fetchone()[0]

    curs.execute(""" UPDATE language_supports set support_persian=?, support_english=?, support_chinese=?, support_russian=?,
    support_german=?, support_french=?, support_japanese=?, support_italian=?
    WHERE language_support_id = (SELECT language_support_id from profiles WHERE profile_id = (SELECT profile_id from users WHERE user_id = ?))""",
    (langs[0], langs[1], langs[2], langs[3], langs[4], langs[5], langs[6], langs[7], user_id))

    curs.execute(""" UPDATE profiles set intro=?, about=?, featured=?, background=?, accomplishments=?, additional_information=?, job_status=?, company=?, skills=?
    WHERE profile_id = (SELECT profile_id from users WHERE user_id = ?)""",
    (intro, about, featured, background, accomplishments, additional_information, job_status, company, skills, user_id))
    conn.commit()

    # notification
    if (prev_job_status != job_status):

        curs.execute("""SELECT user_id FROM users WHERE EXISTS (SELECT network_id FROM networks
        WHERE user_id IN (sender_id, receiver_id) AND ? IN (sender_id, receiver_id) AND user_id != ? AND network_status = 1)""", (user_id, user_id))
        users = curs.fetchall()
        users = [user[0] for user in users]

        for user in users:
            curs.execute("SELECT email FROM users WHERE user_id = ?", (user_id, ))
            email = curs.fetchone()[0]
            create_notification(user, 7, str(email)+" changed his/her job status.")

    return


def sign_up(email, password, confirm_pass, first_name, last_name, day, month, year, country):

    if (password != confirm_pass):
        raise SignupErrorPassword()

    curs.execute("SELECT * FROM users WHERE email = ?", (email,))
    if len(curs.fetchall()) > 0:
        # email has been used
        raise SignupErrorEmail()
    else:
        # signed up
        curs.execute("""INSERT INTO language_supports(support_persian, support_english, support_chinese, support_russian,
        support_german, support_french, support_japanese, support_italian)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (True, False, False, False, False, False, False, False))
        curs.execute("SELECT language_support_id FROM language_supports")
        language_support_id = curs.fetchall()[-1][0]

        curs.execute("""INSERT INTO profiles(first_name, last_name, day, month, year, country,
        intro, about, featured, background, accomplishments, additional_information, job_status, company, skills, language_support_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (first_name, last_name, day, month, year, country, "", "", "", "", "", "", "", "", "", language_support_id))
        curs.execute("SELECT profile_id FROM profiles")
        profile_id = curs.fetchall()[-1][0]

        curs.execute("INSERT INTO users(email, password, profile_id) VALUES (?, ?, ?)", (email, password, profile_id))
        conn.commit()

        # return user_id
        curs.execute("SELECT user_id FROM users")
        return curs.fetchall()[-1][0]

def login(email, password):

    curs.execute("SELECT * FROM users WHERE email = ?", (email,))
    accounts = curs.fetchall()

    if len(accounts) <= 0:
        # there is no account with this email
        raise LoginError("Invalid email")

    else:
        pw = accounts[0][2]
        if pw != password:
            # wrong password
            raise LoginError()

        else:
            # logged in
            # return user_id
            return accounts[0][0]
