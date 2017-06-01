from pymorphy2 import MorphAnalyzer
import random

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
    f = open (name, 'r')
    text = f.read()
    f.close()
    text = Clean(text)
    mas = Add (text, mas)
    mas=set(mas)
    return mas

def Dict (mas): #словарь часть речи:слово
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

mas=[]
n='C:\\Users\\1\\Desktop\\PythonProjects\\HW3(project)\\coriolanus.txt'
mastext = OpenAndAdd(n, mas)
n='C:\\Users\\1\\Desktop\\PythonProjects\\HW3(project)\\hamlet.txt'
mastext = OpenAndAdd(n, mas)
n='C:\\Users\\1\\Desktop\\PythonProjects\\HW3(project)\\lear.txt'
mastext = OpenAndAdd(n, mas)
n='C:\\Users\\1\\Desktop\\PythonProjects\\HW3(project)\\macbeth.txt'
mastext = OpenAndAdd(n, mas)
n='C:\\Users\\1\\Desktop\\PythonProjects\\HW3(project)\\othello.txt'
mastext = OpenAndAdd(n, mas)
n='C:\\Users\\1\\Desktop\\PythonProjects\\HW3(project)\\romeo.txt'
mastext = OpenAndAdd(n, mas)

dict_word=Dict(mastext) #в dict_word - часть речи:слово для замены

message=input()
message=message.split(' ')
reply=''

for word in message:
    form = CollectForm (word) #массив для характеристики word
    wor_rep = MakeReplyWord(word, dict_word) #сырое слово на замену
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
        wor_re=word
    reply = reply+wor_re+' '

print(reply)
