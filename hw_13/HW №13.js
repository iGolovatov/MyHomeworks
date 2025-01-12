
const weatherApiKey = `40912d1f0b06c30fcf43559380d37f53`;

const cityInput = document.getElementById('cityInput');
const searchButton = document.getElementById('searchButton');

// Функция для получения данных о погоде и качестве воздуха
async function getWeatherAndAirQualityData(cityName) {
  const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${weatherApiKey}&units=metric`;
  const response = await fetch(apiUrl);

  if (!response.ok) {
    throw new Error(`Ошибка получения данных: ${cityName}`); 
  }

  const weatherData = await response.json();

  const { lat, lon } = weatherData.coord; 

  const airQualityUrl = `https://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=${weatherApiKey}`;
  const airQualityResponse = await fetch(airQualityUrl);

  if (!airQualityResponse.ok) {
    throw new Error(`Ошибка получения данных о качестве воздуха: ${cityName}`); 
  }

  const airQualityData = await airQualityResponse.json();

  return { weatherData, airQualityData };
}

// Функция для отображения данных
async function displayWeatherAndAirQuality(cityName) {
  try {
    const { weatherData, airQualityData } = await getWeatherAndAirQualityData(cityName);

    // Отображение данных о погоде
    const { main: { temp, feels_like }, weather: [{ description }] } = weatherData;
    document.getElementById('weatherData').innerHTML = `<h2>Погода в городе  ${cityName}</h2>
      <p>Температура: ${temp.toFixed(1)}°C</p>
      <p>Ощущается как: ${feels_like.toFixed(1)}°C</p>
      <p>Описание: ${description}</p>`;

    // Отображение данных о качестве воздуха
    const { list: [{ main: { aqi } }] } = airQualityData;
    document.getElementById('airQualityData').innerHTML = `<h2>Качество воздуха в  городе ${cityName}</h2>
      <p>AQI: ${aqi}</p>`;

    // Сохранение города в localStorage
    localStorage.setItem('lastCity', cityName);
  } catch (error) {
    console.error(error);
    alert(error.message);
  }
}

// Обработчик события для кнопки "Поиск"
searchButton.addEventListener('click', () => {
  const cityName = cityInput.value;
  displayWeatherAndAirQuality(cityName);
});

// Обработчик события для кнопки "Поиск"( первая с большой буквы всегда, остальные в нижнем)
searchButton.addEventListener('click', () => {
    const cityName = cityInput.value;
    const formattedCityName = cityName.charAt(0).toUpperCase() + cityName.slice(1).toLowerCase();
   
    displayWeatherAndAirQuality(formattedCityName);
   });


   // При загрузке страницы проверяем последний сохраненный город
document.addEventListener('DOMContentLoaded', () => {
  const lastCity = localStorage.getItem('lastCity');
  
  if (lastCity) {
    // Устанавливаем значение последнего города в поле ввода
    cityInput.value = lastCity;
    
    // Автоматически загружаем погоду для последнего города
    displayWeatherAndAirQuality(lastCity);
  }
});