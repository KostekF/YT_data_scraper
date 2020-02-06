# YT_data_scraper

Program scrapuje dane o filmach na YouTube po wpisaniu przez nas oczekiwanej frazy. 
Scrapowane dane: link, nazwa, opis, kategoria, data dodania filmu.

Program wykorzystuje wątki w celu szybszego pobierania stron z filmami.

Program zwraca jsona z danymi każdego filmu zapisanymi w oddzielnym JsonObject.

Przykładowe wywołanie programu: python3 yt_scraping.py {szukana fraza} 
