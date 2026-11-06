from pathlib import Path
from bs4 import BeautifulSoup
import json
S=Path(__file__).resolve().parent
keys=[]
for slug in ['hoobuy-spreadsheet-women','hoobuy-budget-finds','hoobuy-links-not-working','hoobuy-spreadsheet-guide']:
 for h in BeautifulSoup((S/'content'/(slug+'.html')).read_text(),'html.parser').select('h2,h3'):
  if h.get_text() not in keys:keys.append(h.get_text())
rows={
'zh-CN':'''先确定商品分类与合身要求
女装购物清单应记录哪些信息
按版型比较上衣、针织衫与连衣裙
裤装与裙装不能只看腰围标签
按实际尺寸需求选择包袋与配件
用 QC 照片回答具体问题
选择便宜商品前先比较总成本
一个实用的选品清单示例
下单前的常见问题
HooBuy 有统一的女装尺码表吗？
卖家图片能当作订单 QC 照片吗？
保存的商品链接应多久检查一次？
来源与核对说明
比较带日期的实例，区分价格与实际价值
先设总预算，再决定商品价格上限
比较相同的商品规格
按购买要求比较，而不是只按低价排序
包装会怎样影响运费计算
计算多加一件商品的额外成本
追加支出前先检查 QC
保持清单精简，并注明下一步
预算常见问题
这些价格是含运费的到手价吗？
最低商品价格一定最省钱吗？
有优惠券就一定更便宜吗？
先确认页面上出现的问题
修改链接前保存原始信息
检查复制的地址与跳转后的页面
区分原始商品页面与平台导入页面
检查是否只是某个规格下架
把替代商品作为新选品重新核对
商品已经下单时该怎么处理
一个逐步排查示例
避免购物清单积累失效链接
来源与适用范围
浏览 HooBuy 好物并保存具体商品信息
一行只记录一个明确规格
核对淘宝、1688 与微店链接
用明确的参照物比较尺码
区分卖家图片与自己订单的 QC
记录选定规格价格与完整购买成本
把确认的商品加入带日期的包裹计划
用明确状态代替笼统的“已验证”
完成你的第一份选品清单
来源与更新说明''',
'de':'''Kategorie und gewünschte Passform festlegen
Was in eine Einkaufstabelle für Damen gehört
Oberteile, Strickwaren und Kleider nach Schnitt vergleichen
Bei Hosen, Jeans und Röcken mehr als den Bund prüfen
Taschen und Accessoires nach konkreten Maßen auswählen
Konkrete Fragen mit QC-Fotos klären
Vor dem günstigeren Fund die Gesamtkosten vergleichen
Ein praktisches Beispiel für eine Produktauswahl
Fragen vor der Bestellung
Gibt es eine einheitliche HooBuy-Größentabelle für Damen?
Kann ich Verkäuferbilder als QC-Fotos verwenden?
Wie oft sollte ich einen gespeicherten Produktlink prüfen?
Quellen und Prüfhinweise
Datierte Beispiele vergleichen: Preis und Nutzen unterscheiden
Zuerst das Gesamtbudget, dann die Preisgrenze festlegen
Dieselbe Produktvariante vergleichen
Nach Anforderungen statt nur nach dem niedrigsten Preis entscheiden
Wie die Verpackung das Ergebnis verändert
Die zusätzlichen Kosten eines weiteren Artikels berechnen
QC prüfen, bevor weitere Kosten entstehen
Eine überschaubare Auswahl mit nächsten Schritten führen
Häufige Budgetfragen
Enthalten diese Preise die Lieferung?
Ist der niedrigste Artikelpreis immer die günstigste Wahl?
Macht ein Gutschein den gesamten Kauf automatisch günstiger?
Mit dem sichtbaren Problem beginnen
Informationen sichern, bevor Sie den Link ändern
Kopierte Adressen und Weiterleitungsziele prüfen
Originalangebot und Plattformimport getrennt prüfen
Prüfen, ob nur die ausgewählte Variante fehlt
Ein Ersatzangebot wie ein neues Produkt prüfen
Was tun, wenn der Artikel bereits bestellt wurde?
Eine schrittweise Fehlersuche als Beispiel
Veraltete Links in der Produkttabelle vermeiden
Quellen und Geltungsbereich
HooBuy-Produkte entdecken und genaue Angaben speichern
Eine Zeile pro ausgewählter Variante verwenden
Taobao-, 1688- und Weidian-Links prüfen
Größen mit einer bekannten Referenz vergleichen
Verkäuferbilder von QC der eigenen Bestellung unterscheiden
Variantenpreis und vollständige Kaufkosten festhalten
Geprüfte Artikel in einen datierten Paketplan aufnehmen
Klare Statusangaben statt eines pauschalen Prüfsiegels verwenden
Die erste Produktauswahl Schritt für Schritt
Quellen und Aktualisierung''',
'fr':'''Choisir une catégorie et définir la coupe souhaitée
Que noter dans un tableau d’achats pour femmes
Comparer la coupe des hauts, mailles et robes
Vérifier pantalons, jeans et jupes au-delà du tour de taille
Choisir sacs et accessoires selon des dimensions précises
Répondre à des questions concrètes avec les photos QC
Comparer le coût total avant de choisir le produit moins cher
Un exemple pratique de sélection
Questions avant de commander
Existe-t-il un guide universel des tailles femme HooBuy ?
Les photos du vendeur peuvent-elles servir de photos QC ?
À quelle fréquence vérifier un lien produit enregistré ?
Sources et vérifications
Comparer des exemples datés sans confondre prix et valeur
Définir le budget total avant le plafond par article
Comparer la même variante du produit
Décider selon les besoins plutôt que le prix le plus bas
Comprendre l’effet de l’emballage sur le résultat
Calculer le coût supplémentaire d’un article
Vérifier le QC avant d’engager d’autres dépenses
Garder une sélection courte avec des actions précises
Questions courantes sur le budget
Ces prix comprennent-ils la livraison ?
Le prix d’article le plus bas est-il toujours le meilleur choix ?
Un coupon rend-il forcément l’achat total moins cher ?
Commencer par le problème visible
Sauvegarder les informations avant de modifier le lien
Vérifier l’adresse copiée et la destination des redirections
Distinguer la fiche d’origine de l’import sur la plateforme
Vérifier si seule la variante choisie a disparu
Évaluer le remplacement comme un nouveau produit
Que faire si le produit a déjà été commandé ?
Un exemple de dépannage étape par étape
Éviter l’accumulation de liens inactifs dans le tableau
Sources et portée du guide
Parcourir les produits HooBuy et conserver leurs références exactes
Utiliser une ligne par variante sélectionnée
Vérifier les liens Taobao, 1688 et Weidian
Comparer les tailles avec une référence connue
Distinguer les photos du vendeur du QC de votre commande
Noter le prix sélectionné et le coût total de l’achat
Intégrer les articles vérifiés à un plan de colis daté
Utiliser des statuts précis plutôt qu’un simple label « vérifié »
Préparer une première sélection étape par étape
Sources et mise à jour''',
'es':'''Elige una categoría y define el ajuste que necesitas
Qué anotar en una lista de compras para mujer
Compara el corte de tops, prendas de punto y vestidos
Revisa pantalones, vaqueros y faldas más allá de la cintura
Elige bolsos y accesorios según medidas concretas
Resuelve dudas específicas con fotos QC
Compara el coste total antes de elegir el producto más barato
Un ejemplo práctico de selección
Preguntas antes de hacer el pedido
¿Existe una tabla universal de tallas HooBuy para mujer?
¿Puedo usar las fotos del vendedor como fotos QC?
¿Con qué frecuencia debo revisar un enlace guardado?
Fuentes y comprobaciones
Compara ejemplos fechados sin confundir precio y valor
Fija el presupuesto total antes del límite por artículo
Compara la misma variante del producto
Decide según tus necesidades, no solo por el menor precio
Cómo puede cambiar el resultado según el embalaje
Calcula el coste adicional de añadir un artículo
Revisa el QC antes de gastar más
Mantén una selección breve con próximos pasos claros
Preguntas frecuentes sobre el presupuesto
¿Estos precios incluyen la entrega?
¿El menor precio del artículo es siempre la opción más económica?
¿Un cupón hace que la compra final sea necesariamente más barata?
Empieza por el problema que puedes observar
Guarda la información antes de cambiar el enlace
Revisa la dirección copiada y el destino de las redirecciones
Distingue la ficha original de la importación en la plataforma
Comprueba si solo falta la variante seleccionada
Evalúa el sustituto como un producto nuevo
Qué hacer si ya has pedido el producto
Un ejemplo de resolución paso a paso
Evita acumular enlaces inactivos en tu lista
Fuentes y alcance
Explora productos HooBuy y guarda sus referencias exactas
Usa una fila por cada variante seleccionada
Verifica los enlaces de Taobao, 1688 y Weidian
Compara tallas con una referencia conocida
Distingue las imágenes del vendedor del QC de tu pedido
Registra el precio seleccionado y el coste completo de la compra
Añade los artículos revisados a un plan de paquete fechado
Utiliza estados claros en lugar de una etiqueta genérica de verificado
Prepara tu primera selección paso a paso
Fuentes y notas de actualización''',
'it':'''Scegli una categoria e definisci la vestibilità desiderata
Cosa annotare in una lista di acquisti donna
Confronta il taglio di top, maglieria e abiti
Controlla pantaloni, jeans e gonne oltre alla misura della vita
Scegli borse e accessori in base a dimensioni precise
Usa le foto QC per chiarire dubbi specifici
Confronta il costo totale prima di scegliere il prodotto meno caro
Un esempio pratico di selezione
Domande prima di ordinare
Esiste una tabella universale delle taglie donna HooBuy?
Posso usare le foto del venditore come foto QC?
Quanto spesso devo controllare un link salvato?
Fonti e verifiche
Confronta esempi datati senza confondere prezzo e valore
Definisci il budget totale prima del limite per articolo
Confronta la stessa variante del prodotto
Decidi in base alle esigenze, non solo al prezzo più basso
Come l’imballaggio può modificare il risultato
Calcola il costo aggiuntivo di un altro articolo
Controlla il QC prima di spendere altro
Mantieni una selezione breve con azioni chiare
Domande frequenti sul budget
Questi prezzi comprendono la consegna?
Il prezzo più basso dell’articolo è sempre la scelta più economica?
Un coupon rende necessariamente più conveniente l’acquisto finale?
Parti dal problema che puoi osservare
Salva le informazioni prima di modificare il link
Controlla gli indirizzi copiati e le destinazioni dei reindirizzamenti
Distingui la pagina originale dall’importazione sulla piattaforma
Verifica se manca solo la variante selezionata
Valuta l’alternativa come un nuovo prodotto
Cosa fare se il prodotto è già stato ordinato
Un esempio di risoluzione passo per passo
Evita l’accumulo di link non funzionanti nella lista
Fonti e ambito della guida
Esplora i prodotti HooBuy e salva i riferimenti esatti
Usa una riga per ogni variante selezionata
Verifica i link Taobao, 1688 e Weidian
Confronta le taglie con un riferimento noto
Distingui le foto del venditore dal QC del tuo ordine
Registra il prezzo selezionato e il costo completo dell’acquisto
Inserisci gli articoli controllati in un piano di spedizione datato
Usa stati precisi invece di un generico «verificato»
Prepara la tua prima selezione passo per passo
Fonti e note di aggiornamento''',
'pl':'''Wybierz kategorię i określ wymagania dotyczące dopasowania
Co zapisać w arkuszu zakupowym dla kobiet
Porównuj kroje bluzek, dzianin i sukienek
Sprawdzaj spodnie, jeansy i spódnice nie tylko w pasie
Wybieraj torby i akcesoria według konkretnych wymiarów
Wyjaśniaj konkretne wątpliwości za pomocą zdjęć QC
Porównaj całkowity koszt przed wyborem tańszego produktu
Praktyczny przykład wyboru produktów
Pytania przed zamówieniem
Czy istnieje jedna uniwersalna tabela damskich rozmiarów HooBuy?
Czy zdjęcia sprzedawcy mogą zastąpić zdjęcia QC?
Jak często sprawdzać zapisany link do produktu?
Źródła i weryfikacja
Porównuj datowane przykłady, odróżniając cenę od wartości
Ustal pełny budżet przed limitem ceny pojedynczego produktu
Porównuj ten sam wariant produktu
Decyduj według potrzeb, a nie tylko najniższej ceny
Jak opakowanie może zmienić wynik
Oblicz dodatkowy koszt kolejnego produktu
Sprawdź QC przed poniesieniem dalszych kosztów
Prowadź krótką listę z jasnymi kolejnymi krokami
Częste pytania o budżet
Czy te ceny obejmują dostawę?
Czy najniższa cena produktu zawsze oznacza najtańszy zakup?
Czy kupon musi obniżyć całkowity koszt zakupu?
Zacznij od widocznego problemu
Zapisz informacje przed zmianą linku
Sprawdź skopiowany adres i cel przekierowania
Oddziel stronę źródłową od importu na platformę
Sprawdź, czy zniknął tylko wybrany wariant
Oceń zamiennik jak nowy produkt
Co zrobić, jeśli produkt jest już zamówiony
Przykład rozwiązywania problemu krok po kroku
Nie gromadź niedziałających linków w arkuszu
Źródła i zakres poradnika
Przeglądaj produkty HooBuy i zapisuj dokładne dane
Jeden wiersz dla jednego wybranego wariantu
Sprawdzaj linki Taobao, 1688 i Weidian
Porównuj rozmiary ze znanym punktem odniesienia
Oddziel zdjęcia sprzedawcy od QC własnego zamówienia
Zapisuj cenę wariantu i pełny koszt zakupu
Dodawaj sprawdzone produkty do datowanego planu paczki
Używaj konkretnych statusów zamiast ogólnego „zweryfikowano”
Przygotuj pierwszą listę produktów krok po kroku
Źródła i informacje o aktualizacji''',
'nl':'''Kies een categorie en bepaal de gewenste pasvorm
Wat noteer je in een boodschappenlijst voor dames?
Vergelijk de snit van tops, gebreide kleding en jurken
Controleer broeken, jeans en rokken op meer dan de taillemaat
Kies tassen en accessoires op basis van concrete afmetingen
Beantwoord specifieke vragen met QC-foto’s
Vergelijk de totale kosten voordat je een goedkoper product kiest
Een praktisch voorbeeld van een productselectie
Vragen voordat je bestelt
Is er één universele HooBuy-maattabel voor dames?
Kan ik verkopersfoto’s als QC-foto’s gebruiken?
Hoe vaak moet ik een opgeslagen productlink controleren?
Bronnen en controles
Vergelijk gedateerde voorbeelden zonder prijs en waarde te verwarren
Bepaal eerst het totale budget en daarna de maximale artikelprijs
Vergelijk dezelfde productvariant
Beslis op basis van je eisen, niet alleen de laagste prijs
Hoe de verpakking het resultaat kan veranderen
Bereken de extra kosten van nog een artikel
Controleer QC voordat je meer uitgeeft
Houd een korte selectie met duidelijke vervolgstappen bij
Veelgestelde budgetvragen
Zijn deze prijzen inclusief bezorging?
Is de laagste artikelprijs altijd de voordeligste keuze?
Maakt een kortingsbon de volledige aankoop automatisch goedkoper?
Begin bij het zichtbare probleem
Bewaar de informatie voordat je de link wijzigt
Controleer gekopieerde adressen en bestemmingen van omleidingen
Maak onderscheid tussen de bronpagina en de platformimport
Controleer of alleen de gekozen variant ontbreekt
Beoordeel een vervanging als een nieuw product
Wat te doen als het product al besteld is
Een voorbeeld van stapsgewijs problemen oplossen
Voorkom dat je spreadsheet volloopt met dode links
Bronnen en reikwijdte
Bekijk HooBuy-producten en bewaar de exacte gegevens
Gebruik één rij per geselecteerde variant
Controleer Taobao-, 1688- en Weidian-links
Vergelijk maten met een bekende referentie
Onderscheid verkopersfoto’s van QC van je eigen bestelling
Noteer de geselecteerde prijs en de volledige aankoopkosten
Neem gecontroleerde artikelen op in een gedateerd pakketplan
Gebruik duidelijke statussen in plaats van een algemeen keurmerk
Stel stap voor stap je eerste productselectie samen
Bronnen en update-informatie''',
'pt':'''Escolha uma categoria e defina o ajuste pretendido
O que registar numa lista de compras para mulher
Compare o corte de tops, malhas e vestidos
Verifique calças, jeans e saias para além da cintura
Escolha malas e acessórios com base em medidas concretas
Use fotos QC para esclarecer dúvidas específicas
Compare o custo total antes de escolher o produto mais barato
Um exemplo prático de seleção
Perguntas antes de encomendar
Existe uma tabela universal de tamanhos femininos HooBuy?
Posso usar as fotos do vendedor como fotos QC?
Com que frequência devo verificar um link guardado?
Fontes e verificações
Compare exemplos datados sem confundir preço e valor
Defina o orçamento total antes do limite por artigo
Compare a mesma variante do produto
Decida pelas necessidades, não apenas pelo preço mais baixo
Como a embalagem pode alterar o resultado
Calcule o custo adicional de mais um artigo
Verifique o QC antes de gastar mais
Mantenha uma seleção curta com próximos passos claros
Perguntas frequentes sobre o orçamento
Estes preços incluem a entrega?
O menor preço do artigo é sempre a opção mais económica?
Um cupão torna necessariamente a compra final mais barata?
Comece pelo problema que consegue observar
Guarde as informações antes de alterar o link
Verifique o endereço copiado e o destino dos redirecionamentos
Distinga a página original da importação na plataforma
Verifique se desapareceu apenas a variante escolhida
Avalie a alternativa como um novo produto
O que fazer se o produto já foi encomendado
Um exemplo de resolução passo a passo
Evite acumular links inativos na lista
Fontes e âmbito do guia
Explore produtos HooBuy e guarde as referências exatas
Use uma linha para cada variante selecionada
Verifique links de Taobao, 1688 e Weidian
Compare tamanhos com uma referência conhecida
Distinga as fotos do vendedor do QC da sua encomenda
Registe o preço selecionado e o custo completo da compra
Inclua os artigos verificados num plano de encomenda datado
Use estados claros em vez de um rótulo genérico de verificado
Prepare a primeira seleção passo a passo
Fontes e notas de atualização'''}
p=S/'release-overrides.json';out=json.loads(p.read_text())
for l,body in rows.items():
 values=body.splitlines();assert len(values)==len(keys),(l,len(values),len(keys));out[l].update(zip(keys,values))
p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Reviewed headings',len(keys),'in',len(rows),'languages')
