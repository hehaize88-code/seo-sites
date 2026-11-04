import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
catalog = {}
faq = {}

def add_catalog(locale, rows):
    for line in rows.strip().splitlines():
        slug, title, description = line.split('|||')
        catalog.setdefault(slug, {})[locale] = {'title': title, 'description': description}

def add_faq(locale, rows):
    faq[locale] = []
    for line in rows.strip().splitlines():
        q, a = line.split('|||')
        faq[locale].append({'q': q, 'a': a})

add_catalog('en', '''
best-agent-2026|||CSSBuy vs Other Shopping Agents: Costs, QC and Shipping|||Compare CSSBuy with other agents using the same parcel, destination and services. Check total costs, QC options, shipping rules and support.
cssbuy-consolidate-or-split-parcel-cost-model|||CSSBuy Parcels: Combine or Split Your Order?|||Compare combined and separate CSSBuy parcels using packed dimensions, shipping fees, item restrictions and protection needs before you decide.
cssbuy-domestic-shipping-seller-to-warehouse|||CSSBuy Domestic Shipping: Seller-to-Warehouse Costs|||Understand CSSBuy domestic shipping charges, compare seller offers and check delivery to the warehouse separately from international freight.
cssbuy-insurance-guide-parcel-claims|||CSSBuy Parcel Insurance: Coverage, Exclusions and Claims|||Check CSSBuy parcel insurance terms, insured value, exclusions and claim evidence. Review the current policy for your selected shipping line.
cssbuy-mixed-parcel-qc-volume-weight-audit-2026-07-12|||CSSBuy Mixed Parcels: QC, Weight and Shipping Checks|||Plan a CSSBuy parcel containing different item types. Review QC, packaging, volumetric weight and shipping restrictions with a practical worksheet.
cssbuy-pro-calculator-route-fees-guide|||CSSBuy Shipping Calculator Guide: Weight, Size and Fees|||Learn how to use the CSSBuy shipping calculator, compare actual and volumetric weight, and reconcile estimates with the final parcel charge.
cssbuy-pro-coupon-exchange-rate-reward-guide|||CSSBuy Coupons, Points and Exchange Rates Explained|||Check CSSBuy coupon conditions, reward points and currency conversion separately. Compare the final payment amount before using a promotion.
cssbuy-pro-fee-qc-shipping-route-index|||How CSSBuy Works: Buying, QC and Shipping Costs|||Follow the CSSBuy buying process from product selection to warehouse QC and international shipping. Separate item costs from parcel charges.
cssbuy-pro-parcel-risk-qc-2026-07-09|||CSSBuy Parcel Checklist: QC, Packing and Shipping Limits|||Review a CSSBuy parcel before dispatch: check unresolved QC issues, fragile goods, weight, packaging, storage timing and shipping-line restrictions.
cssbuy-pro-qc-lab-photo-video-extra-fee|||CSSBuy Extra QC Photos: Requests, Fees and Timing|||Request useful CSSBuy QC photos and measurements, check any extra charges, and resolve missing evidence before packing or international shipping.
cssbuy-pro-w2c-qc-shipping-workflow-2026|||CSSBuy Order Checklist: Product Links, QC and Dispatch|||Keep a clear CSSBuy order record from the original product link to QC approval and dispatch. Track missing details and the next action at each stage.
cssbuy-restricted-items-shipping|||CSSBuy Shipping Restrictions: Batteries and Liquids|||Check CSSBuy shipping restrictions for batteries, electronics, liquids and mixed parcels. Confirm current eligibility for your destination and line.
cssbuy-service-payment-fees-prepayment-audit|||CSSBuy Service and Payment Fees: What to Check|||Separate CSSBuy service fees, payment charges and currency conversion. Compare the amount paid with the balance credited and reconcile receipts.
cssbuy-shipping-line-comparison-framework|||CSSBuy Shipping Lines: Compare Cost, Weight and Delivery|||Compare CSSBuy shipping lines using one parcel's measurements and contents. Check eligible routes, full quotes, delivery estimates and tracking.
cssbuy-shoe-box-removal|||CSSBuy Shoe Box Removal: Shipping Cost and Protection|||Compare keeping or removing shoe boxes in a CSSBuy parcel. Check packed dimensions, protection, optional service fees and the final shipping quote.
cssbuy-spreadsheet|||CSSBuy Spreadsheet Guide: Product Links, QC and Costs|||Organize CSSBuy product links, sizes, prices and warehouse QC in a useful spreadsheet. Keep item research separate from parcel shipping budgets.
cssbuy-total-landed-cost-worksheet|||CSSBuy Total Cost Worksheet: From Item Price to Delivery|||Build a CSSBuy budget covering products, China delivery, payment charges, packing and international shipping. Separate estimates from paid costs.
cssbuy-tracking-not-updating-parcel-status-guide|||CSSBuy Tracking Not Updating? Status Checks and Next Steps|||Check why CSSBuy tracking has stopped updating. Identify the shipping stage, save scan details and send a useful enquiry through your parcel record.
cssbuy-vacuum-packing-clothes|||CSSBuy Vacuum Packing: Clothing Volume, Cost and Care|||Compare folding, compression and vacuum packing for CSSBuy clothing parcels. Check garment suitability, chargeable weight and extra packing fees.
cssbuy-volumetric-weight|||CSSBuy Volumetric Weight: Formula and Parcel Examples|||Calculate CSSBuy volumetric weight with the divisor specified by your shipping line. Compare actual weight, packed dimensions and billing increments.
qc-guide|||CSSBuy QC Photos: Check Sizes, Defects and Return Options|||Use a CSSBuy QC checklist to check sizes, selected variations and visible defects. Request missing views and review return options before shipping.
w2c|||CSSBuy Product Links: Find, Verify and Plan Your Order|||Find and verify CSSBuy product links, check the selected size and seller, then record the information needed for warehouse QC and parcel planning.
''')

add_catalog('de', '''
best-agent-2026|||CSSBuy im Agentenvergleich: Kosten, QC und Versand|||Vergleiche CSSBuy mit anderen Einkaufsagenten anhand desselben Pakets und Ziellands. Prüfe Gesamtkosten, QC-Angebote, Versandbedingungen und Support.
cssbuy-consolidate-or-split-parcel-cost-model|||CSSBuy-Pakete zusammenlegen oder getrennt versenden?|||Vergleiche gemeinsame und getrennte CSSBuy-Sendungen anhand von Paketmaßen, Versandkosten, Warenbeschränkungen und benötigtem Schutz.
cssbuy-domestic-shipping-seller-to-warehouse|||CSSBuy-Inlandsversand: Kosten vom Händler zum Lager|||Verstehe die Kosten des chinesischen Inlandsversands bei CSSBuy. Vergleiche Händlerangebote und trenne die Lagerzustellung vom internationalen Versand.
cssbuy-insurance-guide-parcel-claims|||CSSBuy-Paketversicherung: Leistungen und Schadensmeldung|||Prüfe Versicherungssumme, Ausschlüsse und erforderliche Nachweise für CSSBuy-Pakete. Maßgeblich sind die aktuellen Bedingungen deiner Versandlinie.
cssbuy-mixed-parcel-qc-volume-weight-audit-2026-07-12|||CSSBuy-Mischpakete: QC, Gewicht und Versand prüfen|||Plane CSSBuy-Pakete mit verschiedenen Waren. Prüfe QC-Fotos, Verpackung, Volumengewicht und Versandbeschränkungen mit einer praktischen Übersicht.
cssbuy-pro-calculator-route-fees-guide|||CSSBuy-Versandkostenrechner: Anleitung zu Gewicht und Gebühren|||Nutze den CSSBuy-Versandkostenrechner mit passenden Paketmaßen. Vergleiche tatsächliches Gewicht und Volumengewicht sowie Schätzung und Endkosten.
cssbuy-pro-coupon-exchange-rate-reward-guide|||CSSBuy-Gutscheine, Punkte und Wechselkurse erklärt|||Prüfe CSSBuy-Gutscheinbedingungen, Prämienpunkte und Währungsumrechnung getrennt. Vergleiche vor einer Aktion den endgültigen Zahlungsbetrag.
cssbuy-pro-fee-qc-shipping-route-index|||So funktioniert CSSBuy: Einkauf, QC und Versandkosten|||Verfolge den CSSBuy-Ablauf von der Produktauswahl über die Qualitätskontrolle bis zum Versand. Unterscheide Artikelkosten und Paketgebühren.
cssbuy-pro-parcel-risk-qc-2026-07-09|||CSSBuy-Paketcheck: QC, Verpackung und Versandgrenzen|||Prüfe vor dem CSSBuy-Versand offene QC-Fragen, empfindliche Waren, Gewicht, Verpackung, Lagerfristen und die Bedingungen der Versandlinie.
cssbuy-pro-qc-lab-photo-video-extra-fee|||Zusätzliche CSSBuy-QC-Fotos: Anfrage, Kosten und Zeitpunkt|||Fordere gezielte CSSBuy-QC-Fotos und Maße an. Kläre Zusatzkosten und fehlende Informationen, bevor du Verpackung und internationalen Versand freigibst.
cssbuy-pro-w2c-qc-shipping-workflow-2026|||CSSBuy-Bestellcheckliste: Produktlinks, QC und Versand|||Dokumentiere deine CSSBuy-Bestellung vom ursprünglichen Produktlink bis zur QC-Freigabe und zum Versand. Halte offene Fragen und nächste Schritte fest.
cssbuy-restricted-items-shipping|||CSSBuy-Versandbeschränkungen: Batterien und Flüssigkeiten|||Prüfe CSSBuy-Versandregeln für Batterien, Elektronik, Flüssigkeiten und Mischpakete. Bestätige die Zulässigkeit für dein Zielland und die Versandlinie.
cssbuy-service-payment-fees-prepayment-audit|||CSSBuy-Service- und Zahlungsgebühren richtig prüfen|||Trenne CSSBuy-Servicegebühren, Zahlungskosten und Währungsumrechnung. Vergleiche Zahlung und gutgeschriebenes Guthaben anhand deiner Belege.
cssbuy-shipping-line-comparison-framework|||CSSBuy-Versandlinien: Kosten, Gewicht und Laufzeit vergleichen|||Vergleiche CSSBuy-Versandlinien für dasselbe Paket. Prüfe Warenzulässigkeit, vollständige Angebote, voraussichtliche Laufzeiten und Sendungsverfolgung.
cssbuy-shoe-box-removal|||CSSBuy ohne Schuhkarton: Versandkosten und Schutz|||Vergleiche CSSBuy-Versand mit und ohne Schuhkartons. Prüfe Paketmaße, Schutz, optionale Verpackungsgebühren und das endgültige Versandangebot.
cssbuy-spreadsheet|||CSSBuy-Spreadsheet: Produktlinks, QC und Kosten planen|||Ordne CSSBuy-Produktlinks, Größen, Preise und QC-Ergebnisse in einer übersichtlichen Tabelle. Trenne Artikelsuche und Versandbudget für das Paket.
cssbuy-total-landed-cost-worksheet|||CSSBuy-Gesamtkosten: Budget vom Artikel bis zur Zustellung|||Plane Produktkosten, Inlandsversand, Zahlung, Verpackung und internationalen Versand bei CSSBuy. Halte Schätzungen und bezahlte Beträge getrennt.
cssbuy-tracking-not-updating-parcel-status-guide|||CSSBuy-Tracking ohne Update: Status und nächste Schritte|||Prüfe ausbleibende CSSBuy-Tracking-Updates nach Versandphase. Sichere die letzten Meldungen und stelle eine konkrete Anfrage im Paketdatensatz.
cssbuy-vacuum-packing-clothes|||CSSBuy-Vakuumverpackung: Volumen, Kosten und Kleidungsschutz|||Vergleiche Falten, Kompression und Vakuumverpackung für CSSBuy-Kleidung. Prüfe Materialeignung, Abrechnungsgewicht und zusätzliche Verpackungskosten.
cssbuy-volumetric-weight|||CSSBuy-Volumengewicht: Formel und Paketbeispiele|||Berechne das CSSBuy-Volumengewicht mit dem Divisor deiner Versandlinie. Vergleiche tatsächliches Gewicht, Paketmaße und Abrechnungsschritte.
qc-guide|||CSSBuy-QC-Fotos: Größen, Mängel und Rückgabe prüfen|||Prüfe mit der CSSBuy-QC-Checkliste Größen, bestellte Varianten und sichtbare Mängel. Fordere fehlende Ansichten an und kläre Rückgaben vor dem Versand.
w2c|||CSSBuy-Produktlinks finden, prüfen und Bestellung planen|||Finde und prüfe CSSBuy-Produktlinks, Händler und ausgewählte Größen. Halte die Angaben fest, die du später für QC und Versandplanung benötigst.
''')

add_catalog('fr', '''
best-agent-2026|||CSSBuy face aux autres agents : frais, QC et livraison|||Comparez CSSBuy à d'autres agents pour un même colis et une même destination. Vérifiez le coût total, les contrôles QC, la livraison et l'assistance.
cssbuy-consolidate-or-split-parcel-cost-model|||Colis CSSBuy : regrouper ou séparer ses achats ?|||Comparez les envois CSSBuy groupés et séparés selon les dimensions emballées, les frais, les restrictions et la protection nécessaire.
cssbuy-domestic-shipping-seller-to-warehouse|||Livraison intérieure CSSBuy : du vendeur à l'entrepôt|||Comprenez les frais de livraison intérieure en Chine avec CSSBuy. Comparez les vendeurs et distinguez cette étape du transport international.
cssbuy-insurance-guide-parcel-claims|||Assurance CSSBuy : garanties, exclusions et réclamations|||Vérifiez le montant assuré, les exclusions et les justificatifs pour un colis CSSBuy. Consultez les conditions actuelles de la ligne choisie.
cssbuy-mixed-parcel-qc-volume-weight-audit-2026-07-12|||Colis mixtes CSSBuy : QC, poids et vérifications avant envoi|||Préparez un colis CSSBuy contenant plusieurs types d'articles. Vérifiez photos QC, emballage, poids volumétrique et restrictions de transport.
cssbuy-pro-calculator-route-fees-guide|||Calculateur CSSBuy : guide des poids, dimensions et frais|||Utilisez le calculateur de livraison CSSBuy avec les bonnes mesures. Comparez poids réel et volumétrique, puis estimation et facture finale.
cssbuy-pro-coupon-exchange-rate-reward-guide|||CSSBuy : comprendre les coupons, points et taux de change|||Vérifiez séparément les conditions des coupons CSSBuy, les points et la conversion monétaire. Comparez le montant final avant d'utiliser une offre.
cssbuy-pro-fee-qc-shipping-route-index|||Comment fonctionne CSSBuy : achat, QC et frais de livraison|||Suivez un achat CSSBuy de la sélection du produit au contrôle en entrepôt et à l'expédition. Distinguez le prix des articles des frais du colis.
cssbuy-pro-parcel-risk-qc-2026-07-09|||Vérifier son colis CSSBuy : QC, emballage et restrictions|||Avant l'envoi CSSBuy, vérifiez les questions QC, les articles fragiles, le poids, l'emballage, les délais de stockage et les restrictions de transport.
cssbuy-pro-qc-lab-photo-video-extra-fee|||Photos QC supplémentaires CSSBuy : demandes, frais et délais|||Demandez des photos QC CSSBuy et des mesures précises. Vérifiez les frais éventuels et les détails manquants avant l'emballage et l'expédition.
cssbuy-pro-w2c-qc-shipping-workflow-2026|||Suivi d'achat CSSBuy : liens produits, QC et expédition|||Gardez un dossier CSSBuy clair du lien produit à la validation QC et à l'envoi. Notez les informations manquantes et la prochaine étape à chaque stade.
cssbuy-restricted-items-shipping|||Restrictions CSSBuy : batteries, liquides et électronique|||Vérifiez les règles CSSBuy pour les batteries, liquides, appareils et colis mixtes. Confirmez leur admissibilité pour la destination et la ligne choisies.
cssbuy-service-payment-fees-prepayment-audit|||Frais de service et de paiement CSSBuy : les points à vérifier|||Distinguez frais de service CSSBuy, frais de paiement et conversion. Comparez le montant débité au solde crédité et conservez les justificatifs.
cssbuy-shipping-line-comparison-framework|||Lignes CSSBuy : comparer les frais, le poids et les délais|||Comparez les lignes CSSBuy avec les mêmes mesures et le même contenu. Vérifiez les restrictions, le devis complet, le suivi et les délais estimés.
cssbuy-shoe-box-removal|||Retirer les boîtes à chaussures CSSBuy : coût et protection|||Comparez l'envoi CSSBuy avec ou sans boîtes à chaussures. Vérifiez les dimensions du colis, la protection, les frais d'emballage et le devis final.
cssbuy-spreadsheet|||Tableur CSSBuy : liens produits, photos QC et budget|||Organisez vos liens CSSBuy, tailles, prix et contrôles QC dans un tableur utile. Séparez les recherches sur les articles du budget d'expédition.
cssbuy-total-landed-cost-worksheet|||Budget CSSBuy : calculer le coût total jusqu'à la livraison|||Préparez un budget CSSBuy incluant articles, livraison en Chine, paiement, emballage et transport international. Séparez estimations et frais réglés.
cssbuy-tracking-not-updating-parcel-status-guide|||Suivi CSSBuy bloqué : vérifier le statut et agir|||Comprenez l'absence de mise à jour du suivi CSSBuy. Identifiez l'étape, conservez les derniers scans et contactez l'assistance depuis le colis concerné.
cssbuy-vacuum-packing-clothes|||Vêtements CSSBuy sous vide : volume, coût et précautions|||Comparez pliage, compression et emballage sous vide pour un colis CSSBuy. Vérifiez les textiles, le poids facturable et les frais de préparation.
cssbuy-volumetric-weight|||Poids volumétrique CSSBuy : formule et exemples de colis|||Calculez le poids volumétrique CSSBuy avec le diviseur de votre ligne. Comparez poids réel, dimensions emballées et paliers de facturation.
qc-guide|||Photos QC CSSBuy : tailles, défauts et possibilités de retour|||Vérifiez tailles, variantes commandées et défauts visibles avec une liste QC CSSBuy. Demandez les vues manquantes et examinez les retours avant l'envoi.
w2c|||Liens produits CSSBuy : trouver, vérifier et préparer l'achat|||Trouvez et vérifiez les liens produits CSSBuy, le vendeur et la taille choisie. Notez les informations utiles au contrôle QC et à la préparation du colis.
''')

add_catalog('es', '''
best-agent-2026|||CSSBuy frente a otros agentes: costes, QC y envíos|||Compara CSSBuy con otros agentes usando el mismo paquete y destino. Revisa el coste total, las opciones QC, las condiciones de envío y la asistencia.
cssbuy-consolidate-or-split-parcel-cost-model|||Paquetes CSSBuy: ¿agrupar o dividir tus compras?|||Compara envíos CSSBuy conjuntos y separados según las dimensiones, los gastos, las restricciones de los artículos y la protección necesaria.
cssbuy-domestic-shipping-seller-to-warehouse|||Envío nacional CSSBuy: costes del vendedor al almacén|||Entiende los gastos de envío dentro de China con CSSBuy. Compara ofertas y distingue la entrega al almacén del transporte internacional.
cssbuy-insurance-guide-parcel-claims|||Seguro CSSBuy: cobertura, exclusiones y reclamaciones|||Revisa el valor asegurado, las exclusiones y las pruebas para reclamar por un paquete CSSBuy. Consulta las condiciones vigentes de la línea elegida.
cssbuy-mixed-parcel-qc-volume-weight-audit-2026-07-12|||Paquetes mixtos CSSBuy: QC, peso y comprobaciones de envío|||Prepara un paquete CSSBuy con distintos tipos de artículos. Revisa las fotos QC, el embalaje, el peso volumétrico y las restricciones de transporte.
cssbuy-pro-calculator-route-fees-guide|||Calculadora de envíos CSSBuy: guía de peso, medidas y costes|||Aprende a usar la calculadora de envíos CSSBuy. Compara peso real y volumétrico y comprueba la estimación frente al importe final del paquete.
cssbuy-pro-coupon-exchange-rate-reward-guide|||CSSBuy: cupones, puntos y tipos de cambio explicados|||Comprueba por separado las condiciones de los cupones CSSBuy, los puntos y la conversión de moneda. Compara el pago final antes de aplicar una oferta.
cssbuy-pro-fee-qc-shipping-route-index|||Cómo funciona CSSBuy: compras, QC y gastos de envío|||Sigue el proceso CSSBuy desde la elección del producto hasta las fotos QC y el envío internacional. Distingue los costes del artículo y del paquete.
cssbuy-pro-parcel-risk-qc-2026-07-09|||Lista de revisión CSSBuy: QC, embalaje y límites de envío|||Antes de enviar con CSSBuy, revisa dudas QC, artículos frágiles, peso, embalaje, plazos de almacenamiento y restricciones de la línea.
cssbuy-pro-qc-lab-photo-video-extra-fee|||Fotos QC adicionales en CSSBuy: solicitudes, costes y plazos|||Solicita fotos QC y medidas útiles en CSSBuy. Confirma los cargos adicionales y resuelve las dudas antes del embalaje y del envío internacional.
cssbuy-pro-w2c-qc-shipping-workflow-2026|||Lista de pedido CSSBuy: enlaces, QC y preparación del envío|||Organiza tu pedido CSSBuy desde el enlace original hasta la aprobación QC y el envío. Registra los datos pendientes y la siguiente acción de cada etapa.
cssbuy-restricted-items-shipping|||Restricciones CSSBuy: baterías, líquidos y electrónica|||Revisa las restricciones CSSBuy para baterías, líquidos, electrónica y paquetes mixtos. Confirma la admisión según el destino y la línea elegida.
cssbuy-service-payment-fees-prepayment-audit|||Comisiones CSSBuy: servicio, pago y cambio de moneda|||Distingue las comisiones de servicio CSSBuy, los cargos de pago y la conversión. Compara el importe pagado con el saldo recibido y revisa los comprobantes.
cssbuy-shipping-line-comparison-framework|||Líneas CSSBuy: comparar costes, peso y plazos de entrega|||Compara las líneas CSSBuy con el mismo paquete. Revisa restricciones, presupuesto completo, plazo estimado y seguimiento antes de elegir.
cssbuy-shoe-box-removal|||Quitar cajas de zapatos en CSSBuy: costes y protección|||Compara el envío CSSBuy con y sin cajas de zapatos. Comprueba las dimensiones, la protección, los cargos de embalaje y el presupuesto final.
cssbuy-spreadsheet|||Hoja de cálculo CSSBuy: enlaces, QC y presupuesto|||Organiza enlaces CSSBuy, tallas, precios y fotos QC en una hoja útil. Separa la búsqueda de productos del presupuesto de envío del paquete.
cssbuy-total-landed-cost-worksheet|||Presupuesto CSSBuy: coste total del producto a la entrega|||Calcula un presupuesto CSSBuy con productos, envío en China, pagos, embalaje y transporte internacional. Distingue estimaciones e importes pagados.
cssbuy-tracking-not-updating-parcel-status-guide|||Seguimiento CSSBuy sin actualizar: qué revisar y qué hacer|||Comprueba por qué no avanza el seguimiento CSSBuy. Identifica la etapa, guarda los últimos registros y consulta desde el paquete correspondiente.
cssbuy-vacuum-packing-clothes|||Ropa CSSBuy al vacío: volumen, coste y cuidados|||Compara doblado, compresión y envasado al vacío para ropa CSSBuy. Revisa la compatibilidad de las prendas, el peso facturable y los gastos de embalaje.
cssbuy-volumetric-weight|||Peso volumétrico CSSBuy: fórmula y ejemplos de paquetes|||Calcula el peso volumétrico CSSBuy con el divisor de tu línea de envío. Compara peso real, dimensiones del paquete e incrementos de facturación.
qc-guide|||Fotos QC CSSBuy: revisar tallas, defectos y devoluciones|||Usa una lista QC CSSBuy para revisar tallas, variantes y defectos visibles. Pide las fotos que falten y comprueba las opciones de devolución antes del envío.
w2c|||Enlaces CSSBuy: encontrar, verificar y preparar tu pedido|||Busca y verifica enlaces de productos CSSBuy, el vendedor y la talla elegida. Guarda los datos necesarios para las fotos QC y la planificación del envío.
''')

add_catalog('it', '''
best-agent-2026|||CSSBuy e altri agenti: confronto tra costi, QC e spedizioni|||Confronta CSSBuy con altri agenti usando lo stesso pacco e la stessa destinazione. Valuta costo totale, servizi QC, condizioni di spedizione e assistenza.
cssbuy-consolidate-or-split-parcel-cost-model|||Pacchi CSSBuy: riunire gli acquisti o spedire separatamente?|||Confronta spedizioni CSSBuy riunite e separate in base a dimensioni, costi, restrizioni degli articoli e protezione necessaria.
cssbuy-domestic-shipping-seller-to-warehouse|||Spedizione interna CSSBuy: costi dal venditore al magazzino|||Comprendi i costi della spedizione interna in Cina con CSSBuy. Confronta i venditori e distingui la consegna al magazzino dal trasporto internazionale.
cssbuy-insurance-guide-parcel-claims|||Assicurazione CSSBuy: copertura, esclusioni e richieste|||Controlla valore assicurato, esclusioni e prove necessarie per i pacchi CSSBuy. Verifica le condizioni attuali della linea di spedizione scelta.
cssbuy-mixed-parcel-qc-volume-weight-audit-2026-07-12|||Pacchi misti CSSBuy: QC, peso e controlli prima dell'invio|||Prepara un pacco CSSBuy con articoli diversi. Controlla foto QC, imballaggio, peso volumetrico e restrizioni di trasporto con una scheda pratica.
cssbuy-pro-calculator-route-fees-guide|||Calcolatore CSSBuy: guida a peso, dimensioni e costi|||Impara a usare il calcolatore di spedizione CSSBuy. Confronta peso reale e volumetrico e verifica la stima rispetto al costo finale del pacco.
cssbuy-pro-coupon-exchange-rate-reward-guide|||CSSBuy: coupon, punti e tassi di cambio spiegati|||Verifica separatamente condizioni dei coupon CSSBuy, punti premio e conversione valutaria. Confronta l'importo finale prima di usare una promozione.
cssbuy-pro-fee-qc-shipping-route-index|||Come funziona CSSBuy: acquisti, QC e costi di spedizione|||Segui un acquisto CSSBuy dalla scelta del prodotto al controllo in magazzino e alla spedizione. Distingui il costo degli articoli dalle spese del pacco.
cssbuy-pro-parcel-risk-qc-2026-07-09|||Controlli del pacco CSSBuy: QC, imballaggio e limiti di invio|||Prima di spedire con CSSBuy, verifica dubbi QC, articoli fragili, peso, imballaggio, scadenze di deposito e restrizioni della linea.
cssbuy-pro-qc-lab-photo-video-extra-fee|||Foto QC aggiuntive CSSBuy: richieste, costi e tempi|||Richiedi foto QC e misure utili su CSSBuy. Verifica gli eventuali supplementi e chiarisci i dubbi prima dell'imballaggio e della spedizione internazionale.
cssbuy-pro-w2c-qc-shipping-workflow-2026|||Ordini CSSBuy: lista di controllo per link, QC e spedizione|||Organizza un ordine CSSBuy dal link originale all'approvazione QC e all'invio. Registra le informazioni mancanti e il prossimo passo di ogni fase.
cssbuy-restricted-items-shipping|||Restrizioni CSSBuy: batterie, liquidi ed elettronica|||Verifica le regole CSSBuy per batterie, elettronica, liquidi e pacchi misti. Conferma l'ammissibilità per la destinazione e la linea selezionate.
cssbuy-service-payment-fees-prepayment-audit|||Commissioni CSSBuy: servizio, pagamento e cambio valuta|||Separa commissioni di servizio CSSBuy, costi di pagamento e conversione. Confronta la somma pagata con il saldo accreditato e verifica le ricevute.
cssbuy-shipping-line-comparison-framework|||Linee CSSBuy: confrontare costi, peso e tempi di consegna|||Confronta le linee CSSBuy usando le stesse misure e lo stesso contenuto. Verifica restrizioni, preventivi completi, tempi stimati e tracciamento.
cssbuy-shoe-box-removal|||CSSBuy senza scatole per scarpe: costi e protezione|||Confronta spedizioni CSSBuy con e senza scatole per scarpe. Controlla dimensioni, protezione, eventuali costi di imballaggio e preventivo finale.
cssbuy-spreadsheet|||Foglio di calcolo CSSBuy: link prodotti, QC e budget|||Organizza link CSSBuy, taglie, prezzi e controlli QC in un foglio utile. Separa la ricerca dei prodotti dal budget di spedizione del pacco.
cssbuy-total-landed-cost-worksheet|||Budget CSSBuy: costo totale dall'acquisto alla consegna|||Prepara un budget CSSBuy con prodotti, consegna in Cina, pagamento, imballaggio e trasporto internazionale. Distingui stime e costi già pagati.
cssbuy-tracking-not-updating-parcel-status-guide|||Tracking CSSBuy fermo: controlli sullo stato e prossimi passi|||Scopri cosa verificare se il tracking CSSBuy non cambia. Individua la fase, salva gli ultimi aggiornamenti e contatta l'assistenza dal pacco interessato.
cssbuy-vacuum-packing-clothes|||Vestiti CSSBuy sottovuoto: volume, costi e precauzioni|||Confronta piegatura, compressione e sottovuoto per i vestiti CSSBuy. Verifica i tessuti, il peso fatturabile e i costi aggiuntivi di imballaggio.
cssbuy-volumetric-weight|||Peso volumetrico CSSBuy: formula ed esempi di pacchi|||Calcola il peso volumetrico CSSBuy con il divisore della tua linea. Confronta peso reale, dimensioni imballate e scaglioni di fatturazione.
qc-guide|||Foto QC CSSBuy: taglie, difetti e possibilità di reso|||Usa una lista QC CSSBuy per verificare taglie, varianti e difetti visibili. Richiedi le immagini mancanti e valuta il reso prima della spedizione.
w2c|||Link CSSBuy: trovare, verificare e preparare l'ordine|||Trova e verifica link di prodotti CSSBuy, venditore e taglia scelta. Conserva le informazioni necessarie per i controlli QC e la preparazione del pacco.
''')

add_catalog('zh', '''
best-agent-2026|||CSSBuy 与其他代购平台比较：费用、QC 和运输|||用相同商品、包裹尺寸和收货地区比较 CSSBuy 与其他代购平台，逐项检查总费用、QC 服务、运输条件和客服处理方式。
cssbuy-consolidate-or-split-parcel-cost-model|||CSSBuy 合包还是分包？比较运费与保护需求|||比较 CSSBuy 合并包裹和分开寄送的完整成本，结合包装尺寸、商品运输限制、固定费用和保护需求作出选择。
cssbuy-domestic-shipping-seller-to-warehouse|||CSSBuy 国内运费：卖家到仓库的费用如何计算|||了解 CSSBuy 商品从中国卖家到仓库的国内运费，比较卖家报价、核对费用调整，并与后续国际运费分别记录。
cssbuy-insurance-guide-parcel-claims|||CSSBuy 包裹保险：保障范围、除外责任与索赔|||核对 CSSBuy 包裹保险的保额、保障范围、除外责任和索赔材料，按所选运输线路的现行条款准备寄件记录。
cssbuy-mixed-parcel-qc-volume-weight-audit-2026-07-12|||CSSBuy 混合包裹检查：QC、体积重与运输限制|||准备包含不同商品的 CSSBuy 包裹时，逐项检查 QC、包装、实际重量、体积重及线路限制，用清单整理待确认信息。
cssbuy-pro-calculator-route-fees-guide|||CSSBuy 运费计算器使用指南：重量、尺寸与费用|||了解 CSSBuy 运费计算器需要哪些数据，比较实际重量和体积重，核对包装方案、估算报价与最终包裹收费的差异。
cssbuy-pro-coupon-exchange-rate-reward-guide|||CSSBuy 优惠券、积分与汇率：如何核对实际费用|||分别检查 CSSBuy 优惠券的适用条件、积分奖励和货币兑换，在使用促销前比较最终实付金额，避免把折扣与汇率混为一谈。
cssbuy-pro-fee-qc-shipping-route-index|||CSSBuy 怎么买：下单、仓库 QC 与运输费用|||按照商品选择、付款、仓库检查和国际运输的顺序了解 CSSBuy 流程，将商品费用与包裹运输费用分开核对。
cssbuy-pro-parcel-risk-qc-2026-07-09|||CSSBuy 发货前检查清单：QC、包装与线路限制|||寄出 CSSBuy 包裹前，检查未解决的 QC 问题、易碎商品、重量、包装保护、仓储期限及运输线路的具体限制。
cssbuy-pro-qc-lab-photo-video-extra-fee|||CSSBuy 补拍 QC 照片：申请方法、费用与检查时机|||向 CSSBuy 提出明确的照片和测量需求，确认补拍费用，在包装及国际发货前补齐影响商品验收判断的必要信息。
cssbuy-pro-w2c-qc-shipping-workflow-2026|||CSSBuy 订单清单：从商品链接、QC 到发货|||从原始商品链接到 QC 验收和包裹发货，整理 CSSBuy 订单记录，明确每个阶段尚缺的信息和下一步操作。
cssbuy-restricted-items-shipping|||CSSBuy 运输限制：电池、液体与电子产品|||检查 CSSBuy 对电池、电子产品、液体和混合包裹的运输限制，按收货地区、商品属性及所选线路确认是否可寄。
cssbuy-service-payment-fees-prepayment-audit|||CSSBuy 服务费与支付费用：付款前核对哪些项目|||将 CSSBuy 服务费、支付手续费和货币兑换分别核对，比较实际付款与到账余额，并通过交易凭证检查费用差异。
cssbuy-shipping-line-comparison-framework|||CSSBuy 运输线路比较：费用、计费重量与时效|||用同一包裹的尺寸和商品信息比较 CSSBuy 运输线路，先确认可寄范围，再查看完整报价、预计时效和物流跟踪方式。
cssbuy-shoe-box-removal|||CSSBuy 拆鞋盒：比较运输费用与商品保护|||比较 CSSBuy 保留或拆除鞋盒的方案，核对包装尺寸、鞋子保护、可选包装费用和最终运费，避免只看鞋盒重量。
cssbuy-spreadsheet|||CSSBuy 商品清单：整理链接、QC 与购买预算|||使用实用的 CSSBuy 商品清单记录链接、尺码、价格和仓库 QC，将商品研究与包裹运输预算分开，方便后续核对。
cssbuy-total-landed-cost-worksheet|||CSSBuy 总费用预算表：从商品价格到最终送达|||建立包含商品、中国国内运费、支付费用、包装和国际运输的 CSSBuy 预算表，区分估算、报价与已付金额。
cssbuy-tracking-not-updating-parcel-status-guide|||CSSBuy 物流不更新：按包裹状态检查与处理|||遇到 CSSBuy 物流停止更新时，先确认当前运输阶段，保存最后扫描记录，再从对应包裹中向客服提供可核查的信息。
cssbuy-vacuum-packing-clothes|||CSSBuy 衣物真空包装：体积、费用与保护注意事项|||比较 CSSBuy 衣物折叠、压缩和真空包装方案，检查面料是否适合、计费重量变化及额外包装费用，再确认操作。
cssbuy-volumetric-weight|||CSSBuy 体积重计算：公式、包裹尺寸与示例|||按 CSSBuy 所选运输线路的体积重除数计算，比较实际重量、外包装尺寸和计费进位规则，理解最终收费依据。
qc-guide|||CSSBuy QC 照片：检查尺码、瑕疵与退货选择|||按照 CSSBuy QC 清单核对尺码、所选款式和可见瑕疵，申请缺失角度的照片，并在国际发货前确认可用的退货方案。
w2c|||CSSBuy 商品链接：查找、核对与下单准备|||查找并核对 CSSBuy 商品链接、卖家和所选尺码，保存仓库 QC 与运输规划需要的资料，避免把失效或错误链接当作同款。
''')

add_faq('en', '''
Is cssbuys.pro the official CSSBuy website?|||No. This is an independent guide site. It does not accept orders, hold account balances, take warehouse photos or arrange shipping. Those services are handled through CSSBuy.
How do I order a product through CSSBuy?|||Open the original product listing, check the seller and selected variation, then use the link in CSSBuy. Confirm size, colour, quantity and current charges before paying. If the link cannot be read, ask about the Expert Buy option.
Why are product payment and international shipping separate?|||The item is purchased and delivered to the Chinese warehouse first. International shipping is arranged later, after warehouse checks and parcel preparation. Budget for both stages rather than treating the product price as the delivered price.
What should I include in a CSSBuy budget?|||Record the product price, Chinese domestic delivery, any service and payment charges, currency conversion, optional warehouse services, international freight and applicable destination charges. Keep estimates separate from confirmed and paid amounts.
Does this site quote live CSSBuy shipping rates?|||No. Our planning tools and examples explain weight and cost calculations. For available lines and current prices, use the official CSSBuy calculator with your destination, item attributes and packed measurements.
Why can two parcels with the same weight cost different amounts?|||Their dimensions, contents, destination or eligible shipping lines may differ. A bulky parcel can have a higher chargeable weight. Compare complete quotes using the same inputs and check each line's billing rules.
How do I calculate volumetric weight?|||Multiply the packed length, width and height using the units required by the line, then divide by that line's stated divisor. Check whether the route bills actual weight, volumetric weight or the larger amount, including any rounding.
How long does CSSBuy delivery take?|||There is no single delivery time for every order. Seller dispatch, warehouse processing, packing, international transport and local delivery are separate stages. Use the current estimate for the selected line and allow for uncertainty.
How many free QC photos does CSSBuy advertise?|||The official homepage reviewed on 4 November 2026 advertises 3–5 free QC photos. Confirm what is included for your specific order and check additional-photo or measurement options before requesting them.
Why can I see a warehouse weight but no QC photos?|||A weight entry alone does not show whether the photo task is complete. Check the order status and selected services, then ask about the missing images in that order. Avoid approving shipment while an important QC question remains unanswered.
How much do extra photos or video checks cost?|||Check the current service menu or ask CSSBuy for a quote describing the exact view or measurement you need. Do not assume additional photos, measurements or videos are free or available for every item.
Can QC photos prove authenticity or product performance?|||No. Photos can help check the received variation, visible condition, measurements and included parts. They cannot establish every material, hidden defect, battery condition or long-term performance characteristic.
What should I do if the warehouse photos show the wrong size or damage?|||Save the order details and relevant photos, describe the visible mismatch, and contact CSSBuy through the order promptly. Ask about return or replacement options before removing packaging or authorising international shipment.
How long do I have to request a warehouse return?|||CSSBuy's public Q&A lists conditions including seller acceptance, less than seven days in the warehouse and payment of return postage. Check the actual order promptly; this is not an unconditional return promise for every product.
Is returning an item the same as withdrawing my account balance?|||No. A product return concerns the seller and the item. A balance withdrawal concerns money already held in your CSSBuy account. Use the appropriate request and keep the two transaction records separate.
Will a refund automatically go back to my card or bank?|||Do not assume it will. Check whether the transaction is an account credit or a refund to the original payment method. For a balance withdrawal, verify the available route, fees and processing information in your account or with support.
Why can the final shipping charge differ from the deposit?|||The deposit uses estimated shipment information. Final verified dimensions, weight and line conditions can change the calculation. Compare the parcel invoice with the original estimate; check your account for any credit rather than assuming a bank refund.
How long is free warehouse storage?|||Official product information distinguishes 90 days for regular goods and 30 days for sensitive goods. Check your item's classification and expiry date in the account; do not apply the general 90-day wording to every item.
Can I extend storage or reset it by combining items?|||Ask about an extension before the displayed expiry date and confirm the price and affected order. Do not assume consolidation, a new purchase or a support enquiry resets the storage clock for older items.
What should I do if my stored item has expired?|||Contact CSSBuy immediately with the order or parcel identifier and ask whether the goods are still available and what action remains possible. Do not assume an expired item is recoverable or that a past clearance notice gives you extra time.
Should I combine all my items into one parcel?|||Compare a combined parcel with realistic split options. Check item compatibility, packed dimensions, fixed fees, protection and storage deadlines. A larger combined parcel is not automatically the least expensive suitable option.
Does removing shoe boxes always reduce shipping costs?|||No. It can reduce volume, but the result depends on the final carton, billing rules and any packing fees. Consider the value of the box and protection needed for the shoes before requesting removal.
Is vacuum packing suitable for all clothing?|||No. Review the garment's construction, material, shape and trims first. Compare simple folding, gentle compression and vacuum packing, and ask the warehouse to confirm what is suitable before applying pressure.
Can CSSBuy ship electronics with batteries or liquids?|||Eligibility depends on the exact product, battery or liquid attributes, destination and current line rules. Provide accurate specifications and ask about an eligible route before placing the item into a mixed parcel.
What should I check when tracking stops updating?|||Identify the last confirmed shipping stage and carrier, save the latest scan and time, and review the selected line's guidance. Use the parcel record for an enquiry; a gap in scans alone does not prove loss.
Does parcel insurance cover every loss, damage or customs problem?|||Do not assume universal coverage. Check the current policy for your shipping line, including insured value, exclusions, reporting deadlines and evidence. Keep photos, invoices and packaging records that the policy requires.
How do I check a CSSBuy coupon, points reward or exchange rate?|||Review eligibility, expiry, minimum spend, limits and where a reward can be used. Compare the final payment and credited balance separately from the advertised discount. A coupon does not establish the currency conversion rate.
What should I do when a product link no longer works?|||Reopen the original seller listing and check the item identifier, stock and selected variation. Ask CSSBuy for help if parsing fails. Do not treat a different product reached through a replacement link as the same item without checking it.
''')

add_faq('de', '''
Ist cssbuys.pro die offizielle Website von CSSBuy?|||Nein. Dies ist eine unabhängige Ratgeberseite. Sie nimmt keine Bestellungen an, verwaltet kein Guthaben, erstellt keine Lagerfotos und organisiert keinen Versand. Diese Leistungen werden über CSSBuy abgewickelt.
Wie bestelle ich einen Artikel über CSSBuy?|||Öffne das ursprüngliche Angebot und prüfe Händler sowie Variante. Verwende den Link anschließend bei CSSBuy. Bestätige Größe, Farbe, Menge und aktuelle Gebühren vor der Zahlung. Falls der Link nicht erkannt wird, frage nach der Funktion „Expert Buy“.
Warum werden Artikel und internationaler Versand getrennt bezahlt?|||Zuerst wird der Artikel gekauft und zum chinesischen Lager geliefert. Der internationale Versand folgt nach der Lagerprüfung und Paketvorbereitung. Plane beide Schritte ein, statt den Artikelpreis als Preis einschließlich Zustellung zu betrachten.
Welche Kosten gehören in mein CSSBuy-Budget?|||Erfasse Artikelpreis, chinesischen Inlandsversand, mögliche Service- und Zahlungsgebühren, Währungsumrechnung, zusätzliche Lagerleistungen, internationalen Versand und anfallende Kosten im Zielland. Trenne Schätzungen von bestätigten und bezahlten Beträgen.
Zeigt diese Website aktuelle CSSBuy-Versandtarife an?|||Nein. Unsere Planungshilfen und Beispiele erklären Gewichts- und Kostenberechnungen. Aktuelle Linien und Preise findest du im offiziellen CSSBuy-Rechner mit deinem Zielland, den Wareneigenschaften und den Paketmaßen.
Warum können gleich schwere Pakete unterschiedlich viel kosten?|||Maße, Inhalt, Zielland oder zulässige Versandlinien können verschieden sein. Ein sperriges Paket kann ein höheres Abrechnungsgewicht haben. Vergleiche vollständige Angebote mit gleichen Angaben und prüfe die Regeln jeder Linie.
Wie berechne ich das Volumengewicht?|||Multipliziere Länge, Breite und Höhe des verpackten Pakets in den geforderten Einheiten und teile durch den Divisor der Linie. Prüfe, welches Gewicht berechnet wird und welche Rundungen oder Abrechnungsschritte gelten.
Wie lange dauert die Lieferung mit CSSBuy?|||Es gibt keine einheitliche Lieferzeit für alle Bestellungen. Händlerversand, Lagerbearbeitung, Verpackung, internationaler Transport und lokale Zustellung sind getrennte Phasen. Nutze die aktuelle Schätzung der gewählten Linie und plane Unsicherheit ein.
Wie viele kostenlose QC-Fotos bewirbt CSSBuy?|||Die am 4. November 2026 geprüfte offizielle Startseite wirbt mit 3–5 kostenlosen QC-Fotos. Prüfe den Umfang für deine konkrete Bestellung sowie Optionen für zusätzliche Fotos oder Maße vor der Beauftragung.
Warum sehe ich ein Lagergewicht, aber keine QC-Fotos?|||Ein Gewichtseintrag zeigt nicht, ob die Fotoaufnahme abgeschlossen ist. Prüfe Bestellstatus und gebuchte Leistungen und frage im betreffenden Auftrag nach den Bildern. Gib den Versand nicht frei, solange eine wichtige QC-Frage offen ist.
Was kosten zusätzliche Fotos oder Videoprüfungen?|||Prüfe das aktuelle Serviceangebot oder bitte CSSBuy um ein Angebot mit der gewünschten Ansicht oder Messung. Zusätzliche Fotos, Maße oder Videos sind nicht automatisch kostenlos oder für jeden Artikel verfügbar.
Beweisen QC-Fotos Echtheit oder Funktionsfähigkeit?|||Nein. Fotos helfen bei Variante, sichtbarem Zustand, Maßen und Zubehör. Sie belegen nicht alle Materialien, verborgenen Mängel, den Batteriezustand oder die langfristige Funktion eines Produkts.
Was tun bei falscher Größe oder Schäden auf den Lagerfotos?|||Sichere Bestelldaten und relevante Fotos, beschreibe die sichtbare Abweichung und kontaktiere CSSBuy zeitnah im Auftrag. Kläre Rückgabe oder Ersatz, bevor du Verpackungen entfernen oder die Ware international versenden lässt.
Wie lange kann ich eine Rückgabe aus dem Lager beantragen?|||CSSBuy nennt in den öffentlichen Fragen und Antworten unter anderem die Zustimmung des Verkäufers, weniger als sieben Tage im Lager und bezahltes Rückporto. Prüfe den konkreten Auftrag sofort; dies ist kein bedingungsloses Rückgaberecht für jeden Artikel.
Ist eine Warenrückgabe dasselbe wie eine Guthabenauszahlung?|||Nein. Bei einer Warenrückgabe geht es um den Verkäufer und den Artikel. Eine Guthabenauszahlung betrifft Geld auf deinem CSSBuy-Konto. Stelle den passenden Antrag und bewahre beide Vorgänge getrennt auf.
Geht eine Erstattung automatisch auf meine Karte oder mein Bankkonto?|||Gehe nicht davon aus. Prüfe, ob eine Gutschrift im CSSBuy-Konto oder eine Rückzahlung auf das ursprüngliche Zahlungsmittel vorgesehen ist. Kläre bei einer Auszahlung den verfügbaren Weg, Gebühren und Bearbeitungsinformationen im Konto oder beim Support.
Warum kann die endgültige Versandgebühr von der Vorauszahlung abweichen?|||Die Vorauszahlung beruht auf geschätzten Versanddaten. Bestätigte Maße, Gewicht und Linienbedingungen können die Berechnung verändern. Vergleiche die Abrechnung mit der Schätzung und prüfe eine mögliche Kontogutschrift, statt eine Bankrückzahlung vorauszusetzen.
Wie lange ist die Lagerung kostenlos?|||Offizielle Produktinformationen unterscheiden zwischen 90 Tagen für reguläre Waren und 30 Tagen für sensible Waren. Prüfe Einstufung und Ablaufdatum des Artikels im Konto; die allgemeine Angabe von 90 Tagen gilt nicht automatisch für alles.
Kann ich Lagerung verlängern oder durch Zusammenlegen neu starten?|||Frage vor dem angezeigten Ablaufdatum nach einer Verlängerung und bestätige Preis sowie betroffenen Auftrag. Zusammenlegung, ein neuer Einkauf oder eine Supportanfrage setzen die Frist älterer Artikel nicht automatisch zurück.
Was soll ich tun, wenn die Lagerfrist bereits abgelaufen ist?|||Kontaktiere CSSBuy sofort mit der Bestell- oder Paketnummer. Frage, ob die Ware noch verfügbar ist und welche Schritte möglich sind. Verlasse dich weder auf eine Wiederherstellung noch auf zusätzliche Zeit durch eine frühere Räumungsankündigung.
Soll ich alle Artikel zu einem Paket zusammenlegen?|||Vergleiche ein gemeinsames Paket mit realistischen getrennten Sendungen. Prüfe Warenverträglichkeit, Paketmaße, feste Gebühren, Schutz und Lagerfristen. Ein großes Paket ist nicht automatisch die günstigste geeignete Lösung.
Senkt das Entfernen von Schuhkartons immer die Versandkosten?|||Nein. Es kann Volumen sparen, doch entscheidend sind der endgültige Karton, die Abrechnungsregeln und mögliche Verpackungsgebühren. Berücksichtige den Wert der Schuhkartons und den nötigen Schutz, bevor du ihre Entfernung beauftragst.
Ist Vakuumverpackung für alle Kleidungsstücke geeignet?|||Nein. Prüfe zunächst Verarbeitung, Material, Form und Verzierungen. Vergleiche normales Falten, vorsichtige Kompression und Vakuumverpackung und lasse das Lager die geeignete Methode bestätigen.
Kann CSSBuy Elektronik mit Batterien oder Flüssigkeiten versenden?|||Das hängt vom genauen Produkt, Batterie- oder Flüssigkeitseigenschaften, Zielland und aktuellen Linienregeln ab. Gib korrekte Spezifikationen an und bestätige eine geeignete Versandmöglichkeit, bevor du einen Mischkarton zusammenstellst.
Was prüfe ich, wenn die Sendungsverfolgung keine Updates zeigt?|||Ermittle die letzte bestätigte Transportphase und den Beförderer. Sichere Scan und Zeitpunkt und prüfe die Hinweise der Versandlinie. Stelle eine Anfrage im Paketdatensatz; fehlende Scans allein beweisen keinen Verlust.
Deckt die Paketversicherung jeden Verlust, Schaden oder Zollfall ab?|||Gehe nicht von einer umfassenden Deckung aus. Prüfe die aktuelle Police deiner Versandlinie einschließlich Versicherungswert, Ausschlüssen, Meldefristen und Nachweisen. Bewahre die geforderten Fotos, Rechnungen und Verpackungsunterlagen auf.
Wie prüfe ich CSSBuy-Gutscheine, Punkte und Wechselkurse?|||Prüfe Berechtigung, Ablauf, Mindestbetrag, Höchstgrenzen und Verwendungszweck der Prämie. Vergleiche Zahlung und gutgeschriebenes Guthaben getrennt vom beworbenen Rabatt. Ein Gutschein bestimmt nicht den Umrechnungskurs.
Was tun, wenn ein Produktlink nicht mehr funktioniert?|||Öffne das ursprüngliche Händlerangebot und prüfe Artikelnummer, Verfügbarkeit und Variante. Bitte CSSBuy bei Importproblemen um Hilfe. Ein anderes Produkt hinter einem Ersatzlink ist erst nach Prüfung als Alternative zu bewerten.
''')

add_faq('fr', '''
cssbuys.pro est-il le site officiel de CSSBuy ?|||Non. Ce site propose des guides indépendants. Il ne prend pas de commandes, ne conserve pas de solde, ne réalise pas de photos en entrepôt et n'organise pas d'expéditions. Ces services passent par CSSBuy.
Comment commander un produit avec CSSBuy ?|||Ouvrez l'annonce d'origine, vérifiez le vendeur et la variante, puis utilisez son lien sur CSSBuy. Confirmez taille, couleur, quantité et frais actuels avant de payer. Si le lien n'est pas reconnu, renseignez-vous sur l'option « Expert Buy ».
Pourquoi paie-t-on séparément l'article et l'expédition internationale ?|||L'article est d'abord acheté puis livré à l'entrepôt chinois. Le transport international se prépare ensuite, après les contrôles et la préparation du colis. Prévoyez les deux étapes : le prix du produit n'est pas son prix livré.
Que faut-il inclure dans un budget CSSBuy ?|||Notez le prix des articles, la livraison en Chine, les éventuels frais de service et de paiement, la conversion, les services en entrepôt, le fret international et les frais applicables à destination. Séparez estimations, montants confirmés et paiements.
Ce site fournit-il les tarifs CSSBuy en temps réel ?|||Non. Nos outils et exemples expliquent les calculs de poids et de coût. Pour connaître les lignes disponibles et leurs tarifs, utilisez le calculateur officiel avec votre destination, les caractéristiques des articles et les dimensions emballées.
Pourquoi deux colis de même poids peuvent-ils coûter différemment ?|||Leurs dimensions, contenus, destinations ou lignes admissibles peuvent différer. Un colis volumineux peut avoir un poids facturable supérieur. Comparez des devis complets avec les mêmes données et vérifiez les règles de chaque ligne.
Comment calculer le poids volumétrique ?|||Multipliez longueur, largeur et hauteur du colis emballé dans les unités demandées, puis divisez par le diviseur indiqué pour la ligne. Vérifiez le poids retenu pour la facturation ainsi que les arrondis et paliers éventuels.
Combien de temps prend une livraison CSSBuy ?|||Il n'existe pas de délai unique. Expédition du vendeur, traitement en entrepôt, emballage, transport international et livraison locale sont des étapes distinctes. Consultez l'estimation actuelle de la ligne choisie et prévoyez une marge d'incertitude.
Combien de photos QC gratuites CSSBuy annonce-t-il ?|||La page d'accueil officielle consultée le 4 novembre 2026 annonce 3 à 5 photos QC gratuites. Vérifiez ce qui est inclus pour votre commande ainsi que les options de photos ou de mesures supplémentaires avant de les demander.
Pourquoi vois-je un poids en entrepôt sans photos QC ?|||Un poids enregistré ne prouve pas que les photos sont terminées. Vérifiez le statut et les services sélectionnés, puis demandez les images manquantes dans la commande concernée. N'autorisez pas l'envoi tant qu'une question QC importante reste ouverte.
Combien coûtent des photos supplémentaires ou une vérification vidéo ?|||Consultez les services actuels ou demandez à CSSBuy un devis précisant la vue ou la mesure souhaitée. Ne supposez pas que les photos, mesures ou vidéos supplémentaires sont gratuites ou disponibles pour chaque article.
Les photos QC prouvent-elles l'authenticité ou le fonctionnement ?|||Non. Elles aident à vérifier variante reçue, état visible, mesures et accessoires. Elles ne permettent pas d'établir tous les matériaux, défauts cachés, l'état d'une batterie ou les performances à long terme.
Que faire si les photos montrent une mauvaise taille ou des dégâts ?|||Conservez les détails de la commande et les photos utiles, décrivez l'écart visible et contactez rapidement CSSBuy depuis la commande. Vérifiez les possibilités de retour ou d'échange avant de retirer l'emballage ou d'autoriser l'expédition internationale.
Quel est le délai pour demander un retour depuis l'entrepôt ?|||La FAQ publique de CSSBuy mentionne notamment l'accord du vendeur, moins de sept jours à l'entrepôt et le paiement du retour. Vérifiez rapidement votre commande : ce n'est pas une promesse de retour sans condition pour tous les produits.
Renvoyer un article et retirer mon solde sont-ils la même démarche ?|||Non. Un retour de produit concerne l'article et son vendeur. Le retrait du solde concerne l'argent déjà présent sur votre compte CSSBuy. Choisissez la demande adaptée et gardez séparément les justificatifs des deux opérations.
Un remboursement revient-il automatiquement sur ma carte ou mon compte bancaire ?|||Ne le présumez pas. Vérifiez s'il s'agit d'un crédit sur le compte CSSBuy ou d'un remboursement vers le moyen de paiement initial. Pour retirer un solde, confirmez le mode disponible, les frais et les indications de traitement.
Pourquoi les frais d'expédition finaux diffèrent-ils de l'acompte ?|||L'acompte repose sur une estimation. Les dimensions, le poids vérifiés et les conditions de la ligne peuvent modifier le calcul. Comparez la facture à l'estimation et vérifiez un éventuel crédit CSSBuy sans supposer un remboursement bancaire.
Combien de temps le stockage est-il gratuit ?|||Les informations produit officielles distinguent 90 jours pour les articles ordinaires et 30 pour les articles sensibles. Vérifiez la catégorie et l'échéance dans votre compte : la mention générale de 90 jours ne s'applique pas automatiquement à tout.
Puis-je prolonger le stockage ou le réinitialiser en regroupant les articles ?|||Demandez une prolongation avant l'échéance affichée et confirmez son prix ainsi que la commande concernée. Ne supposez pas qu'un regroupement, un nouvel achat ou une demande d'assistance remet à zéro le délai des anciens articles.
Que faire si la durée de stockage est dépassée ?|||Contactez immédiatement CSSBuy avec l'identifiant de la commande ou du colis. Demandez si les marchandises sont encore disponibles et quelles actions restent possibles. Ne supposez pas qu'elles sont récupérables ou qu'un ancien avis de déstockage prolonge votre délai.
Dois-je regrouper tous mes articles dans un seul colis ?|||Comparez un colis groupé à des envois séparés réalistes. Vérifiez compatibilité des articles, dimensions, frais fixes, protection et échéances de stockage. Un colis plus grand n'est pas automatiquement la solution adaptée la moins chère.
Retirer les boîtes à chaussures réduit-il toujours les frais ?|||Non. Cela peut réduire le volume, mais le résultat dépend du carton final, de la facturation et des frais d'emballage éventuels. Évaluez l'utilité des boîtes et la protection nécessaire avant de demander leur retrait.
L'emballage sous vide convient-il à tous les vêtements ?|||Non. Examinez d'abord la construction, le tissu, la forme et les ornements. Comparez pliage simple, compression légère et sous vide, puis demandez à l'entrepôt de confirmer la méthode appropriée.
CSSBuy peut-il expédier des appareils avec batteries ou des liquides ?|||Cela dépend du produit exact, des caractéristiques de la batterie ou du liquide, de la destination et des règles actuelles. Fournissez des spécifications précises et confirmez une ligne admissible avant d'intégrer l'article à un colis mixte.
Que vérifier lorsque le suivi ne se met plus à jour ?|||Identifiez la dernière étape confirmée et le transporteur. Conservez le dernier scan avec sa date et consultez les indications de la ligne. Posez votre question depuis le colis concerné ; une absence de scans ne prouve pas à elle seule une perte.
L'assurance couvre-t-elle toutes les pertes, détériorations ou difficultés douanières ?|||Ne supposez pas une couverture universelle. Vérifiez la police actuelle de la ligne, le montant assuré, les exclusions, les délais de déclaration et les justificatifs. Conservez les photos, factures et éléments d'emballage demandés.
Comment vérifier un coupon CSSBuy, des points ou un taux de change ?|||Vérifiez l'éligibilité, l'expiration, le minimum d'achat, les plafonds et l'utilisation autorisée de la récompense. Comparez paiement final et solde crédité séparément de la remise annoncée. Un coupon ne détermine pas le taux de conversion.
Que faire si un lien produit ne fonctionne plus ?|||Rouvrez l'annonce d'origine et vérifiez l'identifiant, le stock et la variante. Demandez de l'aide à CSSBuy si l'importation échoue. Un produit différent derrière un nouveau lien ne doit pas être considéré comme identique sans vérification.
''')

add_faq('es', '''
¿cssbuys.pro es la web oficial de CSSBuy?|||No. Esta es una web de guías independientes. No acepta pedidos, guarda saldos, toma fotos en el almacén ni organiza envíos. Esos servicios se gestionan a través de CSSBuy.
¿Cómo compro un producto a través de CSSBuy?|||Abre el anuncio original y comprueba el vendedor y la variante. Usa después el enlace en CSSBuy. Confirma talla, color, cantidad y cargos vigentes antes de pagar. Si no reconoce el enlace, consulta la opción «Expert Buy».
¿Por qué se pagan por separado el producto y el envío internacional?|||Primero se compra el artículo y se entrega en el almacén chino. El transporte internacional se prepara después de las comprobaciones y del embalaje. Incluye ambas etapas en el presupuesto: el precio del producto no equivale al coste entregado.
¿Qué debo incluir en un presupuesto CSSBuy?|||Anota producto, envío dentro de China, posibles comisiones de servicio y pago, cambio de moneda, servicios de almacén, transporte internacional y cargos aplicables en destino. Separa las estimaciones de los importes confirmados y pagados.
¿Esta web muestra tarifas CSSBuy en tiempo real?|||No. Nuestras herramientas y ejemplos explican cálculos de peso y coste. Para consultar líneas y tarifas actuales, usa la calculadora oficial con tu destino, las características del artículo y las medidas del paquete embalado.
¿Por qué dos paquetes del mismo peso pueden costar distinto?|||Pueden cambiar las dimensiones, el contenido, el destino o las líneas admitidas. Un paquete voluminoso puede tener mayor peso facturable. Compara presupuestos completos con los mismos datos y revisa las reglas de cada línea.
¿Cómo calculo el peso volumétrico?|||Multiplica largo, ancho y alto del paquete embalado en las unidades exigidas y divide por el divisor de la línea. Comprueba qué peso se utiliza para cobrar, además de los redondeos y los incrementos aplicables.
¿Cuánto tarda una entrega CSSBuy?|||No existe un plazo único. El envío del vendedor, la gestión del almacén, el embalaje, el transporte internacional y la entrega local son etapas distintas. Consulta la estimación actual de la línea y deja margen para variaciones.
¿Cuántas fotos QC gratuitas anuncia CSSBuy?|||La página oficial revisada el 4 de noviembre de 2026 anuncia entre 3 y 5 fotos QC gratuitas. Comprueba lo incluido en tu pedido y las opciones de fotos o medidas adicionales antes de solicitarlas.
¿Por qué aparece el peso en el almacén, pero no las fotos QC?|||Registrar el peso no significa que la tarea de fotos haya terminado. Revisa el estado y los servicios seleccionados y pregunta por las imágenes en ese pedido. No apruebes el envío si sigue pendiente una duda QC importante.
¿Cuánto cuestan las fotos adicionales o las comprobaciones en vídeo?|||Consulta el menú actual o pide a CSSBuy un presupuesto que especifique la vista o medida necesaria. No des por hecho que las fotos, medidas o vídeos adicionales son gratuitos ni que están disponibles para cualquier artículo.
¿Las fotos QC demuestran autenticidad o funcionamiento?|||No. Ayudan a comprobar la variante recibida, el estado visible, las medidas y las piezas incluidas. No demuestran todos los materiales, defectos ocultos, el estado de la batería ni el rendimiento a largo plazo.
¿Qué hago si las fotos muestran una talla equivocada o daños?|||Guarda los datos del pedido y las fotos relevantes, describe la diferencia visible y contacta pronto con CSSBuy desde ese pedido. Consulta devolución o sustitución antes de retirar embalajes o autorizar el envío internacional.
¿Cuánto tiempo tengo para pedir una devolución desde el almacén?|||La FAQ pública de CSSBuy indica condiciones como aceptación del vendedor, menos de siete días en almacén y pago del transporte de devolución. Revisa tu pedido cuanto antes; no es una devolución incondicional para cualquier producto.
¿Devolver un artículo es lo mismo que retirar el saldo?|||No. La devolución de un producto afecta al artículo y al vendedor. La retirada de saldo afecta al dinero que ya tienes en la cuenta CSSBuy. Usa la solicitud adecuada y conserva por separado los registros de ambas operaciones.
¿Un reembolso vuelve automáticamente a mi tarjeta o banco?|||No lo supongas. Comprueba si se trata de un abono en CSSBuy o de una devolución al método de pago original. Para retirar saldo, confirma la vía disponible, las comisiones y la información de tramitación en la cuenta o con soporte.
¿Por qué el importe final del envío puede diferir del anticipo?|||El anticipo se calcula con datos estimados. Las dimensiones, el peso verificado y las condiciones de la línea pueden cambiar el resultado. Compara la factura con la estimación y revisa posibles abonos en CSSBuy sin asumir un reembolso bancario.
¿Cuánto tiempo es gratuito el almacenamiento?|||La información oficial de productos distingue 90 días para mercancía normal y 30 para mercancía sensible. Comprueba la clasificación y la fecha límite de cada artículo en tu cuenta; no apliques los 90 días generales a todos los casos.
¿Puedo ampliar el almacenamiento o reiniciarlo al agrupar artículos?|||Solicita la ampliación antes de la fecha mostrada y confirma el precio y el pedido afectado. No supongas que agrupar, comprar algo nuevo o preguntar al soporte reinicia el plazo de artículos anteriores.
¿Qué hago si mi artículo ha superado el plazo de almacenamiento?|||Contacta inmediatamente con CSSBuy e indica el identificador del pedido o paquete. Pregunta si la mercancía sigue disponible y qué opciones quedan. No supongas que puede recuperarse ni que un aviso antiguo de vaciado concede tiempo adicional.
¿Conviene agrupar todos los artículos en un paquete?|||Compara un paquete conjunto con alternativas separadas realistas. Revisa compatibilidad, dimensiones, gastos fijos, protección y plazos de almacenamiento. Un paquete mayor no siempre es la opción adecuada más barata.
¿Quitar las cajas de zapatos siempre abarata el envío?|||No. Puede reducir volumen, pero depende del embalaje final, las reglas de cobro y los posibles cargos de preparación. Considera el valor de la caja y la protección necesaria antes de pedir que la retiren.
¿El envasado al vacío sirve para toda la ropa?|||No. Revisa primero la confección, el material, la forma y los adornos. Compara doblado normal, compresión suave y vacío, y pide al almacén que confirme qué método es adecuado.
¿CSSBuy puede enviar electrónica con baterías o líquidos?|||Depende del producto exacto, los atributos de la batería o del líquido, el destino y las reglas vigentes. Proporciona especificaciones correctas y confirma una línea admitida antes de incluir el artículo en un paquete mixto.
¿Qué compruebo cuando el seguimiento no se actualiza?|||Identifica la última etapa confirmada y el transportista, guarda el registro con su fecha y consulta las indicaciones de la línea. Pregunta desde el paquete correspondiente: una pausa en los registros no demuestra por sí sola una pérdida.
¿El seguro cubre cualquier pérdida, daño o problema aduanero?|||No presupongas una cobertura universal. Revisa la póliza vigente para tu línea: valor asegurado, exclusiones, plazos de aviso y pruebas. Conserva las fotos, facturas y registros de embalaje exigidos.
¿Cómo compruebo cupones CSSBuy, puntos y tipos de cambio?|||Revisa requisitos, caducidad, compra mínima, límites y usos permitidos de la recompensa. Compara el pago final y el saldo recibido por separado del descuento anunciado. Un cupón no determina el tipo de cambio.
¿Qué hago cuando un enlace de producto deja de funcionar?|||Abre el anuncio original del vendedor y comprueba identificador, disponibilidad y variante. Pide ayuda a CSSBuy si falla la importación. No consideres idéntico un producto distinto al que llegue un enlace de sustitución sin revisarlo.
''')

add_faq('it', '''
cssbuys.pro è il sito ufficiale di CSSBuy?|||No. Questo è un sito di guide indipendenti. Non accetta ordini, custodisce saldi, scatta foto in magazzino o organizza spedizioni. Questi servizi vengono gestiti tramite CSSBuy.
Come ordino un prodotto tramite CSSBuy?|||Apri l'inserzione originale e controlla venditore e variante, poi usa il link su CSSBuy. Conferma taglia, colore, quantità e costi attuali prima di pagare. Se il link non viene riconosciuto, chiedi informazioni sull'opzione «Expert Buy».
Perché articolo e spedizione internazionale si pagano separatamente?|||L'articolo viene prima acquistato e consegnato al magazzino cinese. Il trasporto internazionale si organizza dopo i controlli e la preparazione del pacco. Prevedi entrambe le fasi: il prezzo del prodotto non è il costo fino alla consegna.
Che cosa devo includere in un budget CSSBuy?|||Registra prezzo del prodotto, consegna interna in Cina, eventuali commissioni di servizio e pagamento, conversione valutaria, servizi di magazzino, trasporto internazionale e costi applicabili a destinazione. Separa stime, importi confermati e somme pagate.
Questo sito fornisce tariffe CSSBuy in tempo reale?|||No. Strumenti ed esempi spiegano i calcoli di peso e costo. Per linee disponibili e prezzi aggiornati, usa il calcolatore ufficiale con destinazione, caratteristiche degli articoli e misure del pacco imballato.
Perché due pacchi dello stesso peso possono costare diversamente?|||Possono differire dimensioni, contenuto, destinazione o linee ammesse. Un pacco ingombrante può avere un peso fatturabile maggiore. Confronta preventivi completi con gli stessi dati e verifica le regole di ogni linea.
Come si calcola il peso volumetrico?|||Moltiplica lunghezza, larghezza e altezza del pacco imballato nelle unità richieste, poi dividi per il divisore indicato dalla linea. Verifica quale peso viene fatturato, compresi eventuali arrotondamenti e scaglioni.
Quanto impiega una consegna CSSBuy?|||Non esiste un tempo unico per tutti gli ordini. Invio del venditore, gestione in magazzino, imballaggio, trasporto internazionale e consegna locale sono fasi distinte. Consulta la stima attuale della linea scelta e considera possibili variazioni.
Quante foto QC gratuite pubblicizza CSSBuy?|||La pagina ufficiale consultata il 4 novembre 2026 pubblicizza 3–5 foto QC gratuite. Verifica cosa comprende il tuo ordine e le opzioni per immagini o misure aggiuntive prima di richiederle.
Perché vedo il peso in magazzino ma non le foto QC?|||Il peso registrato non dimostra che le fotografie siano pronte. Controlla stato e servizi selezionati, poi chiedi delle immagini nel relativo ordine. Non approvare la spedizione finché resta una domanda QC importante senza risposta.
Quanto costano foto aggiuntive o controlli video?|||Consulta i servizi attuali o chiedi a CSSBuy un preventivo indicando la vista o la misura necessaria. Non presumere che fotografie, misure o video aggiuntivi siano gratuiti o disponibili per ogni prodotto.
Le foto QC provano l'autenticità o il funzionamento?|||No. Aiutano a verificare variante ricevuta, condizioni visibili, misure e accessori. Non dimostrano tutti i materiali, i difetti nascosti, lo stato della batteria o le prestazioni nel tempo.
Cosa faccio se le foto mostrano taglia sbagliata o danni?|||Salva dettagli dell'ordine e foto pertinenti, descrivi la differenza visibile e contatta presto CSSBuy tramite l'ordine. Chiedi le possibilità di reso o sostituzione prima di rimuovere l'imballaggio o autorizzare l'invio internazionale.
Quanto tempo ho per chiedere un reso dal magazzino?|||Le FAQ pubbliche CSSBuy indicano condizioni quali accettazione del venditore, meno di sette giorni in magazzino e pagamento del trasporto di ritorno. Controlla subito l'ordine: non è una promessa di reso incondizionato per ogni prodotto.
Restituire un articolo equivale a ritirare il saldo dell'account?|||No. Il reso riguarda l'articolo e il venditore. Il prelievo del saldo riguarda denaro già presente sull'account CSSBuy. Usa la richiesta corretta e conserva separatamente le registrazioni delle due operazioni.
Un rimborso torna automaticamente sulla carta o sul conto bancario?|||Non darlo per scontato. Verifica se si tratta di un credito CSSBuy o di un rimborso sul metodo originale. Per ritirare il saldo, conferma modalità disponibili, commissioni e informazioni di elaborazione nell'account o con l'assistenza.
Perché il costo finale della spedizione può differire dall'anticipo?|||L'anticipo usa dati stimati. Dimensioni e peso verificati, insieme alle condizioni della linea, possono modificare il calcolo. Confronta il conto finale con la stima e controlla eventuali crediti CSSBuy senza presumere un rimborso bancario.
Per quanto tempo il deposito è gratuito?|||Le informazioni ufficiali dei prodotti distinguono 90 giorni per merci ordinarie e 30 per merci sensibili. Controlla classificazione e scadenza nell'account; non applicare automaticamente l'indicazione generale di 90 giorni a ogni articolo.
Posso prolungare il deposito o azzerarlo riunendo gli articoli?|||Chiedi una proroga prima della scadenza indicata e conferma prezzo e ordine interessato. Non presumere che riunire articoli, effettuare un nuovo acquisto o contattare l'assistenza faccia ripartire il termine degli articoli precedenti.
Cosa faccio se il periodo di deposito è scaduto?|||Contatta immediatamente CSSBuy con l'identificativo dell'ordine o del pacco. Chiedi se la merce è ancora disponibile e quali azioni restano possibili. Non presumere che sia recuperabile o che un vecchio avviso di sgombero conceda altro tempo.
Conviene riunire tutti gli articoli in un solo pacco?|||Confronta un pacco unico con alternative separate realistiche. Verifica compatibilità degli articoli, dimensioni, costi fissi, protezione e scadenze. Un pacco più grande non è automaticamente la soluzione adatta meno costosa.
Rimuovere le scatole per scarpe riduce sempre la spedizione?|||No. Può ridurre il volume, ma il risultato dipende dal cartone finale, dalle regole tariffarie e dai costi di preparazione. Valuta il valore delle scatole e la protezione delle scarpe prima di richiederne la rimozione.
Il sottovuoto è adatto a tutti i capi?|||No. Esamina prima costruzione, tessuto, forma e decorazioni. Confronta normale piegatura, compressione delicata e sottovuoto, poi chiedi al magazzino di confermare il metodo adatto.
CSSBuy può spedire elettronica con batterie o liquidi?|||Dipende dal prodotto preciso, dalle caratteristiche della batteria o del liquido, dalla destinazione e dalle regole vigenti. Fornisci specifiche corrette e conferma una linea ammessa prima di includere l'articolo in un pacco misto.
Cosa controllo quando il tracking non si aggiorna?|||Identifica l'ultima fase confermata e il corriere, salva l'ultimo evento con data e ora e consulta le indicazioni della linea. Chiedi informazioni dal pacco interessato: l'assenza di scansioni da sola non prova lo smarrimento.
L'assicurazione copre ogni perdita, danno o problema doganale?|||Non presumere una copertura universale. Leggi la polizza attuale della linea, compresi valore assicurato, esclusioni, termini di segnalazione e prove. Conserva foto, fatture e documentazione dell'imballaggio richieste.
Come verifico coupon CSSBuy, punti e tassi di cambio?|||Controlla requisiti, scadenza, spesa minima, limiti e utilizzi consentiti del premio. Confronta pagamento finale e saldo accreditato separatamente dallo sconto pubblicizzato. Un coupon non determina il tasso di conversione.
Cosa faccio se un link prodotto non funziona più?|||Riapri l'inserzione originale e controlla identificativo, disponibilità e variante. Chiedi aiuto a CSSBuy se l'importazione fallisce. Non considerare identico un prodotto diverso raggiunto tramite un link sostitutivo senza verificarlo.
''')

add_faq('zh', '''
cssbuys.pro 是 CSSBuy 官方网站吗？|||不是。本站提供独立购买和运输指南，不接收订单、不保管账户余额、不拍摄仓库照片，也不安排发货。相关服务需要通过 CSSBuy 办理。
如何通过 CSSBuy 购买商品？|||先打开原始商品页面，核对卖家和所选款式，再将链接用于 CSSBuy 下单。付款前确认尺码、颜色、数量和当前费用。链接无法识别时，可以咨询 Expert Buy 人工代购选项。
为什么商品和国际运输需要分别付款？|||商品先完成购买并送到中国仓库，仓库检查和包裹准备完成后再安排国际运输。预算应覆盖这两个阶段，不能把商品标价直接当作最终送达价格。
CSSBuy 预算应该包括哪些费用？|||记录商品价格、中国国内运费、可能产生的服务费与支付手续费、货币兑换、可选仓库服务、国际运费及适用的目的地费用。把估算、已确认报价和已付金额分开。
本站提供 CSSBuy 实时运费报价吗？|||不提供。本站的工具和示例用于解释重量和费用的计算方法。查询可用线路和现行价格时，请在 CSSBuy 官方计算器中输入目的地、商品属性和包装后的尺寸重量。
为什么相同重量的两个包裹运费不同？|||包裹尺寸、内容、目的地或可选线路可能不同。体积较大的包裹也可能有更高的计费重量。比较时应使用相同输入条件，查看完整报价和每条线路的计费规则。
如何计算体积重？|||按照线路要求的单位，将包装后的长、宽、高相乘，再除以该线路注明的体积重除数。还要确认线路使用实际重量、体积重还是两者较大值，以及进位和计费档位。
CSSBuy 多久能送达？|||所有订单没有统一时效。卖家发货、仓库处理、包装、国际运输和末端派送是不同阶段。应参考所选线路的最新预计时效，并为可能的变化预留时间。
CSSBuy 官方介绍包含多少张免费 QC 照片？|||2026 年 11 月 4 日核查的官方首页介绍为 3–5 张免费 QC 照片。请确认具体订单包含哪些照片，并在申请额外角度或测量前查看对应服务选项。
为什么仓库显示重量，却没有 QC 照片？|||出现重量记录不能证明拍照任务已完成。先查看订单状态和已选服务，再在对应订单中咨询缺少的照片。影响验收的重要问题未解决前，不应直接批准国际发货。
补拍照片或视频检查多少钱？|||查看当前服务菜单，或向 CSSBuy 描述需要的具体角度和测量方式后询价。不能默认补拍照片、测量或视频免费，也不能假设每种商品都提供这些服务。
QC 照片能证明商品真伪或使用性能吗？|||不能。照片有助于检查收到的款式、可见状况、尺寸和配件，但无法证明所有材料、隐藏瑕疵、电池状态或长期使用性能。
仓库照片显示尺码错误或破损怎么办？|||保存订单详情和相关照片，客观描述可见的不符之处，并尽快通过对应订单联系 CSSBuy。拆除包装或批准国际发货前，先确认退货或换货的可行方案。
商品入库后有多久可以申请退货？|||CSSBuy 公开问答列出的条件包括卖家接受退货、商品入库不足七天，以及支付退货运费。请及时核查具体订单；这不是对所有商品无条件退货的承诺。
商品退货与提取账户余额是一回事吗？|||不是。商品退货涉及卖家和具体商品，余额提取涉及已经存入 CSSBuy 账户的资金。应使用相应申请入口，并将两类交易记录分别保存。
退款会自动退回银行卡或原付款渠道吗？|||不能直接假设。先确认该笔交易是退入 CSSBuy 余额，还是退回原支付方式。需要提取余额时，应在账户或客服处核对可用渠道、费用和处理说明。
为什么最终运费可能不同于预付金额？|||预付款根据估算信息计算，最终核实的尺寸、重量和线路条件可能改变结果。应将包裹账单与原估算逐项比较，并检查账户中的差额记录，不能默认是银行卡退款。
免费仓储期限有多久？|||官方商品说明区分普通商品 90 天和敏感商品 30 天。请以账户里具体商品的分类和到期日期核对，不要把一般介绍中的 90 天套用到所有商品。
可以延长仓储，或通过合包重新开始计时吗？|||应在显示的到期日前咨询延期，确认价格和适用订单。不能假设合包、新购买一件商品或向客服咨询，就会重新计算旧商品的仓储期限。
仓储已经到期的商品应该怎么办？|||立即提供订单号或包裹号联系 CSSBuy，询问商品是否仍在仓库，以及目前还有哪些处理方式。不能假设过期商品一定可以找回，也不能把过去的清仓公告当作新的宽限期。
是否应该把所有商品合成一个包裹？|||将合包方案与实际可行的分包方案比较，检查商品兼容性、包装尺寸、固定费用、保护要求和仓储期限。更大的合并包裹不一定是合适方案中最便宜的一个。
拆除鞋盒一定能降低运费吗？|||不一定。拆鞋盒可能减少体积，但最终效果取决于外箱尺寸、计费规则和包装服务费。申请前还要考虑鞋盒本身的用途，以及鞋子需要怎样保护。
所有衣物都适合真空包装吗？|||不适合。先检查衣物结构、面料、版型和装饰配件，再比较普通折叠、轻度压缩与真空包装，并请仓库确认适合的处理方式。
CSSBuy 可以寄带电池的电子产品或液体吗？|||是否可寄取决于具体商品、电池或液体属性、目的地和最新线路规则。应提供准确规格，确认存在合适的运输方式后，再将其加入混合包裹。
物流信息不更新时应该检查什么？|||确认最后一次已知运输阶段和承运商，保存扫描记录及时间，并查看所选线路的说明。咨询时使用对应包裹记录；单凭一段时间没有更新，不能认定包裹丢失。
包裹保险能覆盖所有丢失、破损或海关问题吗？|||不能默认全部覆盖。请查看所选线路的现行保单，核对保额、除外责任、报案期限和证据要求，并保存需要的照片、发票及包装记录。
如何核对 CSSBuy 优惠券、积分和汇率？|||检查适用资格、有效期、最低消费、优惠上限和奖励用途。把最终实付金额及到账余额与宣传折扣分别核对；优惠券不能代表货币兑换汇率。
商品链接打不开应该怎么办？|||重新打开卖家的原始商品页面，核对商品编号、库存和所选款式。若链接解析失败，可向 CSSBuy 咨询。替换链接指向不同商品时，应重新核对，不能直接视为同款。
''')

if __name__ == '__main__':
    expected = {'en', 'de', 'fr', 'es', 'it', 'zh'}
    assert len(catalog) == 22, len(catalog)
    assert all(set(v) == expected for v in catalog.values())
    assert set(faq) == expected
    assert all(len(v) == 28 for v in faq.values())
    for slug, langs in catalog.items():
        for locale, item in langs.items():
            assert 'CSSBuy' in item['title'], (slug, locale)
            assert len(item['description']) >= (40 if locale == 'zh' else 100)
    (HERE / 'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'faq.json').write_text(json.dumps(faq, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'catalog_slugs': len(catalog), 'catalog_variants': sum(len(v) for v in catalog.values()), 'faq_counts': {k: len(v) for k,v in faq.items()}}, ensure_ascii=False))
