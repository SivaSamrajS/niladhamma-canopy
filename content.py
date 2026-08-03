# -*- coding: utf-8 -*-
"""
Every page's prose, in both languages, side by side.

build.py is the renderer and holds no copy of its own beyond the shared chrome
strings in its UI dict. Keeping each Tamil block next to its English makes drift
between the two obvious at a glance.

The Tamil is the authoritative text. The English on content pages is a
translation and is marked as such on the pages that carry doctrinal material.
"""

# Some blocks are shared by both languages (proper nouns, addresses); those are
# written once and repeated deliberately rather than being special-cased.

C = {

    # ===================================================================== home
    "home.meta": {
        "ta": "நிலாதம்மா: சென்னையில் 2012 முதல் தொடர் பௌர்ணமி கூட்டங்கள், "
              "பௌத்தத் திருமணங்கள், அம்பேத்கர் இரவுப் பாடசாலைகள். தம்மபதம் "
              "முப்பத்தோர் நாள் கதைகள் தமிழில்.",
        "en": "A Buddhist sangha in Chennai. Full moon gatherings every month "
              "since 2012, Buddhist marriages, Ambedkar night schools, and the "
              "Dhammapada story collections.",
    },
    "home.city": {"ta": "சென்னை", "en": "Chennai"},
    "home.lede": {
        "ta": "நாங்கள் பௌத்தர்கள். சுதந்திரம், சமத்துவம், சகோதரத்துவம் "
              "காட்டும் தம்மப்பாதையில் பயணிக்கிறோம். 2012 முதல் ஒவ்வொரு "
              "{link} குடும்பமாகக் கூடி, கலைகளைச் சமத்துவக் கருவிகளாக்கி "
              "இயங்கி வருகிறோம்.",
        "en": "We are Buddhists. We tread the Dhamma path founded on liberty, "
              "equality and fraternity. Since 2012 we have gathered as "
              "families on every {link}, making the arts a tool of equality.",
    },
    "home.lede.link": {"ta": "பௌர்ணமி நாளிலும்", "en": "full moon day"},
    "home.cta1": {"ta": "தம்மக் கதைகளைப் படிக்க", "en": "Read the Dhamma stories"},
    "home.cta2": {"ta": "நம்மைப் பற்றி", "en": "About us"},

    "home.stat1": {"ta": "முதல் தொடர் பௌர்ணமி கூட்டம்",
                   "en": "First of the continuous full moon gatherings"},
    "home.stat2": {"ta": "தொடர் பௌர்ணமி கூட்டங்கள், ஜூலை 2026 வரை",
                   "en": "Full moon gatherings held, to July 2026"},
    "home.stat3": {"ta": "தம்மபதம் நாள்தோறும் ஒரு கதை",
                   "en": "Dhammapada stories, one for each day"},
    "home.stat4": {"ta": "தொகுக்கப்பட்ட பௌத்தப் பெயர்கள்",
                   "en": "Buddhist names collected"},

    "home.kathai.sub": {
        "ta": "ஒவ்வொரு நாளும் ஒரு பௌத்தக் கதை. புத்தர், அவர் சீடர்கள், "
              "மகாபஜாபதி, அசோகர், அம்பேத்கர்.",
        "en": "One Buddhist story for each day. The Buddha, his disciples, "
              "Mahapajapati, Ashoka, Ambedkar.",
    },
    "home.kathai.all": {"ta": "31 நாட்களும்", "en": "All 31 days"},

    "home.work.h": {"ta": "நாங்கள் என்ன செய்கிறோம்", "en": "What we do"},
    "home.work.sub": {
        "ta": "பண்பாட்டு அறிதலும் செயலும் பயிற்சியும், தொடர் வேலைகளால் அமைதியாக.",
        "en": "Cultural understanding, action and practice, carried quietly by "
              "steady work.",
    },
    "home.work.readall": {"ta": "முழுவதும் படிக்க", "en": "Read the whole story"},

    "work.pournami.h": {"ta": "தொடர் பௌர்ணமி கூட்டம்",
                        "en": "The continuous full moon gathering"},
    "work.pournami.p": {
        "ta": "உபோசத நாளாக, விழிப்புக்கும் தியானத்துக்கும் உரிய நாளாக "
              "ஒவ்வொரு முழுநிலவிலும் குடும்பமாகக் கூடுகிறோம்.",
        "en": "We gather as families on every full moon, keeping it as an "
              "uposatha day given to wakefulness and meditation.",
    },
    "work.marriage.h": {"ta": "பௌத்தத் திருமணங்கள்", "en": "Buddhist marriages"},
    "work.marriage.p": {
        "ta": "மகாமங்கள முறையில் திருமணங்களை ஒருங்கிணைத்து, அரசிதழ்ப் பதிவு "
              "வரை உடன் நிற்கிறோம்.",
        "en": "We organise marriages in the Mahamangala rite and stay with the "
              "families through to registration in the government gazette.",
    },
    "work.school.h": {"ta": "அம்பேத்கர் இரவுப் பாடசாலைகள்",
                      "en": "Ambedkar night schools"},
    "work.school.p": {
        "ta": "பல இடங்களில் இரவுப் பாடசாலைகளை நடத்தி, குழந்தைகளுக்கான தொடர் "
              "கல்விக் களமாக இருக்கிறோம்.",
        "en": "We run night schools in several places, a steady ground of "
              "learning for children.",
    },
    "work.arts.h": {"ta": "கலைகள் சமத்துவக் கருவிகள்",
                    "en": "The arts as tools of equality"},
    "work.arts.p": {
        "ta": "நாடகம், ஆடல், பாடல், இசை, நிகழ்த்துதல், தொழில்நுட்பம் என "
              "தொடர் பயிற்சிக்கான களம்.",
        "en": "Theatre, dance, song, music, performance and technology: a "
              "ground for continuous practice.",
    },
    "work.cert.h": {"ta": "சான்றிதழும் உரிமையும்",
                    "en": "Certificates and rights"},
    "work.cert.p": {
        "ta": "பௌத்தமேற்ற பட்டியலினத்தினர் சமூகச் சான்றிதழ் பெறுவதில் உள்ள "
              "சிக்கல்களைத் தெளிவுபடுத்துகிறோம்.",
        "en": "We clear up the difficulties Scheduled Caste Buddhists meet in "
              "obtaining a community certificate.",
    },
    "work.recover.h": {"ta": "மீட்டுருவாக்கமும் ஆவணமும்",
                       "en": "Recovery and record"},
    "work.recover.p": {
        "ta": "மறைக்கப்பட்ட, சிதைக்கப்பட்ட பௌத்த அடையாளங்களை மூத்த "
              "வழிகாட்டிகளிடமிருந்து பெற்று மறுகட்டமைக்கிறோம்.",
        "en": "We gather the Buddhist marks that were hidden and broken from "
              "our elders, and rebuild them.",
    },

    "home.moon.eyebrow": {"ta": "பௌர்ணமி", "en": "The full moon"},
    "home.moon.h": {"ta": "முழுநிலவு ஏன் சிறப்பான நாள்",
                    "en": "Why the full moon is a special day"},
    "home.moon.p": {
        "ta": "பௌர்ணமி பௌத்த மரபில் மிகச் சிறப்பான நாள். உபோசத நாட்களாக, "
              "விழிப்புக்கும் தியானத்துக்கும் உரிய நாட்களாகக் "
              "கடைப்பிடிக்கப்படுபவை. குறிப்பாக ஆடி மாத முழுநிலவை, புத்தர் "
              "சாரநாத்தில் தம் முதல் உபதேசத்தை தம்மச் சக்கரம் உருட்டிய "
              "நாளோடும், சங்கம் பிறந்த நாளோடும் மரபு இணைக்கிறது. அந்தக் "
              "கதையை {link} படிக்கலாம்.",
        "en": "The full moon is the most significant day in the Buddhist "
              "tradition. These are kept as uposatha days, given to wakefulness "
              "and meditation. The full moon of Asalha in particular is joined "
              "by tradition to the day the Buddha turned the wheel of Dhamma in "
              "his first discourse at Sarnath, and to the day the Sangha was "
              "born. You can read that story {link}.",
    },
    "home.moon.link": {"ta": "நாள் 6 கதையில்", "en": "as the day 6 story"},
    "home.moon.cta": {"ta": "நிகழ்வுகளைப் பார்க்க", "en": "See what is on"},

    "home.recent.h": {"ta": "சமீபத்திய பதிவுகள்", "en": "Recent writings"},
    "home.recent.sub": {"ta": "சங்கத்தின் நிகழ்வுகள், அறிவிப்புகள், கட்டுரைகள்.",
                        "en": "The sangha's events, announcements and articles."},
    "home.res.h": {"ta": "வளங்கள்", "en": "Resources"},
    "home.res.sub": {"ta": "சங்கம் தொகுத்து வழங்கும் பயன்பாட்டுப் பக்கங்கள்.",
                     "en": "Practical pages the sangha has put together."},

    # ==================================================================== about
    "about.meta": {
        "ta": "நிலாதம்மா பற்றி: சுதந்திரம், சமத்துவம், சகோதரத்துவம் காட்டும் "
              "தம்மப்பாதை. 2012 முதல் சென்னையில் தொடர் பௌர்ணமி கூட்டங்கள்.",
        "en": "About Niladhamma: the Dhamma path of liberty, equality and "
              "fraternity. Full moon gatherings in Chennai since 2012.",
    },
    "about.eyebrow": {"ta": "நம்மைப் பற்றி &middot; About",
                      "en": "About &middot; நம்மைப் பற்றி"},
    "about.h1": {"ta": "நாங்கள் பௌத்தர்கள்", "en": "We are Buddhists"},
    "about.lede": {"ta": "சமத்துவத்திற்கு மேலான ஆற்றல் இல்லை என்பதை அறிவோம்.",
                   "en": "We hold that there is nothing greater than equality."},
    "about.p1": {
        "ta": "சுதந்திரம், சமத்துவம், சகோதரத்துவம் காட்டும் தம்மப்பாதையில் "
              "பயணிக்கிறோம். கலைகளைச் சமத்துவக் கருவிகளாக்கி, குழந்தைகள், "
              "நண்பர்கள், குடும்பங்கள் என இயங்கி வருகிறோம்.",
        "en": "We tread the Dhamma path founded on liberty, equality and "
              "fraternity. Working with children, friends and families, we have "
              "made the arts a tool of equality.",
    },
    "about.p2": {
        "ta": "சமத்துவத் தேடலில் பௌத்தத்தைப் பல வழிகளிலும் தேடியடைந்த "
              "அத்தனை நல்ல மனிதர்களுக்கும் நன்றி பாராட்டும் விதமாக, 2012 "
              "முதல் எல்லா {link} குடும்பமாகக் கூடி வருகிறோம்.",
        "en": "In gratitude to all the good people who found their way to "
              "Buddhism by many roads in the search for equality, we have "
              "gathered as families on every {link} since 2012.",
    },
    "about.p2.link": {"ta": "பௌர்ணமி தினங்களிலும்", "en": "full moon day"},
    "about.h.action": {"ta": "தொடர் நடவடிக்கை", "en": "Steady work"},
    "about.p3": {
        "ta": "பௌத்தம் ஏற்கும் நிகழ்ச்சிகளை ஒருங்கிணைத்தல், அரசிதழில் பதிவு "
              "செய்வது, {link1} என்று ஒரு தொடர் நடவடிக்கையில் "
              "நூற்றுக்கணக்கான குடும்பங்களாக வலிமை பெற்றிருக்கிறோம். "
              "பாபாசாகேப் அம்பேத்கர் இரவுப் பாடசாலைகள் நடத்தி வருகிறோம். "
              "பௌத்தப் பண்பாட்டு நிகழ்வுகளை ஒருங்கிணைக்கின்றோம்; குறிப்பாக "
              "{link2} பல நடத்தியிருக்கின்றோம்.",
        "en": "Organising ceremonies of conversion to Buddhism, registering "
              "them in the government gazette, {link1}: through this steady "
              "work hundreds of families have gained strength together. We run "
              "Babasaheb Ambedkar night schools. We organise Buddhist cultural "
              "events, and have conducted many {link2}.",
    },
    "about.p3.link1": {"ta": "சான்றிதழ்களைப் பெறுவது",
                       "en": "obtaining certificates"},
    "about.p3.link2": {"ta": "பௌத்தத் திருமணங்கள்", "en": "Buddhist marriages"},
    "about.h.recover": {"ta": "மீட்டுருவாக்கம்", "en": "Recovery"},
    "about.p4": {
        "ta": "மறைக்கப்பட்ட, சிதைக்கப்பட்ட பௌத்த அடையாளங்களை, பௌத்த "
              "வாழ்வியலை, வாழும் வாழ்க்கையிலிருந்தும், மிச்சமிருக்கும் "
              "அடையாளங்களிலிருந்தும், இழந்துபட்ட செல்வங்களிலிருந்தும், மூத்த "
              "வழிகாட்டிகளிடமிருந்தும் பெறுகிறோம், மறுகட்டமைப்பு செய்கிறோம். "
              "அந்த மீட்டுருவாக்கத்தின் ஒரு பகுதிதான் {link} தொகுப்பு.",
        "en": "The Buddhist marks that were hidden and broken, and the Buddhist "
              "way of living, we gather back from life as it is lived, from the "
              "marks that remain, from what was lost, and from our elders, and "
              "we rebuild them. The {link} collection is one part of that "
              "recovery.",
    },
    "about.p4.link": {"ta": "தம்மபதம்: முப்பத்தோர் நாள்",
                      "en": "Dhammapada: Thirty-one Days"},
    "about.p5": {
        "ta": "கலைகள் சார்ந்த பயிற்சிகள், நாடகம், ஆடல், பாடல், இசை, "
              "நிகழ்த்துதல், தொழில்நுட்பம் என தொடர் பயிற்சிக்கான களமாக "
              "ஆகியிருக்கிறோம். அனைவரிடமும் சேர்ந்து செயலாற்றுதல் என்பதை "
              "நெறியாகக் கொண்டிருக்கிறோம்.",
        "en": "We have become a ground for continuous practice in the arts: "
              "theatre, dance, song, music, performance, technology. Working "
              "together with everyone is our principle.",
    },
    "about.p6": {
        "ta": "பண்பாட்டு அறிதலும் செயலும் பயிற்சியும் பௌத்த வாழ்க்கை "
              "முறையும் தனிமனித வாழ்வையும் சமூகத்தையும் வளமாக்கி உயர்த்தும் "
              "என்பதை நேரில் கண்டு வருகிறோம்.",
        "en": "We have seen for ourselves that cultural understanding, action, "
              "practice and a Buddhist way of life enrich and raise both the "
              "individual life and the society around it.",
    },
    "about.quote": {
        "ta": "&ldquo;ஏஹி பஸ்ஸிகோ&rdquo; &middot; வாருங்கள், வந்து கண்டுணருங்கள்.",
        "en": "&ldquo;Ehipassiko&rdquo; &middot; come and see for yourself.",
    },
    "about.principles": {"ta": "சங்கத்தின் நெறி", "en": "Our principles"},
    "about.pr1": {"ta": "சமத்துவத்திற்கு மேலான ஆற்றல் இல்லை",
                  "en": "There is nothing greater than equality"},
    "about.pr2": {"ta": "கலைகள் சமத்துவக் கருவிகள்",
                  "en": "The arts are tools of equality"},
    "about.pr3": {"ta": "அனைவரிடமும் சேர்ந்து செயலாற்றுதல்",
                  "en": "Work together with everyone"},
    "about.pr4": {"ta": "தொடர் வேலைகளால் அமைதியாய் பதில்",
                  "en": "Answer quietly, through steady work"},
    "about.where": {"ta": "எங்கே கூடுகிறோம்", "en": "Where we gather"},
    "about.when": {"ta": "ஒவ்வொரு பௌர்ணமியிலும் மாலை 6 மணி முதல்.",
                   "en": "Every full moon day, from 6pm."},
    "about.contactlink": {"ta": "தொடர்பு விவரங்கள்", "en": "Contact details"},
    "about.caption": {
        "ta": "நாகப்பட்டினம் புத்தர், சோழர் காலம், 12ஆம் நூற்றாண்டு. தமிழ் "
              "மண்ணின் பௌத்த அடையாளங்களில் ஒன்று.",
        "en": "The Nagapattinam Buddha, Chola period, 12th century. One of the "
              "Buddhist marks of the Tamil land.",
    },
    "about.heritage.h": {"ta": "பௌத்த அடையாளங்கள்", "en": "Buddhist marks"},
    "about.heritage.sub": {
        "ta": "சங்கம் மீட்டுருவாக்கும் மரபின் சில அடையாளங்கள்.",
        "en": "Some marks of the tradition the sangha is recovering.",
    },
    "about.credits": {
        "ta": "படங்கள் விக்கிமீடியா காமன்ஸிலிருந்து. உரிமை விவரங்கள் "
              "CREDITS.md கோப்பில்.",
        "en": "Images from Wikimedia Commons. Licence details in CREDITS.md.",
    },
    "about.readon": {"ta": "தொடர்ந்து படிக்க", "en": "Read on"},

    # =================================================================== kathai
    "kathai.meta": {
        "ta": "ஜூலை 1 முதல் 31 வரை ஒவ்வொரு நாளும் ஒரு பௌத்தக் கதை. புத்தர், "
              "அவர் சீடர்கள், மகாபஜாபதி, அசோகர், அம்பேத்கர். தம்மக்கருத்து, "
              "அம்பேத்கர் இணைப்பு, ஆதாரத்துடன் தமிழில்.",
        "en": "One Buddhist story for each day from 1 to 31 July. The Buddha, "
              "his disciples, Mahapajapati, Ashoka, Ambedkar. Each with a "
              "Dhamma insight, an Ambedkar connection, and its source.",
    },
    "kathai.lede": {
        "ta": "ஒவ்வொரு நாளும் ஒரு பௌத்தக் கதை. புத்தர் &middot; அவர் சீடர்கள் "
              "&middot; மகாபஜாபதி &middot; அசோகர் &middot; அம்பேத்கர்.",
        "en": "One Buddhist story for each day. The Buddha &middot; his "
              "disciples &middot; Mahapajapati &middot; Ashoka &middot; Ambedkar.",
    },
    "kathai.meta1": {"ta": "ஜூலை 1 முதல் 31 வரை", "en": "1 to 31 July"},
    "kathai.meta2": {"ta": "31 கதைகள்", "en": "31 stories"},
    "kathai.meta3": {"ta": "ஒவ்வொன்றிலும் ஆதாரம்", "en": "Each with its source"},
    "kathai.intro.h": {"ta": "அறிமுக உரை", "en": "Opening letter"},
    "kathai.days.h": {"ta": "முப்பத்தோர் நாள்", "en": "Thirty-one days"},
    "kathai.days.sub": {
        "ta": "ஒரு நாளைத் தேர்ந்து படிக்கவும். ஒவ்வொரு கதையிலும் "
              "தம்மக்கருத்து, அம்பேத்கர் இணைப்பு, ஆதாரம்.",
        "en": "Choose a day and read. Each story carries a Dhamma insight, an "
              "Ambedkar connection, and its source.",
    },
    "kathai.search": {"ta": "தலைப்பில் தேட", "en": "Search by title"},
    "kathai.empty": {"ta": "இந்தத் தேடலுக்குக் கதைகள் எதுவும் இல்லை.",
                     "en": "No stories match that search."},
    "kathai.about.h": {"ta": "இத்தொகுப்பு பற்றி", "en": "About this collection"},

    "kathai.coll.meta": {
        "ta": "{label}: ஒவ்வொரு நாளும் ஒரு பௌத்தக் கதை, {month} 1 முதல் 31 "
              "வரை. ஒவ்வொன்றிலும் தம்மக்கருத்து, அம்பேத்கர் இணைப்பு, ஆதாரம். "
              "நிலாதம்மா தொகுத்தது.",
        "en": "{label}: one Buddhist story for each day from 1 to 31 {month}, "
              "each with a Dhamma insight, an Ambedkar connection and its "
              "source. Collected by Niladhamma.",
    },
    "kathai.hub.meta": {
        "ta": "தம்மபதம்: முப்பத்தோர் நாள். ஒவ்வொரு மாதமும் ஒரு தொகுப்பு, "
              "ஒவ்வொரு நாளும் ஒரு பௌத்தக் கதை. தம்மக்கருத்து, அம்பேத்கர் "
              "இணைப்பு, ஆதாரத்துடன் தமிழில்.",
        "en": "Dhammapada: Thirty-one Days. A collection each month, one "
              "Buddhist story for each day, with a Dhamma insight, an Ambedkar "
              "connection and its source.",
    },
    "kathai.hub.lede": {
        "ta": "ஒவ்வொரு மாதமும் ஒரு தொகுப்பு. ஒவ்வொரு நாளும் ஒரு கதை. "
              "சங்கக் கூட்டத்தில் தினமும் வாசிக்கத் தொகுக்கப்பட்டவை.",
        "en": "A collection each month, a story each day, put together to be "
              "read aloud at the gathering.",
    },
    "kathai.hub.h": {"ta": "தொகுப்புகள்", "en": "The collections"},
    "kathai.hub.sub": {
        "ta": "ஒரு மாதத்தைத் தேர்ந்து படிக்கவும். புதிய கதைகள் அந்தந்த "
              "நாளில் வெளியாகும்.",
        "en": "Choose a month and read. New stories appear on their own day.",
    },
    "kathai.hub.count": {"ta": "{n} / {total} கதைகள் வெளியாகியுள்ளன",
                         "en": "{n} of {total} stories released"},
    "kathai.drip": {
        "ta": "இத்தொகுப்பு நாளுக்கு ஒரு கதையாக வெளியாகிறது. இதுவரை {n} "
              "வெளியாகியுள்ளன; மீதமுள்ளவை அந்தந்த நாளில் சேரும்.",
        "en": "This collection is released a day at a time. {n} of {total} so "
              "far; the rest arrive on their own dates.",
    },

    "story.collection": {
        "ta": "{link} தொகுப்பின் {n}ஆவது கதை. ஜூலை 1 முதல் 31 வரை, ஒவ்வொரு "
              "நாளும் ஒரு பௌத்தக் கதை.",
        "en": "Story {n} of the {link} collection. One Buddhist story for each "
              "day, from 1 to 31 July.",
    },
    "story.seeall": {"ta": "31 நாட்களும் பார்க்க", "en": "See all 31 days"},
    "story.at.h": {"ta": "சங்கக் கூட்டத்தில்", "en": "At the gathering"},
    "story.at.p": {
        "ta": "இக்கதைகள் {venue} இல் பௌர்ணமி கூட்டங்களில் "
              "வாசிக்கப்படுகின்றன. {link}.",
        "en": "These stories are read aloud at the full moon gatherings at "
              "{venue}. {link}.",
    },
    "story.at.link": {"ta": "நிகழ்வுகளைப் பார்க்க", "en": "See what is on"},

    # =================================================================== events
    "events.at.h": {"ta": "ஒரு பௌர்ணமி கூட்டத்தில் என்ன நடக்கும்",
                    "en": "What happens at a full moon gathering"},
    "events.at.sub": {
        "ta": "முதல் முறை வருபவர்களுக்கு. சுமார் இரண்டு மணி நேரம்; "
              "எந்தத் தயாரிப்பும் தேவையில்லை.",
        "en": "For anyone coming for the first time. About two hours, and "
              "nothing to prepare.",
    },
    "events.at.1t": {"ta": "வந்தனையும் திரிசரணமும்", "en": "Homage and the three refuges"},
    "events.at.1d": {
        "ta": "புத்தம், தம்மம், சங்கம், மூன்றையும் சரணடையும் பாலி வரிகளை "
              "எல்லோரும் சேர்ந்து சொல்கிறோம். தெரியாவிட்டால் கேட்டிருந்தாலே "
              "போதும்.",
        "en": "Everyone says the Pali lines of refuge in the Buddha, the "
              "Dhamma and the Sangha together. If you do not know them, "
              "listening is enough.",
    },
    "events.at.2t": {"ta": "பஞ்சசீலம்", "en": "The five precepts"},
    "events.at.2d": {
        "ta": "ஐந்து சீலங்களை ஏற்கும் வரிகள். இவை கட்டளைகள் அல்ல; "
              "நாமே எடுத்துக்கொள்ளும் பயிற்சி.",
        "en": "The lines in which the five precepts are undertaken. They are "
              "not commandments but a training we take on ourselves.",
    },
    "events.at.3t": {"ta": "தியானம்", "en": "Meditation"},
    "events.at.3d": {
        "ta": "பத்து முதல் இருபது நிமிடங்கள் அமைதியான தியானம். நாற்காலியில் "
              "அமர்ந்தும் செய்யலாம்.",
        "en": "Ten to twenty minutes of quiet meditation. Sitting on a chair "
              "is perfectly fine.",
    },
    "events.at.4t": {"ta": "தம்மக் கதை வாசிப்பு", "en": "A Dhamma story, read aloud"},
    "events.at.4d": {
        "ta": "அன்றைய கதையை ஒருவர் உரக்க வாசிக்கிறார்; பிறகு அதைப் பற்றிப் "
              "பேசுகிறோம். {link} ஆன்லைனிலும் படிக்கலாம்.",
        "en": "Someone reads the day's story aloud, and then we talk about it. "
              "You can also read {link} online.",
    },
    "events.at.4l": {"ta": "அதே கதைகளை", "en": "the same stories"},
    "events.at.5t": {"ta": "கலை நிகழ்ச்சிகளும் தானமும்", "en": "Performance and dana"},
    "events.at.5d": {
        "ta": "குழந்தைகளின் பாடல், நாடகம், சில நாட்களில் தானம். "
              "முடிவில் எல்லோரும் சேர்ந்து உணவு.",
        "en": "Songs and theatre from the children, dana on some days, and "
              "a shared meal at the end.",
    },
    "events.bring.h": {"ta": "எடுத்து வர வேண்டியது", "en": "What to bring"},
    "events.bring.p": {
        "ta": "எதுவும் இல்லை. முன்பதிவு இல்லை, கட்டணம் இல்லை, உடைக் "
              "கட்டுப்பாடு இல்லை. தரையில் அமர விரிப்புகள் உண்டு; "
              "நாற்காலிகளும் உண்டு. குழந்தைகள் வரவேற்கப்படுகிறார்கள்.",
        "en": "Nothing. No booking, no fee, no dress code. There are mats on "
              "the floor and chairs as well. Children are welcome.",
    },
    "events.meta": {
        "ta": "சென்னையில் பௌர்ணமி பௌத்தக் கூட்டம்: அசோக் நகர் புத்த "
              "விஹாரில் ஒவ்வொரு முழுநிலவிலும் மாலை 6 மணி முதல். முன்பதிவு "
              "இல்லை, கட்டணம் இல்லை. வரவிருக்கும் நாட்கள் நாட்காட்டியில்.",
        "en": "Buddhist full moon gathering in Chennai, at Ashok Nagar Buddha "
              "Vihar from 6pm. No booking, no fee. Calendar of upcoming dates "
              "and observances.",
    },
    "events.title": {"ta": "பௌர்ணமி கூட்டமும் நாட்காட்டியும்",
                     "en": "Full moon gatherings and calendar"},
    "events.h1": {"ta": "கூடுகிறோம், கற்கிறோம், வளர்கிறோம்",
                  "en": "We gather, we learn, we grow"},
    "events.lede": {
        "ta": "2012 முதல் தொடர்ச்சியாக நடந்துவரும் பௌர்ணமி கூட்டங்களும், "
              "ஆண்டு முழுவதும் நிகழும் பண்பாட்டு நிகழ்வுகளும்.",
        "en": "The full moon gatherings held without a break since 2012, and "
              "the cultural events that run through the year.",
    },
    "cal.h": {"ta": "பௌத்த நாட்காட்டி", "en": "Buddhist calendar"},
    "cal.sub": {"ta": "பௌர்ணமி நாட்கள், பௌத்த மரபு விழாக்கள், அம்பேத்கரிய "
                      "நினைவு நாட்கள்.",
                "en": "Full moon days, observances of the Buddhist tradition, "
                      "and Ambedkarite anniversaries."},
    "cal.sub.h": {"ta": "இந்த நாட்காட்டியை உங்கள் நாட்காட்டியில் சேர்க்க",
                  "en": "Add this calendar to your own"},
    "cal.sub.p": {
        "ta": "கீழுள்ள இணைப்பைச் சேர்த்தால், பௌர்ணமி கூட்டங்களும் நினைவு "
              "நாட்களும் உங்கள் நாட்காட்டியில் தானாகத் தோன்றும். தளம் "
              "தினமும் புதுப்பிக்கப்படுவதால், சந்தா செலுத்தியவர்களுக்குப் "
              "புதிய நாட்களும் தானே சேரும்.",
        "en": "Subscribe and the full moon gatherings and anniversaries appear "
              "in your own calendar. The site rebuilds daily, so a "
              "subscription picks up new dates on its own.",
    },
    "cal.sub.google": {"ta": "Google நாட்காட்டியில் சேர்க்க",
                       "en": "Add to Google Calendar"},
    "cal.sub.file": {"ta": ".ics கோப்பைப் பதிவிறக்க",
                     "en": "Download the .ics file"},
    "cal.sub.note": {
        "ta": "Apple Calendar, Outlook உள்ளிட்ட எந்த நாட்காட்டியிலும் "
              "இந்த முகவரியைச் சந்தாவாகச் சேர்க்கலாம்.",
        "en": "Any calendar that reads iCalendar, including Apple Calendar and "
              "Outlook, can subscribe to this address.",
    },
    "cal.next": {"ta": "அடுத்த பௌர்ணமி", "en": "Next full moon"},
    "cal.up.h": {"ta": "வரவிருக்கும் நிகழ்வுகள்", "en": "What is coming up"},
    "cal.up.sub": {"ta": "பௌர்ணமி கூட்டங்களும் நினைவு நாட்களும், நாள் வரிசையில்.",
                   "en": "Full moon gatherings and anniversaries, in date order."},
    "cal.col.kind": {"ta": "வகை", "en": "Kind"},
    "cal.kind.moon": {"ta": "பௌர்ணமி", "en": "Full moon"},
    "cal.kind.mem": {"ta": "நினைவு நாள்", "en": "Anniversary"},
    "cal.at6": {"ta": "மாலை 6 மணி முதல்", "en": "from 6pm"},
    "cal.moons.h": {"ta": "வரவிருக்கும் பௌர்ணமி நாட்கள்",
                    "en": "Upcoming full moon days"},
    "cal.col.date": {"ta": "நாள்", "en": "Date"},
    "cal.col.time": {"ta": "முழுநிலவு நேரம்", "en": "Moment of full moon"},
    "cal.read": {"ta": "இதைப் பற்றிய பதிவு", "en": "Read our post"},
    "cal.shifted": {"ta": "முழுநிலவு அடுத்த நாள் அதிகாலை",
                    "en": "full moon falls in the small hours of the next day"},
    "cal.col.event": {"ta": "நிகழ்வு", "en": "Gathering"},
    "cal.gathering": {"ta": "தொடர் பௌர்ணமி கூட்டம்",
                      "en": "continuous full moon gathering"},
    "cal.nth": {"ta": "வது", "en": "th"},
    "cal.note1": {
        "ta": "2026 ஜூலை பௌர்ணமி சங்கத்தின் 178வது தொடர் கூட்டம்; அதிலிருந்து "
              "எண்ணிக்கை தொடர்கிறது. முழுநிலவின் வானியல் நேரம் இந்திய "
              "நேரத்தில் தரப்பட்டுள்ளது. மரபுவழி உபோசத நாள் உள்ளூர் சந்திர "
              "கணக்கைப் பொறுத்து ஒரு நாள் முன்னும் பின்னும் அமையலாம்; "
              "சங்கத்தின் கூட்ட நாளுக்கு {link} பாருங்கள்.",
        "en": "The July 2026 full moon was the sangha's 178th continuous "
              "gathering; the count runs on from there. The astronomical moment "
              "of the full moon is given in Indian Standard Time. The uposatha "
              "day as traditionally observed can fall a day either side, "
              "depending on the local lunar reckoning; for the gathering date "
              "see {link}.",
    },
    "cal.note1.link": {"ta": "அறிவிப்புகளைப்", "en": "the announcements"},
    "cal.lunar.h": {"ta": "பௌத்த மரபு விழாக்கள்",
                    "en": "Observances of the Buddhist tradition"},
    "cal.col.festival": {"ta": "விழா", "en": "Observance"},
    "cal.col.when": {"ta": "காலம்", "en": "When"},
    "cal.col.note": {"ta": "குறிப்பு", "en": "Note"},
    "cal.note2": {
        "ta": "இவை சந்திர மாதத்தைப் பின்பற்றுவதால் ஒவ்வொரு ஆண்டும் நாள் "
              "மாறும். எந்தப் பௌர்ணமி எந்த விழா என்பதை பஞ்சாங்கம் "
              "பார்த்தே உறுதிசெய்ய முடியும்; அதனால் இங்கு நிலையான தேதி "
              "தரப்படவில்லை. சங்கத்தின் அறிவிப்பே இறுதியானது.",
        "en": "These follow the lunar month, so the date moves each year. "
              "Which full moon carries which observance can only be settled "
              "against a panchanga, so no fixed date is given here. The "
              "sangha's own announcement is authoritative.",
    },
    "cal.fixed.h": {"ta": "அம்பேத்கரிய நினைவு நாட்கள்",
                    "en": "Ambedkarite anniversaries"},

    "const.h": {"ta": "அரசியலமைப்பும் அம்பேத்கரும்",
                "en": "Ambedkar and the Constitution"},
    "const.sub": {
        "ta": "நவம்பர் 26, ஜனவரி 26, இரண்டும் ஏன் வெவ்வேறு நாட்கள் என்பதும், "
              "அந்த ஆவணம் எழுத எவ்வளவு காலம் ஆனது என்பதும்.",
        "en": "Why 26 November and 26 January are different days, and how long "
              "the document took to write.",
    },
    "const.note": {
        "ta": "அரசியலமைப்பு அவை 1946 டிசம்பர் 9 முதல் 1949 நவம்பர் 26 வரை "
              "இரண்டு ஆண்டுகள் பதினொரு மாதங்கள் பதினெட்டு நாட்கள் "
              "உழைத்தது. வரைவுக் குழு மட்டும் 141 நாட்கள் கூடியது. "
              "எண்கள் அவையின் அதிகாரப்பூர்வப் பதிவிலிருந்து.",
        "en": "The Constituent Assembly worked for two years, eleven months "
              "and eighteen days, from 9 December 1946 to 26 November 1949. "
              "The Drafting Committee alone sat for 141 days. The figures are "
              "from the Assembly's own record.",
    },
    "events.kinds.h": {"ta": "என்னென்ன நிகழ்வுகள்", "en": "What we hold"},
    "events.kinds.sub": {"ta": "ஆண்டு முழுவதும் தொடரும் மூன்று வகை.",
                         "en": "Three kinds, running through the year."},
    "events.k1.h": {"ta": "தொடர் பௌர்ணமி", "en": "The full moon gathering"},
    "events.k1.p": {
        "ta": "ஒவ்வொரு முழுநிலவிலும் {venue} இல், மாலை 6 மணி முதல். வந்தனை, "
              "தியானம், {link}, கலை நிகழ்ச்சிகள்.",
        "en": "Every full moon at {venue}, from 6pm. Homage, meditation, "
              "{link}, and performances.",
    },
    "events.k1.link": {"ta": "தம்மக் கதை வாசிப்பு", "en": "a Dhamma story read aloud"},
    "events.k2.h": {"ta": "பண்பாட்டு விழாக்கள்", "en": "Cultural observances"},
    "events.k2.p": {
        "ta": "புத்த பூர்ணிமா, அசோக விஜயதசமி, பௌத்த மறுமலர்ச்சி தினம், "
              "பௌத்தக் கொடி நாள், சமத்துவ திருநாள்.",
        "en": "Buddha Purnima, Ashoka Vijayadashami, Buddhist Revival Day, "
              "Buddhist Flag Day, and the festival of equality.",
    },
    "events.k3.h": {"ta": "பயிற்சியும் கற்றலும்", "en": "Practice and learning"},
    "events.k3.p": {
        "ta": "தம்மப் பயிற்சி முகாம், விபாசனா கூட்டுத் தியானம், ஆன்லைன் தம்ம "
              "வகுப்பு, அம்பேத்கரிய வினா விடைப் போட்டி.",
        "en": "Dhamma retreats, group Vipassana meditation, online Dhamma "
              "classes, and the Ambedkarite quiz.",
    },
    "events.dana.eyebrow": {"ta": "தானம்", "en": "Dana"},
    "events.dana.h": {"ta": "மோர் தானம், கோடைக்காலச் சேவை",
                      "en": "Buttermilk dana, a summer service"},
    "events.dana.p": {
        "ta": "கோடை மாதங்களில் பௌர்ணமி நாட்களில் {venue} இன் வெளியே, "
              "வெயிலில் சாலையில் செல்வோருக்கு மோர் தானமாக வழங்கப்படுகிறது. "
              "தானம் என்பது சங்கத்தின் தொடர் பயிற்சிகளில் ஒன்று; {link} "
              "அதையே சொல்கிறது.",
        "en": "On full moon days in the summer months, buttermilk is given "
              "outside {venue} to those walking the road in the heat. Dana is "
              "one of the sangha's continuing practices; {link} says the same "
              "thing.",
    },
    "events.dana.link": {"ta": "சுஜாதாவின் தானக் கதையும்",
                         "en": "the story of Sujata's gift"},
    "events.timeline.h": {"ta": "நிகழ்வுக் காலவரிசை", "en": "Recent events"},
    "events.timeline.sub": {"ta": "சமீபத்தில் நடந்தவை, புதியது முதலாக.",
                            "en": "What has happened lately, newest first."},
    "events.allposts": {"ta": "அனைத்துப் பதிவுகளையும் பார்க்க",
                        "en": "See all the writings"},
    "events.poster.cap": {"ta": "பௌர்ணமி விழா அழைப்பிதழ் &middot; அசோக் நகர் "
                                "விஹார், சென்னை.",
                          "en": "Full moon celebration invitation &middot; "
                                "Ashok Nagar Vihar, Chennai."},
    "events.poster.dl": {"ta": "A4 அச்சுப் பதிப்பு", "en": "A4 print version"},
    "events.join.h": {"ta": "பங்கேற்க", "en": "Taking part"},
    "events.join.p": {
        "ta": "அனைவரும் வரவேற்கப்படுகிறார்கள். முன்பதிவு தேவையில்லை. "
              "விபாசனா கூட்டுத் தியானத்திற்கு மட்டும் பதிவு தேவை.",
        "en": "Everyone is welcome. No booking is needed. Only the group "
              "Vipassana meditation requires registration.",
    },
    "events.contact": {"ta": "தொடர்பு கொள்ள", "en": "Get in touch"},
    "events.gallery.h": {"ta": "நிகழ்வுப் படங்கள்", "en": "From the gatherings"},
    "events.gallery.sub": {"ta": "சங்கத்தின் சமீபத்திய கூட்டங்களிலிருந்து.",
                           "en": "Photographs from recent gatherings."},
    "events.photo.alt": {"ta": "சங்க நிகழ்வுப் புகைப்படம்",
                         "en": "Photograph from a sangha gathering"},
    "events.photo.cap": {"ta": "சங்க நிகழ்வு", "en": "Sangha gathering"},

    # ================================================================= writings
    "writings.meta": {
        "ta": "நிலாதம்மா பதிவுகள்: 2017 முதல் இன்று வரை சங்கம் பதிவு செய்த "
              "நிகழ்வுகள், கட்டுரைகள், வரலாற்றுக் குறிப்புகள்.",
        "en": "Niladhamma writings: events, articles and historical notes "
              "recorded by the sangha from 2017 to today.",
    },
    "writings.h1": {"ta": "எழுத்தும் ஆவணமும்", "en": "Writing and record"},
    "writings.lede": {
        "ta": "2017 முதல் இன்று வரை சங்கம் பதிவு செய்த நிகழ்வுகள், "
              "கட்டுரைகள், வரலாற்றுக் குறிப்புகள்.",
        "en": "Events, articles and historical notes recorded by the sangha "
              "from 2017 to today.",
    },
    "writings.all.h": {"ta": "அனைத்துப் பதிவுகளும்", "en": "All the writings"},
    "writings.all.sub": {"ta": "ஆண்டு வாரியாக வடிகட்டவும், தலைப்பில் தேடவும்.",
                         "en": "Filter by year, or search by title."},
    "writings.empty": {"ta": "இந்தத் தேடலுக்குப் பதிவுகள் எதுவும் இல்லை.",
                       "en": "No writings match that search."},

    # ================================================================ resources
    "res.meta": {
        "ta": "நிலாதம்மா தொகுத்து வழங்கும் வளங்கள்: பௌத்தப் பெயர்கள், சமூகச் "
              "சான்றிதழ் வழிமுறை, மின்னூல் தரவிறக்கம், பௌத்தத் திருமணம்.",
        "en": "Resources put together by Niladhamma: Buddhist names, the "
              "community certificate procedure, downloads, and Buddhist "
              "matrimony.",
    },
    "res.h1": {"ta": "சங்கம் தொகுத்த வளங்கள்",
               "en": "Resources the sangha has put together"},
    "res.lede": {
        "ta": "பெயர் தேடல் முதல் சான்றிதழ் வழிமுறை வரை, தொடர்ந்து பயன்படும் "
              "நான்கு பக்கங்கள்.",
        "en": "From name lists to certificate procedure: four pages that get "
              "used again and again.",
    },
    "res.list.h": {"ta": "நான்கு வளங்கள்", "en": "Four resources"},
    "res.list.sub": {"ta": "ஒவ்வொன்றும் ஒரு தனிப் பக்கம். தேவையானதைத் "
                           "தேர்ந்தெடுங்கள்.",
                     "en": "Each has its own page. Choose what you need."},
    "res.alsosee": {"ta": "இவற்றையும் பாருங்கள்", "en": "See also"},

    # ==================================================================== names
    "names.meta": {
        "ta": "குழந்தைகளுக்கான பௌத்தப் பெயர்கள்: 254 ஆண் பெயர்கள், 228 பெண் "
              "பெயர்கள், தேரகதாவின் 518 தேரர் பெயர்கள். தமிழில் "
              "தொகுக்கப்பட்டவை.",
        "en": "Buddhist names for children: 254 names for boys, 228 for girls, "
              "and 518 thera names from the Theragatha.",
    },
    "names.h1": {"ta": "குழந்தைகளுக்குப் பௌத்தப் பெயர்கள்",
                 "en": "Buddhist names for children"},
    "names.lede": {
        "ta": "பௌத்தம் இம்மண்ணின் அடையாளமாகச் செழித்து வளர்ந்த மதம். அதன் "
              "கொடையால் தமிழுக்கு வரிவடிவம் முதல் இலக்கிய இலக்கணங்களும் "
              "கிடைத்தன.",
        "en": "Buddhism grew and flourished here as a mark of this soil. By its "
              "gift Tamil received its script, and its literature and grammar "
              "besides.",
    },
    "names.p1": {
        "ta": "மீண்டெழும் பௌத்த எழுச்சியின் காரணமாக, தங்கள் பிள்ளைகளுக்குப் "
              "பௌத்தப் பெயர்கள் வேண்டும் என்று வினவுவோர் எண்ணிக்கை "
              "பெருகிக்கொண்டே வருகிறது. அதன் காரணமாக இந்தப் பக்கம் "
              "கட்டமைக்கப்பட்டுள்ளது. திரிபீடகத்தில் தேரகதா எனப்படும் "
              "பிக்குகளின் தம்மானுபவக் கோர்வையில் இடம்பெற்றுள்ள பெயர்களும் "
              "இங்குத் தொகுக்கப்பட்டுள்ளன. பெயர்களுக்குப் பின்னால் உள்ள "
              "கதைகளை {link} படிக்கலாம்.",
        "en": "With the Buddhist revival, more and more people ask for Buddhist "
              "names for their children. That is why this page was built. The "
              "names recorded in the Theragatha, the collection in which the "
              "bhikkhus spoke their experience of the Dhamma, are gathered here "
              "as well. The stories behind the names can be read {link}.",
    },
    "names.p1.link": {"ta": "தம்மக் கதைகளில்", "en": "in the Dhamma stories"},
    "names.tab.boys": {"ta": "ஆண் குழந்தைகள்", "en": "For boys"},
    "names.tab.girls": {"ta": "பெண் குழந்தைகள்", "en": "For girls"},
    "names.tab.theras": {"ta": "தேரகதா தேரர்கள்", "en": "Theragatha theras"},
    "names.h.boys": {"ta": "ஆண் குழந்தைகளுக்கான பௌத்தப் பெயர்கள்",
                     "en": "Buddhist names for boys"},
    "names.h.girls": {"ta": "பெண் குழந்தைகளுக்கான பௌத்தப் பெயர்கள்",
                      "en": "Buddhist names for girls"},
    "names.h.theras": {
        "ta": "திரிபீடகத்தின் தேரகதாவில் பதிவு செய்யப்பட்டுள்ள தேரர்களின் "
              "பெயர்கள் &middot; Names of Theras from the Theragatha",
        "en": "Names of the theras recorded in the Theragatha of the Tipitaka",
    },
    "names.search": {"ta": "பெயரில் தேட", "en": "Search names"},
    "names.empty": {"ta": "இந்தத் தேடலுக்குப் பெயர்கள் எதுவும் இல்லை.",
                    "en": "No names match that search."},
    "names.faq.h": {"ta": "பெயர்கள் குறித்த கேள்விகள்",
                    "en": "Questions about the names"},

    # ============================================================== certificate
    "cert.meta": {
        "ta": "பௌத்தமேற்ற பட்டியலினத்தினருக்கான சமூகச் சான்றிதழ்: இ-சேவை "
              "மையம் வழியாக விண்ணப்பிக்கும் வழிமுறை, CAN பதிவு, ஆதாரச் "
              "சான்றிதழ்.",
        "en": "The community certificate for Scheduled Caste Buddhists: how to "
              "apply through an e-Sevai centre, CAN registration, and the "
              "supporting certificate.",
    },
    "cert.h1": {"ta": "பௌத்தமேற்ற பட்டியலினத்தினருக்கான சமூகச் சான்றிதழ்",
                "en": "The community certificate for Scheduled Caste Buddhists"},
    "cert.lede": {"ta": "சான்றிதழ் பெறுவது குறித்த சந்தேகங்களைத் "
                        "தெளிவுபடுத்தும் வழிகாட்டி.",
                  "en": "A guide that clears up the doubts about obtaining the "
                        "certificate."},
    "cert.alert.h": {"ta": "உரிமை பாதுகாக்கப்படுகிறது",
                     "en": "Your rights are protected"},
    "cert.alert.p": {
        "ta": "ஒரு பட்டியலினத்தவர் இந்து, சீக்கிய, பௌத்த மதம் ஆகிய இந்த "
              "மூன்றில் எதற்கு மாறினாலும், பின்பற்றினாலும், அவரின் சமூக "
              "உரிமைகளைப் பெறப் பட்டியலினம் (SC) என்றே சான்றிதழ் "
              "வழங்கப்படுகிறது.",
        "en": "Whichever of the three religions a Scheduled Caste person moves "
              "to or follows, Hindu, Sikh or Buddhist, the certificate is "
              "issued as Scheduled Caste (SC), so that their social rights are "
              "secured.",
    },
    "cert.p1": {
        "ta": "பௌத்தமேற்ற பட்டியலினத்தினருக்கு, அவர்களின் சமூக உரிமையைப் "
              "பெறும் வகையில், பட்டியலினம் என்றே சமூகச் சான்றிதழ் "
              "வழங்கப்படுகிறது.",
        "en": "For Scheduled Caste people who have embraced Buddhism, the "
              "community certificate is issued as Scheduled Caste, so that "
              "their social rights are secured.",
    },
    "cert.p2": {
        "ta": "இச்சான்றிதழ் பெறுவது குறித்துப் பலருக்கும் சந்தேகங்கள் "
              "இருப்பது ஒரு புறமென்றால், அரசு அதிகாரிகளும் இது குறித்த "
              "போதுமான விழிப்புணர்வு இன்றியோ, அல்லது வேண்டுமென்றோ, சரியான "
              "முறையில் சான்றிதழ் அளிக்காமல் மக்களை அலைக்கழிக்கின்றனர். இது "
              "குறித்தே இந்தப் பக்கம்.",
        "en": "Many people are unsure about obtaining this certificate; and "
              "government officials, whether for want of awareness or by "
              "design, send people back and forth without issuing it properly. "
              "That is what this page is about.",
    },
    "cert.steps.h": {"ta": "விண்ணப்பிக்கும் வழிமுறை", "en": "How to apply"},
    "cert.diff.h": {"ta": "பழைய, புதிய சான்றிதழ்களுக்கிடையேயான வேறுபாடு",
                    "en": "Old and recent certificates compared"},
    "cert.old.t": {"ta": "பழைய சான்றிதழ்", "en": "Older certificate"},
    "cert.old.d": {
        "ta": "மதம் குறிப்பிடப்பட்டு, அதன் பின்னர் உட்சாதி "
              "குறிப்பிடப்பட்டிருக்கும். எடுத்துக்காட்டு: இந்து &ndash; "
              "ஆதிதிராவிடர்.",
        "en": "The religion was stated, and the sub-caste after it. For "
              "example: Hindu &ndash; Adi Dravida.",
    },
    "cert.new.t": {"ta": "சமீபத்திய சான்றிதழ்", "en": "Recent certificate"},
    "cert.new.d": {
        "ta": "மதம் குறிப்பிடப்படுவதில்லை. உட்சாதியும் (ஆதிதிராவிடர்), "
              "சமூகமும் (SC) மட்டுமே குறிப்பிடப்படுகிறது.",
        "en": "The religion is not stated. Only the sub-caste (Adi Dravida) "
              "and the category (SC) appear.",
    },
    "cert.trouble.h": {"ta": "சிக்கல் ஏற்பட்டால்", "en": "If you run into trouble"},
    "cert.trouble.p": {
        "ta": "அலுவலகத்தில் சான்றிதழ் மறுக்கப்பட்டாலோ, "
              "தாமதப்படுத்தப்பட்டாலோ, {link} கொள்ளுங்கள். இதுவரை "
              "நூற்றுக்கணக்கான குடும்பங்கள் இந்தச் செயல்முறையைக் "
              "கடந்திருக்கின்றன.",
        "en": "If the certificate is refused or delayed at the office, {link}. "
              "Hundreds of families have already been through this process.",
    },
    "cert.trouble.link": {"ta": "சங்கத்தைத் தொடர்பு", "en": "get in touch with the sangha"},
    "cert.go.h": {"ta": "தொடர்புடைய அரசாணை", "en": "The relevant order"},
    "cert.go.p": {
        "ta": "2021ஆம் ஆண்டு தமிழக அரசு பௌத்தர்களைச் சிறுபான்மையினராக "
              "அங்கீகரித்து அரசாணை வெளியிட்டது. {link}.",
        "en": "In 2021 the Government of Tamil Nadu issued an order recognising "
              "Buddhists as a minority. {link}.",
    },
    "cert.go.link": {"ta": "பதிவுகளில் விவரம்", "en": "Details in the writings"},
    "cert.help.h": {"ta": "உதவி வேண்டுமா", "en": "Need help?"},
    "cert.help.p": {"ta": "சங்கம் உங்களுடன் உடன் நிற்கும்.",
                    "en": "The sangha will stand with you."},
    "cert.lion.cap": {"ta": "சாரநாத் அசோகர் சிங்க முகடு, கி.மு. 3ஆம் நூற்றாண்டு.",
                      "en": "The Ashoka lion capital at Sarnath, 3rd century BCE."},

    # ================================================================ downloads
    "dl.meta": {
        "ta": "பௌத்தம் குறித்த மின்னூல்கள், ஒலி வடிவங்கள், பாபாசாகேப் "
              "அம்பேத்கர் பேச்சுக்களும் எழுத்துகளும் தமிழிலும் ஆங்கிலத்திலும்.",
        "en": "Buddhist e-books and audio, and Babasaheb Ambedkar's writings "
              "and speeches in Tamil and English.",
    },
    "dl.h1": {"ta": "மின்னூல்களும் ஒலி வடிவங்களும்", "en": "E-books and audio"},
    "dl.lede": {
        "ta": "பௌத்தம் குறித்த புத்தகங்கள், பதிப்புகளை மின்னூலாகவும் ஒலி "
              "வடிவாகவும் தரவிறக்கம் செய்துகொள்ளுங்கள்.",
        "en": "Download Buddhist books and editions as e-books and as audio.",
    },
    "dl.audio.h": {"ta": "ஒலி வடிவங்கள்", "en": "Audio"},
    "dl.audio.sub": {
        "ta": "Sasana Abhiwurdhi Wardhana Society, Buddhist Maha Vihara, "
              "Brickfields, KL தயாரிப்பு.",
        "en": "Produced by the Sasana Abhiwurdhi Wardhana Society, Buddhist "
              "Maha Vihara, Brickfields, KL.",
    },
    "dl.a1.h": {"ta": "அன்றாட பௌத்த வழிபாடு", "en": "Daily Buddhist devotions"},
    "dl.a1.p": {"ta": "குரல்: வணக்கத்திற்குரிய சுமங்கலா.",
                "en": "Voice: Venerable Sumangala."},
    "dl.a2.h": {"ta": "மானிட வாழ்வின் மெல்லிய கீதம்",
                "en": "The gentle song of human life"},
    "dl.a2.p": {
        "ta": "பௌத்த மெல்லிசைப் பாடல்கள். பாடல்கள்: பேராசிரியர் ஹ்சிங் யுன். "
              "தமிழாக்கம்: அன்புமலர், பேராசிரியர் வி. சித்தார்த்தா "
              "பெரியார்தாசன். இசை: கண்மணிராஜா. பாடியவர்கள்: உஷாராஜ், "
              "சிங்கப்பூர் சீனு, கண்மணிராஜா, E. அன்பன்.",
        "en": "Buddhist light-music songs. Lyrics: Professor Hsing Yun. Tamil "
              "translation: Anbumalar and Professor V. Siddhartha "
              "Periyardasan. Music: Kanmaniraja. Singers: Usharaj, Singapore "
              "Seenu, Kanmaniraja, E. Anban.",
    },
    "dl.amb.h": {"ta": "பாபாசாகேப் அம்பேத்கர் தொகுதிகள்",
                 "en": "The Babasaheb Ambedkar volumes"},
    "dl.amb.sub": {"ta": "பேச்சுக்களும் எழுத்துகளும், தமிழிலும் ஆங்கிலத்திலும்.",
                   "en": "Writings and speeches, in Tamil and in English."},
    "dl.amb.ta.h": {"ta": "தமிழில்", "en": "In Tamil"},
    "dl.amb.ta.p": {
        "ta": "பாபாசாகேப் Dr. B. R. அம்பேத்கர் அவர்களின் பேச்சுக்களும் "
              "எழுத்துகளும், தமிழ்த் தொகுதிகள்.",
        "en": "Babasaheb Dr B. R. Ambedkar's writings and speeches, the Tamil "
              "volumes.",
    },
    "dl.amb.en.h": {"ta": "In English", "en": "In English"},
    "dl.amb.en.p": {
        "ta": "Babasaheb Dr. B. R. Ambedkar's Writings and Speeches, the full "
              "volume set.",
        "en": "Babasaheb Dr B. R. Ambedkar's Writings and Speeches, the full "
              "volume set.",
    },
    "dl.books.h": {"ta": "Other Books", "en": "Other books"},
    "dl.books.sub": {"ta": "பொது எல்லைக்குட்பட்ட வரலாற்று நூல்கள்.",
                     "en": "Public domain works of history."},
    "dl.pending.h": {"ta": "இணைப்புகள் இன்னும் இணைக்கப்படவில்லை",
                     "en": "The file links are not wired up yet"},
    "dl.pending.p": {
        "ta": "இந்தப் பக்கத்தின் அமைப்பு தயார்; கோப்பு இணைப்புகள் அசல் "
              "தளத்திலிருந்து இடம்பெற வேண்டும். இதுவரை {link} ஆன்லைனில் "
              "படிக்கலாம்.",
        "en": "The structure of this page is ready; the file links still have "
              "to be carried over from the original site. In the meantime you "
              "can read {link} online.",
    },
    "dl.pending.link": {"ta": "தம்மக் கதைகளை", "en": "the Dhamma stories"},

    # ================================================================ matrimony
    "mat.meta": {
        "ta": "பௌத்த மகாமங்கள திருமணம்: சாதி, சடங்கு இல்லாத சமத்துவ முறை. "
              "அரசிதழ்ப் பதிவு உதவி, துணை தேடலுக்கான பதிவு.",
        "en": "The Buddhist Mahamangala marriage: an equal rite without caste "
              "or ritual burden. Help with gazette registration, and a register "
              "for finding a partner.",
    },
    "mat.h1": {"ta": "மகாமங்கள முறையில் திருமணம்",
               "en": "Marriage in the Mahamangala rite"},
    "mat.lede": {
        "ta": "பௌத்தப் பண்பாட்டு நிகழ்வுகளில் சங்கம் தொடர்ச்சியாக "
              "ஒருங்கிணைத்து வருவது திருமணங்கள்.",
        "en": "Of the Buddhist cultural events, marriages are what the sangha "
              "has organised most consistently.",
    },
    "mat.p1": {
        "ta": "சாதி, சடங்கு, பொருட்செலவு என்ற சுமைகளின்றி, சமத்துவத்தை "
              "மையமாகக் கொண்டு நடத்தப்படும் திருமண முறை. வந்தனை, திரிசரணம், "
              "பஞ்சசீலம், உறுதிமொழி, ஆசி என அமைதியாக நிகழ்கிறது.",
        "en": "A marriage rite conducted with equality at its centre, without "
              "the burdens of caste, ritual or expense. It proceeds quietly: "
              "homage, the three refuges, the five precepts, the vows, and the "
              "blessing.",
    },
    "mat.does.h": {"ta": "சங்கம் என்ன செய்கிறது", "en": "What the sangha does"},
    "mat.d1": {"ta": "திருமண நிகழ்வை முழுமையாக ஒருங்கிணைத்தல்",
               "en": "Organising the marriage in full"},
    "mat.d2": {"ta": "பௌத்த முறையிலான வழிபாட்டு ஒழுங்கை வகுத்தல்",
               "en": "Setting out the order of the Buddhist rite"},
    "mat.d3": {"ta": "அரசிதழில் பதிவு செய்வதற்கான வழிகாட்டுதல்",
               "en": "Guidance on registering in the government gazette"},
    "mat.d4": {"ta": "திருமணச் சான்றிதழ் பெறுவதற்கான உதவி",
               "en": "Help in obtaining the marriage certificate"},
    "mat.d5": {"ta": "பௌத்தமேற்பு நிகழ்வுகளை இணைத்து நடத்துதல்",
               "en": "Holding conversion ceremonies alongside, where wanted"},
    "mat.reg.h": {"ta": "துணை தேடலுக்கான பதிவு",
                  "en": "The register for finding a partner"},
    "mat.reg.p": {
        "ta": "பௌத்தக் குடும்பங்களுக்கிடையே துணை தேடலுக்கு உதவும் வகையில் "
              "சங்கம் ஒரு பதிவேட்டை நடத்தி வருகிறது. பதிவு செய்ய, கீழுள்ள "
              "விவரங்களுடன் {link} கொள்ளுங்கள்.",
        "en": "The sangha keeps a register to help Buddhist families find "
              "partners for their sons and daughters. To register, {link} with "
              "the details below.",
    },
    "mat.reg.link": {"ta": "சங்கத்தைத் தொடர்பு", "en": "get in touch with the sangha"},
    "mat.priv.h": {"ta": "பதிவு எப்படி நடக்கிறது", "en": "How the register works"},
    "mat.priv.p": {
        "ta": "விவரங்கள் சங்கத்திடம் மட்டுமே இருக்கும். வெளியில் "
              "வெளியிடப்படுவதில்லை. பொருத்தமான தொடர்புகள் மட்டுமே இருதரப்பு "
              "ஒப்புதலுடன் பகிரப்படும்.",
        "en": "The details stay with the sangha alone. They are not published. "
              "Only suitable introductions are shared, and only with the "
              "consent of both sides.",
    },
    "mat.need.h": {"ta": "தேவையான விவரங்கள்", "en": "Details needed"},
    "mat.n1.t": {"ta": "பெயர், வயது", "en": "Name and age"},
    "mat.n1.d": {"ta": "விண்ணப்பதாரரின் முழுப் பெயரும் பிறந்த ஆண்டும்.",
                 "en": "Full name and year of birth."},
    "mat.n2.t": {"ta": "கல்வி, பணி", "en": "Education and work"},
    "mat.n2.d": {"ta": "தற்போதைய கல்வித் தகுதியும் பணி விவரமும்.",
                 "en": "Current qualification and occupation."},
    "mat.n3.t": {"ta": "ஊர்", "en": "Place"},
    "mat.n3.d": {"ta": "தற்போது வசிக்கும் ஊர், சொந்த ஊர்.",
                 "en": "Where you live now, and your native place."},
    "mat.n4.t": {"ta": "பௌத்தமேற்பு", "en": "Conversion"},
    "mat.n4.d": {"ta": "பௌத்தமேற்ற ஆண்டு, அரசிதழ்ப் பதிவு விவரம் (இருந்தால்).",
                 "en": "Year of embracing Buddhism, and gazette registration "
                       "details if any."},
    "mat.n5.t": {"ta": "தொடர்பு", "en": "Contact"},
    "mat.n5.d": {"ta": "மின்னஞ்சல் அல்லது கைபேசி எண்.",
                 "en": "Email address or mobile number."},
    "mat.send": {"ta": "விவரங்களை அனுப்ப", "en": "Send your details"},
    "mat.past.h": {"ta": "நடந்த திருமணங்கள்", "en": "Marriages held"},
    "mat.past.p": {
        "ta": "சங்கம் பல பௌத்த மகாமங்கள திருமணங்களை நடத்தியிருக்கிறது. "
              "நிகழ்வுப் பதிவுகளைப் {link} காணலாம்.",
        "en": "The sangha has conducted many Buddhist Mahamangala marriages. "
              "The records of them can be seen {link}.",
    },
    "mat.past.link": {"ta": "பதிவுகள் பக்கத்தில்", "en": "on the writings page"},
    "mat.vihar.cap": {"ta": "சென்னையில் ஒரு பௌத்த விஹார்.",
                      "en": "A Buddhist vihara in Chennai."},
    "mat.faq.h": {"ta": "திருமணம் குறித்த கேள்விகள்",
                  "en": "Questions about the marriage rite"},

    # ================================================================== contact
    "contact.meta": {
        "ta": "நிலாதம்மாவைத் தொடர்பு கொள்ள: info@niladhamma.co.in. அசோக் "
              "நகர் புத்த விஹார், 15 4வது அவென்யூ, அசோக் நகர், சென்னை "
              "600083. ஒவ்வொரு பௌர்ணமியிலும் மாலை 6 மணி முதல்.",
        "en": "Contact Niladhamma: info@niladhamma.co.in. Ashok Nagar Buddha "
              "Vihar, 15 4th Avenue, Ashok Nagar, Chennai 600083. Every full "
              "moon day from 6pm.",
    },
    "contact.h1": {"ta": "எங்களைத் தொடர்பு கொள்ளுங்கள்", "en": "Get in touch"},
    "contact.lede": {
        "ta": "கேள்விகள், நிகழ்வுப் பங்கேற்பு, சான்றிதழ் உதவி, திருமணப் பதிவு "
              "எதுவானாலும் எழுதுங்கள்.",
        "en": "Questions, taking part in an event, help with a certificate, "
              "registering for the matrimony list: write to us about any of it.",
    },
    "contact.ways.h": {"ta": "தொடர்பு கொள்ளும் வழிகள்", "en": "Ways to reach us"},
    "contact.ways.sub": {"ta": "மின்னஞ்சல், நேரில் வருகை, சமூக ஊடகங்கள்.",
                         "en": "Email, visiting in person, social media."},
    "contact.email.h": {"ta": "மின்னஞ்சல்", "en": "Email"},
    "contact.write": {"ta": "எழுத", "en": "Write to us"},
    "contact.place.h": {"ta": "கூடும் இடம்", "en": "Where we meet"},
    "contact.social.h": {"ta": "சமூக ஊடகங்கள்", "en": "Social media"},
    "contact.vip.h": {"ta": "விபாசனா கூட்டுத் தியானம்",
                      "en": "Group Vipassana meditation"},
    "contact.vip.p": {
        "ta": "கூட்டுத் தியானப் பதிவுக்கு மின்னஞ்சல் மூலம் தொடர்பு "
              "கொள்ளுங்கள். பௌர்ணமிக் கூட்டங்களுக்கு முன்பதிவு தேவையில்லை.",
        "en": "Write to us by email to register for the group meditation. No "
              "booking is needed for the full moon gatherings.",
    },
    "contact.welcome.h": {"ta": "அனைவரும் வரவேற்கப்படுகிறார்கள்",
                          "en": "Everyone is welcome"},
    "contact.welcome.p": {
        "ta": "&ldquo;ஏஹி பஸ்ஸிகோ&rdquo; &middot; வாருங்கள், வந்து "
              "கண்டுணருங்கள். முதல் முறை வருபவர்கள் {link1} படித்து, {link2} "
              "ஒன்றைப் படித்துவரலாம்.",
        "en": "&ldquo;Ehipassiko&rdquo; &middot; come and see for yourself. If "
              "this is your first visit, read {link1} and perhaps one of {link2} "
              "before you come.",
    },
    "contact.welcome.link1": {"ta": "நம்மைப் பற்றி", "en": "about us"},
    "contact.welcome.link2": {"ta": "தம்மக் கதைகளில்", "en": "the Dhamma stories"},

    # ===================================================================== தானம்
    "dana.meta": {
        "ta": "பௌத்தத்தில் தானத்தின் வகைகள்: ஆமிசம், அபயம், தம்மம் என்று "
              "எதைக் கொடுக்கிறோம்; பாடிபுக்கலிகம், சங்கிகம் என்று யாருக்குக் "
              "கொடுக்கிறோம்; கொடுப்பதற்கான எட்டு காரணங்கள்.",
        "en": "The kinds of dana in Buddhism: what is given, whether goods, "
              "fearlessness or the Dhamma; who receives it, a person or the "
              "Sangha; and the eight grounds for giving.",
    },
    "dana.h1": {"ta": "தானம்: பௌத்தத்தில் கொடையின் வகைகள்",
                "en": "Dana: the kinds of giving in Buddhism"},
    "dana.lede": {
        "ta": "எதைக் கொடுக்கிறோம், யாருக்குக் கொடுக்கிறோம், எப்படிக் "
              "கொடுக்கிறோம், ஏன் கொடுக்கிறோம். புத்தர் தானத்தை இந்த நான்கு "
              "கோணங்களில் பிரித்துச் சொன்னார்.",
        "en": "What is given, who receives it, how it is given, and why. The "
              "Buddha set out giving along these four lines.",
    },
    "dana.p1": {
        "ta": "தானம் என்பது கொடுத்தல். பௌத்தப் பயிற்சி தொடங்கும் இடம் இதுதான். "
              "புண்ணியம் சேர்க்கும் மூன்று வழிகளில், தானம் சீலம் பாவனா என்ற "
              "வரிசையில், தானம் முதலில் நிற்கிறது. பத்துப் பாரமிகளிலும் "
              "முதலாவது இதுவே.",
        "en": "Dana is giving. It is where Buddhist practice begins. Of the "
              "three grounds of merit, giving, virtue and mental cultivation, "
              "giving stands first, and it is the first of the ten paramis as "
              "well.",
    },
    "dana.p2": {
        "ta": "இதற்குக் காரணம் எளிது. கொடுப்பது பற்றை நேரடியாகத் தளர்த்துகிறது. "
              "பிடித்து வைத்திருக்கும் கை திறக்கும்போது மனமும் சேர்ந்து "
              "திறக்கிறது. அதனால்தான் புத்தர் தானத்தை ஒழுக்கத்திற்கும் "
              "தியானத்திற்கும் முன்பாக வைத்தார்.",
        "en": "The reason is plain. Giving loosens attachment directly. When "
              "the holding hand opens, the mind opens with it. That is why the "
              "Buddha placed giving before conduct and before meditation.",
    },
    "dana.what.h": {"ta": "எதைக் கொடுக்கிறோம்: மூன்று வகை",
                    "en": "What is given: three kinds"},
    "dana.what.p": {
        "ta": "கொடுக்கப்படும் பொருளை வைத்துத் தானம் மூன்றாகப் பிரிக்கப்படுகிறது.",
        "en": "Giving divides into three according to what passes from one "
              "hand to the other.",
    },
    "dana.amisa.t": {"ta": "ஆமிச தானம்", "en": "Amisa dana"},
    "dana.amisa.d": {
        "ta": "பொருள் கொடை. உணவு, உடை, இருப்பிடம், மருந்து. உடலைத் தாங்கும் "
              "நான்கும் இதில் அடங்கும். சங்கத்திற்கு அளிக்கப்படும் அன்னதானம் "
              "இதன் மிகப் பழைய வடிவம்.",
        "en": "The material gift: food, clothing, shelter and medicine, the "
              "four things that keep a body going. The meal offered to the "
              "Sangha is its oldest form.",
    },
    "dana.abhaya.t": {"ta": "அபய தானம்", "en": "Abhaya dana"},
    "dana.abhaya.d": {
        "ta": "அச்சமின்மைக் கொடை. ஓர் உயிரை அச்சத்திலிருந்து விடுவிப்பது. "
              "உயிர் காப்பது, கொல்லாமல் இருப்பது, நம்மைக் கண்டு யாரும் "
              "அஞ்சாதிருக்கச் செய்வது.",
        "en": "The gift of fearlessness: releasing a living being from fear. "
              "Saving a life, refraining from killing, being someone in whose "
              "presence no one need be afraid.",
    },
    "dana.dhamma.t": {"ta": "தம்ம தானம்", "en": "Dhamma dana"},
    "dana.dhamma.d": {
        "ta": "வழியைக் கற்பிப்பது. உணவு ஒரு நாளைத் தாங்கும்; வழி ஒரு "
              "வாழ்க்கையைத் திருப்பும். அதனால் இதுவே உயர்ந்த கொடை என்று "
              "சொல்லப்படுகிறது.",
        "en": "Teaching the path. Food carries someone through a day; the path "
              "can turn a life. That is why it is called the highest gift.",
    },
    "dana.dhp": {
        "ta": "எல்லாக் கொடைகளையும் தம்மக் கொடை வெல்லும்.",
        "en": "The gift of the Dhamma excels all gifts.",
    },
    "dana.dhp.src": {"ta": "தம்மபதம், செய்யுள் 354", "en": "Dhammapada 354"},
    "dana.sila.h": {"ta": "ஐந்து சீலமும் ஒரு பெருங்கொடை",
                    "en": "The five precepts are themselves a great gift"},
    "dana.sila.p": {
        "ta": "அபய தானம் கையால் மட்டும் கொடுப்பதில்லை. ஐந்து சீலங்களைக் "
              "கடைப்பிடிப்பதே ஐந்து பெருங்கொடைகள் என்று புத்தர் சொன்னார். "
              "கொல்லாமை, திருடாமை, ஒழுக்கம், பொய்யாமை, மயக்கம் தராத வாழ்வு. "
              "இவற்றை ஒருவர் ஏற்கும்போது, எண்ணிலடங்காத உயிர்களுக்கு அவரிடம் "
              "இனி அச்சமில்லை என்ற உறுதி கிடைக்கிறது. அபிசந்த சுத்தம் "
              "(அங்குத்தர நிகாயம் 8.39).",
        "en": "Fearlessness is not given by hand alone. The Buddha called the "
              "five precepts five great gifts: not killing, not taking what is "
              "not given, conduct, truthful speech, and a life clear of "
              "intoxication. When someone takes them on, a countless number of "
              "beings receive the assurance that they have nothing to fear from "
              "that person. Abhisanda Sutta (Anguttara Nikaya 8.39).",
    },
    "dana.who.h": {"ta": "யாருக்குக் கொடுக்கிறோம்: இரண்டு வகை",
                   "en": "Who receives: two kinds"},
    "dana.who.p": {
        "ta": "மகாபஜாபதி கோதமி தன் கையால் நெய்த ஆடையைப் புத்தருக்குக் "
              "கொடுக்க வந்தார். அதைச் சங்கத்திற்குக் கொடுங்கள் என்று அவர் "
              "சொன்னார்; சங்கத்திற்குக் கொடுத்தால் அது எனக்கும் "
              "கொடுத்ததாகும் என்றார். அந்த உரையாடலில் இருந்து தொடங்கும் "
              "தக்கிணாவிபங்க சுத்தம் தானத்தைப் பெறுபவரை வைத்து "
              "இரண்டாகப் பிரிக்கிறது.",
        "en": "Mahapajapati Gotami came to offer the Buddha a robe she had "
              "woven with her own hands. Give it to the Sangha, he said; in "
              "giving to the Sangha she would be giving to him as well. The "
              "Dakkhinavibhanga Sutta, which opens with that exchange, divides "
              "giving in two according to who receives it.",
    },
    "dana.indiv.t": {"ta": "பாடிபுக்கலிக தானம்", "en": "Patipuggalika dana"},
    "dana.indiv.d": {
        "ta": "ஒரு தனி நபருக்குக் கொடுப்பது. புத்தர் முதல் விலங்கு வரை "
              "பதினான்கு வகைகள் அந்தச் சுத்தத்தில் வரிசைப்படுத்தப்படுகின்றன. "
              "விலங்குக்கு இடும் ஒரு பிடி உணவும் பயனற்றது அல்ல என்பது "
              "இந்தப் பட்டியலின் கடைசி வரி.",
        "en": "Given to one person. The sutta lists fourteen kinds, from a "
              "Buddha down to an animal. The last line of that list says that "
              "a handful of food put out for an animal is not without fruit "
              "either.",
    },
    "dana.sangha.t": {"ta": "சங்கிக தானம்", "en": "Sanghika dana"},
    "dana.sangha.d": {
        "ta": "சங்கத்திற்கே கொடுப்பது. ஏழு வகைகள் சொல்லப்படுகின்றன. "
              "தனிநபருக்குக் கொடுப்பதைவிடச் சங்கத்திற்குக் கொடுப்பது "
              "பெரும் பயன் தரும் என்று புத்தர் சொன்னார். கொடை ஒரு "
              "நபரிடம் நிற்காமல் கூட்டத்தைச் சேரும்போது அது நீடிக்கிறது.",
        "en": "Given to the Sangha itself. Seven kinds are named. A gift to the "
              "Sangha bears greater fruit than a gift to any one person, the "
              "Buddha said. A gift that reaches the community rather than "
              "stopping with one person is a gift that lasts.",
    },
    "dana.mn142": {"ta": "தக்கிணாவிபங்க சுத்தம் (மஜ்ஜிம நிகாயம் 142)",
                   "en": "Dakkhinavibhanga Sutta (Majjhima Nikaya 142)"},
    "dana.how.h": {"ta": "எப்படிக் கொடுக்கிறோம்: மூன்று வகை",
                   "en": "How it is given: three kinds"},
    "dana.how.p": {
        "ta": "கொடுக்கும் முறையை வைத்து உரையாசிரியர்கள் தானத்தை மூன்றாகப் "
              "பிரிக்கிறார்கள். கொடுக்கும் பொருள் ஒன்றாக இருந்தாலும் "
              "மனநிலை வேறுபடுகிறது.",
        "en": "The commentaries divide giving in three by the manner of it. "
              "The thing given may be the same in each; the state of mind is "
              "not.",
    },
    "dana.dasa.t": {"ta": "தாஸ தானம்", "en": "Dasa dana"},
    "dana.dasa.d": {
        "ta": "அடிமையின் கொடை. தான் உண்பதைவிடத் தாழ்ந்ததை, மரியாதையின்றிக் "
              "கொடுப்பது.",
        "en": "A slave's giving: handing over something poorer than one would "
              "eat oneself, and handing it over carelessly.",
    },
    "dana.sahaya.t": {"ta": "சகாய தானம்", "en": "Sahaya dana"},
    "dana.sahaya.d": {
        "ta": "தோழனின் கொடை. தான் உண்பதைப் போன்றதையே கொடுப்பது.",
        "en": "A friend's giving: giving what one would eat oneself.",
    },
    "dana.sami.t": {"ta": "சாமி தானம்", "en": "Sami dana"},
    "dana.sami.d": {
        "ta": "தலைவனின் கொடை. தான் உண்பதைவிடச் சிறந்ததை, மரியாதையோடு "
              "கொடுப்பது. மூன்றில் உயர்ந்தது இது.",
        "en": "A master's giving: giving something better than one would eat "
              "oneself, and giving it with respect. This is the highest of the "
              "three.",
    },
    # Two sections, deliberately separate. The first reports what the sutta
    # records; the second is the sangha speaking. Running them together under
    # "why we give" put Niladhamma's name to a rebirth-reward motive that
    # Navayana exists to reject.
    "dana.why.h": {"ta": "மக்கள் ஏன் கொடுக்கிறார்கள்: சுத்தத்தின் பட்டியல்",
                   "en": "Why people give: the sutta's list"},
    "dana.why.p": {
        "ta": "தானவத்து சுத்தத்தில் புத்தர் மக்கள் எந்தெந்தக் காரணங்களால் "
              "கொடுக்கிறார்கள் என்பதைப் பட்டியலிடுகிறார். இது நோய் "
              "கண்டறிதல், மருந்துச் சீட்டு அல்ல. முதல் நான்கையும் அவரே "
              "மனத்தின் குறைபாடுகள் என்கிறார். எட்டாவதை மட்டுமே அவர் "
              "உயர்த்திப் பிடிக்கிறார்.",
        "en": "In the Danavatthu Sutta the Buddha lists the grounds on which "
              "people give. It is a diagnosis, not a prescription. He names "
              "the first four as faults of mind himself. The one he holds up "
              "is the eighth alone.",
    },
    "dana.us.h": {"ta": "நாம் ஏன் கொடுக்கிறோம்",
                  "en": "Why we give"},
    "dana.us.p1": {
        "ta": "மேலுள்ள எட்டில் நிலாதம்மா எடுத்துக்கொள்வது எட்டாவதை "
              "மட்டும். மனத்திற்கு அணியாகக் கொடுப்பது; பதிலை எண்ணாமல் "
              "கொடுப்பது.",
        "en": "Of the eight above, Niladhamma takes the eighth alone: giving "
              "as an ornament of the mind, with no thought of a return.",
    },
    "dana.us.p2": {
        "ta": "ஆறாவதை நாங்கள் ஏற்கவில்லை. இறந்த பிறகு நல்ல பிறவி "
              "கிடைக்கும் என்பதற்காகக் கொடுப்பது, கம்மமும் மறுபிறவியும் "
              "பற்றிய பிராமணியக் கொள்கையின் நீட்சி. அந்தக் கொள்கைதான், "
              "&ldquo;முற்பிறவியில் செய்த பாவத்தால்தான் இப்பிறவியில் "
              "தாழ்ந்து பிறந்தாய்&rdquo; என்று சொல்லிச் சாதி அமைப்பை "
              "நியாயப்படுத்தி வந்தது. அதை அம்பேத்கர் திட்டவட்டமாக "
              "மறுத்தார்.",
        "en": "We do not accept the sixth. Giving because a good rebirth will "
              "follow is an extension of the Brahminical doctrine of kamma and "
              "rebirth, and that doctrine is what told a person they were born "
              "low because of sin in an earlier life, and so justified caste. "
              "Ambedkar rejected it flatly.",
    },
    "dana.us.p3": {
        "ta": "அவரைப் பொறுத்தவரை புத்தரின் கம்மம் இம்மைக்கானது: இங்கே "
              "செய்யும் செயலுக்கு இங்கேயே விளைவு. ஆன்மா இல்லை என்று "
              "அனத்தாவைச் சொன்ன புத்தர், பலனைப் பெறுவதற்காக ஒரு ஆன்மா "
              "மறுபிறவிக்குச் செல்கிறது என்று சொல்லியிருக்க முடியாது.",
        "en": "For him the Buddha's kamma belongs to this life: what is done "
              "here has its effect here. A teacher who taught anatta, that "
              "there is no soul, cannot also have taught that a soul travels "
              "on to collect a reward.",
    },
    "dana.us.p4": {
        "ta": "எனவே தானம் இம்மைக்கானது. கொடுப்பவரின் அடுத்த பிறவிக்கு "
              "அல்ல; பெறுபவருக்கும், அவர் வாழும் சமூகத்திற்கும்.",
        "en": "So dana is for this life. Not for the giver's next birth, but "
              "for the person receiving it and for the society they live in.",
    },
    "dana.why.1": {"ta": "விருப்பத்தால்", "en": "Out of liking"},
    "dana.why.2": {"ta": "வெறுப்பால்", "en": "Out of dislike"},
    "dana.why.3": {"ta": "மயக்கத்தால்", "en": "Out of confusion"},
    "dana.why.4": {"ta": "அச்சத்தால்", "en": "Out of fear"},
    "dana.why.5": {"ta": "&ldquo;எங்கள் குடும்பத்தில் முன்னோர் கொடுத்து "
                         "வந்தார்கள்; பழைய மரபை நான் விடலாகாது&rdquo; என்று",
                   "en": "Thinking, &ldquo;this was given by those before me "
                         "in my family, and I should not let the old custom "
                         "lapse&rdquo;"},
    "dana.why.6": {"ta": "&ldquo;கொடுத்தால் இறந்த பிறகு நல்ல பிறவி "
                         "கிடைக்கும்&rdquo; என்று",
                   "en": "Thinking, &ldquo;by giving this I will be reborn "
                         "well&rdquo;"},
    "dana.why.7": {"ta": "&ldquo;கொடுக்கும்போது மனம் தெளிகிறது, மகிழ்ச்சி "
                         "பிறக்கிறது&rdquo; என்று",
                   "en": "Thinking, &ldquo;when I give, my mind grows clear "
                         "and gladness arises&rdquo;"},
    "dana.why.8": {"ta": "மனத்திற்கு அணியாகவும் துணையாகவும். இதுவே "
                         "எட்டாவது, உயர்ந்தது.",
                   "en": "As an ornament of the mind and a support for it. "
                         "This eighth is the highest."},
    "dana.an833": {"ta": "தானவத்து சுத்தம் (அங்குத்தர நிகாயம் 8.33)",
                   "en": "Danavatthu Sutta (Anguttara Nikaya 8.33)"},
    "dana.six.h": {"ta": "ஆறு அங்கங்கள் கொண்ட கொடை",
                   "en": "The gift with six factors"},
    "dana.six.p": {
        "ta": "நந்தமாதா என்னும் உபாசிகை அளித்த கொடையை விவரிக்கும்போது "
              "புத்தர் ஆறு அங்கங்களைச் சொன்னார். மூன்று கொடுப்பவரிடம், "
              "மூன்று பெறுபவரிடம். சளங்கதான சுத்தம் (அங்குத்தர நிகாயம் 6.37).",
        "en": "Describing a gift made by the laywoman Nandamata, the Buddha "
              "named six factors, three in the giver and three in those who "
              "receive. Chalangadana Sutta (Anguttara Nikaya 6.37).",
    },
    "dana.six.giver": {"ta": "கொடுப்பவரிடம்", "en": "In the giver"},
    "dana.six.giver.d": {
        "ta": "கொடுப்பதற்கு முன் மனம் மகிழ்கிறது; கொடுக்கும்போது மனம் "
              "தெளிகிறது; கொடுத்த பிறகு மனம் நிறைவடைகிறது.",
        "en": "Glad in mind before giving, clear in mind while giving, "
              "contented in mind after having given.",
    },
    "dana.six.recv": {"ta": "பெறுபவரிடம்", "en": "In those who receive"},
    "dana.six.recv.d": {
        "ta": "பேராசை, வெறுப்பு, மயக்கம் ஆகியவற்றை நீக்கியவர்களாக, "
              "அல்லது நீக்கும் பயிற்சியில் இருப்பவர்களாக இருப்பது.",
        "en": "Free of greed, of hatred and of delusion, or practising to be "
              "rid of them.",
    },
    "dana.food.h": {"ta": "உணவைக் கொடுப்பவர் ஐந்தைக் கொடுக்கிறார்",
                    "en": "One who gives food gives five things"},
    "dana.food.p": {
        "ta": "உணவு ஒரு பொருள் அல்ல, ஐந்து என்று புத்தர் சொன்னார்: ஆயுள், "
              "அழகு, இன்பம், வலிமை, தெளிவு. இந்த ஐந்தையும் கொடுப்பவர் "
              "பின்னர் தாமும் பெறுகிறார். போஜன சுத்தம் (அங்குத்தர நிகாயம் "
              "5.37).",
        "en": "A meal is not one thing but five, the Buddha said: life, "
              "beauty, ease, strength and clarity. Whoever gives those five "
              "comes to share in them. Bhojana Sutta (Anguttara Nikaya 5.37).",
    },
    "dana.pure.h": {"ta": "கொடை தூய்மையாவது நான்கு வகை",
                    "en": "Four ways an offering is made pure"},
    "dana.pure.p": {
        "ta": "தக்கிணாவிபங்க சுத்தம் முடிவில் ஒரு நுட்பமான கருத்தைச் "
              "சொல்கிறது: கொடை தூய்மையாவது கொடுக்கப்படும் பொருளால் அல்ல, "
              "கொடுப்பவரின், பெறுபவரின் ஒழுக்கத்தால்.",
        "en": "The Dakkhinavibhanga Sutta closes on a fine point: an offering "
              "is made pure not by what is in it, but by the conduct of the "
              "one who gives and the one who receives.",
    },
    "dana.pure.1": {"ta": "கொடுப்பவரால் தூய்மை, பெறுபவரால் அல்ல",
                    "en": "Pure by the giver, not by the receiver"},
    "dana.pure.2": {"ta": "பெறுபவரால் தூய்மை, கொடுப்பவரால் அல்ல",
                    "en": "Pure by the receiver, not by the giver"},
    "dana.pure.3": {"ta": "இருவராலும் தூய்மை அல்ல",
                    "en": "Pure by neither"},
    "dana.pure.4": {"ta": "இருவராலும் தூய்மை. இதுவே முழுமையானது.",
                    "en": "Pure by both. This one is complete."},
    "dana.amb.h": {"ta": "அம்பேத்கரும் தானமும்",
                   "en": "Ambedkar on giving"},
    "dana.amb.vow": {
        "ta": "இது கோட்பாட்டளவில் நின்றுவிடவில்லை. இறந்த பிறகு கிடைக்கும் "
              "பலனுக்காகச் சடங்கு செய்யும் வழக்கத்தை அம்பேத்கர் வெளியே "
              "நிறுத்தினார்: 22 உறுதிமொழிகளில் எட்டாவது, சிராத்தம் "
              "செய்வதையும் பிண்டம் இடுவதையும் மறுப்பது. தீட்சை எடுத்த "
              "நாளிலேயே அது உறுதிமொழியாக ஆனது.",
        "en": "This did not stay at the level of doctrine. Ambedkar put the "
              "practice of performing rites for a reward after death outside "
              "the door: the eighth of the twenty two vows refuses shraddha "
              "and pind. It became a vow on the day of the diksha itself.",
    },
    "dana.amb.p": {
        "ta": "&ldquo;புத்தரும் அவரது தம்மமும்&rdquo; நூலில் அம்பேத்கர் "
              "பாரமிகளை வரிசைப்படுத்தும்போது தானத்தை அவ்வாறே வைக்கிறார்: "
              "தன் உடைமையை, தேவைப்பட்டால் தன் உயிரையே, பிறர் நலனுக்காகக் "
              "கொடுப்பது; அதற்குப் பதிலாக எதையும் எதிர்பாராமல். "
              "எதிர்பார்ப்பு நீங்கும் இடத்தில்தான் கொடை கொடையாகிறது.",
        "en": "Setting out the paramis in The Buddha and His Dhamma, Ambedkar "
              "keeps giving in that place: giving away one's possessions, and "
              "one's life if it comes to that, for the good of others, and "
              "expecting nothing in return. Where the expectation ends is "
              "where the gift begins.",
    },
    "dana.here.h": {"ta": "நிலாதம்மாவில்", "en": "At Niladhamma"},
    "dana.here.p": {
        "ta": "ஒவ்வொரு பௌர்ணமிக் கூட்டத்திலும் தானம் உண்டு. மோர், "
              "கடலை, தேநீர், பழம், சில நாட்களில் இரவு உணவு. பெரிய "
              "பொருளல்ல; வந்தவர் யாரும் வெறுங்கையோடு திரும்பக் கூடாது "
              "என்பதே கணக்கு.",
        "en": "There is dana at every full moon gathering: buttermilk, "
              "groundnuts, tea, fruit, and on some days a meal at night. It is "
              "not a large thing. The point is that nobody who comes should go "
              "away empty-handed.",
    },
    "dana.here.link": {"ta": "கூட்டங்களைப் பாருங்கள்", "en": "See the gatherings"},

    # ====================================================================== 404
    "404.meta": {
        "ta": "இந்தப் பக்கம் கிடைக்கவில்லை. நிலாதம்மா தளத்தின் முகப்புக்குச் "
              "செல்லவும்.",
        "en": "This page could not be found. Go to the Niladhamma home page.",
    },
    "404.h1": {"ta": "இந்தப் பக்கம் கிடைக்கவில்லை",
               "en": "This page could not be found"},
    "404.p": {
        "ta": "நீங்கள் தேடிய பக்கம் நகர்த்தப்பட்டிருக்கலாம். கீழுள்ள "
              "இணைப்புகளில் தொடரலாம்.",
        "en": "The page you were looking for may have moved. Carry on from one "
              "of the links below.",
    },
}


# --------------------------------------------------------------------------
# Question and answer sets. Rendered as visible prose and as FAQPage schema.
# --------------------------------------------------------------------------

FAQ = {
    "about": [
        ({"ta": "பௌத்தர்கள் தமிழ்நாட்டில் இருக்கிறார்களா?",
          "en": "Are there Buddhists in Tamil Nadu?"},
         {"ta": "இருக்கிறார்கள். நிலாதம்மா 2012 முதல் சென்னையில் ஒவ்வொரு "
                "பௌர்ணமி நாளிலும் குடும்பமாகக் கூடி வருகிறது. "
                "நூற்றுக்கணக்கான குடும்பங்கள் பௌத்தமேற்று, அரசிதழில் பதிவு "
                "செய்து, சமூகச் சான்றிதழ் பெற்று வலிமை பெற்றிருக்கின்றன.",
          "en": "There are. Niladhamma has gathered as families on every full "
                "moon day in Chennai since 2012. Hundreds of families have "
                "embraced Buddhism, registered it in the government gazette, "
                "obtained their community certificates, and grown strong "
                "together."}),
        ({"ta": "பௌர்ணமி பௌத்தர்களுக்கானதா?",
          "en": "Is the full moon day a Buddhist observance?"},
         {"ta": "ஆம். பௌர்ணமி பௌத்த மரபில் உபோசத நாள்; விழிப்புக்கும் "
                "தியானத்துக்கும் உரிய நாள். புத்தரின் பிறப்பு, ஞானம், முதல் "
                "உபதேசம், பரிநிர்வாணம் ஆகிய நிகழ்வுகள் முழுநிலவு நாட்களோடு "
                "இணைக்கப்படுகின்றன.",
          "en": "Yes. In the Buddhist tradition the full moon is an uposatha "
                "day, given to wakefulness and meditation. The Buddha's birth, "
                "his awakening, his first discourse and his parinibbana are all "
                "joined to full moon days."}),
        ({"ta": "சங்கக் கூட்டத்தில் யார் பங்கேற்கலாம்?",
          "en": "Who can attend the gathering?"},
         {"ta": "அனைவரும். முன்பதிவு தேவையில்லை. அசோக் நகர் புத்த விஹாரில் "
                "(15, 4வது அவென்யூ, டாக்டர் அம்பேத்கர் நகர், பிருந்தாவன் "
                "எக்ஸ்டென்ஷன், அசோக் நகர், சென்னை 600083) ஒவ்வொரு பௌர்ணமி "
                "நாளும் மாலை 6 மணி முதல் கூடுகிறோம். விபாசனா கூட்டுத் "
                "தியானத்திற்கு மட்டும் முன்பதிவு தேவை.",
          "en": "Anyone. No booking is needed. We meet at Ashok Nagar Buddha "
                "Vihar (15, 4th Avenue, Dr Ambedkar Nagar, Brindavan "
                "Extension, Ashok Nagar, Chennai 600083) on every full moon "
                "day from 6pm. Only the group Vipassana meditation requires "
                "registration."}),
        ({"ta": "சங்கம் என்னென்ன செய்கிறது?",
          "en": "What does the sangha do?"},
         {"ta": "தொடர் பௌர்ணமி கூட்டங்கள், பௌத்த மகாமங்கள திருமணங்கள், "
                "பாபாசாகேப் அம்பேத்கர் இரவுப் பாடசாலைகள், கலைப் பயிற்சிகள், "
                "பௌத்தமேற்பு நிகழ்வுகளை ஒருங்கிணைத்தல், சமூகச் சான்றிதழ் "
                "பெறுவதற்கான உதவி.",
          "en": "Continuous full moon gatherings, Buddhist Mahamangala "
                "marriages, Babasaheb Ambedkar night schools, training in the "
                "arts, organising ceremonies of conversion to Buddhism, and "
                "help in obtaining community certificates."}),
    ],
    "kathai": [
        ({"ta": "தம்மபதம்: முப்பத்தோர் நாள் என்றால் என்ன?",
          "en": "What is Dhammapada: Thirty-one Days?"},
         {"ta": "ஜூலை 1 முதல் 31 வரை, ஒவ்வொரு நாளுக்கும் ஒரு பௌத்தக் கதை "
                "கொண்ட தமிழ்த் தொகுப்பு. புத்தர், அவர் சீடர்கள், "
                "மகாபஜாபதி, அசோகர், அம்பேத்கர் ஆகியோரின் வாழ்க்கைக் கதைகள். "
                "சங்கக் கூட்டத்தில் தினமும் வாசிக்கத் தொகுக்கப்பட்டது.",
          "en": "A Tamil collection with one Buddhist story for each day from "
                "1 to 31 July: stories from the lives of the Buddha, his "
                "disciples, Mahapajapati, Ashoka and Ambedkar. It was put "
                "together to be read aloud each day at the gathering."}),
        ({"ta": "ஒவ்வொரு கதையிலும் என்ன இருக்கும்?",
          "en": "What does each story contain?"},
         {"ta": "நான்கு பகுதிகள்: கதை, தம்மக்கருத்து, அம்பேத்கர் இணைப்பு, "
                "ஆதாரம். ஒவ்வொரு கதையும் எந்த நூலில் சொல்லப்பட்டுள்ளது என்ற "
                "ஆதாரத்துடன் தரப்படுகிறது.",
          "en": "Four parts: the story, a Dhamma insight, an Ambedkar "
                "connection, and the source. Every story is given with the text "
                "in which it is recorded."}),
        ({"ta": "இதை யார் படிக்கலாம்?", "en": "Who is it for?"},
         {"ta": "அனைவரும். சங்கக் கூட்டங்களில் உரக்க வாசிக்கவும், குடும்பமாகப் "
                "படிக்கவும், குழந்தைகளுக்குச் சொல்லவும் ஏற்ற வகையில் எளிய "
                "தமிழில் எழுதப்பட்டுள்ளது.",
          "en": "Anyone. It is written in plain language, so that it can be "
                "read aloud at a gathering, read together as a family, or told "
                "to children."}),
        ({"ta": "கதைகள் வரலாற்று நிகழ்வுகளா?",
          "en": "Are these stories historical?"},
         {"ta": "சில வரலாற்று நிகழ்வுகள்; சில மரபுவழி உருவகக் கதைகள். "
                "அம்பேத்கர் கற்பித்தபடி, கதையின் அற்புதத்தை அல்ல, அதன் "
                "கருத்தைக் கவனிக்க வேண்டும் என்பதே இத்தொகுப்பின் நோக்கம்.",
          "en": "Some are historical events; some are traditional allegories. "
                "As Ambedkar taught, what matters is the meaning of the story "
                "and not its marvels, and that is how this collection is "
                "intended to be read."}),
    ],
    "names": [
        ({"ta": "குழந்தைக்குப் பௌத்தப் பெயர் வைப்பது எப்படி?",
          "en": "How do I choose a Buddhist name for a child?"},
         {"ta": "இப்பக்கத்தில் ஆண் குழந்தைகளுக்கான 254 பெயர்களும், பெண் "
                "குழந்தைகளுக்கான 228 பெயர்களும், திரிபீடகத்தின் தேரகதாவில் "
                "பதிவான 518 தேரர் பெயர்களும் தொகுக்கப்பட்டுள்ளன. தேடல் "
                "பெட்டியில் எழுத்தைத் தட்டச்சு செய்து வடிகட்டலாம்.",
          "en": "This page collects 254 names for boys, 228 for girls, and 518 "
                "thera names recorded in the Theragatha of the Tipitaka. Type "
                "into the search box to filter the list."}),
        ({"ta": "தேரகதா என்றால் என்ன?", "en": "What is the Theragatha?"},
         {"ta": "திரிபீடகத்தில் இடம்பெறும் ஒரு நூல். பிக்குகள் தம் "
                "தம்மானுபவத்தைப் பாடல்களாகச் சொன்ன கோர்வை. அதில் இடம்பெறும் "
                "தேரர்களின் பெயர்கள் இங்குத் தொகுக்கப்பட்டுள்ளன.",
          "en": "A text within the Tipitaka: the collection in which the "
                "bhikkhus spoke their experience of the Dhamma in verse. The "
                "names of the theras who appear in it are gathered here."}),
        ({"ta": "பௌத்தப் பெயர்களுக்கும் தமிழுக்கும் என்ன தொடர்பு?",
          "en": "What is the connection between Buddhist names and Tamil?"},
         {"ta": "பௌத்தம் இம்மண்ணின் அடையாளமாகச் செழித்து வளர்ந்த மதம். அதன் "
                "கொடையால் தமிழுக்கு வரிவடிவம் முதல் இலக்கிய இலக்கணங்களும் "
                "கிடைத்தன. பல ஊர்ப்பெயர்களும் பௌத்தத்தைத் தாங்கியே இன்றும் "
                "நீடிக்கின்றன.",
          "en": "Buddhism grew and flourished here as a mark of this soil. By "
                "its gift Tamil received its script, and its literature and "
                "grammar besides. Many place names still carry Buddhism in "
                "them today."}),
    ],
    "cert": [
        ({"ta": "பௌத்தம் ஏற்றால் சமூகச் சான்றிதழ் பறிபோகுமா?",
          "en": "Will I lose my community certificate if I become a Buddhist?"},
         {"ta": "இல்லை. ஒரு பட்டியலினத்தவர் இந்து, சீக்கிய, பௌத்த மதம் ஆகிய "
                "இந்த மூன்றில் எதற்கு மாறினாலும், பின்பற்றினாலும், அவரின் "
                "சமூக உரிமைகளைப் பெறப் பட்டியலினம் (SC) என்றே சான்றிதழ் "
                "வழங்கப்படுகிறது.",
          "en": "No. Whichever of the three religions a Scheduled Caste person "
                "moves to or follows, Hindu, Sikh or Buddhist, the certificate "
                "is issued as Scheduled Caste (SC), so that their social rights "
                "are secured."}),
        ({"ta": "சான்றிதழ் பெற எங்கே விண்ணப்பிக்க வேண்டும்?",
          "en": "Where do I apply for the certificate?"},
         {"ta": "மற்றவர்கள் சமூகச் சான்றிதழ் பெறுவது போன்றே, இ-சேவை மையம் "
                "மூலமே விண்ணப்பித்துப் பெற்றுக்கொள்ளலாம். பௌத்தர்களுக்குத் "
                "தனி வழிமுறை எதுவும் இல்லை.",
          "en": "Through an e-Sevai centre, exactly as anyone else obtains a "
                "community certificate. There is no separate procedure for "
                "Buddhists."}),
        ({"ta": "CAN பதிவில் மதம் என்ன தேர்வு செய்வது?",
          "en": "What religion should I select in the CAN registration?"},
         {"ta": "CAN registration அல்லது குடிமக்கள் கணக்கு எண் பதிவு "
                "செய்கையில், மதம் என்ற இடத்தில் Buddhist என்று தேர்வு "
                "செய்தால் போதும்.",
          "en": "When completing the CAN registration, that is the Citizen "
                "Account Number registration, selecting Buddhist in the "
                "religion field is enough."}),
        ({"ta": "புதிய சான்றிதழில் மதம் ஏன் இல்லை?",
          "en": "Why does the new certificate not state a religion?"},
         {"ta": "பழைய சான்றிதழ்களில் மதம் குறிப்பிடப்பட்டு, அதன் பின்னர் "
                "உட்சாதி குறிப்பிடப்பட்டிருக்கும். சமீபத்திய "
                "சான்றிதழ்களில் மதம் குறிப்பிடப்படுவதில்லை; உட்சாதியும் "
                "சமூகமும் (SC) மட்டுமே குறிப்பிடப்படுகிறது.",
          "en": "Older certificates stated the religion, with the sub-caste "
                "after it. Recent certificates do not state the religion; only "
                "the sub-caste and the category (SC) appear."}),
        ({"ta": "அலுவலகத்தில் மறுத்தால் என்ன செய்வது?",
          "en": "What if the office refuses?"},
         {"ta": "நிலாதம்மாவைத் தொடர்பு கொள்ளுங்கள். இதுவரை "
                "நூற்றுக்கணக்கான குடும்பங்கள் இந்தச் செயல்முறையைக் "
                "கடந்திருக்கின்றன; சங்கம் உங்களுடன் உடன் நிற்கும்.",
          "en": "Get in touch with Niladhamma. Hundreds of families have "
                "already been through this process, and the sangha will stand "
                "with you."}),
    ],
    "dana": [
        ({"ta": "தானத்தில் எத்தனை வகை?", "en": "How many kinds of dana are there?"},
         {"ta": "கேள்வியைப் பொறுத்தது. கொடுக்கப்படும் பொருளை வைத்தால் "
                "மூன்று: ஆமிசம், அபயம், தம்மம். பெறுபவரை வைத்தால் இரண்டு: "
                "தனிநபருக்கு, சங்கத்திற்கு. கொடுக்கும் முறையை வைத்தால் "
                "மூன்று: தாஸம், சகாயம், சாமி. கொடுப்பதற்கான காரணங்களை "
                "வைத்தால் எட்டு.",
          "en": "It depends which question you are asking. By what is given, "
                "three: material goods, fearlessness, and the Dhamma. By who "
                "receives, two: an individual, or the Sangha. By the manner of "
                "giving, three: a slave's, a friend's, a master's. By the "
                "grounds for giving, eight."}),
        ({"ta": "எந்தத் தானம் உயர்ந்தது?", "en": "Which gift is the highest?"},
         {"ta": "தம்ம தானம். எல்லாக் கொடைகளையும் தம்மக் கொடை வெல்லும் "
                "என்கிறது தம்மபதம், செய்யுள் 354. உணவு ஒரு நாளைத் தாங்குகிறது; வழி "
                "ஒரு வாழ்க்கையைத் திருப்புகிறது.",
          "en": "The gift of the Dhamma. The gift of the Dhamma excels all "
                "gifts, says Dhammapada 354. Food carries someone through a "
                "day; the path can turn a life."}),
        ({"ta": "பணம் இல்லாதவர் தானம் செய்ய முடியுமா?",
          "en": "Can someone with no money give dana?"},
         {"ta": "முடியும். ஐந்து சீலங்களைக் கடைப்பிடிப்பதே ஐந்து "
                "பெருங்கொடைகள் என்று புத்தர் சொன்னார். கொல்லாமல், "
                "திருடாமல், பொய்யாமல் வாழ்பவர் தன்னைச் சுற்றியுள்ள "
                "எண்ணற்ற உயிர்களுக்கு அச்சமின்மையைக் கொடுக்கிறார். "
                "அதற்குச் செலவில்லை.",
          "en": "Yes. The Buddha called the five precepts five great gifts. "
                "Someone who lives without killing, without stealing and "
                "without lying is giving fearlessness to every being around "
                "them, and that costs nothing."}),
        ({"ta": "சங்கத்திற்குக் கொடுப்பதும் ஒருவருக்குக் கொடுப்பதும் "
                "வேறுபடுமா?",
          "en": "Is giving to the Sangha different from giving to a person?"},
         {"ta": "வேறுபடும். மகாபஜாபதி கோதமி தன் கையால் நெய்த ஆடையைத் "
                "தனக்குக் கொடுக்க வந்தபோது, அதைச் சங்கத்திற்குக் கொடுங்கள் "
                "என்று புத்தர் சொன்னார். சங்கத்திற்குக் கொடுப்பது பெரும் "
                "பயன் தரும் என்பது தக்கிணாவிபங்க சுத்தத்தின் கருத்து.",
          "en": "It is. When Mahapajapati Gotami came to offer him a robe she "
                "had woven herself, the Buddha told her to give it to the "
                "Sangha instead. A gift to the Sangha bears the greater fruit, "
                "the Dakkhinavibhanga Sutta holds."}),
        ({"ta": "மறுபிறவியில் பலன் கிடைக்கும் என்பதற்காகக் கொடுக்கலாமா?",
          "en": "Should one give in order to be repaid in a future birth?"},
         {"ta": "இல்லை. அது கம்மமும் மறுபிறவியும் பற்றிய பிராமணியக் "
                "கொள்கை; முற்பிறவிப் பாவத்தைச் சொல்லிச் சாதியை "
                "நியாயப்படுத்திய அதே கொள்கை. அம்பேத்கர் அதை மறுத்தார். "
                "புத்தரின் கம்மம் இம்மைக்கானது; ஆன்மாவே இல்லை என்று "
                "சொன்னவர், பலன் பெற ஒரு ஆன்மா மறுபிறவிக்குச் செல்கிறது "
                "என்று சொல்லியிருக்க முடியாது. தானவத்து சுத்தத்தில் அது "
                "ஒரு காரணமாகப் பட்டியலிடப்பட்டுள்ளது, பரிந்துரையாக "
                "அல்ல. நிலாதம்மா அதை ஏற்கவில்லை.",
          "en": "No. That is the Brahminical doctrine of kamma and rebirth, "
                "the same doctrine that justified caste by pointing to sin in "
                "an earlier life, and Ambedkar rejected it. The Buddha's kamma "
                "belongs to this life; a teacher who said there is no soul "
                "cannot have taught that a soul travels on to collect a "
                "reward. The Danavatthu Sutta lists it as a ground people "
                "give on, not as a recommendation. Niladhamma does not accept "
                "it."}),
    ],
    "events": [
        ({"ta": "பௌர்ணமி கூட்டத்திற்கு யார் வரலாம்?",
          "en": "Who can come to the full moon gathering?"},
         {"ta": "அனைவரும். பௌத்தராக இருக்க வேண்டியதில்லை; முன்பதிவோ "
                "கட்டணமோ இல்லை. அசோக் நகர் புத்த விஹாரில் ஒவ்வொரு பௌர்ணமி "
                "நாளும் மாலை 6 மணி முதல் கூடுகிறோம். குழந்தைகளுடன் "
                "வரலாம்.",
          "en": "Anyone. You do not have to be a Buddhist, and there is no "
                "booking and no fee. We meet at Ashok Nagar Buddha Vihar on "
                "every full moon day from 6pm. Children are welcome."}),
        ({"ta": "கூட்டம் எவ்வளவு நேரம் நடக்கும்?",
          "en": "How long does it last?"},
         {"ta": "சுமார் இரண்டு மணி நேரம். வந்தனை, பஞ்சசீலம், தியானம், "
                "தம்மக் கதை வாசிப்பு, கலை நிகழ்ச்சிகள், இறுதியில் "
                "சேர்ந்து உணவு.",
          "en": "About two hours: homage, the five precepts, meditation, a "
                "Dhamma story read aloud, performances from the children, and "
                "a shared meal at the end."}),
        ({"ta": "எதையாவது எடுத்து வர வேண்டுமா?",
          "en": "Do I need to bring anything?"},
         {"ta": "எதுவும் தேவையில்லை. உடைக் கட்டுப்பாடு இல்லை. தரையில் "
                "அமர விரிப்புகள் உண்டு; நாற்காலிகளும் உண்டு. பாலி வரிகள் "
                "தெரியாவிட்டால் கேட்டிருந்தாலே போதும்.",
          "en": "Nothing at all. There is no dress code. There are mats on the "
                "floor and chairs as well. If you do not know the Pali lines, "
                "listening is enough."}),
        ({"ta": "அடுத்த பௌர்ணமி எப்போது?",
          "en": "When is the next full moon gathering?"},
         {"ta": "இப்பக்கத்தின் நாட்காட்டியில் வரவிருக்கும் நாட்கள் "
                "தரப்பட்டுள்ளன. மரபுவழி உபோசத நாள் உள்ளூர் சந்திர "
                "கணக்கைப் பொறுத்து ஒரு நாள் மாறலாம்; சங்கத்தின் "
                "அறிவிப்பே இறுதியானது.",
          "en": "The calendar on this page lists the upcoming dates. The "
                "uposatha day as observed can shift by a day depending on the "
                "local lunar reckoning, so the sangha's own announcement is "
                "authoritative."}),
        ({"ta": "பௌர்ணமி தவிர வேறு என்ன நிகழ்வுகள்?",
          "en": "What else happens besides the full moon?"},
         {"ta": "புத்த பூர்ணிமா, அசோக விஜயதசமி, பௌத்த மறுமலர்ச்சி தினம், "
                "பௌத்தக் கொடி நாள் போன்ற பண்பாட்டு விழாக்கள்; தம்மப் "
                "பயிற்சி முகாம், விபாசனா கூட்டுத் தியானம், ஆன்லைன் தம்ம "
                "வகுப்பு; பௌத்த மகாமங்கள திருமணங்கள்.",
          "en": "Cultural observances such as Buddha Purnima, Ashoka "
                "Vijayadashami, Buddhist Revival Day and Buddhist Flag Day; "
                "Dhamma retreats, group Vipassana and online Dhamma classes; "
                "and Buddhist Mahamangala marriages."}),
    ],
    "matrimony": [
        ({"ta": "பௌத்த மகாமங்கள திருமணம் என்றால் என்ன?",
          "en": "What is a Buddhist Mahamangala marriage?"},
         {"ta": "சாதி, சடங்கு, பொருட்செலவு என்ற சுமைகளின்றி, சமத்துவத்தை "
                "மையமாகக் கொண்டு நடத்தப்படும் திருமண முறை. வந்தனை, "
                "திரிசரணம், பஞ்சசீலம், உறுதிமொழி, ஆசி என அமைதியாக நிகழ்கிறது.",
          "en": "A marriage rite conducted with equality at its centre, "
                "without the burdens of caste, ritual or expense. It proceeds "
                "quietly: homage, the three refuges, the five precepts, the "
                "vows, and the blessing."}),
        ({"ta": "சங்கம் என்ன உதவி செய்யும்?",
          "en": "What help does the sangha give?"},
         {"ta": "திருமண நிகழ்வை முழுமையாக ஒருங்கிணைத்தல், பௌத்த முறையிலான "
                "வழிபாட்டு ஒழுங்கை வகுத்தல், அரசிதழில் பதிவு செய்வதற்கான "
                "வழிகாட்டுதல், திருமணச் சான்றிதழ் பெறுவதற்கான உதவி.",
          "en": "Organising the marriage in full, setting out the order of the "
                "Buddhist rite, guidance on registering in the government "
                "gazette, and help in obtaining the marriage certificate."}),
        ({"ta": "துணை தேடல் பதிவு எப்படி நடக்கிறது?",
          "en": "How does the matrimony register work?"},
         {"ta": "விவரங்கள் சங்கத்திடம் மட்டுமே இருக்கும்; வெளியில் "
                "வெளியிடப்படுவதில்லை. பொருத்தமான தொடர்புகள் மட்டுமே "
                "இருதரப்பு ஒப்புதலுடன் பகிரப்படும்.",
          "en": "The details stay with the sangha alone; they are not "
                "published. Only suitable introductions are shared, and only "
                "with the consent of both sides."}),
    ],
}
