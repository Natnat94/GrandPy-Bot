var x = document.getElementById("display")
// <<-------- Definis la fonction ajaxPost --------->>
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

function display(obj){
    var resultat = obj.result.wiki;
    x.innerHTML += "<div class=\"container\"><img src=\"../static/image/bandmember.jpg\" alt=\"Avatar\" style=\"width:100%;\"><p> Voici l'adresse que tu recherche: "+ obj.result.address + "</p></div>";
    var no_thumb = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Gnome-image-missing.svg/200px-Gnome-image-missing.svg.png";
    var thumbnail = resultat[0].thumbnail || no_thumb;
    // affichage de la reponse dans la page de maniere visuelle
    x.innerHTML += "<div class=\"container\"> <img src=\"../static/image/bandmember.jpg\" alt=\"Avatar\" style=\"width:100%;\"><div class=\"response\"><p>" + resultat[0]["abstract"] + "</p><img src=\"" + resultat[0]["thumbnail"] + "\"id=\"wikip\" alt=\"wikipedia\"></div>";    
}

// formulaire texte et envoie a flask en POST
var form = document.querySelector("form");
// Gestion de la soumission du formulaire
form.addEventListener("submit", function (e) {
    e.preventDefault();
    // Récupération des champs du formulaire dans l'objet FormData
    var data = new FormData(form);
    // Envoi des données du formulaire au serveur
    ajaxPost("/map", data, function (response) {
        // Affichage dans la console en cas de succès
        console.log("Commande envoyée au serveur");
        // transformation a partir d'un JSON
        var obj = JSON.parse(response);
        var question = data.get('Text1');
        // affichage de la question de maniere visuelle
        x.innerHTML += "<div class=\"container darker\"><img src=\"../static/image/avatar_g2.jpg\" alt=\"Avatar\" class=\"right\" style=\"width:100%;\"><p>" + question + "</p></div>";
        console.log(question);
        console.log(obj.result.here);
        console.log(obj.result.address);
        var localisation = obj.result.here;
        var latitude = localisation[0];
        var longitude = localisation[1];
        const platform = new H.service.Platform({ "app_id": "W82jOVCtSiQ4dZHBaU8e", "app_code": "2J6YA4nvRMB_IHJlwo7uXQ" });
        const map = new H.Map(document.getElementById("map"), platform.createDefaultLayers().normal.map, { zoom: 17, center: { lat: latitude, lng: longitude } });
        const mapEvent = new H.mapevents.MapEvents(map);
        const mapBehavior = new H.mapevents.Behavior(mapEvent);
        const marker = new H.map.Marker({ lat: latitude, lng: longitude });
        map.addObject(marker);
        display(obj);
    });
});