const proxyurl = "https://cors-anywhere.herokuapp.com/"; //indispensable pour l'API de Saba
// const url = "https://becode-predict-ades.herokuapp.com/predict"; //API Saba
// {"0":{"property-type":"APARTMENT","rooms-number":2,"zip-code":1000,"full-address":"","facades-number":2,"area":150}} // API Saba

const url = "http://roberta-eliza.herokuapp.com/predict"; //API Luis



document.querySelector("#go").addEventListener("click",function(event){
    document.querySelectorAll(".error").forEach(element => {
        element.remove()
    });

    event.preventDefault();

    let propertytype = document.querySelector("#type").value;
    let area = parseInt(document.querySelector("#area").value);
    let rooms = parseInt(document.querySelector("#room").value);
    let zipcode = parseInt(document.querySelector("#zip").value);
    let garden =  Boolean(document.querySelector("#garden").value);
    let kitchen =  Boolean(document.querySelector("#kitchen").value);
    let swimmingpool = Boolean(document.querySelector("#swimmingpool").value);
    let terrace =  Boolean(document.querySelector("#terrace").value);
    let state = document.querySelector("#state").value;

    // console.log(area);
    // console.log(zipcode);
    // console.log(rooms);
    // console.log(propertytype);
    // console.log(garden);
    // console.log(kitchen);
    // console.log(swimmingpool);
    // console.log(terrace);
    // console.log(state);

    if (document.querySelector("#area").value == false) {
        document.querySelector("#divarea").insertAdjacentHTML("afterend",`<p class="error" style="color:red">veuillez remplir ce champ</p>`)
    }
    if (document.querySelector("#zip").value == false || zipcode < 1000 || zipcode > 9999 ){
        document.querySelector("#divzip").insertAdjacentHTML("afterend",`<p class="error" style="color:red">veuillez remplir ce champ avec un code postal valable (en quatre chiffres)</p>`)
    }
    if (document.querySelector("#room").value == false) {
        document.querySelector("#divroom").insertAdjacentHTML("afterend",`<p class="error" style="color:red">veuillez remplir ce champ</p>`)
    }
    if (document.querySelector("#area").value != false && document.querySelector("#zip").value != false && document.querySelector("#room").value != false && zipcode >= 1000 && zipcode <= 9999 ){

        let info = {
            data:{
                // "property-type": "APARTMENT", //API Saba
                "property-type": propertytype,
                "area": area,
                "rooms-number": rooms,
                "zip-code": zipcode,
                "garden": garden,
                "equipped-kitchen": kitchen,
                "swimmingpool": swimmingpool,
                "terrace": terrace,
                "building-state": state,
                "full-address":"",
                "facades-number":2
            }
        }
        
        fetch(proxyurl + url, {
            method: 'POST', 
            body: JSON.stringify(info), 
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // document.querySelector("#go").insertAdjacentHTML("afterend",`<p id="price">price: ${data.prediction[0]} € </p>`) //API Saba
            document.querySelector("#go").insertAdjacentHTML("afterend",`<p id="price">price: ${data.prediction.price} € </p>`)

        })
        .catch(() => console.log("Can’t access " + url + " response. Blocked by browser?"))     
    }else{
        document.querySelector("#go").insertAdjacentHTML("afterend",`<p class="error" style="color:red">veuillez remplir correctement tous les champs</p>`)
    }   
})

