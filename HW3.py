from pymorphy2 import MorphAnalyzer
import random
import telebot
import conf
import flask

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

def Clean(text): #чистит текст
    text = text.replace('I', ' ')
    text = text.replace('V', ' ')
    text = text.replace('X', ' ')
    text = text.replace('…', ' ')
    text = text.replace('1', ' ')
    text = text.replace('2', ' ')
    text = text.replace('3', ' ')
    text = text.replace('4', ' ')
    text = text.replace('5', ' ')
    text = text.replace('6', ' ')
    text = text.replace('7', ' ')
    text = text.replace('8', ' ')
    text = text.replace('9', ' ')
    text = text.replace('0', ' ')
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace(';', ' ')
    text = text.replace(':', ' ')
    text = text.replace('-', ' ')
    text = text.replace('?', ' ')
    text = text.replace('!', ' ')
    text = text.replace('^', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('+', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\t\t', ' ')
    text = text.replace('/', ' ')
    text = text.replace('_', ' ')
    text = text.replace('«', ' ')
    text = text.replace('»', ' ')
    text = text.replace('"', ' ')
    text = text.replace('—', ' ')
    text = text.replace('~', ' ')
    text = text.replace('@', ' ')
    text = text.replace('&', ' ')
    text = text.replace('  ', ' ')
    text=text.lower()
    return text

def Add(text, mas): #добавляет слова из нового файла
    m=text.split(' ')
    for part in m:
        if part !='':
            mas.append(part)
    return mas

def OpenAndAdd (name, mas): #открывает файл
    f = open (name, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    text = Clean(text)
    mas = Add (text, mas)
    mas=set(mas)
    return mas

def Dicts (mas): #словарь часть речи:слово
    dict={}
    morph = MorphAnalyzer()
    for word in mas:
        wordm = morph.parse(word)[0]
        p = str(wordm.tag.POS)
        if p == 'NOUN':
            g = str(wordm.tag.gender)
            if p + ' ' + g in dict:
                dict[p + ' ' + g].append(word)
            else:
                dict[p + ' ' + g] = [word]
        elif p == 'NPRO':
            g = str(wordm.tag.gender)
            if p + ' ' + g in dict:
                dict[p + ' ' + g].append(word)
            else:
                dict[p + ' ' + g] = [word]
        elif p == 'VERB':
            t = str(wordm.tag.transitivity)
            if p + ' ' + t in dict:
                dict[p + ' ' + t].append(word)
            else:
                dict[p + ' ' + t] = [word]
        elif p == 'INFN':
            t = str(wordm.tag.transitivity)
            if p + ' ' + t in dict:
                dict[p + ' ' + t].append(word)
            else:
                dict[p + ' ' + t] = [word]
        else:
            if p in dict:
                dict[p].append(word)
            else:
                dict[p] = [word]
    return dict

def CollectForm(word):
    form=[]
    morph = MorphAnalyzer()
    wordm = morph.parse(word)[0]
    if 'NOUN' in wordm.tag:
        form.append(wordm.tag.case)
        form.append(wordm.tag.number)
    elif 'NPRO' in wordm.tag:
        form.append(wordm.tag.case)
        form.append(wordm.tag.number)
        form.append(wordm.tag.person)
    elif 'PRTF' or 'ADJF' in wordm.tag:
        form.append(wordm.tag.case)
        form.append(wordm.tag.gender)
        form.append(wordm.tag.number)
    elif 'ADJS' or 'PRTS' in wordm.tag:
        form.append(wordm.tag.gender)
        form.append(wordm.tag.number)
    if 'VERB' in wordm.tag:
        if 'pres' or 'futr' in wordm.tag:
            form.append(wordm.tag.number)
            form.append(wordm.tag.tense)
            form.append(wordm.tag.person)
    return form

def MakeReplyWord(word, dict_word):
    morph = MorphAnalyzer()
    wordm = morph.parse(word)[0]
    p = str(wordm.tag.POS)
    if p == 'NOUN':
        g = str(wordm.tag.gender)
        wor_rep = random.choice(dict_word[p + ' ' + g])
    elif p == 'NPRO':
        g = str(wordm.tag.gender)
        wor_rep = random.choice(dict_word[p + ' ' + g])
    elif p == 'VERB':
        t = str(wordm.tag.transitivity)
        wor_rep = random.choice(dict_word[p + ' ' + t])
    elif p == 'INFN':
        t = str(wordm.tag.transitivity)
        wor_rep = random.choice(dict_word[p + ' ' + t])
    else:
        wor_rep = random.choice(dict_word[p])
    return wor_rep

mas = []
n = '/home/justamistake/mysite/coriolanus.txt'
mastext = OpenAndAdd(n, mas)
n = '/home/justamistake/mysite/hamlet.txt'
mastext = OpenAndAdd(n, mas)
n = '/home/justamistake/mysite/lear.txt'
mastext = OpenAndAdd(n, mas)
n = '/home/justamistake/mysite/macbeth.txt'
mastext = OpenAndAdd(n, mas)
n = '/home/justamistake/mysite/othello.txt'
mastext = OpenAndAdd(n, mas)
n = '/home/justamistake/mysite/romeo.txt'
mastext = OpenAndAdd(n, mas)
dict_word = Dicts(mastext)  # в dict_word - часть речи:слово для замены

@bot.message_handler(commands=['start'])
def send_welcome(message): bot.send_message(message.chat.id, "Привет. Я - бот, который может в грамматику. Напиши мне что-нибудь. Только не используй знаки препинания, пожалуйста.")

@bot.message_handler(func=lambda m: True)
def send_len(message):
    reply = ''
    mes = message.text
    mes=mes.split()
    for word in mes:
        form = CollectForm(word)  # массив для характеристики word
        wor_rep = MakeReplyWord(word, dict_word)  # сырое слово на замену
        morph = MorphAnalyzer()
        wordm = morph.parse(word)[0]
        if wordm.tag.POS == 'VERB':
            if 'past' in wordm.tag:
                if 'sing' in wordm.tag:
                    form.append(wordm.tag.gender)
        if None in form:
            form.remove(None)
        form = set(form)
        print(wor_rep)
        wor_re = morph.parse(wor_rep)[0]
        try:
            if wor_re.tag.POS == 'INFN':
                wor_re = wor_rep
            else:
                wor_re = wor_re.inflect(form)
                wor_re = wor_re.inflect(form).word
        except:
            wor_re = word
        reply = reply + wor_re + ' '
    bot.send_message(message.chat.id, reply)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    bot.polling(none_stop=True)
