import time, openai, ftfy, requests
from unsplash.api import Api
from unsplash.auth import Auth

client_id = "KgSkM_iREcGUZA4PYUwPUmg1vFxLsiaNJkpWXGoXJnA"
client_secret = "31RTVz0Fk045ZBRklmJ-eAFwAIcO4kz8WBz8mNPK09U"
redirect_uri = ""
code = ""
openai.api_base = "https://neuroapi.host/v1"
openai.api_key = "sk-X8pOq3nPsXw1lRtUA9AcB19aE42f4fE29800122a3c60D40c"
auth = Auth(client_id, client_secret, redirect_uri, code=code)
api = Api(auth)
photo = api.search.photos("office")
print(photo['results'][0])
url = photo['results'][0].links.download
response = requests.get(url, allow_redirects=True)
open('../bild.jpg', 'wb').write(response.content)

# Automatic selection of provider
prompt = '''Schreibe den folgenden Artikel um, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der neue Artikel muss mindesttens so lang wie der gegebene Artikel sein.
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt:
Keywords:
Kategorie:
Bildtag:

Artikel:
Titel: Regierung und Opposition bilden Notstandsregierung
Beschreibung: Israels Ministerpräsident Netanyahu hat sich mit der Opposition auf die Bildung einer Notstandsregierung geeinigt. Beobachter werten den Schritt als Zeichen einer möglicherweise bevorstehenden Bodenoffensive im Gazastreifen.
Inhalt: Israels Ministerpräsident Benjamin Netanyahu hat sich mit Oppositionspolitiker Benny Gantz auf die Bildung einer "gemeinsamen Notstandsregierung und eines Kriegskabinetts" geeinigt. Das teilten beide in einer gemeinsamen Erklärung mit. Israelische Medien berichten, dass Netanyahu, Verteidigungsminister Joav Galant sowie der ehemalige Verteidigungsminister Gantz von der Partei Nationale Union das Kriegskabinett bilden. Als Beisitzer ohne Stimmrecht sollen der ehemalige Generalstabschef Gadi Eisenkot und Likud-Minister Ron Dermer dienen. Gantz will den Berichten zufolge fünf Minister für das Sicherheitskabinett stellen. Oppositionsführer Jair Lapid schloss sich nicht an, ihm werde aber ein Sitz in dem neuen Kabinett freigehalten. Zuvor hatten sich die Spitzen der Regierungskoalition einstimmig für die Bildung einer Notstandsregierung mit der Opposition ausgesprochen. Ohne Ausnahme unterstütze die Koalition dieses Vorhaben und autorisiere Netanyahu, sich dafür einzusetzen, teilte ein Sprecher von Netanyahus Likud-Partei nach einem Treffen der Koalition. Netanyahu hatte am Samstag den beiden Oppositionsführern Lapid und Gantz den Eintritt in eine Notstandsregierung angeboten. Seit Tagen laufen im Hintergrund Bemühungen über eine Einigung. Lapid hatte schon Bereitschaft signalisiert. Er habe Netanyahu angeboten, eine Koalition zu bilden, "die den harten, komplexen und langen Krieg führen kann, der uns bevorsteht". Experten gehen davon aus, dass eine breite Koalition notwendig ist, um weitreichende militärische und politische Entscheidungen in den nächsten Tagen durchsetzen zu können. Viele Beobachter werten die Bemühungen um eine solche Notstandsregierung daher als Zeichen einer möglicherweise bevorstehenden israelischen Bodenoffensive in den Gazastreifen. Seit Jahresbeginn ist es in Israel zu massiven Protesten gegen einen Justizumbau gekommen, den Netanyahus teilweise rechtsextreme Regierung vorantreibt. Der bittere Streit polarisierte die Gesellschaft. Einige Beobachter glauben, Israel sei durch die internen Streitigkeiten von der Gefahr, die von der Hamas ausging, abgelenkt gewesen.'''


# streamed completion

for i in range(10):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    print(ftfy.fix_text(answer))
    time.sleep(2)
    print("---------------------------------------------------")