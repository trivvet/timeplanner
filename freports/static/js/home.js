function initMap() {
    // The location of Uluru
    var uluru = {lat: 49.426805, lng: 26.984316};
    // The map, centered at Uluru
    var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 16, center: uluru});
    // The marker, positioned at Uluru
    var marker = new google.maps.Marker({position: uluru, map: map});
}

$(document).ready(function(){
    initMap();
})