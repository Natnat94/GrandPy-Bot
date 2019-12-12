const platform = new H.service.Platform({"app_id": "W82jOVCtSiQ4dZHBaU8e","app_code": "2J6YA4nvRMB_IHJlwo7uXQ"});
const map = new H.Map(document.getElementById("map"),platform.createDefaultLayers().normal.map,{zoom: 15,center: { lat: 48.85824, lng: 2.2945 }});
const mapEvent = new H.mapevents.MapEvents(map);
const mapBehavior = new H.mapevents.Behavior(mapEvent);
const marker = new H.map.Marker({ lat: 48.85824, lng: 2.2945 });
map.addObject(marker);
var x = document.getElementById( "map" )

// Exécute un appel AJAX POST
// Prend en paramètres l'URL cible, la donnée à envoyer et la fonction callback appelée en cas de succès
function ajaxPost(url, data, callback) {
    var req = new XMLHttpRequest();
    req.open("POST", url);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            // Appelle la fonction callback en lui passant la réponse de la requête
            callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url);
        }
    });
    req.addEventListener("error", function () {
        console.error("Erreur réseau avec l'URL " + url);
    });
    req.send(data);
}


var form = document.querySelector("form");
// Gestion de la soumission du formulaire
form.addEventListener("submit", function (e) {
    e.preventDefault();
    // Récupération des champs du formulaire dans l'objet FormData
    var data = new FormData(form);
    // Envoi des données du formulaire au serveur
    // La fonction callback est ici vide
    ajaxPost("/api", data, function (response) {
        // Affichage dans la console en cas de succès
        console.log("Commande envoyée au serveur");
        var places = response["result"];
        for (var p in places) {
            console.error(p)
            var thumbnail = places[p].thumbnail || no_thumb;

            x.innerHTML += "<div class=\"item\"><div class=\"col-xs-8 no-padding\"><h5><a href=\"" +
                places[p]["articleUrl"] + "\" target=\"_blank\">" +
                places[p]["title"] + "</a></h5><p>" +
                places[p]["description"] + "</p><span>📍" +
                " miles</p></div><div class=\"col-xs-4 no-padding\"><img src=\"" +
                thumbnail + " \"></div></div>";
        }
        });
});
