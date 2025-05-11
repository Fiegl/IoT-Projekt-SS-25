# Abschlussbericht Stefan Fiegl SE III


## Einleitung

Im Rahmen des Moduls SE III (1.5) habe ich zusammen mit Marvin Volkmann und Patrick Diebold eine Webseite zur Buchung von Arbeitszeit erstellt. 
In diesem Bericht möchte ich zuerst auf die eingesetzten Mittel im Sinne des Projekt-Managements eingehen und wie unsere Vorstellung und deren technische Umsetzung aussah; Anschließend mein individueller Beitrag zum Projekt und auf welche Probleme und Herausforderungen man gestoßen ist.



## Projekt-Management

Zuerst haben wir auf Teams einen Projekt-Ordner erstellt und unter dem Reiter Aufgaben-Liste ein Kan-Ban-System eingerichtet, welches unterteilt war in die Bereiche Frontend, Backend und Organisation (siehe ScreenShot).

![ScreenShot](https://i.imgur.com/6j2nCzX.png)

Wir haben bei diesem Projekt auf in sich abgeschlossene Sprints verzichtet und mehr Wert auf Agilität gelegt. Im Hinblick auf die Komplexität dieses Projektes lag der Schwerpunkt auf dem Bereich Backend, weniger auf die Erstellung von Templates.
Zum Austausch von Code wurde die Plattform GitHub (Link: https://github.com/Fiegl/Sys1-Projekt-DVM2023) genutzt; sobald ein Team-Mitglied den Code aktualisiert hat, wurde entsprechend im Teams-Ordner ein Beitrag gepostet. Zusätzlich kam auf GitHub die Pull-Request-Funktion zum Einsatz, d.h. neuer Code wurde erst mal als Vorschlag eingetragen und konnte dann von einem anderen Team-Mitglied bestätigt ("gemergt") werden. Erst dann wurde der alte Code aktualisiert.
Auf dem Teams-Ordner hat Patrick zudem eine Word-Tabelle eingestellt, die eine Übersicht über alle geforderten Funktionen enthielt. Gemäß den Ampel-System wurden dann die Funktionen ihrem Bearbeitungsstand entsprechend von den jeweiligen Team-Mitgliedern gefärbt (grün = fertig, gelb = in Bearbeitung, rot = ausstehend). 
Um den aktuellen Projekt-Fortschritt zu besprechen, neue Aufgaben zuzuweisen oder technische Herausforderungen anzugehen, haben wir in zeitlich unabhängigen Abständen oder kurzfristig auf Abruf Video-Konferenzen (jour fixe) auf Teams abgehalten.



## Grundgedanken, "Spielregeln"

Im ersten Jour fix wurden generelle Gedanken ausgestauscht, zum groben Aufbau im Frontend, wie die Daten im Backend gespeichert werden oder ob in unserem Zeitbuchungs-System ein Timer ingtegriert werden soll.

Wir haben uns dann auf folgende Parameter geeinigt:

- es werden aus dem Django-Framework nur notwendige Module importiert, sowie sinnvolle Module (z.B. uuid)
- keine Benutzung der Django-internen SQL-Datenbank, Daten sollen in JSON-Datenbanken persistiert werden
- der User soll seine Arbeitsberichte händisch eintragen, kein Einsatz eines Timers beim Anklicken eines Semester-Moduls



## Frontend

Wie bereits oben erwähnt, lag der Schwerpunkt der Arbeit im Backend und in der logischen Verknüpfung der JSON-Datenbanken mit den Funktionen in der views.py (Korrelation).
Für die Webseite wurden insgesamt 10 Templates plus dazugehörige CSS-Dateien eingebaut. Auf neuartigen Code in den Templates (z.B. HTML-Tabellen) gehe ich gesondert bei den Funktionen in den Kacheln der Home-Seite ein.
Wie bereits im Vor-Projekt wurden die einzelnen Pfade der Templates in der Datei urls.py des App-Ordners angelegt. Diese Datei wiederum wurde referenziert in der übergeordneten Datei urls.py im allgemeinen Projekt-Ordner.
Die CSS-Dateien wurden wie gewohnt im "static"-Ordner abgelegt. Oftmals gab es Probleme, Änderungen im CSS anzeigen zu lassen; das habe ich dadurch gelöst, indem ich im Browser den Cache gelöscht habe. 
Gegen Ende des Projektes habe ich bei allen Templates im head-Element noch eine Meta-Tag-Deklaration eingefügt für mehr responsives Design. 
Ebenso media queries in den CSS-Dateien für eine optimierte Darstellung auf Smartphones.
Für uns war es wichtig, frühzeitig ein Frontend mit den grundlegenden Funktionen wie Registrierung, Ein- und Ausloggen zu erstellen (Grundstock), um uns mit der herausfordernden Aufgabe der neuen Funktionen zu beschäftigen.



## Grundstock 

Nächster Schritt war der Aufbau eines Grundstockes für die Webseite, d.h. es mussten die grundlegenden Templates (login, register, home) plus der dazugehörigen Logik im Backend erstellt werden. Ich habe mich um die Funktion Ein- und Ausloggen gekümmert und mit an der Funktion Registrieren gearbeitet.
Ursprünglich hatte das Template register.html nur 2 Eingabe-Felder (Benutzername + Passwort). Patrick hat dies dann später um ein weiteres Feld names "Matrikelnummer" sowie ein verstecktes input-Attribut ("status") erweitert. Der neue User kann sich somit mit Name, Passwort und seiner Matrikel-Nr. registrieren und gleichzeitig wird er im Backend als "basis"-User (Status) hinterlegt.

Als nächster Schritt für den Aufbau des Grundstockes war die Home-Seite unserer Webseite. 
Hier eine Abbildung einer früheren Idee der home.html 

<img src="https://i.imgur.com/Unk3OnW.png" alt="ScreenShot" width="500" height="300">

Ich entschloss mich dann dazu, ein sogenanntes Kachel-System auf der Home-Seite einzurichten, unterteilt in 4 Kacheln, welche die einzelnen Funktionen schlüssig und aufbauend wiedergeben sollten. Wichtig war hier eine Benutzerfreundlichkeit im Frontend und eine übersichtliche, logische Struktur, nach der der User seinen Arbeitsbericht eintragen, ansehen, je nach Status herrunterladen konnte.

Insgesamt wurden vier Kacheln eingerichtet, nämlich: "Arbeitsbericht anlegen", "alle Berichte anzeigen", "Download&Upload", "dein Profil"

<img src="https://i.imgur.com/F1mXjXr.png" alt="ScreenShot" width="500" height="300">

Um die Templates vor unauthorisiertem Zugriff zu schützen (nicht eingeloggter User), haben wir bei allen Funktionen der zu schützenden Templates die Code-Zeile "username = request.session.get("username")" verwendet, wonach bei einem eingeloggten User der Name geprüft wird; falls nicht, wird er auf die Login-Seite geleitet.
Im vorherigen Projekt wurden @login_required-Decorators seitens Django verwendet.



## Die Funktionen der Kacheln (Backend)

Meine Schwerpunkt-Aufgabe waren die Funktionen bei den Kacheln "Download&Upload" und "alle Berichte anzeigen".

### die Kachel "Arbeitsbericht anlegen"

Das Template "arbeitsbericht_erstellen" hat Marvin erstellt. Anschließend haben wir zu dritt in der views.py die Funktionen eingebaut.
Erste große Hürde war es, die Eingaben des Users in eine JSON-Datei abzuspeichern. Hierzu haben wir die JSON-Datei "arbeitsberichte.json" angelegt.
Diese Datenbank gilt als Informations-Quelle für viele weitere Funktionen.
Beim Anlegen der JSON-Datei kam die große Herausforderung, die Struktur so zu gestalten, dass nacheinander erstellte Arbeitsberichte abgespeichert werden können. 
Zudem sollte jeder Arbeitsbericht nicht nur einer Person zugeordnet werden können, sondern der Bericht sollte auch später anhand einer bestimmten Wertes referenziert werden.
Patrick hat hier das Modul uuid importiert, wonach jedem einzelnen Arbeitsbericht eine eigene ID zugeordnet werden kann.
Anbei ein ScreenShot, der einen Teil der Funktion für das Template darstellt; hier werden die vom User gemachten Eingaben in die JSON persistiert und jeder neue Arbeitsbericht
wird in der JSON gespeichert (serialisiert). Siehe ScreenShot:
![ScreenSHot](https://i.imgur.com/CEzNDlI.png)

### die Kachel "alle Berichte anzeigen"

Eine weitere Vorgabe war, dass der User sich eine Übersicht all seiner erstellten Arbeitsberichte anzeigen lassen kann. Hier war die erste Problem-Stellung, wie die technische Umsetzung, gerade im Template, erfolgen soll.
Bei der Vorstellung des Projekt-Fortschritts anderer Teams war dann schnell klar, dass sich dafür am besten eine HTML-Tabelle eignet.
Diese ist aufgebaut in einem table-Element, das wiederum in eine Kopfzeile (thead) und den restlichen Tabellen-Körper (tbody) aufgebaut ist.
Innerhalb des tbody-Elements können dann tr-Elemente für jede weitere Zeile genutzt werden. In diesem tr-Element werden dann td-Element gebaut, also Spalten, die dann die jeweilige Werte der Arbeitsberichte aus der JSON-Datenbank enthalten.
Ein weiteres großes Problem war, dass in dieser Übersicht nur die Arbeitsberichte des Users angezeigt werden sollen und eben nicht die Berichte aller User. Dies wurde dadurch gelöst, indem Patrick die Syntax in der JSON der gespeicherten Arbeitsberichte so strukturiert hat, dass
Die Korrelation zwischen dem Template "arbeitsberichte_anzeigen.html" und den Funktionen in der views.py erfolgt durch einen sogenannten Django-Loop; also durch eine als Variable in der views.oy definierte Schleife, die im Template die entsprechenden Spalten durchiteriert und die Werte aus der JSON-Datei dann als HTML-Tabelle anzeigt.
Ich habe dann noch eine zusätzliche Spalte eingefügt und dort ein Form-Element eingebaut, mit der Funktion zur Löschung des jeweiligen Arbeitsberichtes.
Code-Beispiel Korrelation:
![ScreenShot](https://i.imgur.com/3UcbKgx.png)

### die Kachel "Download & Upload"

Hier war einerseits die Vorgabe, dass der User, sofern er zum VIP oder höher geupgradet wurde, die Möglichkeit hat, seine erstellten Arbeitsberichte in die Formate JSON, CSV und XML herunterzuladen. Zudem soll es eine Funktion geben, dass er einen heruntergelanden Bericht im JSON-Format abändern und als JSON-Datei wieder hochladen kann.
Auch hier ist wieder die JSON-Datenbank mit den gespeicherten Berichten die Quelle aller Information an Daten.
Ich habe hier wie ähnlich bei dem Template "arbeitsberichte_anzeigen.html" eine HTML-Tabelle erstellt. Zusätzlich habe ich in den Spalten des jeweiligen Arbeitsberichtes Buttons eingebaut für den Download im jeweiligen Datei-Format.
Während sich der Arbeits-Bericht problemlos als CSV-Datei (Excel) herunterladen lies, fiel mir auf, dass beim Download von JSON und XML der Inhalt im Browser angezeigt wird und nicht separat eine Datei heruntergeladen worden ist.
Dieses Problem habe ich dadurch gelöst, dass ich bei den einzelnen Download-Funktionen in der views.py folgende Zeile eingefügt habe:

response["Content-Disposition"] = f'attachment; filename="bericht_{bericht_id}.xml"'    (Beispiel für XML-Format)

Diese Zeile bewirkt eine Anweisung an den Browser, die Datei explizit herunterzuladen, anstatt sie im Browser anzeigen zu lassen.
In der views.py habe ich für jeden Download dem Datei-Format entsprechend eine Funktion erstellt.

Wie ich im Austausch mit einem anderen Team erfahren habe, wäre auch der Import der Python-Bibliothek pandas eine Option gewesen, um mit noch weniger Code Daten im JSON-, CSV- oder XML-Format zu bearbeiten.

Beispiel-Code für Funktion JSON-Download:
![ScreenShot](https://i.imgur.com/53JHj7b.png)

Weitaus größere Schwierigkeiten hatte ich bei der Erstellung der Funktion für den JSON-Upload:
Es galt zu beachten, dass das System die hochgeladene und veränderte JSON-Datei als dieselbe erkennt wie beim Herunterladen und entsprechend in der JSON-Datenbank der Arbeitsberichte überschreibt.

Im Template "arbeitsberichte_download_drucken.html" habe ich eine zusätzliche Spalte eingefügt und darin ein multipart form data eingefügt, um ein HTTP-request für das Hochladen der JSON-Datei zu erzeugen. Zusätzlich wurde dem input-Element ein accept-Attribut hinzugefügt mit dem Wert ".json", wonach eben nur Dateien im JSON-Format hochgeladen werden können.
Mit der Code-Zeile "request.FILES.get("upload_file")" greift die Funktion in der views.py auf das input-Element zu und prüft anschließend, ob es sich um eine JSON-Datei handelt. Erst bei gültiger Prüfung wird sie hochgeladen. Zuvor wird die JSON-Datei mit den Arbeitsberichten geöffnet und die bestehenden Berichte in die Variable "daten" gespeichert (Deserialisierung).
Die Herausforderung, dass das System die neue Datei mit der alten überschreiben soll und nicht als völlig neuen Bericht zusätzlich abspeichern soll, wurde damit gelöst, dass die JSON-Datei eine eigene ID (uuid) enthalten muss. Wenn die JSON-Datei keine ID enthält, wird sie gar nicht erst hochgeladen. Sollte sie aber eine vom System zugewiesene ID enthalten, dann wird sie entsprechend in der JSON-Datenbank der Arbeitsberichte überschrieben (Serialisierung).

Beispiel-Code Korrelation:
![ScreenShot](https://i.imgur.com/9GviVjK.png)



### die Kachel "mein Profil"

Hierfür war ich nicht verantwortlich.



## Fazit

Uns ist es leider nicht mehr gelungen eine Klasse im Sinne der OOP zu integrieren. Denn eine Klasse hat den Vorteil, dass sie mehrere Funktionen bündelt. Somit muss man nicht mehr einzelne Funktionen aufrufen, sondern eben nur die entsprechende Klasse.