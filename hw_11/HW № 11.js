let apiAnswer = {
    coord: { lon: 37.6156, lat: 55.7522 },
    weather: [
      { id: 804, main: "Clouds", description: "пасмурно", icon: "04n" },
    ],
    base: "stations",
    main: {
      temp: 8.12,
      feels_like: 6.25,
      temp_min: 7.24,
      temp_max: 8.52,
      pressure: 1025,
      humidity: 80,
      sea_level: 1025,
      grnd_level: 1005,
    },
    visibility: 10000,
    wind: { speed: 3.01, deg: 247, gust: 7.69 },
    clouds: { all: 100 },
    dt: 1729952527,
    sys: {
      type: 2,
      id: 2094500,
      country: "RU",
      sunrise: 1729916600,
      sunset: 1729951403,
    },
    timezone: 10800,
    id: 524901,
    name: "Москва",
    cod: 200,
  };

    const divResult = document.getElementById('divResult');
    const weatherBtn = document.getElementById('weatherBtn');

function getClearWeatherObject(weatherObj) {
    return {
        temp: weatherObj.main.temp,
        feels_like: weatherObj.main.feels_like,
        pressure: weatherObj.main.pressure,
        humidity: weatherObj.main.humidity,
        windSpeed: weatherObj.wind.speed,
        cityName: weatherObj.name
    }
}

function displayP(text, parent) {
    let p = document.createElement('p')
    p.innerText = text
    parent.append(p)
}

function displayWeather(weatherObj) {
    let h1 = document.querySelector('h1');
    divResult.innerHTML = ''
    h1.innerText = 'Погода в городе ....'

    let weather = getClearWeatherObject(weatherObj);

    h1.innerText = weather.cityName;
    displayP(`Температура: ${weather.temp}`, divResult);
    displayP(`Ощущается как: ${weather.feels_like}`, divResult);
    displayP(`Давление: ${weather.pressure}`, divResult);
    displayP(`Влажность: ${weather.humidity}`, divResult);
    displayP(`Скорость ветра: ${weather.windSpeed}`, divResult);
    displayP(`Город: ${weather.cityName}`, divResult);
}

weatherBtn.addEventListener('click', () => {
    displayWeather(apiAnswer)
})


