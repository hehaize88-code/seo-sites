import type {Locale} from './i18n';
// Display-only vocabulary, never a product catalogue. Brand/model strings and source IDs stay intact.
const rows = [
['pants/shorts','Hosen/Shorts','Pantalons/shorts','Pantalones/pantalones cortos','Pantaloni/shorts','Calças/bermudas','Spodnie/szorty','长裤／短裤'],
['hoodies/sweaters','Hoodies/Pullover','Sweats à capuche/pulls','Sudaderas/jerséis','Felpe/maglioni','Moletons/suéteres','Bluzy/swetry','连帽卫衣／毛衣'],
['phone cases|phone case|cellphone case','Handyhülle','Coque de téléphone','Funda de móvil','Custodia per telefono','Capa de celular','Etui na telefon','手机壳'],
['card holders?|cardholde','Kartenetui','Porte-cartes','Tarjetero','Portacarte','Porta-cartões','Etui na karty','卡包'],
['down ?jackets?','Daunenjacke','Doudoune','Chaqueta de plumas','Piumino','Jaqueta de plumas','Kurtka puchowa','羽绒服'],
['down vests?','Daunenweste','Doudoune sans manches','Chaleco de plumas','Gilet imbottito','Colete de plumas','Kamizelka puchowa','羽绒马甲'],
['puffer jackets?','Steppjacke','Veste matelassée','Chaqueta acolchada','Giacca imbottita','Jaqueta acolchoada','Kurtka pikowana','棉服'],
['denim jackets?','Jeansjacke','Veste en jean','Chaqueta vaquera','Giacca di jeans','Jaqueta jeans','Kurtka jeansowa','牛仔夹克'],
['shoulder bags?','Schultertasche','Sac à bandoulière','Bolso de hombro','Borsa a spalla','Bolsa de ombro','Torba na ramię','单肩包'],
['tote bags?','Tragetasche','Cabas','Bolso tote','Borsa tote','Bolsa tote','Torba shopper','托特包'],
['belt bags?','Gürteltasche','Sac banane','Riñonera','Marsupio','Pochete','Nerka','腰包'],
['baseball caps?','Baseballkappe','Casquette de baseball','Gorra de béisbol','Cappellino da baseball','Boné de beisebol','Czapka z daszkiem','棒球帽'],
['bucket hats?','Fischerhut','Bob','Sombrero de pescador','Cappello da pescatore','Chapéu bucket','Kapelusz rybacki','渔夫帽'],
['football jerseys?|soccer jerseys?','Fußballtrikot','Maillot de football','Camiseta de fútbol','Maglia da calcio','Camisa de futebol','Koszulka piłkarska','足球球衣'],
['basketball jerseys?','Basketballtrikot','Maillot de basket','Camiseta de baloncesto','Canotta da basket','Camisa de basquete','Koszulka koszykarska','篮球球衣'],
['zippers?|zippered','Reißverschluss','Fermeture éclair','Cremallera','Cerniera','Zíper','Zamek błyskawiczny','拉链'],
['short sleeved|short sleeves?','Kurzarm','Manches courtes','Manga corta','Maniche corte','Manga curta','Krótki rękaw','短袖'],
['sweatshirts?','Sweatshirt','Sweat-shirt','Sudadera','Felpa','Moletom','Bluza','卫衣'],
['hoodies?|hoodi','Kapuzenpullover','Sweat à capuche','Sudadera con capucha','Felpa con cappuccio','Moletom com capuz','Bluza z kapturem','连帽卫衣'],
['longsleeves?|long sleeves?','Langarmshirt','Haut à manches longues','Camiseta de manga larga','Maglia a maniche lunghe','Camiseta de manga longa','Koszulka z długim rękawem','长袖上衣'],
['t[ -]?shirts?|tees?|tee shirt','T-Shirt','T-shirt','Camiseta','T-shirt','Camiseta','T-shirt','T恤'],
['sweaters?','Pullover','Pull','Jersey','Maglione','Suéter','Sweter','毛衣'],
['sweatpants?|joggers?','Jogginghose','Pantalon de jogging','Pantalón de chándal','Pantaloni della tuta','Calça de moletom','Spodnie dresowe','运动长裤'],
['tracksuits?','Trainingsanzug','Survêtement','Chándal','Tuta sportiva','Agasalho','Dres','运动套装'],
['short sets?','Shorts-Set','Ensemble avec short','Conjunto con pantalón corto','Completo con shorts','Conjunto com bermuda','Zestaw z szortami','短袖短裤套装'],
['suits?|sets?','Set','Ensemble','Conjunto','Completo','Conjunto','Zestaw','套装'],
['shorts?|swimshorts?','Shorts','Short','Pantalón corto','Shorts','Bermuda','Szorty','短裤'],
['pants?|slacks','Hose','Pantalon','Pantalón','Pantaloni','Calça','Spodnie','长裤'],
['jeans','Jeans','Jean','Vaqueros','Jeans','Jeans','Jeansy','牛仔裤'],
['underwear|boxer briefs','Unterwäsche','Sous-vêtements','Ropa interior','Intimo','Roupa íntima','Bielizna','内裤'],
['sneakers?','Sneaker','Baskets','Zapatillas','Sneakers','Tênis','Sneakersy','运动鞋'],
['shoes?','Schuhe','Chaussures','Zapatos','Scarpe','Calçados','Buty','鞋子'],
['socks?','Socken','Chaussettes','Calcetines','Calzini','Meias','Skarpety','袜子'],
['jackets?','Jacke','Veste','Chaqueta','Giacca','Jaqueta','Kurtka','夹克'],
['coats?','Mantel','Manteau','Abrigo','Cappotto','Casaco','Płaszcz','外套'],
['vests?','Weste','Gilet','Chaleco','Gilet','Colete','Kamizelka','马甲'],
['windbreakers?','Windjacke','Coupe-vent','Cortavientos','Giacca antivento','Corta-vento','Wiatrówka','防风外套'],
['jerseys?','Trikot','Maillot','Camiseta deportiva','Maglia sportiva','Camisa esportiva','Koszulka sportowa','球衣'],
['shirts?','Hemd','Chemise','Camisa','Camicia','Camisa','Koszula','衬衫'],
['backpacks?|mochila','Rucksack','Sac à dos','Mochila','Zaino','Mochila','Plecak','双肩包'],
['wallets?|cartera','Geldbörse','Portefeuille','Cartera','Portafoglio','Carteira','Portfel','钱包'],
['bags?|bolsa','Tasche','Sac','Bolso','Borsa','Bolsa','Torba','包袋'],
['belts?|cinturon','Gürtel','Ceinture','Cinturón','Cintura','Cinto','Pasek','腰带'],
['bracelets?','Armband','Bracelet','Pulsera','Bracciale','Pulseira','Bransoletka','手链'],
['necklaces?','Halskette','Collier','Collar','Collana','Colar','Naszyjnik','项链'],
['rings?|anillo','Ring','Bague','Anillo','Anello','Anel','Pierścionek','戒指'],
['keychains?','Schlüsselanhänger','Porte-clés','Llavero','Portachiavi','Chaveiro','Brelok','钥匙扣'],
['sunglasses?','Sonnenbrille','Lunettes de soleil','Gafas de sol','Occhiali da sole','Óculos de sol','Okulary przeciwsłoneczne','太阳镜'],
['eyeglasses|glasses','Brille','Lunettes','Gafas','Occhiali','Óculos','Okulary','眼镜'],
['beanies?','Strickmütze','Bonnet','Gorro','Berretto','Gorro','Czapka zimowa','针织帽'],
['hats?|caps?','Mütze','Casquette','Gorra','Cappello','Boné','Czapka','帽子'],
['watches|watch','Uhr','Montre','Reloj','Orologio','Relógio','Zegarek','手表'],
['perfume','Parfüm','Parfum','Perfume','Profumo','Perfume','Perfumy','香水'],
['electronics','Elektronik','Électronique','Electrónica','Elettronica','Eletrônicos','Elektronika','电子产品'],
['other stuff','Sonstiges','Autres articles','Otros artículos','Altri articoli','Outros itens','Inne produkty','其他商品'],
['accessories','Accessoires','Accessoires','Accesorios','Accessori','Acessórios','Akcesoria','配饰'],
['styles?|models?|colorways?','Varianten','Modèles','Modelos','Modelli','Modelos','Warianty','款式'],
['colors?|colours?','Farben','Couleurs','Colores','Colori','Cores','Kolory','颜色'],
['hooded','mit Kapuze','à capuche','con capucha','con cappuccio','com capuz','z kapturem','连帽'],
['mechanical','Mechanisch','Mécanique','Mecánico','Meccanico','Mecânico','Mechaniczny','机械'],
['automatic','Automatisch','Automatique','Automático','Automatico','Automático','Automatyczny','自动'],
['graphic print','Grafikdruck','Imprimé graphique','Estampado gráfico','Stampa grafica','Estampa gráfica','Nadruk graficzny','图案印花'],
['print','Druck','Imprimé','Estampado','Stampa','Estampa','Nadruk','印花'],
['graphic','Grafik','Graphique','Gráfico','Grafica','Gráfico','Grafika','图案'],
['logo','Logo','Logo','Logotipo','Logo','Logotipo','Logo','标志'],
['denim','Denim','Denim','Denim','Denim','Jeans','Denim','牛仔布'],
['distressed','Used-Look','Délavé','Desgastado','Effetto vissuto','Desgastado','Przetarty','做旧'],
['collection','Kollektion','Collection','Colección','Collezione','Coleção','Kolekcja','系列'],
['women\x27s','Damen','Femme','Mujer','Donna','Feminino','Damskie','女士'],
['men\x27s','Herren','Homme','Hombre','Uomo','Masculino','Męskie','男士'],
['and','und','et','y','e','e','i','及'],
];
const columns:Record<Locale,number>={en:0,de:1,fr:2,es:3,it:4,pt:5,pl:6,zh:7};
const pattern=new RegExp('\\b('+rows.map(r=>r[0]).join('|')+')\\b','gi');
export function localizeProductName(name:string,locale:Locale){
 const normalized=name.replace(/t\s*-\s*shirts?/gi,word=>word.replace(/\s+/g,''))
  .replace(/(t[ -]?shirts?)(?=shorts?)/gi,'$1 / ')
  .replace(/(shorts?)(?=[A-Z]{2})/g,'$1 ')
  .replace(/(sweatshirts?)(?=t[ -]?shirt)/gi,'$1 ')
  .replace(/(t[ -]?shirts?)(?=short\s?sleeve)/gi,'$1 ')
  .replace(/(short\s?sleeves?)(?=tee)/gi,'$1 ')
  .replace(/(tees?)(?=pants)/gi,'$1 ')
  .replace(/(pants?)(?=zipper)/gi,'$1 ')
  .replace(/(zippers?)(?=set)/gi,'$1 ')
  .replace(/(\d)(?=colors?|colours?|styles?)/gi,'$1 ');
 if(locale==='en')return normalized.replace(/^shoes(?=-)/i,'Shoes');
 return normalized.replace(pattern,word=>{const entry=rows.find(r=>new RegExp('^(?:'+r[0]+')$','i').test(word));return entry?.[columns[locale]]||word;});
}
// Translate common local-language catalogue queries back into the source search vocabulary.
export function sourceSearchQuery(query:string){const clean=query.trim();for(const row of rows){if(row.slice(1).some(word=>word.toLocaleLowerCase()===clean.toLocaleLowerCase()))return row[0].split('|')[0].replace(/\??/g,'').replace(/\(.*?\)|\[.*?\]/g,'');}return clean;}
