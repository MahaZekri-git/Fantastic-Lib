// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

window.addEventListener('load',(event)=>{
    console.log('page is fully loaded')
    function get_books(){
        fetch('http://127.0.0.1:8000/books/book_list')
        .then(response=>response.body)
        .then(data=>{console.log(data)})
    }
    get_books()
})


