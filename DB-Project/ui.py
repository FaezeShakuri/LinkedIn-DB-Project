import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QDialog, QWidget

import server
import exeptions

from UI.ui_mainpage import Ui_MainWindow
from UI.login import Ui_Dialog_login
from UI.signup import Ui_Dialog_signup
from UI.profile import Ui_profile
from UI.my_network import Ui_myNetwork
from UI.other_profile import Ui_Dialog_Show_profile
from UI.user_search import Ui_Form_search_user
from UI.direct import Ui_Form_direct
from UI.chat import Ui_Dialog_chat
from UI.comment import Ui_Dialog_comment
from UI.my_post import Ui_Form_my_posts
from UI.notificatons import Ui_Dialog_notif

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, user_id, *args, **kwargs):
        self.w = None
        self.w2 = None
        self.user_id = user_id

        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Update home
        self.update_info()

        # refresh
        self.pushButton_refresh.clicked.connect(self.update_info)

        # Set current user
        self.label_current_user.setText("current user_id: " + str(self.user_id))

        # Log out
        self.actionlog_out.triggered.connect(self.log_out)

        # Profile
        self.actionEdit_profile.triggered.connect(self.edit_profile)

        # My network
        self.actionMy_network.triggered.connect(self.my_network_window)

        # User search
        self.actionSearch_user.triggered.connect(self.user_search)

        # Direct
        self.actionDirect.triggered.connect(self.show_direct)

        # My post
        self.actionMy_Post.triggered.connect(self.my_post)

        # Notification
        self.actionShow.triggered.connect(self.notif)

        # information on homepage
        # show comments
        self.pushButton_show_comments.clicked.connect(self.show_comments)
        self.pushButton_show_comments_2.clicked.connect(self.show_comments_2)
        self.pushButton_show_comments_3.clicked.connect(self.show_comments_3)

        # Like posts
        self.pushButton_like_posts.clicked.connect(self.like_post)
        self.pushButton_like_posts_2.clicked.connect(self.like_post_2)
        self.pushButton_like_posts_3.clicked.connect(self.like_post_3)

        # share post
        self.pushButton_share_posts.clicked.connect(self.share_post)
        self.pushButton_share_posts_2.clicked.connect(self.share_post_2)
        self.pushButton_share_posts_3.clicked.connect(self.share_post_3)

    def share_post(self):
        # get post_id
        if self.listWidget_posts_by_users_in_network.currentItem():
            post_index = self.listWidget_posts_by_users_in_network.currentItem().text().split(": ", )[0]
            post_id = server.get_posts(self.user_id, 1, 0, 0)[int(post_index)][0]

            server.share_post(self.user_id, post_id)

        # update  info
        self.update_info()

    def share_post_2(self):
        # get post_id
        if self.listWidget_posts_by_users_in_network_2.currentItem():
            post_index = self.listWidget_posts_by_users_in_network_2.currentItem().text().split(": ", )[0]
            post_id = server.get_posts(self.user_id, 0, 1, 0)[int(post_index)][0]

            server.share_post(self.user_id, post_id)

        # update  info
        self.update_info()

    def share_post_3(self):
        # get post_id
        if self.listWidget_posts_by_users_in_network_3.currentItem():
            post_index = self.listWidget_posts_by_users_in_network_3.currentItem().text().split(": ", )[0]
            post_id = server.get_posts(self.user_id, 0, 0, 1)[int(post_index)][0]

            server.share_post(self.user_id, post_id)

        # update  info
        self.update_info()

    def like_post(self):
        # get post_id
        if self.listWidget_posts_by_users_in_network.currentItem():
            post_index = self.listWidget_posts_by_users_in_network.currentItem().text().split(": ", )[0]
            post_id = server.get_posts(self.user_id, 1, 0, 0)[int(post_index)][0]

            server.like_post(self.user_id, post_id)

        # update  info
        self.update_info()

    def like_post_2(self):
        # get post_id
        if self.listWidget_posts_by_users_in_network_2.currentItem():
            post_index = self.listWidget_posts_by_users_in_network_2.currentItem().text().split(": ", )[0]
            post_id = server.get_posts(self.user_id, 0, 1, 0)[int(post_index)][0]

            server.like_post(self.user_id, post_id)

        # update  info
        self.update_info()

    def like_post_3(self):
        # get post_id
        if self.listWidget_posts_by_users_in_network_3.currentItem():
            post_index = self.listWidget_posts_by_users_in_network_3.currentItem().text().split(": ", )[0]
            post_id = server.get_posts(self.user_id, 0, 0, 1)[int(post_index)][0]

            server.like_post(self.user_id, post_id)

        # update  info
        self.update_info()

    def show_comments(self):
        # Get post_id
        if self.listWidget_posts_by_users_in_network.currentItem():
            post_index = self.listWidget_posts_by_users_in_network.currentItem().text().split(": ",)[0]
            post_id = server.get_posts(self.user_id, 1, 0, 0)[int(post_index)][0]

            if self.w2 is None:
                self.w2 = Comment(self.user_id, post_id)
            else:
                self.w2.close()
                self.w2 = Comment(self.user_id, post_id)
            self.w2.show()
            # self.close()

    def show_comments_2(self):
        if self.listWidget_posts_by_users_in_network_2.currentItem():
            post_index = self.listWidget_posts_by_users_in_network_2.currentItem().text().split(": ",)[0]
            post_id = server.get_posts(self.user_id, 0, 1, 0)[int(post_index)][0]

            if self.w2 is None:
                self.w2 = Comment(self.user_id, post_id)
            else:
                self.w2.close()
                self.w2 = Comment(self.user_id, post_id)
            self.w2.show()
            # self.close()

    def show_comments_3(self):
        if self.listWidget_posts_by_users_in_network_3.currentItem():
            post_index = self.listWidget_posts_by_users_in_network_3.currentItem().text().split(": ",)[0]
            post_id = server.get_posts(self.user_id, 0, 0, 1)[int(post_index)][0]

            if self.w2 is None:
                self.w2 = Comment(self.user_id, post_id)
            else:
                self.w2.close()
                self.w2 = Comment(self.user_id, post_id)
            self.w2.show()
            # self.close()

    def update_info(self):
        # updates info in homepage
        # posts
        self.listWidget_posts_by_users_in_network_3.clear()
        self.listWidget_posts_by_users_in_network_2.clear()
        self.listWidget_posts_by_users_in_network.clear()

        # infos
        self.listWidget_info.clear()
        self.listWidget_info_2.clear()
        self.listWidget_info_3.clear()

        # set posts and info
        # posts
        posts = server.get_posts(self.user_id, 1, 0, 0)

        i = 0
        for p in posts:
            self.listWidget_posts_by_users_in_network.addItem(str(i) + ": " + p[1])
            i = i + 1

            like_counts = server.get_number_of_post_likes(post_id=p[0])
            comment_counts = server.get_number_of_post_comments(post_id=p[0])
            self.listWidget_info.addItem("likes: " + str(like_counts) + ", comments: " + str(comment_counts))

        # liked posts
        liked_posts = server.get_posts(self.user_id, 0, 1, 0)
        i = 0
        for p in liked_posts:
            self.listWidget_posts_by_users_in_network_2.addItem(str(i) + ": " + p[1])
            i = i + 1

            like_counts = server.get_number_of_post_likes(post_id=p[0])
            comment_counts = server.get_number_of_post_comments(post_id=p[0])
            self.listWidget_info_2.addItem("likes: " + str(like_counts) + ", comments: " + str(comment_counts))

        # commented posts
        commented_posts = server.get_posts(self.user_id, 0, 0, 1)
        i = 0
        for p in commented_posts:
            self.listWidget_posts_by_users_in_network_3.addItem(str(i) + ": " + p[1])
            i = i + 1

            like_counts = server.get_number_of_post_likes(post_id=p[0])
            comment_counts = server.get_number_of_post_comments(post_id=p[0])
            self.listWidget_info_3.addItem("likes: " + str(like_counts) + ", comments: " + str(comment_counts))

    def notif(self):
        # show posts of current user
        if self.w is None:
            self.w = Notif(self.user_id)
        self.w.show()
        self.close()

    def my_post(self):
        # show posts of current user
        if self.w is None:
            self.w = MyPost(self.user_id)
        self.w.show()
        self.close()

    def show_direct(self):
        # Shows direct window
        if self.w is None:
            self.w = Direct(self.user_id)
        self.w.show()
        self.close()

    def user_search(self):
        # search by location or current company or languages
        if self.w is None:
            self.w = UserSearch(self.user_id)
        self.w.show()
        self.close()

    def my_network_window(self):
        if self.w is None:
            self.w = MyNetwork(self.user_id)
        self.w.show()
        self.close()

    def edit_profile(self):
        if self.w is None:
            self.w = EditProfile(self.user_id)
        self.w.show()
        self.close()

    def log_out(self):
        self.window = LoginDlg()
        self.window.show()
        self.close()

class Notif(QDialog):
    def __init__(self, user_id):
        super().__init__()
        # Current user (who created the conversation and can sending messages)
        self.user_id = user_id
        self.w = None

        # Create an instance of the GUI
        self.ui = Ui_Dialog_notif()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # update
        self.set_info()

        # read all
        self.ui.pushButton_readAll.clicked.connect(self.read_all)

        # Back
        self.ui.pushButton_back.clicked.connect(self.back_to_home)

    def back_to_home(self):
        self.window = MainWindow(self.user_id)
        self.window.show()
        self.close()

    def read_all(self):
        server.read_all_notifications(self.user_id)
        self.set_info()

    def set_info(self):
        notifs = server.get_notifications(self.user_id)
        self.ui.listWidget_notifs.clear();

        if notifs:
            for notif in notifs:
                self.ui.listWidget_notifs.addItem(str(notif[0]) + ", " + str(notif[1]))

class Comment(QDialog):
    def __init__(self, user_id, post_id):
        super().__init__()
        # Current user (who created the conversation and can sending messages)
        self.user_id = user_id
        self.post_id = post_id
        self.w = None
        self.ids = []

        # Create an instance of the GUI
        self.ui = Ui_Dialog_comment()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # update comments
        self.set_information()

        # refresh
        self.ui.pushButton_refresh.clicked.connect(self.set_information)

        # like
        self.ui.pushButton_like.clicked.connect(self.like)

        # add comment
        self.ui.pushButton_comment.clicked.connect(self.comment_on)

        # Reply
        self.ui.pushButton_reply.clicked.connect(self.reply)

    def reply(self):
        # TODO: does not work
        # comment_on_comment(user_id, post_id, content, comment_id):
        if self.ui.listWidget_comments.currentItem():
            index = self.ui.listWidget_comments.currentItem().text().split(": ")[0]
            comment_id = self.ids[int(index)]

            content = self.ui.textEdit_content.toPlainText()
            if content:
                server.comment_on_comment(self.user_id, self.post_id, content, comment_id)

                self.ui.textEdit_content.clear()
                self.set_information()

    def comment_on(self):
        content = self.ui.textEdit_content.toPlainText()
        if content:
            server.comment_on_post(user_id=self.user_id, post_id=self.post_id, content=content)

            self.ui.textEdit_content.clear()
            self.set_information()

    def like(self):
        if self.ui.listWidget_comments.currentItem():
            index = self.ui.listWidget_comments.currentItem().text().split(": ")[0]
            comment_id = self.ids[int(index)]

            server.like_comment(self.user_id, comment_id)

            self.set_information()

    def set_information(self):
        self.ids = []
        self.ui.listWidget_comments.clear()
        self.ui.listWidget_count.clear()

        # get comments
        comments = server.get_post_comments(self.post_id)

        # if comments is exists then show it
        i = 0
        if comments:
            for comment in comments: # comment_id, text
                # Show this comment
                self.ui.listWidget_comments.addItem(str(i) + ": " + comment[1])
                self.ids.append(int(comment[0]))
                i = i + 1

                # Show number of likes
                self.ui.listWidget_count.addItem("Likes: " + str(server.get_number_of_comment_likes(comment[0])))

                # get replys of this comment
                replys = server.get_comment_comments(comment[0])
                if replys:
                    # show replys
                    for reply in replys:
                        # show reply
                        self.ui.listWidget_comments.addItem("      " + str(i) + ": " + reply[1])
                        self.ids.append(int(reply[0]))
                        i = i + 1

                        # show number of likes
                        self.ui.listWidget_count.addItem("Likes: " + str(server.get_number_of_comment_likes(reply[0])))

class MyPost(QWidget):
    def __init__(self, user_id):
        super().__init__()
        # Current user (who created the conversation and can sending messages)
        self.user_id = user_id
        self.w = None

        # Create an instance of the GUI
        self.ui = Ui_Form_my_posts()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # set posts
        self.set_information()

        # refresh
        self.ui.pushButton_refresh.clicked.connect(self.set_information)

        # back to home
        self.ui.pushButton_back.clicked.connect(self.back_to_home)

        # add post
        self.ui.pushButton_add_post.clicked.connect(self.add_post)

    def add_post(self):
        content = self.ui.textEdit_content_post.toPlainText()
        if content != "":
            server.create_post(self.user_id, content)

        self.ui.textEdit_content_post.clear()

        # update posts list
        self.set_information()

    def back_to_home(self):
        self.window = MainWindow(self.user_id)
        self.window.show()
        self.close()

    def set_information(self):
        self.ui.listWidget_counts.clear()
        self.ui.listWidget_my_posts.clear()
        i = 0
        posts = server.get_user_posts(self.user_id)
        if posts:
            for p in posts:
                self.ui.listWidget_my_posts.addItem(str(i) + ": " + p[1])
                i = i + 1

                counts_like = server.get_number_of_post_likes(p[0])
                counts_comments = server.get_number_of_post_comments(p[0])

                self.ui.listWidget_counts.addItem("likes: " + str(counts_like) + ", comments: " + str(counts_comments))

class Chat(QDialog):
    def __init__(self, user_id, target_email, conversation_id):
        super().__init__()
        # Current user (who created the conversation and can sending messages)
        self.user_id = user_id
        self.target_email = target_email
        self.conversation_id = conversation_id
        self.w = None

        # Create an instance of the GUI
        self.ui = Ui_Dialog_chat()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # Set name
        self.ui.label_name.setText(str(self.target_email))

        # set information from server
        self.set_information()

        # Send message
        self.ui.pushButton_send.clicked.connect(self.send_message)

        # refresh
        self.ui.pushButton_refresh.clicked.connect(self.refresh)

    def refresh(self):
        self.set_information()

    def send_message(self):
        # get text
        text = self.ui.textEdit_message.toPlainText()

        if text != "":
            # send message to server
            server.send_message(user_id=self.user_id, conversation_id=self.conversation_id, text=text)

        # clear text box
        self.ui.textEdit_message.clear()

        # update chat box
        self.set_information()

    def set_information(self):
        # update
        self.ui.listWidget_chat.clear()

        # Set information
        info_lst = server.get_messages(self.conversation_id)
        for message in info_lst:
            self.ui.listWidget_chat.addItem(message)


class Direct(QWidget):
    def __init__(self, user_id):
        super().__init__()
        # Current user
        self.user_id = user_id
        self.w = None # view profile
        self.w2 = None # chat

        # Create an instance of the GUI
        self.ui = Ui_Form_direct()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # Back to home
        self.ui.pushButton_back.clicked.connect(self.back_to_home)

        # Show information
        self.set_information()

        # Create conversation
        self.ui.pushButton_create_conversation.clicked.connect(self.create_conversation)

        # Open conversation
        self.ui.pushButton_open.clicked.connect(self.open_chat)

        # View profile - conversation
        self.ui.pushButton_view_profile_conversation.clicked.connect(self.view_profile_conversation)

        # View profile - other users
        self.ui.pushButton_view_profile_other.clicked.connect(self.view_profile_other)

        # Refresh
        self.ui.pushButton_refresh.clicked.connect(self.refresh)

    def refresh(self):
        self.set_information()

    def view_profile_other(self):
        if self.ui.listWidget_other_users_in_network.currentItem():
            target_email = self.ui.listWidget_other_users_in_network.currentItem().text()

            server.get_user_id(target_email)

            # Show other profile window
            if self.w is None:
                self.w = OtherProfile(str(target_email), self.user_id)
            else:
                self.w.close()
                self.w = OtherProfile(str(target_email), self.user_id)
            self.w.show()

    def view_profile_conversation(self):
        if self.ui.listWidget_conversation.currentItem():
            target_email = self.ui.listWidget_conversation.currentItem().text()
            id_of_user = server.get_user_id(target_email)


            # Show other profile window
            if self.w is None:
                self.w = OtherProfile(str(target_email), self.user_id)
            else:
                self.w.close()
                self.w = OtherProfile(str(target_email), self.user_id)
            self.w.show()

    def create_conversation(self):
        # Create conversation and create a instance of chat class
        if self.ui.listWidget_other_users_in_network.currentItem():
            target_email = self.ui.listWidget_other_users_in_network.currentItem().text()
            try:
                server.create_conversation(self.user_id, str(target_email))

            except exeptions.ConversationAlreadyExists as e:
                self.ui.label_message.setText("Conversation is already exists.")

            # get conversation id
            conversation_id = server.get_conversation_id(self.user_id, str(target_email))

            # Show chat window
            if self.w is None:
                self.w = Chat(self.user_id, target_email, conversation_id)
            else:
                self.w.close()
                self.w = Chat(self.user_id, target_email, conversation_id)
            self.w.show()

            self.set_information()

    def open_chat(self):
        # opens chatroom with current user and conversation id
        target_email = self.ui.listWidget_conversation.currentItem().text()
        conversation_id = server.get_conversation_id(self.user_id, target_email)

        # Show chat window
        if self.w is None:
            self.w = Chat(self.user_id, target_email, conversation_id)
        else:
            self.w.close()
            self.w = Chat(self.user_id, target_email, conversation_id)
        self.w.show()

    def set_information(self):
        # get information from server and show it
        # update
        self.ui.listWidget_conversation.clear()
        self.ui.listWidget_other_users_in_network.clear()

        # Conversation
        conversation_lst = server.get_conversations(self.user_id)
        for email in conversation_lst:
            self.ui.listWidget_conversation.addItem(email)

        # other users in network
        other = server.get_network_users_with_no_conversation(self.user_id)
        for email in other:
            self.ui.listWidget_other_users_in_network.addItem(email)

    def back_to_home(self):
        self.window = MainWindow(self.user_id)
        self.window.show()
        self.close()


class UserSearch(QWidget):
    def __init__(self, user_id):
        super().__init__()
        # Current user
        self.user_id = user_id
        self.w = None

        self.emails = []

        # Create an instance of the GUI
        self.ui = Ui_Form_search_user()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # invite
        self.ui.pushButton_invite.clicked.connect(self.invite)

        # Show profile
        self.ui.pushButton_show_profile.clicked.connect(self.show_profile)

        # Search
        self.ui.pushButton_search.clicked.connect(self.search)

        # Back to home
        self.ui.pushButton_back.clicked.connect(self.back_to_home)

    def back_to_home(self):
        self.window = MainWindow(self.user_id)
        self.window.show()
        self.close()

    def search(self):
        # get name
        first_name = self.ui.lineEdit_first_name.text()
        last_name = self.ui.lineEdit_last_name.text()

        # print(first_name + last_name)

        self.emails = []
        self.ui.listWidget_users.clear()

        location = self.ui.comboBox_location.currentText()
        company = self.ui.lineEdit_current_company.text()

        checkBoxeslst = [self.ui.checkBox_1, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4, self.ui.checkBox_5, self.ui.checkBox_6, self.ui.checkBox_7, self.ui.checkBox_8]
        langs = []
        for i in range(len(checkBoxeslst)):
            if checkBoxeslst[i].isChecked():
                langs.append(1)
            else:
                langs.append(0)

        if location == "All":
            location = None

        # user_id, country, langs, company, first_name, last_name
        # return: email, fullname
        # call search func from server to get user
        found_users = server.get_users(user_id=self.user_id, country=location, langs=langs, company=company, first_name=first_name, last_name=last_name)

        if not found_users:
            self.ui.message.setText("no user found")

        else:
            i = 0
            self.ui.message.setText("")
            for u in found_users:
                self.ui.listWidget_users.addItem(str(i) + ": " + u[1] + ", " + str(server.get_number_of_mutural_friends(user_id=self.user_id, target_email=u[0])))
                self.emails.append(u[0])
                i = i + 1

    def show_profile(self):
        if self.ui.listWidget_users.currentItem():
            index = int(self.ui.listWidget_users.currentItem().text().split(": ")[0])
            email = self.emails[index]
            if self.w is None:
                self.w = OtherProfile(str(email), self.user_id)
            self.w.show()
            # self.close()

    def invite(self):
        # Send invitation
        try:
            if self.ui.listWidget_users.currentItem():
                receiver_email_index = int(self.ui.listWidget_users.currentItem().text().split(": ")[0])
                receiver_email = self.emails[receiver_email_index]
                server.send_invitation(sender_id=self.user_id, receiver_email=receiver_email)
                self.ui.message.setText("invitation sent")

        except exeptions.InvitationErrorInvalidEmail as e:
            self.ui.message.setText("email does not exist")

        except exeptions.InvitationErrorAlreadyFollow as e:
            self.ui.message.setText("already in network")

        except exeptions.InvitationErrorAlreadySent as e:
            self.ui.message.setText("already sent")


class OtherProfile(QDialog):
    # To show the profile of other people
    def __init__(self, email, current_user_id):
        super().__init__()

        self.user_id = server.get_user_id(email)

        # notification
        server.send_view_profile_notification(current_user_id, self.user_id)

        # Create an instance of the GUI
        self.ui = Ui_Dialog_Show_profile()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        self.checkBoxeslst = [self.ui.checkBox_1, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4, self.ui.checkBox_5, self.ui.checkBox_6, self.ui.checkBox_7, self.ui.checkBox_8]

        # Set the user_id of this profile
        self.ui.label_user_id.setText("profile of " + str(email))

        # update
        self.set_information()


    def change(self):
        if not self.ui.checkBox_1.isChecked():
            self.ui.checkBox_1.setChecked(True)
        self.ui.checkBox_1.setChecked(True)

    def set_information(self):
        # [intro, about, featured, background, accomplishments, additional_information, supported_languages, job_status, company, skills]
        info = server.get_information(self.user_id)

        self.ui.textEdit_intro.setText(info[0])
        self.ui.textEdit_about.setText(info[1])
        self.ui.textEdit_featured.setText(info[2])
        self.ui.textEdit_background.setText(info[3])
        self.ui.textEdit_accomplishments.setText(info[4])
        self.ui.textEdit_additional_information.setText(info[5])
        self.ui.textEdit_job_status.setText(info[7])
        self.ui.textEdit_company.setText(info[8])
        self.ui.textEdit_skills.setText(info[9])

        # boolean list
        # [support_persian, support_english, support_chinese,
        # support_russian, support_german, support_french,
        # support_japanese, support_italian]

        langs = info[6]
        for i in range(len(langs)):
            self.checkBoxeslst[i].toggled.connect(self.on_click)
            if langs[i]:
                self.checkBoxeslst[i].setChecked(True)
            else:
                self.checkBoxeslst[i].setCheckable(False)

    def on_click(self):
        b = self.sender()
        b.setChecked(True)

class MyNetwork(QWidget):
    def __init__(self, user_id):
        super().__init__()
        # Current user
        self.user_id = user_id
        self.w = None

        # Create an instance of the GUI
        self.ui = Ui_myNetwork()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # set information
        self.set_information(self.user_id)

        # Back to home
        self.ui.pushButton_backToHome.clicked.connect(self.back_to_main_window)

        # Invitation
        self.ui.pushButton_accept.clicked.connect(self.accept_invitation)
        self.ui.pushButton_decline.clicked.connect(self.decline_invitation)

        # People you may know
        self.ui.pushButton_showProfile.clicked.connect(self.show_profile)
        self.ui.pushButton_invite.clicked.connect(self.invite)

        # Refresh
        self.ui.pushButton_refresh.clicked.connect(self.refresh)

    def refresh(self):
        self.set_information(self.user_id)

    def set_information(self, id_of_user):
        # Get "invitation" list and "people you may know" list from server and show them
        self.ui.listWidget_invitaion.clear()
        self.ui.listWidget_peopleYouyMayKnow.clear()

        invitations = server.get_invitations(id_of_user)
        for i in invitations:
            self.ui.listWidget_invitaion.addItem(i + ", " + str(server.get_number_of_mutural_friends(user_id=id_of_user, target_email=i)))

        people_you_may_know = server.get_people_you_may_know(id_of_user)
        for p in people_you_may_know:
            self.ui.listWidget_peopleYouyMayKnow.addItem(p + ", " + str(server.get_number_of_mutural_friends(user_id=id_of_user, target_email=p)))

    def show_profile(self, user_id):
        if self.ui.listWidget_peopleYouyMayKnow.currentItem():
            email = self.ui.listWidget_peopleYouyMayKnow.currentItem().text().split(", ")[0]

            if self.w is None:
                self.w = OtherProfile(str(email), self.user_id)
            else:
                self.w.close()
                self.w = OtherProfile(str(email), self.user_id)
            self.w.show()
            # self.close()

    def auto_refresh(self, second_email):
        second_user_id = server.get_user_id(second_email)
        self.set_information(second_user_id)
        self.set_information(self.user_id)

    def invite(self):
        # Send invitation
        try:
            if self.ui.listWidget_peopleYouyMayKnow.currentItem():
                receiver_email = self.ui.listWidget_peopleYouyMayKnow.currentItem().text().split(", ")[0]
                server.send_invitation(sender_id=self.user_id, receiver_email=receiver_email)
                self.auto_refresh(receiver_email)

        except exeptions.InvitationErrorInvalidEmail as e:
            self.ui.message.setText("email does not exist")

        except exeptions.InvitationErrorAlreadyFollow as e:
            self.ui.message.setText("already in network")

        except exeptions.InvitationErrorAlreadySent as e:
            self.ui.message.setText("already sent")

        self.set_information(self.user_id)

    def decline_invitation(self):
        # call the function
        if self.ui.listWidget_invitaion.currentItem():
            sender_email = self.ui.listWidget_invitaion.currentItem().text().split(", ")[0]
            server.decline_invitation(sender_email=sender_email, receiver_id=self.user_id)

            self.auto_refresh(sender_email)

    def accept_invitation(self):
        # call the function for accepting
        if self.ui.listWidget_invitaion.currentItem():
            sender_email = self.ui.listWidget_invitaion.currentItem().text().split(", ")[0]
            server.accept_invitation(sender_email=sender_email, receiver_id=self.user_id)

            # delete this user from list
            # index = self.ui.listWidget_invitaion.currentIndex()
            # self.ui.listWidget_invitaion.takeItem(index.row())

            self.auto_refresh(sender_email)

    def back_to_main_window(self):
        self.window = MainWindow(self.user_id)
        self.window.show()
        self.close()


class OtherProfileNetwork(QDialog):
    # To show the profile of other people
    def __init__(self, user_id, email):
        super().__init__()
        self.user_id = user_id
        # Create an instance of the GUI
        self.ui = Ui_Dialog_Show_profile()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # Set the user_id of this profile
        self.ui.label_user_id.setText("profile of " + str(email))

        # back
        self.ui.pushButton_back.clicked.connect(self.back)

    def back(self):
        self.window = MyNetwork(self.user_id)
        self.window.show()
        self.close()


class EditProfile(QWidget):
    def __init__(self, user_id):
        super().__init__()
        # Current user
        self.user_id = user_id

        # Create an instance of the GUI
        self.ui = Ui_profile()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        self.checkBoxeslst = [self.ui.checkBox_1, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4, self.ui.checkBox_5, self.ui.checkBox_6, self.ui.checkBox_7, self.ui.checkBox_8]
        self.ui.pushButton_back.clicked.connect(self.back_to_main_window)
        self.ui.pushButton_save.clicked.connect(self.edit_information)

        self.set_information()

    # [intro, about, featured, background, accomplishments, additional_information, supported_languages, skills]
    def edit_information(self):
        intro = self.ui.textEdit_intro.toPlainText()
        about = self.ui.textEdit_about.toPlainText()
        featured = self.ui.textEdit_featured.toPlainText()
        background = self.ui.textEdit_background.toPlainText()
        accomplishments = self.ui.textEdit_accomplishments.toPlainText()
        additional_information = self.ui.textEdit_additional_information.toPlainText()
        job_status = self.ui.textEdit_job_status.toPlainText()
        company = self.ui.textEdit_company.toPlainText()
        skills = self.ui.textEdit_skills.toPlainText()
        langs = []
        for i in range(len(self.checkBoxeslst)):
            if self.checkBoxeslst[i].isChecked():
                langs.append(1)
            else:
                langs.append(0)

        server.edit_information(self.user_id, intro, about, featured, background, accomplishments, additional_information, langs, job_status, company, skills)
        self.set_information()

        self.window = MainWindow(self.user_id)
        self.window.show()
        self.close()

    def set_information(self):
        # info is a list
        info = server.get_information(self.user_id)

        self.ui.textEdit_intro.setText(info[0])
        self.ui.textEdit_about.setText(info[1])
        self.ui.textEdit_featured.setText(info[2])
        self.ui.textEdit_background.setText(info[3])
        self.ui.textEdit_accomplishments.setText(info[4])
        self.ui.textEdit_additional_information.setText(info[5])
        self.ui.textEdit_job_status.setText(info[7])
        self.ui.textEdit_company.setText(info[8])
        self.ui.textEdit_skills.setText(info[9])


        # boolean list
        # [support_persian, support_english, support_chinese,
        # support_russian, support_german, support_french,
        # support_japanese, support_italian]
        langs = info[6]
        for i in range(len(langs)):
            if langs[i]:
                self.checkBoxeslst[i].setChecked(True)

    def back_to_main_window(self):
        self.window = MainWindow(self.user_id)
        self.window.show()
        self.close()


class LoginDlg(QDialog):
    """ Login Dialog """

    def show_mainwindow(self, user_id):
        self.window = MainWindow(user_id)
        self.window.show()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog_login()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        self.ui.pushButton_login.clicked.connect(self.login)
        self.ui.pushButton_createacc.clicked.connect(self.createacc)

    def login(self):

        if (self.ui.lineEdit_email.text() == "") or (self.ui.lineEdit_pass.text() == ""):
            self.ui.message.setText("fill out all required fields")
            return

        try:
            user_id = server.login(self.ui.lineEdit_email.text(), self.ui.lineEdit_pass.text())
            self.ui.message.setText("successfully logged in")
            self.show_mainwindow(user_id)
            self.close()

        except exeptions.LoginError as e:
            self.ui.message.setText("invalid email or password")

    def createacc(self):
        signupDlg = SignupDlg()
        # self.close()
        signupDlg.exec_()


class SignupDlg(QDialog):
    """ Signup Dialog """

    def show_mainwindow(self, user_id):
        self.mainWindow = QtWidgets.QMainWindow()
        self.window = Ui_MainWindow()
        self.window.setupUi(self.mainWindow)
        self.mainWindow.show()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog_signup()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        self.ui.pushButton_signup.clicked.connect(self.signUp)

    def signUp(self):
        email = self.ui.lineEdit_email.text()
        password = self.ui.lineEdit_pass.text()
        confirm_pass = self.ui.lineEdit_confirmpass.text()
        first_name = self.ui.lineEdit_fisrtsanme.text()
        last_name = self.ui.lineEdit_lastname.text()
        day = self.ui.comboBox_birth_day.currentText()
        month = self.ui.comboBox_birth_month.currentText()
        year = self.ui.comboBox_birth_year.currentText()
        country = self.ui.comboBox_country.currentText()

        if (email == "") or (password == "") or (confirm_pass == "") or (first_name == "") or (last_name == ""):
            self.ui.message.setText("fill out all required fields")
            return

        try:
            user_id = server.sign_up(email, password, confirm_pass, first_name, last_name, day, month, year, country)
            self.ui.message.setText("successfully signed up")
            # self.show_mainwindow(user_id)
            self.close()

        except exeptions.SignupErrorEmail as e:
            self.ui.message.setText("this email has been used")

        except exeptions.SignupErrorPassword as e:
            self.ui.message.setText("passwords don't match")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = LoginDlg()
    window.show()

    sys.exit(app.exec_())
