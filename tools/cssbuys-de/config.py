LANGS = ['en','de','fr','es','it','pl']
HREFLANG = dict(zip(LANGS,['en','de-DE','fr-FR','es-ES','it-IT','pl-PL']))
DATE = '2026-11-02'
UI = {
'en': ['Home','Spreadsheet','QC','Shipping','Articles','FAQ','Browse finds','Independent buyer guide','Updated 2 November 2026','On this page','Related guides','Read all 22 guides','Start here','Compare product links, check warehouse photos and plan shipping with 22 practical guides.','Quick answer','Example, not a measured shipment'],
'de': ['Start','Spreadsheet','QC','Versand','Ratgeber','FAQ','Produkte ansehen','Unabhängiger Kaufratgeber','Aktualisiert am 2. November 2026','Auf dieser Seite','Passende Ratgeber','Alle 22 Ratgeber ansehen','Hier beginnen','Produktlinks vergleichen, Lagerfotos prüfen und den Versand mit 22 praktischen Ratgebern planen.','Kurz erklärt','Beispiel, keine gemessene Sendung'],
'fr': ['Accueil','Spreadsheet','QC','Livraison','Guides','FAQ','Voir les articles','Guide indépendant','Mis à jour le 2 novembre 2026','Sur cette page','Guides associés','Voir les 22 guides','Pour commencer','Comparez les liens, vérifiez les photos en entrepôt et préparez votre envoi avec 22 guides pratiques.','Réponse rapide','Exemple, pas un colis mesuré'],
'es': ['Inicio','Spreadsheet','QC','Envíos','Guías','FAQ','Ver productos','Guía independiente','Actualizado el 2 de noviembre de 2026','En esta página','Guías relacionadas','Ver las 22 guías','Empieza aquí','Compara enlaces, revisa fotos de almacén y prepara el envío con 22 guías prácticas.','Respuesta rápida','Ejemplo, no un paquete medido'],
'it': ['Home','Spreadsheet','QC','Spedizioni','Guide','FAQ','Sfoglia i prodotti','Guida indipendente','Aggiornato il 2 novembre 2026','In questa pagina','Guide correlate','Leggi tutte le 22 guide','Inizia qui','Confronta link, verifica foto del magazzino e prepara la spedizione con 22 guide pratiche.','Risposta rapida','Esempio, non un pacco misurato'],
'pl': ['Start','Spreadsheet','QC','Wysyłka','Poradniki','FAQ','Zobacz produkty','Niezależny poradnik','Aktualizacja: 2 listopada 2026','Na tej stronie','Powiązane poradniki','Zobacz wszystkie 22 poradniki','Zacznij tutaj','Porównaj linki, sprawdź zdjęcia magazynowe i zaplanuj wysyłkę z 22 praktycznymi poradnikami.','Krótka odpowiedź','Przykład, nie zmierzona przesyłka']}
SLUGS=['cssbuy-coupons-2026','cssbuy-payment-methods-fees-refunds','cssbuy-tracking-last-mile-germany-eu','cssbuy-spreadsheet','w2c','qc-guide','cssbuy-shipping-fees-weight-route-planning']
TITLES={
'en':['CSSBuy Coupons 2026: Code Status & Shipping Discounts','CSSBuy Payment Methods: Fees, Balance & Refunds','CSSBuy Tracking: Germany Statuses & No-Update Help','CSSBuy Spreadsheet: Find Links, Check Sizes & Plan QC','CSSBuy W2C Links: Find the Right Product and Variant','CSSBuy QC Photos: Size Checks, Defects & Return Decisions','CSSBuy Shipping Costs to Germany: Weight & Fee Guide'],
'de':['CSSBuy Gutscheine 2026: Codes und Versandrabatte prüfen','CSSBuy Zahlungsmethoden: Gebühren, Guthaben und Erstattung','CSSBuy Tracking: Sendungsstatus und Hilfe für Deutschland','CSSBuy Spreadsheet: Produktlinks, Größen und QC prüfen','CSSBuy W2C Links: Produkt und Variante richtig auswählen','CSSBuy QC-Fotos prüfen: Größen, Mängel und Rücksendung','CSSBuy Versandkosten nach Deutschland: Gewicht und Gebühren'],
'fr':['Coupons CSSBuy 2026 : codes et réductions de livraison','Paiements CSSBuy : méthodes, frais, solde et remboursements','Suivi CSSBuy : statuts et absence de mises à jour en Allemagne','CSSBuy Spreadsheet : liens, tailles et contrôle QC','Liens W2C CSSBuy : trouver le produit et la bonne variante','Photos QC CSSBuy : tailles, défauts et décisions de retour','Frais de livraison CSSBuy en Allemagne : poids et calcul'],
'es':['Cupones CSSBuy 2026: códigos y descuentos de envío','Pagos CSSBuy: métodos, comisiones, saldo y reembolsos','Seguimiento CSSBuy: estados y falta de novedades en Alemania','CSSBuy Spreadsheet: enlaces, tallas y revisión QC','Enlaces W2C CSSBuy: producto y variante correctos','Fotos QC CSSBuy: tallas, defectos y devoluciones','Gastos de envío CSSBuy a Alemania: peso y cálculo'],
'it':['Coupon CSSBuy 2026: codici e sconti sulla spedizione','Pagamenti CSSBuy: metodi, commissioni, saldo e rimborsi','Tracking CSSBuy: stati e aggiornamenti per la Germania','CSSBuy Spreadsheet: link, taglie e controllo QC','Link W2C CSSBuy: scegliere prodotto e variante','Foto QC CSSBuy: taglie, difetti e decisioni di reso','Costi di spedizione CSSBuy in Germania: peso e calcolo'],
'pl':['Kupony CSSBuy 2026: kody i rabaty na wysyłkę','Płatności CSSBuy: metody, opłaty, saldo i zwroty','Śledzenie CSSBuy: statusy i brak aktualizacji w Niemczech','CSSBuy Spreadsheet: linki, rozmiary i kontrola QC','Linki W2C CSSBuy: wybór produktu i wariantu','Zdjęcia QC CSSBuy: rozmiary, wady i decyzja o zwrocie','Koszty wysyłki CSSBuy do Niemiec: waga i opłaty']}
# Buyer-facing replacements, kept in the same order in each locale.
COPY={
'en':[
'No universal CSSBuy coupon has been verified in checkout by this publication. Check the offer in your account, its expiry and eligible shipping line, then compare the final payable amount. A code copied from another page is not evidence of a working discount.',
'Use the payment methods actually offered for your transaction. Compare the amount charged with the CNY credited, including conversion and provider fees. An order refund to CSSBuy balance is separate from a withdrawal to your bank or card.',
'Start with the package number and last physical scan. An electronic announcement does not establish carrier possession. Save any local tracking number and contact the party responsible for the stage shown in the current parcel record.',
'Use the catalogue to find a product, then verify the exact seller option, size chart and current price. Save the original item ID. After warehouse arrival, compare your own order and QC photos before planning a parcel.',
'W2C means “where to cop”: a link helps locate an item, but the selected size, colour and bundle still need checking. Keep the original item ID and order record so the warehouse photos can be compared with what you actually bought.',
'Check item identity and size first, then visible defects. Mark each item accept, clarify or resolve before shipping. Photos can show a mismatch; they do not prove authenticity, fabric composition, waterproofing or long-term durability.',
'Compare eligible routes using the same packed weight, dimensions, contents and destination. Keep actual weight, volumetric weight, billing increments and optional services separate. A public route card is a reference, not your final quote.',
'Separate shoes, hoodies and jackets because they need different measurements and protection. Save only options you would actually buy, and mark unavailable sizes instead of keeping them in the shortlist.',
'Keep a row for each selected variant, not just the product family. Save the seller item ID, colour, size, listing date and the evidence still needed. If a seller changes the listing, review the row before ordering again.',
'Use a specific warehouse question: show the size label, measure chest width, or photograph the missing accessory. A clear request can resolve the uncertainty while a return may still be possible.',
'For each shortlisted item, record a decision: buy after clarification, skip, or wait. Do not send international freight for an item with an unresolved wrong size or missing part.',
'Choose packaging after accepting the item. Confirm what will be removed, what must remain and whether the final dimensions will be measured again. Protect structured shapes and delicate finishes rather than removing packaging indiscriminately.',
'Use the current CSSBuy calculator for the completed parcel. The public TYG-EU-Tariffless Express card describes Germany, a volumetric ratio of 9000 and a ten-day estimate; these fields do not confirm eligibility or a payable rate for your parcel.',
'Before shipping, verify the recipient, street and house number, postcode and country. Save the accepted item set, packed measurements and final quotation together so later tracking or billing questions have a clear reference.'
],
'de':[
'Diese Redaktion hat keinen allgemein gültigen CSSBuy-Gutscheincode im Checkout bestätigt. Prüfen Sie Angebot, Ablaufdatum und zulässige Versandlinie in Ihrem Konto und vergleichen Sie den Endbetrag. Ein kopierter Code beweist keinen funktionierenden Rabatt.',
'Nutzen Sie die im konkreten Zahlungsvorgang angebotenen Methoden. Vergleichen Sie Abbuchung und gutgeschriebenen CNY-Betrag einschließlich Umrechnung und Anbietergebühren. Eine Erstattung auf das CSSBuy-Guthaben ist von einer Auszahlung an Bank oder Karte zu unterscheiden.',
'Beginnen Sie mit Paketnummer und letztem physischen Scan. Eine elektronische Ankündigung beweist keine Übergabe an den Transporteur. Speichern Sie eine zusätzliche lokale Nummer und wenden Sie sich an die für den dokumentierten Abschnitt zuständige Stelle.',
'Suchen Sie im Katalog und prüfen Sie anschließend Verkäuferoption, Größentabelle und aktuellen Preis. Speichern Sie die ursprüngliche Artikelnummer. Vergleichen Sie nach Lagereingang Ihre Bestellung mit den QC-Fotos, bevor Sie den Versand planen.',
'W2C bedeutet „where to cop“ und hilft beim Finden eines Artikels. Größe, Farbe und Lieferumfang müssen trotzdem geprüft werden. Bewahren Sie Artikelnummer und Bestellung auf, damit Lagerfotos mit der tatsächlich gekauften Variante verglichen werden können.',
'Prüfen Sie zuerst Artikel und Größe, dann sichtbare Mängel. Vergeben Sie den Status freigeben, klären oder vor Versand lösen. Fotos können Abweichungen zeigen, bestätigen aber weder Echtheit noch Faserzusammensetzung, Wasserdichtigkeit oder Haltbarkeit.',
'Vergleichen Sie zulässige Linien mit identischen Paketmaßen, Gewicht, Inhalt und Zielland. Trennen Sie tatsächliches Gewicht, Volumengewicht, Abrechnungsschritte und Zusatzleistungen. Eine öffentliche Linienkarte ist keine endgültige Paketofferte.',
'Trennen Sie Schuhe, Hoodies und Jacken, da Maße und Schutzbedarf unterschiedlich sind. Behalten Sie nur tatsächlich interessante Varianten in der Auswahl und kennzeichnen Sie nicht verfügbare Größen.',
'Erfassen Sie jede gewählte Variante einzeln: Artikelnummer, Farbe, Größe, Prüfdatum und noch fehlende Nachweise. Ändert der Verkäufer das Angebot, muss der Eintrag vor einer erneuten Bestellung überprüft werden.',
'Stellen Sie eine konkrete Frage an das Lager: Größenetikett zeigen, Brustweite messen oder fehlendes Zubehör fotografieren. So lässt sich die Unsicherheit klären, solange eine Rücksendung möglicherweise noch möglich ist.',
'Notieren Sie zu jedem Artikel eine Entscheidung: nach Klärung kaufen, auslassen oder warten. Versenden Sie keine ungeklärte falsche Größe und keinen Artikel mit fehlenden wichtigen Teilen international.',
'Entscheiden Sie erst nach Freigabe des Artikels über die Verpackung. Klären Sie, was entfernt wird, was bleiben muss und ob die Außenmaße erneut gemessen werden. Formstabile Teile und empfindliche Oberflächen benötigen passenden Schutz.',
'Verwenden Sie den aktuellen CSSBuy-Rechner für das fertige Paket. Die öffentliche TYG-EU-Tariffless-Express-Karte nennt Deutschland, den Volumenfaktor 9000 und eine Zehn-Tage-Schätzung. Das bestätigt weder die Zulässigkeit noch den zahlbaren Tarif Ihrer Sendung.',
'Prüfen Sie vor Versand Empfänger, Straße, Hausnummer, Postleitzahl und Land. Speichern Sie freigegebene Artikel, Paketmaße und endgültiges Angebot gemeinsam als Grundlage für spätere Fragen zu Tracking oder Abrechnung.'
],
'fr':[
'Aucun code CSSBuy universel n’a été confirmé au paiement par notre rédaction. Vérifiez l’offre de votre compte, son expiration et la ligne admissible, puis comparez le total. Un code copié ailleurs ne prouve pas une réduction active.',
'Utilisez les méthodes proposées pour votre transaction. Comparez montant débité et CNY crédités, conversion et frais compris. Un remboursement sur le solde CSSBuy est distinct d’un retrait vers la banque ou la carte.',
'Commencez par le numéro de colis et le dernier scan physique. Une annonce électronique ne prouve pas la possession par le transporteur. Conservez le numéro local éventuel et contactez l’intervenant responsable de l’étape documentée.',
'Cherchez dans le catalogue, puis vérifiez variante, tableau des tailles et prix actuel. Gardez l’identifiant d’origine. Après réception en entrepôt, comparez votre commande aux photos QC avant de préparer l’envoi.',
'W2C signifie « where to cop » et permet de trouver un article. Taille, couleur et contenu du lot restent à contrôler. Gardez identifiant et commande pour comparer les photos à la variante réellement achetée.',
'Vérifiez identité et taille, puis défauts visibles. Décidez : accepter, clarifier ou résoudre avant envoi. Les photos ne prouvent ni authenticité, ni composition, ni imperméabilité ou durabilité.',
'Comparez les lignes admissibles avec les mêmes poids, dimensions, articles et destination. Séparez poids réel, volumétrique, paliers et options. La fiche publique d’une ligne n’est pas votre devis final.',
'Séparez chaussures, hoodies et vestes : mesures et protections diffèrent. Ne conservez que des variantes réellement envisagées et signalez les tailles indisponibles.',
'Créez une ligne par variante choisie avec identifiant, couleur, taille, date et preuves manquantes. Une annonce modifiée doit être vérifiée avant une nouvelle commande.',
'Posez une question précise à l’entrepôt : montrer l’étiquette, mesurer la poitrine ou photographier l’accessoire manquant. Cela aide à décider tant qu’un retour reste éventuellement possible.',
'Attribuez une décision à chaque choix : acheter après clarification, écarter ou attendre. N’expédiez pas un article dont la mauvaise taille ou la pièce manquante reste sans solution.',
'Choisissez l’emballage après acceptation. Confirmez ce qui sera retiré, conservé et remesuré. Protégez formes structurées et finitions délicates plutôt que de supprimer toute protection.',
'Utilisez le calculateur CSSBuy actuel pour le colis terminé. La fiche publique TYG-EU-Tariffless Express mentionne Allemagne, facteur 9000 et dix jours estimés. Ces informations ne confirment ni admissibilité ni montant de votre colis.',
'Avant l’envoi, contrôlez destinataire, rue, numéro, code postal et pays. Gardez articles acceptés, mesures et devis final ensemble pour comprendre ensuite le suivi ou la facturation.'
],
'es':[
'Nuestra publicación no ha confirmado un código CSSBuy universal en el pago. Revisa oferta de tu cuenta, caducidad y línea admitida, y compara el total. Un código copiado no demuestra un descuento activo.',
'Usa los métodos disponibles en tu transacción. Compara cargo real y CNY abonados, incluyendo conversión y comisiones. Un reembolso al saldo CSSBuy es distinto de una retirada al banco o tarjeta.',
'Empieza por el número de paquete y el último escaneo físico. El aviso electrónico no prueba posesión del transportista. Guarda el número local y contacta con quien gestione la etapa documentada.',
'Busca en el catálogo y verifica variante, tabla de tallas y precio actual. Conserva el identificador original. Al llegar al almacén, compara pedido y QC antes de planificar el envío.',
'W2C significa «where to cop» y ayuda a localizar un artículo. Aún debes comprobar talla, color y contenido. Guarda identificador y pedido para comparar fotos con la variante comprada.',
'Comprueba identidad y talla, después defectos visibles. Decide aceptar, aclarar o resolver antes de enviar. Las fotos no prueban autenticidad, composición, impermeabilidad ni durabilidad.',
'Compara líneas admitidas con idénticos peso, dimensiones, artículos y destino. Separa peso real, volumétrico, tramos y extras. Una ficha pública no es el presupuesto final de tu paquete.',
'Separa zapatos, sudaderas y chaquetas porque medidas y protección son distintas. Conserva opciones que realmente comprarías y marca las tallas agotadas.',
'Crea una fila por variante con identificador, color, talla, fecha y pruebas pendientes. Revisa cualquier anuncio cambiado antes de volver a comprar.',
'Pregunta algo concreto al almacén: mostrar etiqueta, medir pecho o fotografiar el accesorio que falta. Así puedes decidir mientras una devolución todavía sea posible.',
'Marca cada opción: comprar tras aclarar, descartar o esperar. No envíes internacionalmente una talla equivocada o un artículo incompleto sin resolver.',
'Elige embalaje después de aceptar el artículo. Confirma qué se retira, qué permanece y qué se volverá a medir. Protege formas estructuradas y acabados delicados.',
'Usa la calculadora CSSBuy actual para el paquete terminado. La ficha pública TYG-EU-Tariffless Express menciona Alemania, factor 9000 y diez días estimados. No confirma admisión ni precio de tu envío.',
'Antes del envío revisa destinatario, calle, número, código postal y país. Conserva artículos aceptados, medidas y presupuesto final juntos para futuras consultas de seguimiento o cobro.'
],
'it':[
'La redazione non ha verificato un codice CSSBuy universale al pagamento. Controlla offerta del conto, scadenza e linea ammessa, poi confronta il totale. Un codice copiato non dimostra uno sconto attivo.',
'Usa i metodi offerti nella tua transazione. Confronta addebito e CNY accreditati, includendo cambio e commissioni. Un rimborso sul saldo CSSBuy è distinto da un prelievo verso banca o carta.',
'Parti dal numero del pacco e dall’ultima scansione fisica. Un annuncio elettronico non prova il possesso del corriere. Conserva il numero locale e contatta chi gestisce la fase documentata.',
'Cerca nel catalogo e controlla variante, tabella taglie e prezzo corrente. Conserva l’identificativo originale. Dopo l’arrivo confronta ordine e foto QC prima di preparare la spedizione.',
'W2C significa «where to cop» e aiuta a trovare un articolo. Taglia, colore e contenuto devono comunque essere verificati. Conserva identificativo e ordine per confrontare le foto con la variante acquistata.',
'Controlla identità e taglia, poi difetti visibili. Decidi se accettare, chiarire o risolvere prima dell’invio. Le foto non provano autenticità, composizione, impermeabilità o durata.',
'Confronta linee ammesse con stessi pesi, misure, articoli e destinazione. Separa peso reale, volumetrico, scaglioni ed extra. Una scheda pubblica non è il preventivo finale del tuo pacco.',
'Separa scarpe, felpe e giacche perché misure e protezioni differiscono. Mantieni opzioni che compreresti davvero e segnala le taglie esaurite.',
'Crea una riga per variante con identificativo, colore, taglia, data e prove mancanti. Controlla un’inserzione modificata prima di riordinare.',
'Fai una domanda precisa al magazzino: mostrare etichetta, misurare torace o fotografare l’accessorio mancante. Aiuta a decidere finché un reso può essere ancora possibile.',
'Segna ogni opzione: acquistare dopo chiarimento, scartare o attendere. Non spedire una taglia sbagliata o un articolo incompleto senza aver risolto il problema.',
'Scegli l’imballaggio dopo aver accettato l’articolo. Conferma cosa eliminare, conservare e rimisurare. Proteggi forme strutturate e finiture delicate.',
'Usa il calcolatore CSSBuy corrente per il pacco finito. La scheda TYG-EU-Tariffless Express indica Germania, fattore 9000 e dieci giorni stimati. Non conferma ammissibilità o tariffa del tuo invio.',
'Prima dell’invio controlla destinatario, via, civico, CAP e Paese. Conserva insieme articoli accettati, misure e preventivo finale per domande su tracking o addebiti.'
],
'pl':[
'Redakcja nie potwierdziła uniwersalnego kodu CSSBuy podczas płatności. Sprawdź ofertę konta, termin i dopuszczalną linię, a potem kwotę końcową. Skopiowany kod nie dowodzi aktywnego rabatu.',
'Używaj metod dostępnych w konkretnej transakcji. Porównaj obciążenie i uznane CNY z kursem oraz prowizjami. Zwrot na saldo CSSBuy jest czymś innym niż wypłata na bank lub kartę.',
'Zacznij od numeru paczki i ostatniego fizycznego skanu. Elektroniczna zapowiedź nie dowodzi posiadania paczki przez przewoźnika. Zachowaj numer lokalny i kontaktuj się z podmiotem odpowiedzialnym za zapisany etap.',
'Znajdź ofertę w katalogu, następnie sprawdź wariant, tabelę rozmiarów i cenę. Zachowaj pierwotny identyfikator. Po przyjęciu do magazynu porównaj zamówienie ze zdjęciami QC przed planowaniem wysyłki.',
'W2C oznacza „where to cop” i pomaga znaleźć produkt. Nadal trzeba sprawdzić rozmiar, kolor i zestaw. Zachowaj identyfikator oraz zamówienie do porównania zdjęć z kupionym wariantem.',
'Sprawdź produkt i rozmiar, potem widoczne wady. Wybierz akceptację, wyjaśnienie lub rozwiązanie przed wysyłką. Zdjęcia nie potwierdzają autentyczności, składu, wodoodporności ani trwałości.',
'Porównuj dopuszczalne linie przy tych samych wagach, wymiarach, towarach i kraju. Oddziel masę rzeczywistą, gabarytową, progi i dodatki. Publiczna karta nie jest końcową wyceną Twojej paczki.',
'Rozdziel buty, bluzy i kurtki, ponieważ pomiary i ochrona są różne. Zachowuj realnie rozważane opcje i oznacz niedostępne rozmiary.',
'Twórz osobny wiersz dla wariantu: identyfikator, kolor, rozmiar, data i brakujące dowody. Zmienioną ofertę sprawdź ponownie przed kolejnym zakupem.',
'Zadaj magazynowi konkretne pytanie: pokaż metkę, zmierz szerokość lub sfotografuj brakujący dodatek. Ułatwia to decyzję, gdy zwrot może być jeszcze możliwy.',
'Oznacz każdą opcję: kup po wyjaśnieniu, pomiń lub poczekaj. Nie wysyłaj za granicę nierozwiązanego błędnego rozmiaru ani niekompletnego produktu.',
'Wybierz opakowanie po akceptacji produktu. Potwierdź, co usunąć, zachować i ponownie zmierzyć. Chroń usztywnione kształty oraz delikatne wykończenia.',
'Użyj aktualnego kalkulatora CSSBuy dla gotowej paczki. Publiczna karta TYG-EU-Tariffless Express podaje Niemcy, dzielnik 9000 i szacunek dziesięciu dni. Nie potwierdza dopuszczalności ani ceny Twojego nadania.',
'Przed nadaniem sprawdź odbiorcę, ulicę, numer, kod i kraj. Przechowuj razem zaakceptowane artykuły, pomiary i wycenę jako odniesienie do późniejszego trackingu lub naliczenia.'
]}
