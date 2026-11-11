export type EditorialGuide = {
  slug: string;
  title: string;
  summary: string;
  sections: Array<{ title: string; body: string }>;
};
export type EditorialContent = {
  faq: Array<{ q: string; a: string }>;
  guides: EditorialGuide[];
};

// Editorial text is authored locally; product facts and imagery remain source-fed.
export const editorial: Record<string, EditorialContent> = {
  "en": {
    "faq": [
      {
        "q": "What is the Hipobuy Spreadsheet?",
        "a": "An independent directory for finding and comparing marketplace listings before opening them on Hipobuy."
      },
      {
        "q": "Is this the official Hipobuy website?",
        "a": "No. This directory is independent. Hipobuy manages its own accounts, purchases, warehouse services and shipping."
      },
      {
        "q": "Where does product information come from?",
        "a": "Product names, images, prices and original links are read from the connected source catalogue. Always check the current seller listing."
      },
      {
        "q": "Can I place an order here?",
        "a": "No. Open the product on Hipobuy, check the details and complete any purchase there."
      },
      {
        "q": "How do I register with Hipobuy?",
        "a": "Use the official registration page at https://hipobuy.com/register. This directory does not create or manage accounts."
      },
      {
        "q": "What does the CNY price mean?",
        "a": "It is the amount shown by the source catalogue in Chinese yuan. A different style or size may cost more."
      },
      {
        "q": "How are currency prices calculated?",
        "a": "Prices are converted from CNY using the latest available daily reference rates from Frankfurter. The rate date is displayed on the product page. These are estimates, not a checkout quote; if rates are unavailable, the original CNY amount is shown."
      },
      {
        "q": "Does the displayed price include shipping?",
        "a": "Treat it as the item price. Confirm domestic delivery, international shipping, service charges and any taxes separately."
      },
      {
        "q": "Is every listed product in stock?",
        "a": "A directory entry does not guarantee availability. Check the selected style, size and stock on Hipobuy before paying."
      },
      {
        "q": "Where can I confirm sizes and styles?",
        "a": "Use the current seller information shown on Hipobuy. Do not infer a size or selected option from a gallery image."
      },
      {
        "q": "Are the gallery images QC photos?",
        "a": "Not necessarily. Source gallery images show the listing; they are not proof of the condition of your own order."
      },
      {
        "q": "Where should I check my order QC?",
        "a": "Review the photos associated with your own order in Hipobuy. Historical references, when available, are separate from your order."
      },
      {
        "q": "Why does a product have no QC gallery?",
        "a": "The source may not provide separately identified QC photos. Missing photos are not replaced with invented images."
      },
      {
        "q": "Can I copy the original marketplace link?",
        "a": "Use the copy-link control when an original link is available. The listing ID identifies the seller product, not a specific variant."
      },
      {
        "q": "Why are there different product numbers?",
        "a": "The directory record number and marketplace product ID can differ. Use the original marketplace ID when matching a purchase link."
      },
      {
        "q": "How does search work?",
        "a": "Search uses the connected catalogue. A product number may not be searchable if the source only indexes product names."
      },
      {
        "q": "Can I switch languages?",
        "a": "Yes. Navigation, guides, buttons and product-type descriptions follow the selected language. Brand names, model names and identifiers remain unchanged. You can expand the original listing title on the product page."
      },
      {
        "q": "What should I do if a product link fails?",
        "a": "Copy the original marketplace URL into Hipobuy search. If it still fails, check whether the seller listing is available."
      },
      {
        "q": "Can I calculate international shipping here?",
        "a": "This preview does not provide live shipping quotes. Use Hipobuy with your destination, parcel weight and dimensions."
      },
      {
        "q": "Who handles payments, returns and support?",
        "a": "Hipobuy and the seller handle their respective transactions and policies. Contact the relevant service about an actual order."
      }
    ],
    "guides": [
      {
        "slug": "how-to-buy",
        "title": "From a find to your first order",
        "summary": "Keep the original product identity and verify the details before paying.",
        "sections": [
          {
            "title": "Start with a shortlist",
            "body": "Browse a category or search for an item, then open its product page. Compare the source gallery, recorded price and original marketplace link. Keep the full link with the listing ID: a catalogue record number may be different from the seller’s product number. A photo alone does not identify a particular size, colour or style."
          },
          {
            "title": "Check the live listing",
            "body": "Open the Hipobuy product link, or paste the original marketplace URL into Hipobuy search. Register through hipobuy.com/register if you need an account. Confirm that the title, images and seller match your shortlist. Check the chosen variant, measurements, stock and current item price before proceeding. The directory’s USD estimate is not a checkout quote."
          },
          {
            "title": "Review each stage",
            "body": "Complete any purchase on Hipobuy. Read the current charges and applicable return conditions there. When your order reaches the warehouse, inspect the photos for that specific order and ask for clarification if needed. Plan international shipping after you know the parcel details; the item price alone is not the full delivered cost."
          }
        ]
      },
      {
        "slug": "check-product-photos",
        "title": "Read the photos before you decide",
        "summary": "Separate seller gallery images from evidence about your own order.",
        "sections": [
          {
            "title": "Know what the image shows",
            "body": "The product gallery displays images supplied by the connected catalogue. These may be seller photographs or other listing references. Unless an image is explicitly identified as a QC reference, do not treat it as warehouse QC. Even a historical QC image belongs to another purchase and cannot establish the condition of your own item."
          },
          {
            "title": "Look for useful details",
            "body": "Compare front, back and detail views where available. Check seams, closures, materials visible in the photo and the stated measurements. Keep the selected colour and style beside the image you are reviewing. Lighting, perspective and screens can change the appearance of colours. Missing angles or measurements should remain unanswered questions, not assumptions."
          },
          {
            "title": "Check your own order",
            "body": "After purchasing, use the order-specific photos in Hipobuy to confirm that the delivered item matches your selection. If a detail is unclear, request the information you need before making a shipping decision. Neither directory images nor visual comparisons certify authenticity, quality, fit or durability. Read the current return rules while you still have time to act."
          }
        ]
      },
      {
        "slug": "plan-shipping",
        "title": "Plan the parcel, not just the item",
        "summary": "Build a complete picture of costs using the actual parcel details.",
        "sections": [
          {
            "title": "Separate the costs",
            "body": "A catalogue price is a starting point for the item. Check domestic seller delivery, any purchasing or optional service charges, international shipping and applicable destination taxes separately. Keep your own budget in your preferred currency. Prices are converted from CNY using the latest available daily reference rates from Frankfurter. The rate date is displayed on the product page. These are estimates, not a checkout quote; if rates are unavailable, the original CNY amount is shown."
          },
          {
            "title": "Use the right parcel information",
            "body": "When getting an estimate from Hipobuy, enter the destination and accurate parcel details. A route may use actual weight or volumetric weight, depending on its rules. Product weight does not always equal packed parcel weight. Packaging, dimensions and the combination of items can change the quote; verify the current route conditions before choosing."
          },
          {
            "title": "Confirm before dispatch",
            "body": "Review the QC photos for your own order, then check the items included in the parcel. Compare the available shipping services, restrictions, tracking and any optional protection shown by Hipobuy. This preview does not promise a delivery date or calculate a live shipping charge. Save the quote and order information so you can follow the shipment with the service handling it."
          }
        ]
      }
    ]
  },
  "de": {
    "faq": [
      {
        "q": "Was ist das Hipobuy Spreadsheet?",
        "a": "Ein unabhängiges Verzeichnis zum Finden und Vergleichen von Marktplatzangeboten, bevor du sie bei Hipobuy öffnest."
      },
      {
        "q": "Ist dies die offizielle Hipobuy-Website?",
        "a": "Nein. Dieses Verzeichnis ist unabhängig. Hipobuy verwaltet seine Konten, Einkäufe, Lagerleistungen und den Versand selbst."
      },
      {
        "q": "Woher stammen die Produktinformationen?",
        "a": "Namen, Bilder, Preise und Originallinks werden aus dem angebundenen Katalog gelesen. Prüfe immer das aktuelle Verkäuferangebot."
      },
      {
        "q": "Kann ich hier bestellen?",
        "a": "Nein. Öffne das Produkt bei Hipobuy, prüfe die Angaben und schließe einen Kauf dort ab."
      },
      {
        "q": "Wie registriere ich mich bei Hipobuy?",
        "a": "Nutze https://hipobuy.com/register. Dieses Verzeichnis erstellt oder verwaltet keine Konten."
      },
      {
        "q": "Was bedeutet der CNY-Preis?",
        "a": "Das ist der im Quellkatalog angegebene Betrag in chinesischen Yuan. Andere Ausführungen oder Größen können mehr kosten."
      },
      {
        "q": "Wie werden Fremdwährungspreise berechnet?",
        "a": "Preise werden aus CNY mit den neuesten verfügbaren täglichen Referenzkursen von Frankfurter umgerechnet. Das Kursdatum steht auf der Produktseite. Die Werte sind Schätzungen, keine verbindlichen Kassenbeträge. Ohne Kursdaten wird der Originalbetrag in CNY angezeigt."
      },
      {
        "q": "Ist der Versand im Preis enthalten?",
        "a": "Betrachte ihn als Artikelpreis. Prüfe Inlandsversand, internationalen Versand, Servicegebühren und mögliche Steuern separat."
      },
      {
        "q": "Sind alle gelisteten Produkte verfügbar?",
        "a": "Ein Katalogeintrag garantiert keine Verfügbarkeit. Prüfe Ausführung, Größe und Bestand bei Hipobuy vor der Zahlung."
      },
      {
        "q": "Wo bestätige ich Größen und Ausführungen?",
        "a": "Nutze die aktuellen Verkäuferangaben bei Hipobuy. Leite Größe oder gewählte Variante nicht allein aus einem Galeriebild ab."
      },
      {
        "q": "Sind die Galeriebilder QC-Fotos?",
        "a": "Nicht unbedingt. Die Quellgalerie zeigt das Angebot und belegt nicht den Zustand deiner eigenen Bestellung."
      },
      {
        "q": "Wo prüfe ich die QC meiner Bestellung?",
        "a": "Prüfe die Fotos zu deiner eigenen Bestellung bei Hipobuy. Historische Referenzen betreffen andere Bestellungen."
      },
      {
        "q": "Warum fehlt eine QC-Galerie?",
        "a": "Die Quelle stellt möglicherweise keine gesondert gekennzeichneten QC-Fotos bereit. Fehlende Fotos werden nicht durch erfundene Bilder ersetzt."
      },
      {
        "q": "Kann ich den ursprünglichen Marktplatzlink kopieren?",
        "a": "Nutze die Kopierfunktion, wenn ein Originallink vorhanden ist. Die Angebots-ID bezeichnet den Verkäuferartikel, keine bestimmte Variante."
      },
      {
        "q": "Warum gibt es verschiedene Produktnummern?",
        "a": "Katalognummer und Marktplatz-ID können unterschiedlich sein. Verwende beim Abgleich eines Kauflinks die ursprüngliche Marktplatz-ID."
      },
      {
        "q": "Wie funktioniert die Suche?",
        "a": "Die Suche nutzt den angebundenen Katalog. Produktnummern sind eventuell nicht suchbar, wenn die Quelle nur Produktnamen durchsucht."
      },
      {
        "q": "Kann ich die Sprache wechseln?",
        "a": "Ja. Navigation, Ratgeber, Schaltflächen und Produktarten folgen der gewählten Sprache. Marken, Modelle und Kennungen bleiben unverändert. Der Originaltitel lässt sich auf der Produktseite aufklappen."
      },
      {
        "q": "Was mache ich bei einem fehlerhaften Produktlink?",
        "a": "Füge die ursprüngliche Marktplatz-URL in die Hipobuy-Suche ein. Prüfe bei weiteren Problemen, ob das Verkäuferangebot noch verfügbar ist."
      },
      {
        "q": "Kann ich hier internationalen Versand berechnen?",
        "a": "Diese Vorschau liefert keine aktuellen Versandangebote. Nutze Hipobuy mit Zielland, Paketgewicht und Abmessungen."
      },
      {
        "q": "Wer bearbeitet Zahlungen, Rückgaben und Support?",
        "a": "Hipobuy und der Verkäufer sind für ihre jeweiligen Transaktionen und Bedingungen zuständig. Wende dich bei Bestellungen an den zuständigen Dienst."
      }
    ],
    "guides": [
      {
        "slug": "how-to-buy",
        "title": "Vom Fund zur ersten Bestellung",
        "summary": "Bewahre den Originallink auf und prüfe die Details vor der Zahlung.",
        "sections": [
          {
            "title": "Eine Auswahl zusammenstellen",
            "body": "Durchsuche eine Kategorie oder suche nach einem Artikel und öffne seine Produktseite. Vergleiche Quellgalerie, erfassten Preis und ursprünglichen Marktplatzlink. Bewahre den vollständigen Link mit Angebots-ID auf: Die Katalognummer kann von der Produktnummer des Verkäufers abweichen. Ein Foto allein legt Größe, Farbe oder Ausführung nicht fest."
          },
          {
            "title": "Das aktuelle Angebot prüfen",
            "body": "Öffne den Hipobuy-Produktlink oder füge die ursprüngliche Marktplatz-URL in die Hipobuy-Suche ein. Falls du ein Konto brauchst, registriere dich über hipobuy.com/register. Vergleiche Titel, Bilder und Verkäufer mit deiner Auswahl. Prüfe Variante, Maße, Bestand und aktuellen Artikelpreis. Die USD-Schätzung des Verzeichnisses ist kein verbindlicher Kassenbetrag."
          },
          {
            "title": "Jeden Schritt kontrollieren",
            "body": "Schließe einen Kauf bei Hipobuy ab und lies dort die aktuellen Gebühren und Rückgabebedingungen. Prüfe nach Ankunft im Lager die Fotos genau dieser Bestellung und frage bei Unklarheiten nach. Plane den internationalen Versand erst mit den tatsächlichen Paketangaben. Der Artikelpreis allein entspricht nicht den gesamten Kosten bis zur Zustellung."
          }
        ]
      },
      {
        "slug": "check-product-photos",
        "title": "Fotos vor der Entscheidung prüfen",
        "summary": "Unterscheide Angebotsbilder von Nachweisen zu deiner eigenen Bestellung.",
        "sections": [
          {
            "title": "Die Bildquelle verstehen",
            "body": "Die Produktgalerie zeigt Bilder aus dem angebundenen Katalog. Das können Verkäuferfotos oder andere Angebotsreferenzen sein. Behandle ein Bild nur dann als QC-Referenz, wenn es ausdrücklich so gekennzeichnet ist. Auch historische QC-Bilder gehören zu einem anderen Kauf und belegen nicht den Zustand deines Artikels."
          },
          {
            "title": "Auf hilfreiche Details achten",
            "body": "Vergleiche Vorder-, Rück- und Detailansichten, soweit vorhanden. Prüfe Nähte, Verschlüsse, sichtbare Materialien und angegebene Maße. Halte die gewählte Farbe und Ausführung beim Vergleich fest. Licht, Perspektive und Bildschirm können Farben verändern. Fehlende Blickwinkel oder Maße bleiben offene Fragen und sollten nicht durch Annahmen ersetzt werden."
          },
          {
            "title": "Die eigene Bestellung prüfen",
            "body": "Kontrolliere nach dem Kauf die bestellbezogenen Fotos bei Hipobuy und vergleiche den gelieferten Artikel mit deiner Auswahl. Fordere unklare Angaben vor der Versandentscheidung an. Verzeichnisbilder und visuelle Vergleiche bestätigen weder Echtheit noch Qualität, Passform oder Haltbarkeit. Lies rechtzeitig die aktuellen Rückgabebedingungen."
          }
        ]
      },
      {
        "slug": "plan-shipping",
        "title": "Das Paket planen, nicht nur den Artikel",
        "summary": "Berücksichtige die vollständigen Kosten anhand der tatsächlichen Paketdaten.",
        "sections": [
          {
            "title": "Kosten getrennt betrachten",
            "body": "Der Katalogpreis ist ein Ausgangspunkt für den Artikel. Prüfe Inlandsversand, Einkaufs- oder Zusatzleistungen, internationalen Versand und mögliche Zielortsteuern separat. Führe dein Budget in deiner bevorzugten Währung. Preise werden aus CNY mit den neuesten verfügbaren täglichen Referenzkursen von Frankfurter umgerechnet. Das Kursdatum steht auf der Produktseite. Die Werte sind Schätzungen, keine verbindlichen Kassenbeträge. Ohne Kursdaten wird der Originalbetrag in CNY angezeigt."
          },
          {
            "title": "Die richtigen Paketdaten verwenden",
            "body": "Gib bei einer Hipobuy-Schätzung das Ziel und genaue Paketdaten an. Je nach Versandbedingungen zählt tatsächliches Gewicht oder Volumengewicht. Artikelgewicht und verpacktes Paketgewicht sind nicht immer gleich. Verpackung, Maße und die Zusammenstellung der Artikel können den Preis ändern. Prüfe vor der Auswahl die aktuellen Bedingungen der Versandlinie."
          },
          {
            "title": "Vor dem Versand bestätigen",
            "body": "Prüfe die QC-Fotos deiner Bestellung und die im Paket enthaltenen Artikel. Vergleiche verfügbare Versanddienste, Einschränkungen, Sendungsverfolgung und optionalen Schutz bei Hipobuy. Diese Vorschau verspricht keinen Liefertermin und berechnet keine aktuellen Versandkosten. Bewahre Angebot und Bestelldaten auf, damit du die Sendung beim zuständigen Dienst verfolgen kannst."
          }
        ]
      }
    ]
  },
  "fr": {
    "faq": [
      {
        "q": "Qu’est-ce que le Hipobuy Spreadsheet ?",
        "a": "Un annuaire indépendant pour trouver et comparer des annonces de places de marché avant de les ouvrir sur Hipobuy."
      },
      {
        "q": "Est-ce le site officiel de Hipobuy ?",
        "a": "Non. Cet annuaire est indépendant. Hipobuy gère ses propres comptes, achats, services d’entrepôt et expéditions."
      },
      {
        "q": "D’où viennent les informations produit ?",
        "a": "Les noms, images, prix et liens d’origine sont lus dans le catalogue connecté. Vérifiez toujours l’annonce actuelle du vendeur."
      },
      {
        "q": "Puis-je commander ici ?",
        "a": "Non. Ouvrez le produit sur Hipobuy, vérifiez les détails et effectuez tout achat sur cette plateforme."
      },
      {
        "q": "Comment créer un compte Hipobuy ?",
        "a": "Utilisez https://hipobuy.com/register. Cet annuaire ne crée ni ne gère de comptes."
      },
      {
        "q": "Que signifie le prix en CNY ?",
        "a": "Il s’agit du montant indiqué par le catalogue source en yuans chinois. Une autre taille ou variante peut coûter davantage."
      },
      {
        "q": "Comment les prix sont-ils convertis ?",
        "a": "Les prix en CNY sont convertis au dernier taux de référence quotidien disponible de Frankfurter. La date figure sur la fiche. Il s’agit d’estimations et non de devis de paiement. En cas d’indisponibilité, le prix original en CNY est affiché."
      },
      {
        "q": "Le prix affiché comprend-il la livraison ?",
        "a": "Considérez-le comme le prix de l’article. Vérifiez séparément livraison intérieure, transport international, frais de service et taxes éventuelles."
      },
      {
        "q": "Tous les produits sont-ils en stock ?",
        "a": "Une entrée dans l’annuaire ne garantit pas la disponibilité. Vérifiez variante, taille et stock sur Hipobuy avant de payer."
      },
      {
        "q": "Où confirmer les tailles et variantes ?",
        "a": "Consultez les informations actuelles du vendeur sur Hipobuy. Une photo seule ne confirme pas la taille ou l’option choisie."
      },
      {
        "q": "Les images de la galerie sont-elles des photos QC ?",
        "a": "Pas nécessairement. Elles présentent l’annonce et ne prouvent pas l’état de votre propre commande."
      },
      {
        "q": "Où vérifier le QC de ma commande ?",
        "a": "Examinez les photos associées à votre commande dans Hipobuy. Les références historiques éventuelles concernent d’autres achats."
      },
      {
        "q": "Pourquoi une galerie QC manque-t-elle ?",
        "a": "La source peut ne pas fournir de photos QC identifiées séparément. Les photos absentes ne sont pas remplacées par des images inventées."
      },
      {
        "q": "Puis-je copier le lien de la place de marché ?",
        "a": "Utilisez la commande de copie lorsqu’un lien d’origine est disponible. L’identifiant désigne le produit du vendeur, pas une variante précise."
      },
      {
        "q": "Pourquoi existe-t-il plusieurs numéros produit ?",
        "a": "Le numéro de l’annuaire peut différer de l’identifiant de la place de marché. Utilisez ce dernier pour vérifier un lien d’achat."
      },
      {
        "q": "Comment fonctionne la recherche ?",
        "a": "Elle interroge le catalogue connecté. Les numéros peuvent être introuvables si la source indexe uniquement les noms de produits."
      },
      {
        "q": "Puis-je changer de langue ?",
        "a": "Oui. Navigation, guides, boutons et types de produits suivent la langue choisie. Marques, modèles et identifiants restent inchangés. Le titre original peut être déplié sur la fiche."
      },
      {
        "q": "Que faire si un lien produit ne fonctionne pas ?",
        "a": "Collez l’URL d’origine dans la recherche Hipobuy. Si elle échoue encore, vérifiez que l’annonce du vendeur existe toujours."
      },
      {
        "q": "Puis-je calculer la livraison internationale ici ?",
        "a": "Cet aperçu ne fournit pas de devis de transport en direct. Utilisez Hipobuy avec la destination, le poids et les dimensions du colis."
      },
      {
        "q": "Qui gère paiements, retours et assistance ?",
        "a": "Hipobuy et le vendeur gèrent leurs transactions et conditions respectives. Contactez le service concerné pour une commande réelle."
      }
    ],
    "guides": [
      {
        "slug": "how-to-buy",
        "title": "De la découverte à la première commande",
        "summary": "Conservez le lien d’origine et vérifiez les détails avant de payer.",
        "sections": [
          {
            "title": "Préparer une sélection",
            "body": "Parcourez une catégorie ou recherchez un article, puis ouvrez sa fiche. Comparez la galerie source, le prix enregistré et le lien de la place de marché. Conservez le lien complet avec l’identifiant de l’annonce : le numéro du catalogue peut différer du numéro produit du vendeur. Une photo seule ne détermine pas une taille, une couleur ou une variante."
          },
          {
            "title": "Vérifier l’annonce actuelle",
            "body": "Ouvrez le lien produit Hipobuy ou collez l’URL d’origine dans la recherche Hipobuy. Inscrivez-vous sur hipobuy.com/register si nécessaire. Vérifiez que titre, images et vendeur correspondent à votre sélection. Confirmez la variante, les mesures, le stock et le prix actuel avant de continuer. L’estimation en USD de l’annuaire n’est pas un devis de paiement."
          },
          {
            "title": "Contrôler chaque étape",
            "body": "Effectuez tout achat sur Hipobuy et consultez les frais et conditions de retour en vigueur. À l’arrivée en entrepôt, examinez les photos de cette commande précise et demandez des explications si nécessaire. Planifiez le transport international une fois les caractéristiques du colis connues. Le prix de l’article ne représente pas à lui seul le coût total livré."
          }
        ]
      },
      {
        "slug": "check-product-photos",
        "title": "Examiner les photos avant de décider",
        "summary": "Distinguez les images de l’annonce des preuves concernant votre commande.",
        "sections": [
          {
            "title": "Identifier ce que montre l’image",
            "body": "La galerie présente les images du catalogue connecté. Il peut s’agir de photos du vendeur ou d’autres références de l’annonce. Sans identification explicite, ne les considérez pas comme du QC d’entrepôt. Même une photo QC historique concerne un autre achat et ne prouve pas l’état de votre propre article."
          },
          {
            "title": "Chercher les détails utiles",
            "body": "Comparez les vues de face, de dos et les détails disponibles. Examinez coutures, fermetures, matières visibles et mesures indiquées. Gardez la couleur et la variante choisies à côté de l’image étudiée. Éclairage, perspective et écrans peuvent modifier les couleurs. Des angles ou mesures manquants doivent rester des questions à résoudre."
          },
          {
            "title": "Contrôler votre propre commande",
            "body": "Après l’achat, utilisez les photos propres à la commande sur Hipobuy pour confirmer que l’article reçu correspond à votre choix. Demandez les informations manquantes avant de décider l’expédition. Les images et comparaisons visuelles ne certifient ni authenticité, ni qualité, ni taille, ni durabilité. Consultez les règles de retour tant qu’il est encore possible d’agir."
          }
        ]
      },
      {
        "slug": "plan-shipping",
        "title": "Préparer le colis, pas seulement l’article",
        "summary": "Évaluez le coût complet à partir des caractéristiques réelles du colis.",
        "sections": [
          {
            "title": "Distinguer les coûts",
            "body": "Le prix du catalogue est un point de départ pour l’article. Vérifiez séparément livraison intérieure, frais d’achat ou options, transport international et taxes applicables à destination. Tenez votre budget dans votre monnaie préférée. Les prix en CNY sont convertis au dernier taux de référence quotidien disponible de Frankfurter. La date figure sur la fiche. Il s’agit d’estimations et non de devis de paiement. En cas d’indisponibilité, le prix original en CNY est affiché."
          },
          {
            "title": "Utiliser les bonnes données",
            "body": "Pour une estimation Hipobuy, indiquez la destination et les caractéristiques exactes du colis. Selon ses règles, une ligne peut facturer le poids réel ou volumétrique. Le poids du produit n’est pas toujours celui du colis emballé. Emballage, dimensions et regroupement d’articles peuvent modifier le devis : vérifiez les conditions actuelles avant de choisir."
          },
          {
            "title": "Confirmer avant l’expédition",
            "body": "Examinez le QC de votre commande puis vérifiez les articles inclus dans le colis. Comparez les services disponibles, restrictions, suivi et protections facultatives proposés par Hipobuy. Cet aperçu ne promet aucun délai et ne calcule pas de tarif en direct. Conservez devis et informations de commande pour suivre l’envoi auprès du service responsable."
          }
        ]
      }
    ]
  },
  "es": {
    "faq": [
      {
        "q": "¿Qué es Hipobuy Spreadsheet?",
        "a": "Un directorio independiente para encontrar y comparar anuncios de mercados antes de abrirlos en Hipobuy."
      },
      {
        "q": "¿Es la web oficial de Hipobuy?",
        "a": "No. Este directorio es independiente. Hipobuy gestiona sus propias cuentas, compras, servicios de almacén y envíos."
      },
      {
        "q": "¿De dónde sale la información de los productos?",
        "a": "Los nombres, imágenes, precios y enlaces originales se leen del catálogo conectado. Comprueba siempre el anuncio actual del vendedor."
      },
      {
        "q": "¿Puedo hacer un pedido aquí?",
        "a": "No. Abre el producto en Hipobuy, revisa los detalles y realiza cualquier compra allí."
      },
      {
        "q": "¿Cómo me registro en Hipobuy?",
        "a": "Utiliza https://hipobuy.com/register. Este directorio no crea ni administra cuentas."
      },
      {
        "q": "¿Qué significa el precio en CNY?",
        "a": "Es el importe indicado por el catálogo de origen en yuanes chinos. Otra talla o variante puede tener un precio distinto."
      },
      {
        "q": "¿Cómo se calculan los precios en otras monedas?",
        "a": "Los precios en CNY se convierten con los últimos tipos de referencia diarios disponibles de Frankfurter. La fecha aparece en la ficha. Son estimaciones, no importes definitivos. Si no hay datos, se muestra el precio original en CNY."
      },
      {
        "q": "¿El precio incluye el envío?",
        "a": "Considéralo el precio del artículo. Comprueba por separado envío nacional, transporte internacional, comisiones y posibles impuestos."
      },
      {
        "q": "¿Todos los productos están disponibles?",
        "a": "Un registro del directorio no garantiza existencias. Revisa variante, talla y disponibilidad en Hipobuy antes de pagar."
      },
      {
        "q": "¿Dónde confirmo tallas y variantes?",
        "a": "Consulta los datos actuales del vendedor en Hipobuy. No deduzcas la talla o la opción elegida solo a partir de una foto."
      },
      {
        "q": "¿Las imágenes de la galería son fotos QC?",
        "a": "No necesariamente. La galería muestra el anuncio y no acredita el estado de tu propio pedido."
      },
      {
        "q": "¿Dónde reviso el QC de mi pedido?",
        "a": "Consulta las fotos asociadas a tu pedido en Hipobuy. Las referencias históricas, cuando existen, pertenecen a otras compras."
      },
      {
        "q": "¿Por qué falta una galería QC?",
        "a": "La fuente puede no ofrecer fotos QC identificadas por separado. Las fotos ausentes no se sustituyen por imágenes inventadas."
      },
      {
        "q": "¿Puedo copiar el enlace original del mercado?",
        "a": "Usa el botón de copiar cuando exista un enlace original. El ID identifica el producto del vendedor, no una variante concreta."
      },
      {
        "q": "¿Por qué hay distintos números de producto?",
        "a": "El número del directorio puede diferir del ID del mercado. Usa el ID original del mercado al comprobar un enlace de compra."
      },
      {
        "q": "¿Cómo funciona la búsqueda?",
        "a": "Consulta el catálogo conectado. Puede que los números no sean buscables si la fuente solo indexa nombres de productos."
      },
      {
        "q": "¿Puedo cambiar el idioma?",
        "a": "Sí. La navegación, las guías, los botones y los tipos de producto siguen el idioma elegido. Las marcas, modelos e identificadores se conservan. Puedes desplegar el título original en la ficha."
      },
      {
        "q": "¿Qué hago si falla un enlace de producto?",
        "a": "Pega la URL original en la búsqueda de Hipobuy. Si sigue fallando, comprueba que el anuncio del vendedor esté disponible."
      },
      {
        "q": "¿Puedo calcular aquí el envío internacional?",
        "a": "Esta vista previa no ofrece tarifas de envío en directo. Usa Hipobuy con destino, peso y dimensiones del paquete."
      },
      {
        "q": "¿Quién gestiona pagos, devoluciones y soporte?",
        "a": "Hipobuy y el vendedor gestionan sus respectivas transacciones y condiciones. Contacta con el servicio correspondiente para un pedido real."
      }
    ],
    "guides": [
      {
        "slug": "how-to-buy",
        "title": "De un descubrimiento al primer pedido",
        "summary": "Conserva el enlace original y verifica los detalles antes de pagar.",
        "sections": [
          {
            "title": "Prepara una selección",
            "body": "Explora una categoría o busca un artículo y abre su ficha. Compara la galería de origen, el precio registrado y el enlace original del mercado. Conserva el enlace completo con el ID del anuncio: el número del catálogo puede diferir del número del vendedor. Una fotografía por sí sola no identifica una talla, un color o una variante concreta."
          },
          {
            "title": "Comprueba el anuncio actual",
            "body": "Abre el enlace de Hipobuy o pega la URL original en su buscador. Regístrate en hipobuy.com/register si necesitas una cuenta. Confirma que título, imágenes y vendedor coinciden con tu selección. Revisa variante, medidas, existencias y precio actual antes de continuar. La estimación en USD del directorio no es una cotización de pago."
          },
          {
            "title": "Revisa cada etapa",
            "body": "Realiza cualquier compra en Hipobuy y lee allí las comisiones y condiciones de devolución vigentes. Cuando el pedido llegue al almacén, revisa las fotos de ese pedido concreto y pide aclaraciones si hace falta. Planifica el envío internacional cuando conozcas las características del paquete. El precio del artículo no equivale al coste total entregado."
          }
        ]
      },
      {
        "slug": "check-product-photos",
        "title": "Revisa las fotos antes de decidir",
        "summary": "Separa las imágenes del anuncio de las pruebas sobre tu propio pedido.",
        "sections": [
          {
            "title": "Identifica qué muestra la imagen",
            "body": "La galería presenta imágenes suministradas por el catálogo conectado. Pueden ser fotos del vendedor u otras referencias del anuncio. No las trates como QC del almacén salvo que estén identificadas expresamente. Incluso una foto QC histórica corresponde a otra compra y no demuestra el estado de tu artículo."
          },
          {
            "title": "Busca detalles útiles",
            "body": "Compara las vistas frontal, trasera y de detalle que existan. Examina costuras, cierres, materiales visibles y medidas indicadas. Mantén a mano el color y la variante elegidos. La iluminación, la perspectiva y las pantallas pueden cambiar la apariencia del color. Los ángulos o medidas ausentes deben seguir siendo dudas por resolver."
          },
          {
            "title": "Comprueba tu propio pedido",
            "body": "Después de comprar, usa las fotos específicas de tu pedido en Hipobuy para comprobar que el artículo recibido coincide con lo seleccionado. Pide la información que falte antes de decidir el envío. Las imágenes y comparaciones visuales no certifican autenticidad, calidad, ajuste ni durabilidad. Consulta las reglas de devolución mientras aún puedas actuar."
          }
        ]
      },
      {
        "slug": "plan-shipping",
        "title": "Planifica el paquete, no solo el artículo",
        "summary": "Calcula el presupuesto completo con las características reales del paquete.",
        "sections": [
          {
            "title": "Separa los costes",
            "body": "El precio del catálogo es un punto de partida para el artículo. Comprueba por separado envío nacional, servicios de compra u opciones, transporte internacional e impuestos aplicables en destino. Lleva tu presupuesto en tu moneda preferida. Los precios en CNY se convierten con los últimos tipos de referencia diarios disponibles de Frankfurter. La fecha aparece en la ficha. Son estimaciones, no importes definitivos. Si no hay datos, se muestra el precio original en CNY."
          },
          {
            "title": "Usa los datos correctos",
            "body": "Al pedir una estimación en Hipobuy, introduce destino y datos precisos del paquete. Según sus normas, una ruta puede usar peso real o volumétrico. El peso del producto no siempre es el del paquete preparado. Embalaje, dimensiones y combinación de artículos pueden cambiar el presupuesto. Revisa las condiciones actuales antes de elegir."
          },
          {
            "title": "Confirma antes de enviar",
            "body": "Revisa el QC de tu pedido y comprueba qué artículos contiene el paquete. Compara servicios disponibles, restricciones, seguimiento y protección opcional mostrados en Hipobuy. Esta vista previa no promete fechas de entrega ni calcula tarifas en directo. Conserva el presupuesto y los datos del pedido para seguir el envío con el servicio responsable."
          }
        ]
      }
    ]
  },
  "it": {
    "faq": [
      {
        "q": "Che cos’è Hipobuy Spreadsheet?",
        "a": "Una directory indipendente per trovare e confrontare annunci dei marketplace prima di aprirli su Hipobuy."
      },
      {
        "q": "È il sito ufficiale di Hipobuy?",
        "a": "No. La directory è indipendente. Hipobuy gestisce i propri account, acquisti, servizi di magazzino e spedizioni."
      },
      {
        "q": "Da dove arrivano le informazioni sui prodotti?",
        "a": "Nomi, immagini, prezzi e link originali vengono letti dal catalogo collegato. Controlla sempre l’annuncio attuale del venditore."
      },
      {
        "q": "Posso ordinare qui?",
        "a": "No. Apri il prodotto su Hipobuy, verifica i dettagli e completa eventuali acquisti sulla piattaforma."
      },
      {
        "q": "Come mi registro su Hipobuy?",
        "a": "Usa https://hipobuy.com/register. Questa directory non crea né gestisce account."
      },
      {
        "q": "Cosa indica il prezzo in CNY?",
        "a": "È l’importo indicato dal catalogo di origine in yuan cinesi. Un’altra taglia o variante può costare diversamente."
      },
      {
        "q": "Come vengono convertiti i prezzi?",
        "a": "I prezzi in CNY sono convertiti con gli ultimi tassi di riferimento giornalieri disponibili di Frankfurter. La data è indicata nella scheda. Sono stime, non preventivi di pagamento. Senza dati viene mostrato il prezzo originale in CNY."
      },
      {
        "q": "Il prezzo include la spedizione?",
        "a": "Consideralo il prezzo dell’articolo. Verifica separatamente consegna nazionale, spedizione internazionale, commissioni ed eventuali imposte."
      },
      {
        "q": "Tutti i prodotti sono disponibili?",
        "a": "Una voce nella directory non garantisce disponibilità. Controlla variante, taglia e scorte su Hipobuy prima di pagare."
      },
      {
        "q": "Dove confermo taglie e varianti?",
        "a": "Consulta i dati aggiornati del venditore su Hipobuy. Non dedurre taglia o opzione selezionata soltanto da una foto."
      },
      {
        "q": "Le immagini della galleria sono foto QC?",
        "a": "Non necessariamente. La galleria mostra l’annuncio e non dimostra le condizioni del tuo ordine."
      },
      {
        "q": "Dove controllo il QC del mio ordine?",
        "a": "Esamina le foto associate al tuo ordine su Hipobuy. Eventuali riferimenti storici riguardano altri acquisti."
      },
      {
        "q": "Perché manca una galleria QC?",
        "a": "La fonte potrebbe non fornire foto QC identificate separatamente. Le foto mancanti non vengono sostituite con immagini inventate."
      },
      {
        "q": "Posso copiare il link originale del marketplace?",
        "a": "Usa il comando di copia quando è disponibile un link originale. L’ID identifica il prodotto del venditore, non una variante specifica."
      },
      {
        "q": "Perché esistono numeri prodotto diversi?",
        "a": "Il numero della directory può differire dall’ID del marketplace. Usa l’ID originale del marketplace per verificare un link d’acquisto."
      },
      {
        "q": "Come funziona la ricerca?",
        "a": "Interroga il catalogo collegato. I numeri potrebbero non essere ricercabili se la fonte indicizza solo i nomi dei prodotti."
      },
      {
        "q": "Posso cambiare lingua?",
        "a": "Sì. Navigazione, guide, pulsanti e tipi di prodotto seguono la lingua scelta. Marchi, modelli e identificativi restano invariati. Puoi espandere il titolo originale nella scheda."
      },
      {
        "q": "Cosa faccio se un link prodotto non funziona?",
        "a": "Incolla l’URL originale nella ricerca Hipobuy. Se non funziona ancora, controlla che l’annuncio del venditore sia disponibile."
      },
      {
        "q": "Posso calcolare qui la spedizione internazionale?",
        "a": "Questa anteprima non offre preventivi di spedizione in tempo reale. Usa Hipobuy con destinazione, peso e dimensioni del pacco."
      },
      {
        "q": "Chi gestisce pagamenti, resi e assistenza?",
        "a": "Hipobuy e il venditore gestiscono le rispettive transazioni e condizioni. Per un ordine, contatta il servizio competente."
      }
    ],
    "guides": [
      {
        "slug": "how-to-buy",
        "title": "Da una scoperta al primo ordine",
        "summary": "Conserva il link originale e controlla i dettagli prima di pagare.",
        "sections": [
          {
            "title": "Prepara una selezione",
            "body": "Esplora una categoria o cerca un articolo, poi apri la scheda prodotto. Confronta galleria di origine, prezzo registrato e link originale del marketplace. Conserva il link completo con l’ID dell’annuncio: il numero del catalogo può differire dal numero prodotto del venditore. Una foto da sola non identifica una taglia, un colore o una variante specifica."
          },
          {
            "title": "Controlla l’annuncio attuale",
            "body": "Apri il link Hipobuy oppure incolla l’URL originale nella ricerca Hipobuy. Registrati su hipobuy.com/register se ti serve un account. Verifica che titolo, immagini e venditore corrispondano alla tua scelta. Controlla variante, misure, disponibilità e prezzo attuale prima di proseguire. La stima in USD della directory non è un preventivo di pagamento."
          },
          {
            "title": "Verifica ogni fase",
            "body": "Completa eventuali acquisti su Hipobuy e leggi commissioni e condizioni di reso vigenti. All’arrivo in magazzino, controlla le foto di quello specifico ordine e chiedi chiarimenti se necessario. Pianifica la spedizione internazionale quando conosci i dati del pacco. Il prezzo dell’articolo non rappresenta da solo il costo totale consegnato."
          }
        ]
      },
      {
        "slug": "check-product-photos",
        "title": "Guarda le foto prima di decidere",
        "summary": "Distingui le immagini dell’annuncio dalle prove relative al tuo ordine.",
        "sections": [
          {
            "title": "Comprendi cosa mostra l’immagine",
            "body": "La galleria presenta immagini fornite dal catalogo collegato. Possono essere fotografie del venditore o altri riferimenti dell’annuncio. Non considerarle QC di magazzino senza un’indicazione esplicita. Anche una foto QC storica riguarda un altro acquisto e non dimostra le condizioni del tuo articolo."
          },
          {
            "title": "Cerca dettagli utili",
            "body": "Confronta le viste anteriori, posteriori e di dettaglio disponibili. Osserva cuciture, chiusure, materiali visibili e misure dichiarate. Tieni presenti colore e variante selezionati. Illuminazione, prospettiva e schermi possono modificare l’aspetto dei colori. Angolazioni o misure mancanti devono restare domande aperte, non essere sostituite da supposizioni."
          },
          {
            "title": "Controlla il tuo ordine",
            "body": "Dopo l’acquisto, usa le foto specifiche del tuo ordine su Hipobuy per verificare che l’articolo ricevuto corrisponda alla scelta. Richiedi i dettagli mancanti prima di decidere la spedizione. Immagini e confronti visivi non certificano autenticità, qualità, vestibilità o durata. Leggi le regole di reso finché hai ancora tempo per intervenire."
          }
        ]
      },
      {
        "slug": "plan-shipping",
        "title": "Pianifica il pacco, non solo l’articolo",
        "summary": "Valuta il costo completo usando i dati reali del pacco.",
        "sections": [
          {
            "title": "Separa i costi",
            "body": "Il prezzo di catalogo è un punto di partenza per l’articolo. Verifica separatamente consegna nazionale, servizi di acquisto o opzionali, trasporto internazionale e imposte applicabili a destinazione. Tieni il budget nella valuta che preferisci. I prezzi in CNY sono convertiti con gli ultimi tassi di riferimento giornalieri disponibili di Frankfurter. La data è indicata nella scheda. Sono stime, non preventivi di pagamento. Senza dati viene mostrato il prezzo originale in CNY."
          },
          {
            "title": "Usa i dati corretti",
            "body": "Per una stima Hipobuy, inserisci destinazione e dati precisi del pacco. Una linea può usare peso effettivo o volumetrico secondo le proprie regole. Il peso del prodotto non coincide sempre con quello imballato. Confezione, dimensioni e combinazione degli articoli possono cambiare il preventivo. Verifica le condizioni aggiornate prima di scegliere."
          },
          {
            "title": "Conferma prima della partenza",
            "body": "Controlla il QC del tuo ordine e gli articoli inclusi nel pacco. Confronta servizi disponibili, restrizioni, tracciamento ed eventuali protezioni opzionali mostrate da Hipobuy. Questa anteprima non promette date di consegna e non calcola tariffe in tempo reale. Conserva preventivo e informazioni d’ordine per seguire la spedizione con il servizio competente."
          }
        ]
      }
    ]
  },
  "pt": {
    "faq": [
      {
        "q": "O que é a Hipobuy Spreadsheet?",
        "a": "Um diretório independente para encontrar e comparar anúncios de marketplaces antes de abri-los na Hipobuy."
      },
      {
        "q": "Este é o site oficial da Hipobuy?",
        "a": "Não. O diretório é independente. A Hipobuy administra suas próprias contas, compras, serviços de armazém e envios."
      },
      {
        "q": "De onde vêm as informações dos produtos?",
        "a": "Nomes, imagens, preços e links originais são lidos do catálogo conectado. Confira sempre o anúncio atual do vendedor."
      },
      {
        "q": "Posso fazer um pedido aqui?",
        "a": "Não. Abra o produto na Hipobuy, confira os detalhes e faça qualquer compra na plataforma."
      },
      {
        "q": "Como criar uma conta na Hipobuy?",
        "a": "Use https://hipobuy.com/register. Este diretório não cria nem administra contas."
      },
      {
        "q": "O que significa o preço em CNY?",
        "a": "É o valor informado pelo catálogo de origem em yuans chineses. Outro tamanho ou variante pode ter preço diferente."
      },
      {
        "q": "Como os preços em outras moedas são calculados?",
        "a": "Os preços em CNY são convertidos com as últimas taxas de referência diárias disponíveis da Frankfurter. A data aparece na página do produto. São estimativas, não valores finais de pagamento. Sem taxas disponíveis, aparece o preço original em CNY."
      },
      {
        "q": "O preço inclui frete?",
        "a": "Considere-o o preço do item. Confira separadamente frete doméstico, transporte internacional, tarifas de serviço e possíveis impostos."
      },
      {
        "q": "Todos os produtos estão em estoque?",
        "a": "Um registro no diretório não garante disponibilidade. Confira variante, tamanho e estoque na Hipobuy antes de pagar."
      },
      {
        "q": "Onde confirmar tamanhos e variantes?",
        "a": "Consulte as informações atuais do vendedor na Hipobuy. Não deduza o tamanho ou a opção escolhida apenas por uma foto."
      },
      {
        "q": "As imagens da galeria são fotos de QC?",
        "a": "Não necessariamente. A galeria apresenta o anúncio e não comprova o estado do seu próprio pedido."
      },
      {
        "q": "Onde verificar o QC do meu pedido?",
        "a": "Analise as fotos associadas ao seu pedido na Hipobuy. Referências históricas, quando disponíveis, pertencem a outras compras."
      },
      {
        "q": "Por que não há uma galeria de QC?",
        "a": "A fonte pode não fornecer fotos de QC identificadas separadamente. Fotos ausentes não são substituídas por imagens inventadas."
      },
      {
        "q": "Posso copiar o link original do marketplace?",
        "a": "Use o botão de copiar quando houver um link original. O ID identifica o produto do vendedor, não uma variante específica."
      },
      {
        "q": "Por que existem números de produto diferentes?",
        "a": "O número do diretório pode ser diferente do ID do marketplace. Use o ID original do marketplace para conferir um link de compra."
      },
      {
        "q": "Como funciona a busca?",
        "a": "Ela consulta o catálogo conectado. Números podem não ser pesquisáveis se a fonte indexar apenas nomes de produtos."
      },
      {
        "q": "Posso mudar o idioma?",
        "a": "Sim. Navegação, guias, botões e tipos de produto seguem o idioma selecionado. Marcas, modelos e identificadores são mantidos. O título original pode ser expandido na página do produto."
      },
      {
        "q": "O que fazer se um link de produto falhar?",
        "a": "Cole a URL original na busca da Hipobuy. Se ainda falhar, verifique se o anúncio do vendedor continua disponível."
      },
      {
        "q": "Posso calcular o frete internacional aqui?",
        "a": "Esta prévia não fornece cotações de frete ao vivo. Use a Hipobuy com destino, peso e dimensões do pacote."
      },
      {
        "q": "Quem cuida de pagamentos, devoluções e suporte?",
        "a": "A Hipobuy e o vendedor cuidam de suas respectivas transações e políticas. Para um pedido real, contate o serviço responsável."
      }
    ],
    "guides": [
      {
        "slug": "how-to-buy",
        "title": "Do achado ao primeiro pedido",
        "summary": "Guarde o link original e confira os detalhes antes de pagar.",
        "sections": [
          {
            "title": "Monte uma seleção",
            "body": "Explore uma categoria ou busque um item e abra sua página. Compare a galeria de origem, o preço registrado e o link original do marketplace. Guarde o link completo com o ID do anúncio: o número do catálogo pode ser diferente do número de produto do vendedor. Uma foto sozinha não identifica um tamanho, uma cor ou uma variante específica."
          },
          {
            "title": "Confira o anúncio atual",
            "body": "Abra o link da Hipobuy ou cole a URL original na busca da Hipobuy. Cadastre-se em hipobuy.com/register se precisar de conta. Confirme se título, imagens e vendedor correspondem à sua seleção. Verifique variante, medidas, estoque e preço atual antes de continuar. A estimativa em USD do diretório não é uma cotação de pagamento."
          },
          {
            "title": "Revise cada etapa",
            "body": "Faça qualquer compra na Hipobuy e leia as tarifas e condições de devolução em vigor. Quando o pedido chegar ao armazém, confira as fotos daquele pedido específico e peça esclarecimentos se necessário. Planeje o frete internacional quando souber os dados do pacote. O preço do item não representa sozinho o custo total até a entrega."
          }
        ]
      },
      {
        "slug": "check-product-photos",
        "title": "Analise as fotos antes de decidir",
        "summary": "Separe as imagens do anúncio das evidências sobre seu próprio pedido.",
        "sections": [
          {
            "title": "Entenda o que a imagem mostra",
            "body": "A galeria exibe imagens fornecidas pelo catálogo conectado. Elas podem ser fotos do vendedor ou outras referências do anúncio. Não as considere QC de armazém sem identificação explícita. Mesmo uma foto histórica de QC pertence a outra compra e não comprova o estado do seu item."
          },
          {
            "title": "Procure detalhes úteis",
            "body": "Compare vistas de frente, de trás e detalhes disponíveis. Examine costuras, fechos, materiais visíveis e medidas informadas. Mantenha a cor e a variante escolhidas ao lado da imagem analisada. Iluminação, perspectiva e telas podem mudar a aparência das cores. Ângulos ou medidas ausentes devem continuar sendo dúvidas a esclarecer."
          },
          {
            "title": "Confira seu próprio pedido",
            "body": "Após a compra, use as fotos específicas do pedido na Hipobuy para confirmar se o item recebido corresponde à seleção. Solicite os detalhes que faltam antes de decidir o envio. Imagens e comparações visuais não certificam autenticidade, qualidade, caimento ou durabilidade. Leia as regras de devolução enquanto ainda há tempo para agir."
          }
        ]
      },
      {
        "slug": "plan-shipping",
        "title": "Planeje o pacote, não apenas o item",
        "summary": "Avalie o custo completo usando os dados reais do pacote.",
        "sections": [
          {
            "title": "Separe os custos",
            "body": "O preço do catálogo é um ponto de partida para o item. Confira separadamente entrega doméstica, serviços de compra ou opcionais, transporte internacional e impostos aplicáveis no destino. Organize seu orçamento na moeda que preferir. Os preços em CNY são convertidos com as últimas taxas de referência diárias disponíveis da Frankfurter. A data aparece na página do produto. São estimativas, não valores finais de pagamento. Sem taxas disponíveis, aparece o preço original em CNY."
          },
          {
            "title": "Use os dados corretos",
            "body": "Ao pedir uma estimativa na Hipobuy, informe o destino e os dados exatos do pacote. Conforme as regras, uma rota pode usar peso real ou volumétrico. O peso do produto nem sempre equivale ao peso embalado. Embalagem, dimensões e combinação de itens podem mudar a cotação. Confira as condições atuais antes de escolher."
          },
          {
            "title": "Confirme antes do envio",
            "body": "Revise o QC do seu pedido e confira os itens incluídos no pacote. Compare serviços disponíveis, restrições, rastreamento e proteção opcional mostrados pela Hipobuy. Esta prévia não promete uma data de entrega nem calcula tarifas ao vivo. Guarde a cotação e os dados do pedido para acompanhar o envio com o serviço responsável."
          }
        ]
      }
    ]
  },
  "pl": {
    "faq": [
      {
        "q": "Czym jest Hipobuy Spreadsheet?",
        "a": "To niezależny katalog do wyszukiwania i porównywania ofert platform handlowych przed otwarciem ich w Hipobuy."
      },
      {
        "q": "Czy to oficjalna strona Hipobuy?",
        "a": "Nie. Katalog jest niezależny. Hipobuy samodzielnie obsługuje swoje konta, zakupy, usługi magazynowe i wysyłkę."
      },
      {
        "q": "Skąd pochodzą informacje o produktach?",
        "a": "Nazwy, zdjęcia, ceny i oryginalne linki są odczytywane z połączonego katalogu. Zawsze sprawdź aktualną ofertę sprzedawcy."
      },
      {
        "q": "Czy mogę tutaj złożyć zamówienie?",
        "a": "Nie. Otwórz produkt w Hipobuy, sprawdź szczegóły i tam dokonaj ewentualnego zakupu."
      },
      {
        "q": "Jak zarejestrować się w Hipobuy?",
        "a": "Skorzystaj z https://hipobuy.com/register. Ten katalog nie tworzy kont ani nimi nie zarządza."
      },
      {
        "q": "Co oznacza cena w CNY?",
        "a": "To kwota podana w katalogu źródłowym w chińskich juanach. Inny rozmiar lub wariant może kosztować więcej."
      },
      {
        "q": "Jak przeliczane są ceny w innych walutach?",
        "a": "Ceny w CNY są przeliczane według najnowszych dostępnych dziennych kursów referencyjnych Frankfurter. Data kursu jest widoczna na stronie produktu. Są to szacunki, nie wyceny płatności. Bez danych wyświetlana jest cena oryginalna w CNY."
      },
      {
        "q": "Czy cena obejmuje wysyłkę?",
        "a": "Traktuj ją jako cenę artykułu. Oddzielnie sprawdź dostawę krajową, wysyłkę międzynarodową, opłaty usługowe i ewentualne podatki."
      },
      {
        "q": "Czy wszystkie produkty są dostępne?",
        "a": "Wpis w katalogu nie gwarantuje dostępności. Przed płatnością sprawdź wariant, rozmiar i stan magazynowy w Hipobuy."
      },
      {
        "q": "Gdzie potwierdzić rozmiary i warianty?",
        "a": "Sprawdź aktualne informacje sprzedawcy w Hipobuy. Nie określaj rozmiaru ani wybranego wariantu wyłącznie na podstawie zdjęcia."
      },
      {
        "q": "Czy zdjęcia w galerii to zdjęcia QC?",
        "a": "Niekoniecznie. Galeria źródłowa przedstawia ofertę i nie potwierdza stanu Twojego zamówienia."
      },
      {
        "q": "Gdzie sprawdzić QC swojego zamówienia?",
        "a": "Przejrzyj zdjęcia przypisane do swojego zamówienia w Hipobuy. Ewentualne historyczne materiały dotyczą innych zakupów."
      },
      {
        "q": "Dlaczego brakuje galerii QC?",
        "a": "Źródło może nie udostępniać osobno oznaczonych zdjęć QC. Brakujących zdjęć nie zastępujemy wymyślonymi obrazami."
      },
      {
        "q": "Czy mogę skopiować oryginalny link?",
        "a": "Użyj przycisku kopiowania, jeśli dostępny jest link źródłowy. Identyfikator wskazuje produkt sprzedawcy, nie konkretny wariant."
      },
      {
        "q": "Dlaczego numery produktów są różne?",
        "a": "Numer wpisu w katalogu może różnić się od identyfikatora platformy. Przy sprawdzaniu linku zakupu używaj oryginalnego identyfikatora platformy."
      },
      {
        "q": "Jak działa wyszukiwanie?",
        "a": "Korzysta z połączonego katalogu. Numery mogą być niewyszukiwalne, jeśli źródło indeksuje tylko nazwy produktów."
      },
      {
        "q": "Czy mogę zmienić język?",
        "a": "Tak. Nawigacja, poradniki, przyciski i typy produktów są wyświetlane w wybranym języku. Marki, modele i identyfikatory pozostają bez zmian. Oryginalny tytuł można rozwinąć na stronie produktu."
      },
      {
        "q": "Co zrobić, gdy link produktu nie działa?",
        "a": "Wklej oryginalny adres oferty do wyszukiwarki Hipobuy. Jeśli nadal nie działa, sprawdź dostępność oferty sprzedawcy."
      },
      {
        "q": "Czy obliczę tutaj wysyłkę międzynarodową?",
        "a": "Podgląd nie podaje bieżących wycen wysyłki. Skorzystaj z Hipobuy, podając cel, wagę i wymiary paczki."
      },
      {
        "q": "Kto obsługuje płatności, zwroty i pomoc?",
        "a": "Hipobuy i sprzedawca odpowiadają za własne transakcje i zasady. W sprawie zamówienia skontaktuj się z właściwą usługą."
      }
    ],
    "guides": [
      {
        "slug": "how-to-buy",
        "title": "Od znaleziska do pierwszego zamówienia",
        "summary": "Zachowaj oryginalny link i sprawdź szczegóły przed płatnością.",
        "sections": [
          {
            "title": "Przygotuj krótką listę",
            "body": "Przejrzyj kategorię lub wyszukaj artykuł, a następnie otwórz jego stronę. Porównaj galerię źródłową, zapisaną cenę i oryginalny link do oferty. Zachowaj cały adres z identyfikatorem: numer katalogu może różnić się od numeru produktu sprzedawcy. Samo zdjęcie nie określa konkretnego rozmiaru, koloru ani wariantu."
          },
          {
            "title": "Sprawdź aktualną ofertę",
            "body": "Otwórz link Hipobuy lub wklej oryginalny adres oferty w wyszukiwarkę Hipobuy. Jeśli potrzebujesz konta, zarejestruj się przez hipobuy.com/register. Upewnij się, że tytuł, zdjęcia i sprzedawca odpowiadają Twojemu wyborowi. Sprawdź wariant, wymiary, dostępność i aktualną cenę. Szacunek USD w katalogu nie jest wiążącą wyceną płatności."
          },
          {
            "title": "Kontroluj każdy etap",
            "body": "Dokonaj ewentualnego zakupu w Hipobuy i przeczytaj obowiązujące opłaty oraz zasady zwrotu. Gdy zamówienie dotrze do magazynu, sprawdź zdjęcia właśnie tego zamówienia i poproś o wyjaśnienie niejasności. Zaplanuj wysyłkę międzynarodową, znając dane paczki. Sama cena artykułu nie oznacza pełnego kosztu dostarczenia."
          }
        ]
      },
      {
        "slug": "check-product-photos",
        "title": "Sprawdź zdjęcia przed decyzją",
        "summary": "Odróżniaj zdjęcia oferty od dowodów dotyczących własnego zamówienia.",
        "sections": [
          {
            "title": "Ustal, co pokazuje zdjęcie",
            "body": "Galeria przedstawia zdjęcia dostarczone przez połączony katalog. Mogą to być fotografie sprzedawcy lub inne materiały oferty. Bez wyraźnego oznaczenia nie traktuj ich jako magazynowego QC. Nawet historyczne zdjęcie QC należy do innego zakupu i nie potwierdza stanu Twojego artykułu."
          },
          {
            "title": "Szukaj przydatnych szczegółów",
            "body": "Porównuj dostępne ujęcia przodu, tyłu i detali. Sprawdź szwy, zapięcia, widoczne materiały oraz podane wymiary. Zestawiaj zdjęcie z wybranym kolorem i wariantem. Oświetlenie, perspektywa i ekrany mogą zmieniać wygląd kolorów. Brakujące ujęcia lub wymiary powinny pozostać pytaniami do wyjaśnienia."
          },
          {
            "title": "Sprawdź własne zamówienie",
            "body": "Po zakupie użyj zdjęć konkretnego zamówienia w Hipobuy, aby potwierdzić zgodność dostarczonego artykułu z wyborem. Poproś o brakujące informacje przed decyzją o wysyłce. Zdjęcia i porównania wzrokowe nie potwierdzają autentyczności, jakości, dopasowania ani trwałości. Przeczytaj zasady zwrotu, zanim minie czas na działanie."
          }
        ]
      },
      {
        "slug": "plan-shipping",
        "title": "Zaplanuj paczkę, nie tylko artykuł",
        "summary": "Oceń pełne koszty na podstawie rzeczywistych danych paczki.",
        "sections": [
          {
            "title": "Rozdziel koszty",
            "body": "Cena katalogowa jest punktem wyjścia dla artykułu. Osobno sprawdź dostawę krajową, usługi zakupowe lub opcjonalne, transport międzynarodowy i podatki w miejscu docelowym. Prowadź budżet w wybranej walucie. Ceny w CNY są przeliczane według najnowszych dostępnych dziennych kursów referencyjnych Frankfurter. Data kursu jest widoczna na stronie produktu. Są to szacunki, nie wyceny płatności. Bez danych wyświetlana jest cena oryginalna w CNY."
          },
          {
            "title": "Użyj właściwych danych",
            "body": "Prosząc Hipobuy o wycenę, podaj cel oraz dokładne dane paczki. W zależności od zasad linia może uwzględniać wagę rzeczywistą lub objętościową. Waga produktu nie zawsze odpowiada wadze zapakowanej przesyłki. Opakowanie, wymiary i połączenie artykułów mogą zmienić wycenę. Przed wyborem sprawdź aktualne warunki."
          },
          {
            "title": "Potwierdź przed nadaniem",
            "body": "Przejrzyj QC swojego zamówienia i sprawdź artykuły w paczce. Porównaj dostępne usługi, ograniczenia, śledzenie oraz opcjonalną ochronę pokazaną przez Hipobuy. Ten podgląd nie obiecuje terminu dostawy ani nie oblicza bieżącej opłaty. Zachowaj wycenę i dane zamówienia, aby śledzić przesyłkę u właściwego usługodawcy."
          }
        ]
      }
    ]
  },
  "zh": {
    "faq": [
      {
        "q": "什么是 Hipobuy 商品清单？",
        "a": "这是独立的商品发现目录，用于查找和比较电商平台商品，再前往 Hipobuy 查看与购买。"
      },
      {
        "q": "这是 Hipobuy 官方网站吗？",
        "a": "不是。本站是独立目录；账户、购买、仓储和运输由 Hipobuy 自行提供。"
      },
      {
        "q": "商品信息来自哪里？",
        "a": "商品名称、图片、价格和原始链接均读取自已连接的源目录。下单前请核对卖家的当前商品页面。"
      },
      {
        "q": "可以直接在这里下单吗？",
        "a": "不可以。请打开 Hipobuy 商品链接，核对信息后在该平台完成购买。"
      },
      {
        "q": "如何注册 Hipobuy 账户？",
        "a": "请前往官方入口 https://hipobuy.com/register。本站不创建或管理用户账户。"
      },
      {
        "q": "CNY 价格代表什么？",
        "a": "它是源目录记录的人民币金额。不同尺码或款式的价格可能不同。"
      },
      {
        "q": "不同货币的价格如何换算？",
        "a": "以商品人民币价格为基础，按 Frankfurter 最新可用的每日参考汇率自动换算，商品页会显示汇率日期。换算价格仅供参考，不是平台结算报价；汇率不可用时显示人民币原价。"
      },
      {
        "q": "显示的价格包含运费吗？",
        "a": "请将其视为商品价格；国内运费、国际运费、服务费用及可能的税费需要分别确认。"
      },
      {
        "q": "清单中的商品都有现货吗？",
        "a": "目录收录不代表保证有货。付款前请在 Hipobuy 核对选定款式、尺码与库存。"
      },
      {
        "q": "在哪里确认尺码和款式？",
        "a": "请查看 Hipobuy 展示的当前卖家信息，不要仅根据商品图片推断尺码或已选款式。"
      },
      {
        "q": "商品图库里的图片都是 QC 照片吗？",
        "a": "不一定。源图库展示的是商品页面图片，不能证明你实际购买的商品状态。"
      },
      {
        "q": "在哪里查看自己订单的 QC？",
        "a": "请在 Hipobuy 查看与你的订单对应的照片。即使有历史参考图，也与本次订单不同。"
      },
      {
        "q": "为什么有些商品没有 QC 图库？",
        "a": "源目录可能没有提供单独标记的 QC 照片。缺失的照片不会用编造图片替代。"
      },
      {
        "q": "可以复制原始电商链接吗？",
        "a": "有原始链接时，可以使用复制按钮。链接中的商品 ID 识别的是卖家商品，并不代表某个具体款式。"
      },
      {
        "q": "为什么会看到不同的商品编号？",
        "a": "目录内部编号可能与电商平台商品 ID 不同。核对购买链接时，请以原始电商商品 ID 为准。"
      },
      {
        "q": "搜索是怎样工作的？",
        "a": "搜索使用已连接的源目录。如果源站只索引商品名称，直接搜索商品编号可能无法找到结果。"
      },
      {
        "q": "可以切换语言吗？",
        "a": "可以。导航、指南、按钮和商品类型描述会随语言切换；品牌、型号与编号保持原样。商品详情页还可以展开查看源站原名。"
      },
      {
        "q": "商品链接打不开怎么办？",
        "a": "将原始电商链接粘贴到 Hipobuy 搜索框。如果仍无法打开，请检查卖家商品是否仍然有效。"
      },
      {
        "q": "可以在这里计算国际运费吗？",
        "a": "此预览不提供实时运费报价。请在 Hipobuy 填写目的地、包裹重量和尺寸后查询。"
      },
      {
        "q": "谁负责付款、退货和客服？",
        "a": "Hipobuy 与卖家分别负责其交易和服务规则。涉及实际订单时，请联系相应服务方。"
      }
    ],
    "guides": [
      {
        "slug": "how-to-buy",
        "title": "从发现商品到完成首单",
        "summary": "保留原始商品链接，付款前逐项核对。",
        "sections": [
          {
            "title": "先整理候选商品",
            "body": "浏览分类或搜索商品，再打开详情页。比较源图库、记录价格与原始电商链接，并保留包含商品 ID 的完整地址。目录内部编号可能与卖家商品编号不同。单张照片不能确定具体尺码、颜色或款式，比较时应将这些信息单独记录。"
          },
          {
            "title": "核对当前商品页面",
            "body": "打开 Hipobuy 商品链接，或将原始电商地址粘贴到 Hipobuy 搜索框。需要账户时，使用 hipobuy.com/register 注册。确认标题、图片和卖家与你选中的商品一致，再检查款式、尺寸、库存和当前价格。目录中的美元估价不是最终结算报价。"
          },
          {
            "title": "按订单阶段检查",
            "body": "在 Hipobuy 完成购买，并阅读当前费用及适用的退货规则。商品到仓后，查看这笔订单对应的照片；有疑问时先补充确认。知道包裹的实际信息后，再计划国际运输。商品标价并不等于送达目的地的全部费用。"
          }
        ]
      },
      {
        "slug": "check-product-photos",
        "title": "决定之前，先看懂商品照片",
        "summary": "区分卖家展示图片与自己订单的实际验货照片。",
        "sections": [
          {
            "title": "先确认图片的性质",
            "body": "商品图库显示源目录提供的图片，可能是卖家展示图或其他商品参考图。没有明确标记为 QC 的图片，不应当作仓库验货照片。即使存在历史 QC 图，它也属于其他购买记录，不能证明你这次收到的商品状态。"
          },
          {
            "title": "关注能帮助判断的细节",
            "body": "有条件时对比正面、背面与细节视角，观察缝线、开合结构、图中可见的材料及标注尺寸。将所选颜色和款式与图片对应起来。灯光、拍摄角度和屏幕都可能影响颜色表现。缺少的角度或尺寸应保留为待确认问题，不要自行猜测。"
          },
          {
            "title": "检查自己的订单",
            "body": "购买后，在 Hipobuy 查看与你订单对应的照片，确认到仓商品与所选款式一致。关键细节不清楚时，在决定发货前索取所需信息。目录图片和视觉比较不能认证真伪、质量、合身程度或耐用性；也应及时查看退货规则，避免错过处理时间。"
          }
        ]
      },
      {
        "slug": "plan-shipping",
        "title": "按包裹规划费用",
        "summary": "用真实包裹信息估算完整成本，而不只看商品价格。",
        "sections": [
          {
            "title": "将费用分别列出",
            "body": "目录价格只是商品费用的起点。 国内卖家运费、购买或可选服务费用、国际运输及目的地可能适用的税费，需要分别核对。 建议使用自己常用的货币整理预算。 以商品人民币价格为基础，按 Frankfurter 最新可用的每日参考汇率自动换算，商品页会显示汇率日期。换算价格仅供参考，不是平台结算报价；汇率不可用时显示人民币原价。"
          },
          {
            "title": "使用准确的包裹数据",
            "body": "在 Hipobuy 估算运费时，填写目的地与准确的包裹信息。不同线路可能按实际重量或体积重量计费，具体取决于其当前规则。商品重量不一定等于打包后的包裹重量；包装、尺寸和合并商品的组合都会影响报价。选定线路前请核对适用条件。"
          },
          {
            "title": "发货前再确认一次",
            "body": "检查自己订单的 QC 照片，并确认包裹内的商品清单。比较 Hipobuy 展示的可用运输服务、限制、追踪方式和可选保障。本预览不承诺送达日期，也不计算实时国际运费。保存报价与订单信息，方便向实际承运或服务方查询物流。"
          }
        ]
      }
    ]
  }
};
