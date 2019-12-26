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

function display(obj) {
    buildAnswerBox(x, obj.robot, obj.address, obj);
}

function buildQuestionBox(display, avatar_url, question) {
    // Création du container
    let containerElt = document.createElement("div");
    containerElt.classList.add("container", "darker");
    display.appendChild(containerElt);

    // Création de l'élement image
    let avatarElt = document.createElement("img");
    avatarElt.src = avatar_url;
    avatarElt.alt = "Avatar";
    avatarElt.classList.add("right", "avatar");
    containerElt.appendChild(avatarElt);

    // Création du paragraphe
    let paragraphElt = document.createElement("p");
    paragraphElt.textContent = question;
    containerElt.appendChild(paragraphElt);
}

function buildAnswerBox(display, avatar_url, address, obj) {
    var resultat = obj.wiki;
    // Création du container
    let containerElt = document.createElement("div");
    containerElt.classList.add("container");
    display.appendChild(containerElt);

    let boite = document.createElement("div");
    boite.classList.add("message");
    containerElt.appendChild(boite);

    // Création de l'élement image
    let avatarElt = document.createElement("img");
    avatarElt.src = avatar_url;
    avatarElt.alt = "Avatar";
    avatarElt.classList.add("avatar");
    boite.appendChild(avatarElt);

    // Création du paragraphe
    let paragraphElt = document.createElement("p");
    paragraphElt.textContent = " Voici l'adresse que tu recherche: " + address;
    boite.appendChild(paragraphElt);

    let mapElt = document.createElement("div");
    mapElt.setAttribute("id", "map");
    containerElt.appendChild(mapElt);
    createMap(obj, mapElt);

    let parapar = document.createElement("div");
    parapar.classList.add("container");
    display.appendChild(parapar);

    let avatar = document.createElement("img");
    avatar.src = avatar_url;
    avatar.alt = "Avatar";
    avatar.classList.add("avatar");
    parapar.appendChild(avatar);

    let para = document.createElement("div");
    para.classList.add("response");
    parapar.appendChild(para);

    let yeo = document.createElement("p");
    yeo.textContent = resultat[0]["abstract"];
    para.appendChild(yeo);

    let imi = document.createElement("img");
    var no_thumb = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Gnome-image-missing.svg/200px-Gnome-image-missing.svg.png";
    var thumbnail = resultat[0].thumbnail || no_thumb;
    imi.src = thumbnail;
    imi.alt = "wikipedia";
    imi.setAttribute("id", "wikip");
    para.appendChild(imi);
}

function createMap(obj, mapElt) {
    var localisation = obj.here;
    var latitude = localisation[0];
    var longitude = localisation[1];
    const platform = new H.service.Platform({
        app_id: "W82jOVCtSiQ4dZHBaU8e",
        app_code: "2J6YA4nvRMB_IHJlwo7uXQ",
        useHTTPS: true,
        useCIT: true
    });
    const map = new H.Map(mapElt, platform.createDefaultLayers().normal.map, { zoom: 17, center: { lat: latitude, lng: longitude } });
    const mapEvent = new H.mapevents.MapEvents(map);
    const mapBehavior = new H.mapevents.Behavior(mapEvent);
    const marker = new H.map.Marker({ lat: latitude, lng: longitude });
    map.addObject(marker);

}

// formulaire texte et envoie a flask en POST
var form = document.querySelector("form");
// Gestion de la soumission du formulaire
form.addEventListener("submit", function (e) {
    e.preventDefault();
    // Récupération des champs du formulaire dans l'objet FormData
    var data = new FormData(form);
    // Envoi des données du formulaire au serveur
    ajaxPost("/api", data, function (response) {
        // Affichage dans la console en cas de succès
        console.log("Commande envoyée au serveur");
        // transformation a partir d'un JSON
        var obj = JSON.parse(response);
        var question = data.get('Text1');
        // affichage de la question de maniere visuelle
        buildQuestionBox(x, obj.avatar, question)

        var status = obj.status;
        if (status == 'true') {
            display(obj);
        } else {
            x.innerHTML += "<div class=\"container\"> <img src=\"" + obj.robot + "\" alt=\"Avatar\" style=\"width:100%;\"><div class=\"response\"><p> je suis désolé mais je n'ai pas compris la question.. </p></div>";
        };
    });
});