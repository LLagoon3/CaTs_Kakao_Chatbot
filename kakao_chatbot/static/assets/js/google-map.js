function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: { lat: YOUR_LATITUDE, lng: YOUR_LONGITUDE },
          zoom: 14
        });
        var marker = new google.maps.Marker({
          position: { lat: YOUR_LATITUDE, lng: YOUR_LONGITUDE },
          map: map,
          title: 'Your Location'
        });
      }