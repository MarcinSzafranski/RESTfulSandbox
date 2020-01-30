Cześć,
Żeby zobaczyć jak działa wykonane przeze mnie zadanie najlepiej będzie jeśli po pełnym uruchomieniu docker-compose
ustawi się w definitions.py DOCKER_FLASK_URL - wystarczy zmienić adres IP na dockerowy osiągalny z własnego
środowiska.
Następnie - można zajrzeć do use_example.py lub wykonać komendę 'python use_example.py'. Uruchomią się przykładowe,
poprawne zapytania do API z 10 sekundową przerwą na wykonanie poleceń.

Przykładowe użycie API:
1. GetUrlContents czyli pobranie tekstu i obrazów ze strony oraz zapisanie ich w systemie. Obrazy są umieszczane w
archiwum o nazwie odpowiadającej tej podanej w zapytaniu do API. Nazwy są unikalne. Zwraca ID uruchomionego zadania.
http://HOST_IP:5000/url/<name>/<path:url>       : http://HOST_IP:5000/url/painting/https://www.saatchiart.com/paintings
2. GetTaskStatus czyli uzyskanie statusu zadania na podstawie jego ID:
http://HOST_IP:5000/status/<task_id>            : http://HOST_IP:5000/status/0b81ce65-0316-40db-8bf0-c641427203d3
3. DownloadFile czyli pobieranie obrazów lub tekstu na podstawie nazwy nadanej w GetUrlContents.
http://HOST_IP:5000/download/<name>/<file_type> : http://HOST_IP:5000/download/painting/images
                                                : http://HOST_IP:5000/download/painting/text

Co poszło OK:
Wszystko działa w przypadku poprawnego użycia, obrazy zapisywane są w folderze 'images' w podfolderach o nazwie podanej
w zapytaniu do API, tekst zapisywany jest w bazie danych. W bazie danych przechowywane są wpisy dotyczące tego jaki plik
i jaki tekst przypisany jest do danej nazwy zadania.

Technologie: Opis zadania był tak skonstruowany, że od razu ułożyła mi się w głowie lista bibliotek jakie mógłbym
zastosować. Implementacja i spięcie wszystkiego razem zajęła mi dużo czasu ponieważ nie znałem dobrze części tych bibliotek,
ale mając więcej czasu na przeczytanie dokumentacji i wypróbowanie różnych opcji w praktyce - kod pewnie byłby lepiej
zorganizowany i optymalny.

Testy: Do ostatniego dnia byłem przekonany, że chodzi o testy jednostkowe. Tutaj znowu problematyczne było wykorzystanie
różnych bibliotek po raz pierwszy. Jeśli chodziło o testy funkcjonalne - niestety, jedyne co mogę zaoferować to przykład
użycia w use_example.py.

Co nie poszło ok:
Na pewno ta aplikacja nie jest dobrze zabezpieczona. Pomijając kwestie logowania, haseł itp., nie sądzę żeby trudno było
znaleźć nieobsłużony wyjątek. Strukturę folderów aplikacji również można by było lepiej zorganizować, natomiast przy tak
małej aplikacji uznałem to za kwestię drugorzędną.
Również nie dam sobie głowy obciąć za wyszukiwanie obrazów i czyszczenie tekstu ze strony, ale to z kolei dość skomplikowane
zagadnienia i na pewno łatwiej byłoby pisać API dla konkretnej strony.

Pozdrawiam,
Marcin Szafrański
