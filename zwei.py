import g4f, time
from g4f.Provider import *

g4f.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking
print(g4f.version) # check version
print(g4f.Provider.Ails.params)  # supported args

# Automatic selection of provider
prompt = '''Schreibe den folgenden Artikel um, erfinde nichts hinzu, benutze Fesselnde und informative Sprache. Der neue Artikel muss mindesttens so lang wie der gegebene Artikel sein.
Benutze folgendes Layout:
Titel:
Beschreibung:
Inhalt:
Keywords:
Kategorie:

Artikel:
Titel: Regierung und Opposition bilden Notstandsregierung
Beschreibung: Israels Ministerpräsident Netanyahu hat sich mit der Opposition auf die Bildung einer Notstandsregierung geeinigt. Beobachter werten den Schritt als Zeichen einer möglicherweise bevorstehenden Bodenoffensive im Gazastreifen.
Inhalt: Israels Ministerpräsident Benjamin Netanyahu hat sich mit Oppositionspolitiker Benny Gantz auf die Bildung einer "gemeinsamen Notstandsregierung und eines Kriegskabinetts" geeinigt. Das teilten beide in einer gemeinsamen Erklärung mit. Israelische Medien berichten, dass Netanyahu, Verteidigungsminister Joav Galant sowie der ehemalige Verteidigungsminister Gantz von der Partei Nationale Union das Kriegskabinett bilden. Als Beisitzer ohne Stimmrecht sollen der ehemalige Generalstabschef Gadi Eisenkot und Likud-Minister Ron Dermer dienen. Gantz will den Berichten zufolge fünf Minister für das Sicherheitskabinett stellen. Oppositionsführer Jair Lapid schloss sich nicht an, ihm werde aber ein Sitz in dem neuen Kabinett freigehalten. Zuvor hatten sich die Spitzen der Regierungskoalition einstimmig für die Bildung einer Notstandsregierung mit der Opposition ausgesprochen. Ohne Ausnahme unterstütze die Koalition dieses Vorhaben und autorisiere Netanyahu, sich dafür einzusetzen, teilte ein Sprecher von Netanyahus Likud-Partei nach einem Treffen der Koalition. Netanyahu hatte am Samstag den beiden Oppositionsführern Lapid und Gantz den Eintritt in eine Notstandsregierung angeboten. Seit Tagen laufen im Hintergrund Bemühungen über eine Einigung. Lapid hatte schon Bereitschaft signalisiert. Er habe Netanyahu angeboten, eine Koalition zu bilden, "die den harten, komplexen und langen Krieg führen kann, der uns bevorsteht". Experten gehen davon aus, dass eine breite Koalition notwendig ist, um weitreichende militärische und politische Entscheidungen in den nächsten Tagen durchsetzen zu können. Viele Beobachter werten die Bemühungen um eine solche Notstandsregierung daher als Zeichen einer möglicherweise bevorstehenden israelischen Bodenoffensive in den Gazastreifen. Seit Jahresbeginn ist es in Israel zu massiven Protesten gegen einen Justizumbau gekommen, den Netanyahus teilweise rechtsextreme Regierung vorantreibt. Der bittere Streit polarisierte die Gesellschaft. Einige Beobachter glauben, Israel sei durch die internen Streitigkeiten von der Gefahr, die von der Hamas ausging, abgelenkt gewesen.'''


# streamed completion

for i in range(10):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        provider=g4f.Provider.GptGo,
    )
    print(response)
    time.sleep(2)
    print("---------------------------------------------------")