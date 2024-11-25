<template>
  <div class="container">
    <h1 class="h1">은행 검색하기</h1>
    <div class="search-container">
      <button 
        @click="toggleSearchType('location')" 
        :class="['btn', searchType === 'location' ? 'btn-success active' : 'btn-secondary']"
      >
        내 위치 기반 은행 검색
      </button>
      <button 
        @click="toggleSearchType('area')" 
        :class="['btn', searchType === 'area' ? 'btn-success active' : 'btn-secondary']"
      >
        지역별 은행 검색
      </button>
    </div>
    
    <!-- 내 위치 기반 검색 -->
    <div v-if="searchType === 'location'" class="location-search">
      <input 
        type="text" 
        v-model="keyword" 
        placeholder="은행명을 입력하세요" 
        @keyup.enter="searchBanks" 
        style="width: 200px; padding: 8px; margin-right: 10px;"
      />
      <button @click="searchBanks" class="btn btn-warning">주변 은행 검색</button>
    </div>
    
    <!-- 지역별 검색 -->
    <div v-if="searchType === 'area'" class="area-search">
      <select v-model="selectedProvince" @change="loadCities">
        <option value="">특별시/광역시/도 선택</option>
        <option v-for="province in provinces" :key="province" :value="province">
          {{ province }}
        </option>
      </select>
      <select v-model="selectedCity" @change="loadDistricts" :disabled="!selectedProvince">
        <option value="">시/군/구 선택</option>
        <option v-for="city in cities" :key="city" :value="city">
          {{ city }}
        </option>
      </select>
      <select v-model="selectedDistrict" :disabled="!selectedCity">
        <option value="">동/면/읍 선택</option>
        <option v-for="district in districts" :key="district" :value="district">
          {{ district }}
        </option>
      </select>
      <button @click="searchBanksByArea" class="btn btn-warning">지역 은행 검색</button>
    </div>

    <div class="map-list-container">
      <div id="map"></div>
      <div v-if="showResults" class="search-results">
        <h3>검색 결과</h3>
        <div class="results-container">
          <ul>
            <li v-for="(place, index) in paginatedResults" 
                :key="index" 
                @click="moveToPlace(place)">
              <strong>{{ place.place_name }}</strong>
              <p>{{ place.address_name }}</p>
              <p>{{ place.phone }}</p>
            </li>
          </ul>
        </div>
        <div class="pagination" v-if="totalPages > 1">
          <button :disabled="currentPage === 1" @click="currentPage--">
            이전
          </button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="currentPage++">
            다음
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "KakaoMapBankSearch",
  data() {
    return {
      map: null,
      keyword: "",
      ps: null,
      markers: [],
      infowindow: null,
      currentPosition: null,
      searchResults: [],
      showResults: false,
      currentPage: 1,
      itemsPerPage: 8,
      selectedMarker: null,
      searchType: 'location',
      provinces: ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', 
                 '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', 
                 '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'],
      cities: [],
      districts: [],
      selectedProvince: '',
      selectedCity: '',
      selectedDistrict: ''
    };
  },
  mounted() {
    this.loadKakaoMap();
  },
  methods: {
    toggleSearchType(type) {
      this.searchType = type;
      this.clearSearch();
      
      if (type === 'location') {
        this.getCurrentPosition();
      } else {
        // 지역별 검색일 때는 서울 시청으로 초기 위치 설정
        const seoulCity = new window.kakao.maps.LatLng(37.5665, 126.9780);
        this.map.setCenter(seoulCity);
        this.map.setLevel(8); // 지도 레벨을 좀 더 넓게 설정
      }
    },

    getCurrentPosition() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            this.currentPosition = new window.kakao.maps.LatLng(
              position.coords.latitude,
              position.coords.longitude
            );
            this.map.setCenter(this.currentPosition);
            this.map.setLevel(4); // 현재 위치에 맞는 줌 레벨 설정
          },
          () => {
            alert("위치 정보를 가져올 수 없습니다.");
          }
        );
      } else {
        alert("이 브라우저에서는 위치 정보를 지원하지 않습니다.");
      }
    },
    
    clearSearch() {
      this.keyword = '';
      this.selectedProvince = '';
      this.selectedCity = '';
      this.selectedDistrict = '';
      this.searchResults = [];
      this.showResults = false;
      this.clearMarkers();
    },

    loadCities() {
      // API를 통해 선택된 도/시의 시/군/구 목록을 가져오는 로직
      this.selectedCity = '';
      this.selectedDistrict = '';
      this.cities = []; // API 호출 결과로 업데이트
    },

    loadDistricts() {
      // API를 통해 선택된 시/군/구의 동/면/읍 목록을 가져오는 로직
      this.selectedDistrict = '';
      this.districts = []; // API 호출 결과로 업데이트
    },

    searchBanksByArea() {
      const searchKeyword = this.keyword ? `${this.keyword} 은행` : '은행';
      const searchArea = `${this.selectedProvince} ${this.selectedCity} ${this.selectedDistrict}`.trim();
      
      const options = {
        location: this.map.getCenter(),
        radius: 20000,
        sort: window.kakao.maps.services.SortBy.DISTANCE
      };

      this.ps.keywordSearch(`${searchArea} ${searchKeyword}`, this.placesSearchCB, options);
    },
    loadKakaoMap() {
      const apiKey = import.meta.env.VITE_KAKAO_MAP_API_KEY
      const script = document.createElement("script")
      script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${apiKey}&libraries=services`
      script.onload = () => {
        window.kakao.maps.load(() => {
          const container = document.getElementById("map");
          const options = {
            center: new window.kakao.maps.LatLng(37.5665, 126.9780),
            level: 5,
          };
          this.map = new window.kakao.maps.Map(container, options);
          this.ps = new window.kakao.maps.services.Places();
          this.infowindow = new window.kakao.maps.InfoWindow({ zIndex: 1 });
          this.getCurrentPosition();
        });
      };
      document.head.appendChild(script);
    },
    searchBanks() {
      if (!this.currentPosition) {
        alert("현재 위치를 가져올 수 없습니다.");
        return;
      }
      const searchKeyword = this.keyword ? `${this.keyword} 은행` : '은행';
      const options = {
        location: this.currentPosition,
        radius: 2500,
        sort: window.kakao.maps.services.SortBy.DISTANCE
      };
      this.ps.keywordSearch(searchKeyword, this.placesSearchCB, options);
    },
    placesSearchCB(data, status, pagination) {
      if (status === window.kakao.maps.services.Status.OK) {
        this.clearMarkers();
        this.searchResults = data.filter(place => place.category_name.includes('은행'));
        if (this.searchResults.length > 0) {
          this.showResults = true;
          const bounds = new window.kakao.maps.LatLngBounds();
          this.searchResults.forEach(place => {
            this.displayMarker(place);
            bounds.extend(new window.kakao.maps.LatLng(place.y, place.x));
          });
          this.map.setBounds(bounds);
        } else {
          alert("검색된 은행이 없습니다. 다시 검색해 주세요.");
          this.showResults = false;
        }
      } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
        alert("검색 결과가 없습니다. 은행을 검색해 주세요.");
        this.showResults = false;
        this.searchResults = [];
      } else {
        alert("검색 중 오류가 발생했습니다.");
        this.showResults = false;
        this.searchResults = [];
      }
    },
    displayMarker(place) {
      const marker = new window.kakao.maps.Marker({
        map: this.map,
        position: new window.kakao.maps.LatLng(place.y, place.x),
      });
      this.markers.push(marker);

      window.kakao.maps.event.addListener(marker, "click", () => {
        this.selectMarker(place, marker);
      });
    },
    selectMarker(place, marker) {
      if (this.selectedMarker) {
        this.selectedMarker.setImage(null);
      }
      const redMarkerImage = new window.kakao.maps.MarkerImage(
        'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
        new window.kakao.maps.Size(31, 35)
      );
      marker.setImage(redMarkerImage);
      this.selectedMarker = marker;
      this.showInfoWindow(place, marker);
    },
    showInfoWindow(place, marker) {
      this.infowindow.setContent(`
        <div style="padding:5px;font-size:12px;">
          ${place.place_name}<br>
          ${place.address_name}<br>
          ${place.phone}
        </div>
      `);
      this.infowindow.open(this.map, marker);
    },
    clearMarkers() {
      this.markers.forEach(marker => marker.setMap(null));
      this.markers = [];
      if (this.selectedMarker) {
        this.selectedMarker.setImage(null);
        this.selectedMarker = null;
      }
    },
    moveToPlace(place) {
  const moveLatLon = new window.kakao.maps.LatLng(place.y, place.x);
  this.map.setCenter(moveLatLon);
  
  // 기존 마커와 인포윈도우 제거
  if (this.selectedMarker) {
    this.selectedMarker.setMap(null);
  }
  if (this.infowindow) {
    this.infowindow.close();
  }
  
  // 노란색 별표 마커 이미지 생성
  const starMarkerImage = new window.kakao.maps.MarkerImage(
    'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
    new window.kakao.maps.Size(31, 35)
  );
  
  // 새로운 마커 생성 및 노란색 별표 이미지 적용
  const marker = new window.kakao.maps.Marker({
    map: this.map,
    position: moveLatLon,
    image: starMarkerImage
  });
  
  // 인포윈도우 생성
  const infowindow = new window.kakao.maps.InfoWindow({
    content: `
      <div style="padding:5px;font-size:12px;">
        <strong>${place.place_name}</strong><br>
        ${place.address_name}<br>
        ${place.phone}
      </div>
    `
  });
  
  window.kakao.maps.event.addListener(marker, 'click', () => {
    infowindow.open(this.map, marker);
  });
  
  marker.setMap(this.map);
  infowindow.open(this.map, marker);
  
  this.selectedMarker = marker;
  this.infowindow = infowindow;
  
  this.map.setLevel(3);
}
  },
  computed: {
    totalPages() {
      return Math.ceil(this.searchResults.length / this.itemsPerPage);
    },
    paginatedResults() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.searchResults.slice(start, end);
    }
  },
  watch: {
    searchResults() {
      this.currentPage = 1; // 새로운 검색 결과가 있을 때 첫 페이지로 리셋
    }
  }
};

</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 600px;
  margin: 20px 20px 120px 20px;
}

.h1,p{
  margin: 0;
  padding: 5px;
}

.map-list-container {
  display: flex;
  position: relative;
  height: 500px;
}

#map {
  width: 100% !important;
  height: 500px !important;
}

.search-results {
  width: 300px;
  height: 500px;
  background-color: white;
  border-left: 1px solid #ccc;
  box-shadow: -2px 0 6px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}

.results-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.search-results h3 {
  padding: 10px;
  margin: 0;
  border-bottom: 1px solid #eee;
}

.search-results ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.search-results li {
  cursor: pointer;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.search-results li:hover {
  background-color: #f0f0f0;
}

.pagination {
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #eee;
}

.pagination button {
  padding: 5px 10px;
  cursor: pointer;
}

.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.pagination span {
  font-size: 14px;
}

.location-search, .area-search {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

select {
  padding: 8px;
  margin-right: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
}

.btn-warning {
  background-color: #ffc107;
  color: #000;
}

.btn {
  padding: 10px 20px;
  margin: 0 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn.active {
  transform: scale(1.05);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.search-container {
  display: flex;
  justify-content: left;
  gap: 10px;
  margin: 20px 0;
}

</style>