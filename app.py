import flask
from flask import Flask, request, redirect, url_for, session, render_template, jsonify
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# پایگاه داده کلمات بدون تغییر باقی می‌ماند
WORDS_DATABASE = {
    "غذا": ["قرمه سبزی", "کباب کوبیده", "جوجه کباب", "فسنجان", "ته چین", "باقالی پلو", "زرشک پلو", "آش رشته", "دیزی", "میرزاقاسمی", "کشک بادمجان", "کله پاچه", "آبگوشت", "عدس پلو", "لوبیا پلو", "دلمه", "کوفته", "حلیم", "شله زرد", "قیمه نثار", "پیتزا", "لازانیا", "پاستا", "همبرگر", "سوشی", "استیک", "سالاد سزار", "مرغ سوخاری", "فلافل", "سمبوسه", "بندری", "املت", "نیمرو", "سوپ جو", "کباب تابه ای", "ماهی شکم پر", "میگو پلو", "کالاماری", "بریانی", "یتیمچه", "دمپختک", "آلبالو پلو", "کلم پلو", "رشته پلو", "کباب برگ", "شیشلیک", "ماهی قزل آلا", "کباب ترش", "باقلوا", "کنافه", "چیزکیک", "تیرامیسو", "بستنی سنتی", "فالوده", "کله گنجشکی", "شامی کباب", "کتلت", "ماکارونی", "بیف استروگانف", "راتاتویی", "هات داگ", "سیب زمینی سرخ کرده", "پوره سیب زمینی", "خوراک لوبیا", "عدسی", "تخم مرغ آب پز", "کره بادام زمینی", "نوتلا", "پنکیک", "وافل", "کروسان", "اسکالوپ", "شنیتسل", "گولاش", "پائیا", " تاکو", "بوریتو", "کیمچی", "رامن", "نودل", "فرنی", "شیربرنج", "خاویار", "صدف", "خرچنگ", "شاه میگو", "سالاد شیرازی", "سالاد فصل", "ماست و خیار", "زیتون پرورده", "ترشی", "کیک شکلاتی", "نان بربری", "نان سنگک", "نان تافتون", "حلوا", "سوهان", "گز", "باسلوق"],
    "شغل": ["پزشک", "مهندس نرم افزار", "معلم", "وکیل", "خلبان", "آشپز", "پلیس", "آتشنشان", "پرستار", "جراح", "دندانپزشک", "داروساز", "برقکار", "مکانیک", "نجار", "نقاش", "معمار", "گرافیست", "عکاس", "فیلمبردار", "کارگردان", "بازیگر", "خواننده", "نوازنده", "ورزشکار", "مربی", "داور", "خبرنگار", "نویسنده", "مترجم", "حسابدار", "مدیر مالی", "کارمند بانک", "فروشنده", "مشاور املاک", "راننده", "خیاط", "آرایشگر", "مهماندار", "افسر ارتش", "دانشمند", "استاد دانشگاه", "کشاورز", "دامدار", "قاضی", "نانوا", "قصاب", "ساعت ساز", "طلافروش", "برنامه نویس", "تحلیلگر داده", "متخصص امنیت سایبری", "طراح UI/UX", "دیجیتال مارکتر", "مدیر محصول", "خلبان پهپاد", " فضانورد", "باستان شناس", "زمین شناس", "اقیانوس شناس", "عصب شناس", "روانشناس", "جامعه شناس", "فیلسوف", "سیاستمدار", "دیپلمات", "کتابدار", "موزه دار", "جنگلبان", "محیط بان", "غواص", "بدلکار", "شعبده باز", "گوینده رادیو", "مجری تلویزیون", "کمدین", "انیماتور", "طراح بازی", "مهندس رباتیک", "جوشکار", "لوله کش", "باغبان", "نظافتچی", "پیک موتوری", "کارگر ساختمانی", "معدنچی", "شیرینی پز", "قهوه چی", "سفیر", "رئیس جمهور", "نماینده مجلس", "آمارگیر", "نقشه بردار", "کارآگاه", "مشاور"],
    "حیوان": ["شیر", "ببر", "پلنگ", "یوزپلنگ", "فیل", "کرگدن", "اسب آبی", "زرافه", "گورخر", "کانگورو", "پاندا", "خرس قطبی", "گرگ", "روباه", "شغال", "کفتار", "گوریل", "میمون", "شامپانزه", "عقاب", "شاهین", "جغد", "طوطی", "پنگوئن", "شترمرغ", "نهنگ", "کوسه", "دلفین", "هشت پا", "مار", "تمساح", "لاکپشت", "سگ", "گربه", "اسب", "گاو", "گوسفند", "مرغ", "خروس", "اردک", "مورچه", "زنبور", "عنکبوت", "پروانه", "سنجاب", "راکون", "آفتاب پرست", "ایگوانا", "حلزون", "ستاره دریایی", "عروس دریایی", "اسب دریایی", "فک", "گراز دریایی", "لاما", "آلپاکا", "شتر", "بز کوهی", "آهو", "گوزن", "خرگوش", "همستر", "موش", "خفاش", "کلاغ", "گنجشک", "کبوتر", "دارکوب", "فلامینگو", "پلیکان", "قورباغه", "وزغ", "سمندر", "ماهی پیرانا", "ماهی بادکنکی", "مارماهی", "سوسک", "پشه", "مگس", "کفشدوزک", "عقرب", "رتیل", "هزارپا", "کرم خاکی", "پلاتینی پوس", "جوجه تیغی", "مورچه خوار", "گورکن", "وامبت", "کوآلا", "شیطان تاسمانی", "مارمولک", "بوقلمون", "قناری", "طاووس"],
    "مکان": ["جنگل آمازون", "کویر صحرا", "قطب جنوب", "کوه اورست", "اقیانوس آرام", "مدرسه", "دانشگاه", "بیمارستان", "فرودگاه", "ایستگاه قطار", "ترمینال", "کتابخانه", "موزه لوور", "سینما", "تئاتر شهر", "ورزشگاه", "پارک ملی", "ساحل دریا", "رستوران", "کافی شاپ", "هتل", "دفتر کار", "بانک", "پاساژ", "بازار", "میدان نقش جهان", "تخت جمشید", "دیوار چین", "اهرام ثلاثه", "برج ایفل", "شهر بازی", "باغ وحش", "معدن", "کارخانه", "پالایشگاه", "نیروگاه", "آزمایشگاه", "دادگاه", "کلانتری", "شهرداری", "جزیره کیش", "غار علیصدر", "روستا", "شهر", "آسمان خراش", "آپارتمان", "ویلا", "کلبه", "ایستگاه فضایی", "سیاره مریخ", "کره ماه", "زیردریایی", "کشتی کروز", "دکل نفتی", "گلخانه", "چاپخانه", "سردخانه", "آرایشگاه", "خشکشویی", "باشگاه ورزشی", "استخر", "سونا", "جکوزی", "اتاق عمل", "بخش مراقبت های ویژه", "اورژانس", "داروخانه", "کلاس درس", "سالن آمفی تئاتر", "کارگاه", "پارکینگ", "آسانسور", "پشت بام", "زیرزمین", "انباری", "باغچه", "حیاط", "بالکن", "کلیسا", "مسجد", "کنیسه", "معبد", "قبرستان", "قله دماوند", "برج میلاد", "پل طبیعت", "دریاچه خزر", "خلیج فارس", "دشت لوت", "زندان", "سفارت", "کنسولگری", "صرافی", "سوپرمارکت", "نانوایی"],
    "اشیا": ["میز", "صندلی", "کامپیوتر", "موبایل", "کتاب", "خودکار", "مداد", "تلویزیون", "یخچال", "اجاق گاز", "عینک", "ساعت", "ماشین", "دوچرخه", "موتورسیکلت", "هواپیما", "کشتی", "قطار", "لامپ", "کلید", "قفل", "در", "پنجره", "تختخواب", "کمد", "چاقو", "چنگال", "قاشق", "بشقاب", "لیوان", "دوربین", "تلفن", "رادیو", "میکروفون", "بلندگو", "هدفون", "چکش", "پیچ گوشتی", "انبردست", "آچار", "اره", "مسواک", "خمیردندان", "شانه", "برس", "صابون", "شامپو", "حوله", "دمپایی", "کفش", "جوراب", "شلوار", "پیراهن", "کلاه", "دستکش", "چتر", "کیف", "کوله پشتی", "چمدان", "توپ", "اسباب بازی", "عروسک", "بادکنک", "شمع", "فندک", "کبریت", "آینه", "قاب عکس", "گلدان", "فرش", "پرده", "جاروبرقی", "ماشین لباسشویی", "ماشین ظرفشویی", "اتو", "سشوار", "ریش تراش", "لپ تاپ", "تبلت", "پرینتر", "اسکنر", "موس", "کیبورد", "مانیتور", "کاغذ", "دفتر", "پاک کن", "تراش", "منگنه", "سوزن", "نخ", "قیچی", "چسب", "پله", "نردبان", "انگشتر", "گردنبند", "دستبند"]
}
CITIZEN_SVG = """<svg aria-hidden="true" focusable="false" class="role-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 128c39.77 0 72 32.24 72 72s-39.77 72-72 72s-72-32.24-72-72s32.23-72 72-72zm160.3 256c-31.54-47.33-84.88-80-144.3-80h-32c-59.42 0-112.8 32.67-144.3 80C68.99 344.4 48 299.8 48 256c0-114.7 93.31-208 208-208s208 93.31 208 208c0 43.8-19.12 88.4-47.7 128z"></path></svg>"""
SPY_SVG = """<svg aria-hidden="true" focusable="false" class="role-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M224 256c70.7 0 128-57.3 128-128S294.7 0 224 0S96 57.3 96 128s57.3 128 128 128zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z"></path></svg>"""
HOURGLASS_SVG = """<svg class="timer-icon" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="currentColor" d="M360 0H24A24 24 0 000 24v40a24 24 0 0024 24h336a24 24 0 0024-24V24A24 24 0 00360 0zM24 424h336a24 24 0 0024-24v-40a24 24 0 00-24-24H24a24 24 0 00-24 24v40a24 24 0 0024 24zM32 128h320v256H32V128z"></path><path class="sand" fill="currentColor" d="M32 128h320v100c0 44.18-35.82 80-80 80H112c-44.18 0-80-35.82-80-80V128z"></path></svg>"""

@app.route("/")
def setup_page():
    session.clear()
    return render_template("setup.html", categories=WORDS_DATABASE.keys())

@app.route("/start", methods=["POST"])
def start_game():
    try:
        num_players = int(request.form["num_players"])
        num_spies = int(request.form["num_spies"])
        player_names = request.form.getlist("player_names")
        selected_categories = request.form.getlist("categories")

        session["game_mode"] = request.form.get("game_mode", "free")
        session["time_limit"] = int(request.form.get("time_limit", 0)) if session["game_mode"] == "timed" else 0
        session["num_spies"] = num_spies
        session["selected_categories"] = selected_categories

        if num_spies >= num_players or not selected_categories or len(player_names) != num_players:
            return redirect(url_for("setup_page"))

        players_list = [{"name": name} for name in player_names]
        session["players_list"] = players_list
        session["used_words"] = []

        return redirect(url_for("rematch_game"))
        
    except (ValueError, KeyError):
        return redirect(url_for("setup_page"))

@app.route("/rematch")
def rematch_game():
    if "players_list" not in session or "selected_categories" not in session:
        return redirect(url_for("setup_page"))

    players = session["players_list"]
    selected_categories = session["selected_categories"]
    num_spies = session["num_spies"]
    num_players = len(players)
    used_words = session.get("used_words", [])

    full_word_pool = [word for cat in selected_categories for word in WORDS_DATABASE.get(cat, [])]
    available_words = [word for word in full_word_pool if word not in used_words]

    if not available_words:
        session["used_words"] = []
        available_words = full_word_pool

    secret_word = random.choice(available_words)
    used_words.append(secret_word)
    session["used_words"] = used_words

    roles = ["جاسوس"] * num_spies + [secret_word] * (num_players - num_spies)
    random.shuffle(roles)
    
    random.shuffle(players)
    for i, player in enumerate(players):
        player["role"] = roles[i]
    
    session["players"] = players
    session["current_player_index"] = 0
    return redirect(url_for("game_page"))


@app.route("/game")
def game_page():
    if "players" not in session: return redirect(url_for("setup_page"))
    
    player_index = session.get("current_player_index", 0)
    players = session.get("players", [])

    if player_index >= len(players):
        return render_template("game.html", 
            page_type="final_screen", 
            game_mode=session.get("game_mode"),
            time_limit=session.get("time_limit", 300), 
            hourglass_svg=HOURGLASS_SVG
        )
    else:
        current_player = players[player_index]
        is_spy = current_player["role"].lower() == "جاسوس"
        context = {
            "page_type": "card_reveal",
            "player_name": current_player["name"],
            "role": current_player["role"],
            "is_spy": is_spy,
            "role_icon": SPY_SVG if is_spy else CITIZEN_SVG,
        }
        return render_template("game.html", **context)
        
@app.route("/timesup")
def times_up():
    """ Renders the time's up page with rematch options """
    if "players" not in session:
        return redirect(url_for("setup_page"))
    return render_template("game.html", page_type="times_up")

@app.route("/api/next_turn", methods=["POST"])
def next_turn():
    if "players" not in session: return jsonify({"error": "Game not started"}), 400
    session["current_player_index"] += 1
    session.modified = True
    return jsonify({"success": True})

if __name__ == "__main__":
    print("="*50)
    print(">>> Spy Game PRO (v15 TimesUp) در حال اجرا است...")
    print(f">>> برای شروع، آدرس زیر را در مرورگر خود باز کنید: http://127.0.0.1:5000")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)