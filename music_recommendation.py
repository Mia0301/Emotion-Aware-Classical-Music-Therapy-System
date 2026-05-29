def recommend_music(emotion):
    emotion = emotion.lower()

    music_map = {
        "happy": {
            "emoji": "😊",
            "description": "Bright and cheerful classical piano music.",
            "therapy": "Maintain a positive mood with bright and energetic piano music.",
            "image": "https://images.unsplash.com/photo-1511379938547-c1f69419868d",
            "music": [
                {
                    "title": "Mozart - Turkish March",
                    "composer": "Wolfgang Amadeus Mozart",
                    "era": "Classical Period",
                    "reason": "Fast tempo and cheerful melody match a happy emotion.",
                    "url": "https://www.youtube.com/results?search_query=Mozart+Turkish+March+piano"
                },
                {
                    "title": "Mozart - Piano Sonata No.16",
                    "composer": "Wolfgang Amadeus Mozart",
                    "era": "Classical Period",
                    "reason": "Light and bright piano style helps maintain a positive mood.",
                    "url": "https://www.youtube.com/results?search_query=Mozart+Piano+Sonata+No+16"
                },
                {
                    "title": "Beethoven - Für Elise",
                    "composer": "Ludwig van Beethoven",
                    "era": "Classical / Romantic",
                    "reason": "Familiar and lively melody is suitable for a pleasant mood.",
                    "url": "https://www.youtube.com/results?search_query=Beethoven+Fur+Elise+piano"
                }
            ]
        },

        "sad": {
            "emoji": "😢",
            "description": "Soft and emotional classical piano music.",
            "therapy": "Listen to soft piano music and take a short rest.",
            "image": "https://images.unsplash.com/photo-1507838153414-b4b713384a76",
            "music": [
                {
                    "title": "Chopin - Nocturne Op.9 No.2",
                    "composer": "Frédéric Chopin",
                    "era": "Romantic Period",
                    "reason": "Soft and lyrical melody is suitable for sadness and emotional relaxation.",
                    "url": "https://www.youtube.com/results?search_query=Chopin+Nocturne+Op+9+No+2"
                },
                {
                    "title": "Debussy - Clair de Lune",
                    "composer": "Claude Debussy",
                    "era": "Impressionist Period",
                    "reason": "Dreamlike atmosphere helps calm sad emotions.",
                    "url": "https://www.youtube.com/results?search_query=Debussy+Clair+de+Lune"
                },
                {
                    "title": "Liszt - Liebestraum No.3",
                    "composer": "Franz Liszt",
                    "era": "Romantic Period",
                    "reason": "Emotional and expressive piano music supports emotional release.",
                    "url": "https://www.youtube.com/results?search_query=Liszt+Liebestraum+No+3"
                }
            ]
        },

        "angry": {
            "emoji": "😠",
            "description": "Powerful piano music for emotional release.",
            "therapy": "Take deep breaths and use strong but structured music to release tension.",
            "image": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0",
            "music": [
                {
                    "title": "Beethoven - Moonlight Sonata",
                    "composer": "Ludwig van Beethoven",
                    "era": "Classical / Romantic",
                    "reason": "Strong emotional expression can help release anger.",
                    "url": "https://www.youtube.com/results?search_query=Beethoven+Moonlight+Sonata+piano"
                },
                {
                    "title": "Chopin - Prelude Op.28 No.4",
                    "composer": "Frédéric Chopin",
                    "era": "Romantic Period",
                    "reason": "Slow and serious mood helps reduce tension.",
                    "url": "https://www.youtube.com/results?search_query=Chopin+Prelude+Op+28+No+4"
                },
                {
                    "title": "Rachmaninoff - Prelude in C Sharp Minor",
                    "composer": "Sergei Rachmaninoff",
                    "era": "Late Romantic Period",
                    "reason": "Dramatic and powerful style matches intense emotion.",
                    "url": "https://www.youtube.com/results?search_query=Rachmaninoff+Prelude+in+C+Sharp+Minor"
                }
            ]
        },

        "neutral": {
            "emoji": "😐",
            "description": "Peaceful piano music for a stable mood.",
            "therapy": "Use calm piano music as background music to maintain emotional balance.",
            "image": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0",
            "music": [
                {
                    "title": "Bach - Prelude in C Major",
                    "composer": "Johann Sebastian Bach",
                    "era": "Baroque Period",
                    "reason": "Stable harmony and simple flow suit a neutral mood.",
                    "url": "https://www.youtube.com/results?search_query=Bach+Prelude+in+C+Major"
                },
                {
                    "title": "Satie - Gymnopédie No.1",
                    "composer": "Erik Satie",
                    "era": "Modern / Impressionist",
                    "reason": "Calm and minimal melody helps maintain relaxation.",
                    "url": "https://www.youtube.com/results?search_query=Satie+Gymnopedie+No+1"
                },
                {
                    "title": "Schubert - Impromptu Op.90 No.3",
                    "composer": "Franz Schubert",
                    "era": "Romantic Period",
                    "reason": "Gentle and balanced piano sound fits stable emotion.",
                    "url": "https://www.youtube.com/results?search_query=Schubert+Impromptu+Op+90+No+3"
                }
            ]
        },

        "surprise": {
            "emoji": "😲",
            "description": "Fast and lively classical piano music.",
            "therapy": "Use lively music to stabilize sudden emotional changes.",
            "image": "https://images.unsplash.com/photo-1506157786151-b8491531f063",
            "music": [
                {
                    "title": "Mozart - Rondo Alla Turca",
                    "composer": "Wolfgang Amadeus Mozart",
                    "era": "Classical Period",
                    "reason": "Fast rhythm and playful melody fit surprise.",
                    "url": "https://www.youtube.com/results?search_query=Mozart+Rondo+Alla+Turca"
                },
                {
                    "title": "Beethoven - Für Elise",
                    "composer": "Ludwig van Beethoven",
                    "era": "Classical / Romantic",
                    "reason": "Recognizable melody creates a light and active feeling.",
                    "url": "https://www.youtube.com/results?search_query=Beethoven+Fur+Elise+piano"
                },
                {
                    "title": "Tchaikovsky - Dance of the Sugar Plum Fairy",
                    "composer": "Pyotr Ilyich Tchaikovsky",
                    "era": "Romantic Period",
                    "reason": "Magical and playful sound matches sudden surprise.",
                    "url": "https://www.youtube.com/results?search_query=Tchaikovsky+Dance+of+the+Sugar+Plum+Fairy+piano"
                }
            ]
        },

        "fear": {
            "emoji": "😨",
            "description": "Gentle piano music to create comfort.",
            "therapy": "Listen to soft music and focus on slow breathing.",
            "image": "https://images.unsplash.com/photo-1507838153414-b4b713384a76",
            "music": [
                {
                    "title": "Yiruma - River Flows in You",
                    "composer": "Yiruma",
                    "era": "Contemporary",
                    "reason": "Soft and simple melody gives a comforting feeling.",
                    "url": "https://www.youtube.com/results?search_query=Yiruma+River+Flows+in+You"
                },
                {
                    "title": "Debussy - Arabesque No.1",
                    "composer": "Claude Debussy",
                    "era": "Impressionist Period",
                    "reason": "Flowing melody helps reduce fear and anxiety.",
                    "url": "https://www.youtube.com/results?search_query=Debussy+Arabesque+No+1"
                },
                {
                    "title": "Satie - Gnossienne No.1",
                    "composer": "Erik Satie",
                    "era": "Modern / Impressionist",
                    "reason": "Slow and mysterious sound helps calm unstable emotion.",
                    "url": "https://www.youtube.com/results?search_query=Satie+Gnossienne+No+1"
                }
            ]
        },

        "disgust": {
            "emoji": "🤢",
            "description": "Slow and relaxing piano music.",
            "therapy": "Use relaxing music to shift attention and reduce negative feelings.",
            "image": "https://images.unsplash.com/photo-1511379938547-c1f69419868d",
            "music": [
                {
                    "title": "Debussy - Reverie",
                    "composer": "Claude Debussy",
                    "era": "Impressionist Period",
                    "reason": "Soft atmosphere helps shift attention from negative emotion.",
                    "url": "https://www.youtube.com/results?search_query=Debussy+Reverie+piano"
                },
                {
                    "title": "Chopin - Waltz in A Minor",
                    "composer": "Frédéric Chopin",
                    "era": "Romantic Period",
                    "reason": "Gentle and slightly melancholic style helps emotional relaxation.",
                    "url": "https://www.youtube.com/results?search_query=Chopin+Waltz+in+A+Minor"
                },
                {
                    "title": "Brahms - Intermezzo Op.118 No.2",
                    "composer": "Johannes Brahms",
                    "era": "Romantic Period",
                    "reason": "Warm and calm piano texture helps reduce discomfort.",
                    "url": "https://www.youtube.com/results?search_query=Brahms+Intermezzo+Op+118+No+2"
                }
            ]
        }
    }

    return music_map.get(emotion, music_map["neutral"])
