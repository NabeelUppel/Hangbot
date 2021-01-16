import logging
import os
import string
import time
import tweepy
import random
import _pickle as cPickle
import atexit
from config import create_api


class Hangman:
    def __init__(self):
        self.wordbank = ['Aruba', 'Afghanistan', 'Angola', 'Anguilla', 'Aland Islands', 'Albania', 'Algeria', 'Andorra',
                         'Argentina', 'Armenia', 'Samoa', 'Antarctica', 'Antigua and Barbuda', 'Australia', 'Austria',
                         'Azerbaijan',
                         'Burundi', 'Belgium', 'Bonaire', 'Burkina Faso', 'Bangladesh', 'Bulgaria', 'Bahrain',
                         'Bahamas', 'Bosnia and Herzegovina', 'Belarus', 'Belize', 'Bermuda', 'Bolivia', 'Brazil',
                         'Barbados', 'Botswana',
                         'Canada', 'Cocos Islands', 'Chile', 'China', 'Cameroon', 'Congo', 'Cook Islands', 'Colombia',
                         'Comoros', 'Cabo Verde', 'Costa Rica', 'Cuba', 'Cayman Islands', 'Cyprus', 'Czechia',
                         'Croatia', 'Cambodia', 'Chad',
                         'Djibouti', 'Dominica', 'Denmark',
                         'Ecuador', 'Egypt', 'Eritrea', 'Estonia', 'Ethiopia',
                         'Spain', 'Sri Lanka', 'Saint Lucia', 'Switzerland',
                         'Finland', 'Fiji', 'Falkland Islands ', 'France',
                         'Gabon', 'Germany', 'Georgia', 'Ghana', 'Gibraltar', 'Guinea', 'Guadeloupe', 'Gambia',
                         'Greece', 'Grenada', 'Greenland', 'Guatemala',
                         'United Kingdom', 'United Arab Emirates',
                         'Hong Kong', 'Honduras', 'Haiti', 'Hungary',
                         'Indonesia', 'Isle of Man', 'India', 'Ireland', 'Iran', 'Iraq', 'Iceland', 'Italy',
                         'Jamaica', 'Jersey', 'Jordan', 'Japan',
                         'Kazakhstan', 'Kenya', 'Kyrgyzstan', 'Kuwait',
                         'Lebanon', 'Liberia', 'Libya',
                         'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia',
                         'Macao', 'Morocco', 'Monaco', 'Madagascar', 'Maldives', 'Mexico', 'Mali', 'Malta', 'Myanmar',
                         'Mongolia',
                         'Mozambique', 'Mauritania', 'Mauritius', 'Malawi', 'Malaysia',
                         'Namibia', 'Niger', 'Nigeria', 'Netherlands', 'Norway', 'Nepal', 'Nauru', 'New Zealand',
                         'Oman',
                         'Pakistan', 'Panama', 'Peru', 'Philippines', 'Papua New Guinea', 'Poland', 'Puerto Rico',
                         'Portugal', 'Paraguay', 'Palestine',
                         'Qatar',
                         'Romania', 'Russia', 'Rwanda',
                         'Saudi Arabia', 'Sudan', 'Senegal', 'Singapore', 'Solomon Islands', 'Sierra Leone',
                         'El Salvador',
                         'San Marino', 'Somalia', 'Serbia', 'Slovakia', 'Slovenia', 'Sweden', 'Seychelles', 'Syrian',
                         'South Africa', 'Samoa',
                         'Togo', 'Thailand', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Taiwan', 'Tanzania',
                         'Uganda', 'Ukraine', 'Uruguay', 'United States', 'Uzbekistan', 'Vatican City', 'Venezuela',
                         'Vietnam', 'Yemen',
                         'Zambia', 'Zimbabwe']
        self.puzzle = ""
        self.setPuzzle()
        self.blank = ""
        self.setBlank()
        self.answer = ""
        self.strikes = 0
        self.won = False
        self.lost = False
        self.used = []
        self.hangmanart = [
            '''
     + - - - - +
|              |
               |
               |
               |
               |
=========
''',
            '''
     + - - - - +
|              |
O            |
               |
               |
               |
=========
''', '''
     + - - - - +
|              |
O            |
 |             |
               |
               |
=========
''', '''
     + - - - - +
|              |
O            |
/|            |
               |
               |
=========
''', '''
     + - - - - +
|              |
O            |
/|\          |
               |
               |
=========
''', '''
     + - - - - +
|              |
O            |
/|\          |
/             |
               |
=========
''', '''
     + - - - - +
|              |
O            |
/|\          |
/ \          |
               |
=========
''']

    def hasLost(self):
        if self.strikes > 7:
            self.lost = True

    def setPuzzle(self):
        rand = random.randint(0, len(self.wordbank) - 1)
        self.puzzle = self.wordbank[rand].lower().replace(" ", "\n")

    def setBlank(self):
        blank = ""
        for l in self.puzzle:
            if l != "\n":
                blank = blank + "_ "
            else:
                blank = blank + "\n"
        self.blank = blank.lstrip().rstrip()

    def getBlank(self):
        return self.blank

    def isDone(self):
        if self.answer == self.puzzle:
            return True
        else:
            return False

    def Check(self, letter):
        if letter not in self.used:
            if letter in self.puzzle:
                puzLis = list(self.puzzle)
                blanLis = list(self.blank.replace(" ", ""))

                for x in range(0, len(puzLis)):
                    if puzLis[x] == letter:
                        blanLis[x] = letter
                b = ""
                for x in blanLis:
                    if x != " ":
                        b += x
                    else:
                        b += " "

                self.blank = b.rstrip().lstrip()
                self.answer = self.blank.replace("_", "")

                if self.isDone():
                    self.won = True
                    return "You Win!" + "\n" + "Final Answer: " + self.puzzle.upper().replace("\n", " ")
                if self.strikes > 0:
                    return self.hangmanart[self.strikes - 1] + "\n" + "-".join(self.used) + '\n\n' + self.blank.upper()
                else:
                    return self.blank.upper()
            else:
                self.used.append(letter.upper())
                if self.strikes < 7:
                    self.strikes += 1
                if self.strikes == 7:
                    self.lost = True
                    return self.hangmanart[
                               self.strikes - 1] + "\n" + "You Lose!" + "\n" + "Final Answer: " + self.puzzle.upper().replace(
                        "\n", " ")
                if not self.lost:
                    return self.hangmanart[self.strikes - 1] + "-".join(self.used) + '\n\n' + self.blank.upper()


class Games:
    def __init__(self, t_id):
        self.Game = Hangman()
        self.tweet_id = t_id
        self.thread = [t_id]
        self.user = t_id

    def setTweet(self, tweet):
        self.tweet_id = tweet


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
repliedMessages = set()
rGamesMessages = {}
repliedMentions = set()
rGamesMentions = {}


def storeData(i, saveFile):
    dbFile = open(saveFile, 'wb')
    cPickle.dump(i, dbFile)
    dbFile.close()


def loadData(loadFile):
    dbFile = open(loadFile, 'rb')
    db = cPickle.load(dbFile)
    dbFile.close()
    return db


def check_mentions(api, keywords, since_id):
    global repliedMentions, rGamesMentions
    logger.info("Retrieving mentions")
    new_since_id = since_id
    mentions = list(tweepy.Cursor(api.mentions_timeline, since_id=since_id).items())
    for tweet in mentions:
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            if any(keyword in tweet.text.lower() for keyword in keywords):
                logger.info(f"Answering to {tweet.user.name}")
                g = rGamesMentions.get(tweet.user.id)
                if g is not None:
                    g.setTweet(tweet.id)
                    thisGame = g.Game
                    t = tweet.text.split(" ")
                    txt = t[-1]
                    if not thisGame.lost and not thisGame.won:
                        chk = thisGame.Check(txt.lower())
                        api.update_status(
                            status=chk,
                            in_reply_to_status_id=g.tweet_id,
                            auto_populate_reply_metadata=True)

                    else:
                        rGamesMentions.pop(tweet.user.id)
                        del g
        else:
            repliedMentions.add(tweet.id)
            game = Games(tweet.id)
            rGamesMentions[tweet.user.id] = game
            api.update_status(
                status=game.Game.blank,
                in_reply_to_status_id=game.tweet_id,
                auto_populate_reply_metadata=True
            )
        repliedMentions.clear()
        repliedMentions.add(tweet.id)
    return new_since_id


def check_DMs(api, keywords):
    global repliedMessages, rGamesMessages
    me = int(api.me().id)
    logger.info("Retrieving DMs")
    messages = api.list_direct_messages()[::-1]
    recMessages = set([mes.id for mes in messages if int(mes.message_create['target']['recipient_id']) == me])
    newMessages = recMessages - repliedMessages
    repliedMessages = recMessages.intersection(repliedMessages)
    for i in newMessages:
        m = api.get_direct_message(i)
        txt = m.message_create['message_data']['text'].lower()
        user = int(m.message_create['sender_id'])
        name = api.get_user(user).name
        logger.info(f"Messaging to {name}")
        if txt == "New Game".lower():
            game = Games(user)
            rGamesMessages[user] = game
            api.send_direct_message(user, game.Game.blank)
        if txt in keywords:
            g = rGamesMessages.get(user)
            if g is not None:
                thisGame = g.Game
                if not thisGame.lost and not thisGame.won:
                    chk = thisGame.Check(txt)
                    api.send_direct_message(user, chk)
                else:
                    rGamesMessages.pop(user)
                    del g
        repliedMessages.add(m.id)



def main():
    global rGamesMentions, repliedMentions, rGamesMessages, repliedMessages

    api = create_api()
    if os.path.getsize('repliedMentions') > 0:
        repliedMentions = set(loadData('repliedMentions'))
    if os.path.getsize('rGamesMentions') > 0:
        rGamesMentions = loadData('rGamesMentions')
    if os.path.getsize('repliedMessages') > 0:
        repliedMessages = set(loadData('repliedMessages'))
    if os.path.getsize('rGamesMessages') > 0:
        rGamesMessages = loadData('rGamesMessages')

    since_id = max(repliedMentions)
    while True:
        check_DMs(api, list(string.ascii_lowercase))
        for x in range(5):
            since_id = check_mentions(api, list(string.ascii_lowercase), since_id)
            time.sleep(12)


def exit_handler():
    logger.info("SAVING DATA")
    if len(repliedMentions) != 0:
        storeData(repliedMentions, 'repliedMentions')

    if len(rGamesMentions) != 0:
        storeData(rGamesMentions, 'rGamesMentions')

    if len(repliedMessages) != 0:
        storeData(repliedMessages, 'repliedMessages')

    if len(rGamesMessages) != 0:
        storeData(rGamesMessages, 'rGamesMessages')


if __name__ == "__main__":
    atexit.register(exit_handler)
    main()
