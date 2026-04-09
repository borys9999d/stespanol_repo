from flask import Flask, render_template, request, redirect, url_for, make_response
import random, math, os

app = Flask(__name__)
asked = []
selected_set = []



common_words = [
    {"ser": "to be (essential|permanent quality)"},#0
    {"estar": "to be (temporary state)"},#1
    {"tener": "to have"},#2
    {"hacer": "to do|make"},#3  
    {"ir": "to go"},#4
    {"decir": "to say|tell"},#5
    {"poder": "to be able to|can"},#6
    {"ver": "to see"},#7
    {"dar": "to give"},#8
    {"la gente": "people"},#9
    {"el tiempo": "time|weather"},#10
    {"la día": "day"},#11
    {"la mano": "hand"},#12
    {"el año": "year"},#13
    {"un|a": "a (masculine|feminine)"},#14
    {"y": "and"},#15
    {"en": "in|on|at"},#16
    {"que": "that|which|who"},#17
    {"no": "no|not"},#18
    {"de": "of|from"},#19
    {"la": "the (feminine)"},#20
    {"el": "the (masculine)"},#21
    ]
confusing_similar_words = [
    {"por que, porque": "why, because"},#0
    {"pero, perro": "but, dog"},#1
    {"tubo, tuvo": "tube, had"},#2
    {"caro, carro": "expensive, car"},#3
    {"si, sí": "if, yes"},#4
    {"tú, tu": "you (informal), your"},#5
    {"mi, mí": "my, me"},#6
    {"como, cómo": "like|as, how"},#7
    {"donde, dónde": "where(fact), where(question)"},#8
    {"cuando, cuándo": "when(fact), when(question)"},#9
    {"y, e": "and, and(before i sounds)"},#10
    {"o, u": "or, or(before o sounds)"},#11
    {"casa, caza": "house, hunt"},#12
    {"vaca, vací-a|o": "cow, empty"},#13
    {"grabar, gravar": "(to)record, (the)tax"},#14
    {"lío, tío": "mess, uncle"},#15
    {"río, frío": "river, (he's|it's)cold"},#16
]
presente = [
    ["hablar","habl"],
    ["caminar", "camin"],
    ["comprar", "compr"],
    ["vender", "vend"],
    ["comer", "com"],
    ["beber", "beb"],
    ["vivir", "viv"],
    ["abrir", "abr"],
    ["compartir", "compart"]
]


kontexts = ["yo","tú", "él|ella", "nosotr-os|as","vosotr-os|as","ell-os|as"]


presente_end_ar = ["o","as","a","amos","áis","an"]
presente_end_erir = ["o","es","e","imos","ís","en"]

indefinido_end_ar = ["é","aste","ó","amos","asteis","aron"]
indefinido_end_erir = ["í","iste","ió","imos","isteis","ieron"]


@app.route('/')
def menu():
    return render_template('menu.html')
@app.route('/Vocabs')
def vocabs():
    try:
        valI = int(request.cookies.get('common_words_progress'))
        valII = int(request.cookies.get('confusing_similarities_progress'))
    except:
        valI = 0
        valII = 0

    resp = make_response(render_template('Vocabs_menu.html', common_words_progress=valI, confusing_similarities_progress=valII))

    # Overwrite (replace) the cookie by setting it again with the same name
    if int(request.cookies.get('common_words_progress')) > 100:
        valI = 99
    elif int(request.cookies.get('common_words_progress')) < -100:
        valI = -99
    elif int(request.cookies.get('confusing_similarities_progress')) > 100:
        valII = 99
    elif int(request.cookies.get('confusing_similarities_progress')) < -100:
        valII = -99


    else:pass

    resp = make_response(render_template('Vocabs_menu.html', common_words_progress=valI,\
        confusing_similarities_progress=valII))
    resp.set_cookie('common_words_progress', str(valI), max_age=60*60*24*365)
    resp.set_cookie('confusing_similarities_progress', str(valII), max_age=60*60*24*365)

    return resp

@app.route('/Times')
def times():
    
    try:
        valI = int(request.cookies.get('presente_prog'))
        
    except:
        valI = 0
        

    resp = make_response(render_template('Times_menu.html', presente_prog=valI))

    # Overwrite (replace) the cookie by setting it again with the same name
    try:
        if int(request.cookies.get('presente_prog')) > 100:
            valI = 99
        elif int(request.cookies.get('presente_prog')) < -100:
            valI = -99

        else:pass
    except:valI= 0

    resp = make_response(render_template('Times_menu.html', presente_prog=valI\
        ))
    resp.set_cookie('presente_prog', str(valI), max_age=60*60*24*365)
   

    return resp

@app.route('/words/<set>/<back>/<word_id>/<easy>/<was_front>/<was_back>')
def words(set, back, word_id, easy, was_front, was_back):
    progress_in_common_words= 0
    progress_in_confusing_similarities = 0
    resp=""

    selected_set = []
    word_id = int(word_id)
    if set == 'most_common':
        selected_set = common_words
    elif set == 'confusing_similarities':
        selected_set = confusing_similar_words

    else:
        return redirect(url_for('menu'))
    if back == 'False':
        random_num = random.randint(0, len(selected_set) - 1)
        pair = selected_set[random_num]
        backside = list(pair.keys())[0]
        front_side = list(pair.values())[0]
        if easy == 'False':
            selected_set.append({was_back:was_front})
            try:
                t = request.cookies.get('common_words_progress')
                progress_in_common_words = str(int(t)-1)
                t = request.cookies.get('confusing_similarities_progress')
                progress_in_confusing_similarities = str(int(t)-1)


            except:pass

            resp = make_response(render_template('rendering_cards.html', front_side = front_side, backside = backside, back = back, word_id = random_num, easy=easy, set=set))
            if set == 'most_common':
                resp.set_cookie('common_words_progress',str(progress_in_common_words), max_age=60*60*24*365)
            elif set == 'confusing_similarities':
                resp.set_cookie('confusing_similarities_progress',str(progress_in_confusing_similarities), max_age=60*60*24*365)
            
            for n in selected_set:
                print("\n",n, "l. 61" )

            o = 0
            for k in selected_set: 
                if selected_set.count(k) > math.floor(len(selected_set)/4) :
                    selected_set.pop(o)
                else:pass
                o += 1
        else:
            if selected_set.count(selected_set[(int(word_id))]) != 1 :
                selected_set.pop(int(word_id))
            
            for n in selected_set:
                print("\n",n, "l. 190" )
            
            try:
                if set == 'most_common':
                    t=  request.cookies.get('common_words_progress')
                    progress_in_common_words = str(int(t) + 1)
                elif set == 'confusing_similarities':
                    t=  request.cookies.get('confusing_similarities_progress')
                    progress_in_common_words = str(int(t) + 1)
                else:pass
            except:pass

            resp = make_response(render_template('rendering_cards.html', set=set,front_side = front_side, backside = backside, back = back, word_id = random_num, easy=easy))
            if set == 'most_common':
                resp.set_cookie('common_words_progress',str(progress_in_common_words), max_age=60*60*24*365)
            elif set == 'confusing_similarities':
                resp.set_cookie('confusing_similarities_progress',str(progress_in_common_words), max_age=60*60*24*365)

        return resp
    elif back == 'True':
        random_num = random.randint(0, len(selected_set) - 1)
        try :
            pair = selected_set[word_id]
            backside = list(pair.keys())[0]
            front_side = list(pair.values())[0]
        except:
            backside = "NONE"
            front_side = "NONE"
        return render_template('rendering_cards.html',set=set, front_side = front_side, backside = backside, back = back, word_id = word_id, easy=easy)
    
@app.route('/presente_forward',methods=['POST','GET'])
def presente_forward():
    resp = make_response(render_template('el_presente_forward.html'))

    random_endingsI = []
    
    random_num = random.randint(0, len(presente) - 1)
    verb = presente[random_num][0]
    const = presente[random_num][1]
    

    if verb.endswith("ar"):
        random_endingsI = presente_end_ar
        random_choiceI = random.randint(0,5)
        wordI = random_endingsI[random_choiceI]
        random_endingsI.pop(random_choiceI)
        random_endingsI.append(wordI)
        
    else:
        random_endingsI = presente_end_erir
        random_choiceI = random.randint(0,5)
        wordI = random_endingsI[random_choiceI]
        random_endingsI.pop(random_choiceI)
        random_endingsI.append(wordI)

    
    resp = make_response(render_template('el_presente_forward.html',verb=verb,const=const,endingsI=random_endingsI))
    resp.set_cookie('verb', verb, max_age=60*5)
    resp.set_cookie('const', const, max_age=60*5)
    return resp

@app.route('/presente_backward', methods=['POST'])
def presente_backward():
    resp = make_response('el_presente_backside')
    
    chosen_ends = []
    right_ends = []

    sI = request.form.get('sI')
    chosen_ends.append(sI)
    sII = request.form.get('sII')
    chosen_ends.append(sII)
    sIII = request.form.get('sIII')
    chosen_ends.append(sIII)
    sIV = request.form.get('sIV')
    chosen_ends.append(sIV)
    sV = request.form.get('sV')
    chosen_ends.append(sV)
    sVI = request.form.get('sVI')
    chosen_ends.append(sVI)

    res = 0
    # determine correct endings from the verb stored in cookies
    verb = request.cookies.get('verb')
    const = request.cookies.get('const')
    try:
        presente_prog = int(request.cookies.get("presente_prog"))
    except:
        presente_prog = 0


    if verb and verb.endswith("ar"):
        right_ends = ["o","as","a","amos","áis","an"]
    else:
        right_ends = ["o","es","e","imos","ís","en"]

    
    for i, j in zip(chosen_ends,right_ends):
        if i == j:
            res += 1
        else:res-=1

    resp= make_response(render_template('el_presente_backside.html', verb=verb, const=const,
                           chosen_ends=chosen_ends, right_ends=right_ends,
                           kontexts=kontexts, zip=zip))
    

    
    resp.set_cookie('presente_prog', str(res+presente_prog), max_age=60*60*24*365)

    return resp

if __name__ == "__main__":
    # 1. Get the port from the environment variable (Render sets this automatically)
    # 2. Default to 10000 if PORT isn't found (local testing)
    port = int(os.environ.get("PORT", 10000))
    
    # host='0.0.0.0' tells Flask to listen on all public IPs
    app.run(host='0.0.0.0', port=port)
   