var map = L.map('map').setView([-12.163200486951586, -53.51511964322111], 3);

// Mapa claro
var Stadia_AlidadeSmoothLight = L.tileLayer('https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=4wF6jQHaoE1IdtQRtvlG', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
}).addTo(map);
// mapa escuro

var Stadia_AlidadeSmoothDark = L.tileLayer('https://tile.jawg.io/jawg-dark/{z}/{x}/{y}{r}.png?access-token={accessToken}', {
    attribution: '<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    minZoom: 0,
    maxZoom: 22,
    accessToken: 'ecnC19divPdCgJbJ0vliyy40mHr9BwI3vVr3cU2bF8oC1RihP8qLlQGCWCeAqsL2'

});


// Adiciona um evento de clique ao botão "All"
var isIFAB = false;

// Adiciona um evento de clique ao botão "All"
document.getElementById('map-control-ifab').addEventListener('click', function () {
    // Alterna o estado da variável entre true e false
    isIFAB = !isIFAB;

    // Altera o texto do botão com base no estado atual da variável
    if (isIFAB) {
        this.textContent = 'All';
    } else {
        this.textContent = 'IFAB';
    }

    // Aqui você pode adicionar qualquer ação adicional que desejar quando o modo for alterado
});

var darkModeIcon = document.getElementById('dark-mode-icon');

// Adiciona um evento de mudança ao seletor de modo de mapa
document.getElementById('map-mode').addEventListener('change', function () {
    var selectedMode = this.value;
    console.log('Modo selecionado:', selectedMode);
    // Aqui você pode fazer o que for necessário com o modo selecionado
});

// Adiciona um evento de clique ao botão de alternar modo escuro/claro
document.getElementById('dark-mode-toggle').addEventListener('click', function () {
    if (map.hasLayer(Stadia_AlidadeSmoothLight)) {
        map.removeLayer(Stadia_AlidadeSmoothLight);
        map.addLayer(Stadia_AlidadeSmoothDark);
        darkModeIcon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sun" viewBox="0 0 16 16"><path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8M8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0m0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13m8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5M3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8m10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0m-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0m9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707M4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708"/></svg>';
    } else {
        map.removeLayer(Stadia_AlidadeSmoothDark);
        map.addLayer(Stadia_AlidadeSmoothLight);
        darkModeIcon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-moon" viewBox="0 0 16 16"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278M4.858 1.311A7.27 7.27 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.32 7.32 0 0 0 5.205-2.162q-.506.063-1.029.063c-4.61 0-8.343-3.714-8.343-8.29 0-1.167.242-2.278.681-3.286"/></svg>';
    }
});
var markerLayer = L.layerGroup().addTo(map);

// Função para configurar o valor padrão do seletor de modo de mapa
function setDefaultMapMode() {
    // Define o valor selecionado do seletor de modo de mapa para "expert"
    document.getElementById('map-mode').value = 'expert';

    // Dispara o evento change manualmente para acionar a ação correspondente
    var changeEvent = new Event('change');
    document.getElementById('map-mode').dispatchEvent(changeEvent);
}

// Adiciona um evento de carregamento da página para chamar a função setDefaultMapMode
window.addEventListener('load', setDefaultMapMode);

var sessionId = '';

const getDistanceInNauticalMiles = (lat1, lon1, lat2, lon2) => {
    const R = 3440.069; // Earth's radius in nautical miles
    const dLat = toRadians(lat2 - lat1);
    const dLon = toRadians(lon2 - lon1);
    lat1 = toRadians(lat1);
    lat2 = toRadians(lat2);

    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.sin(dLon / 2) ** 2 * Math.cos(lat1) * Math.cos(lat2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
};

// Calcula aprocemadamente a hora de chegada do destino final.
const calculateArrivalTime = (distance, speed) => {
    const secondsPerHour = 3600;
    const travelTimeInSeconds = distance / speed * secondsPerHour;
    const arrivalTime = new Date(Date.now() + travelTimeInSeconds * 1000);
    // Obter a hora e os minutos do tempo de chegada estimado
    const hours = arrivalTime.getHours();
    const minutes = arrivalTime.getMinutes();

    // Formatando a hora para garantir que tenha sempre dois dígitos
    const formattedHours = String(hours).padStart(2, '0');

    // Formatando os minutos para garantir que tenha sempre dois dígitos
    const formattedMinutes = String(minutes).padStart(2, '0');

    // Retornar a hora formatada no formato 'HH:mm'
    return `${formattedHours}:${formattedMinutes}`;
};


function toRadians(graus) {
    return graus * Math.PI / 180;
}

var currentPolyline = null; // Declare a variável fora da função para manter a referência à polyline

// Função para criar a polyline com os pontos e altitudes obtidos
function createPolyline(polylinePoints, altitudes) {
    // Se já houver uma polyline, remova-a antes de adicionar a nova
    if (currentPolyline) {
        map.removeLayer(currentPolyline);
    }

    // Função auxiliar para definir a cor baseado na altitude
    function getColorFromAltitude(altitude) {
        if (altitude < 3000) return '#FF0000'; // Vermelho para altitudes muito baixas
        if (altitude < 6000) return '#FF4500'; // Laranja avermelhado
        if (altitude < 9000) return '#FF7F00'; // Laranja
        if (altitude < 12000) return '#FFD700'; // Dourado
        if (altitude < 15000) return '#FFFF00'; // Amarelo
        if (altitude < 18000) return '#ADFF2F'; // Verde amarelado
        if (altitude < 21000) return '#00FF00'; // Verde
        if (altitude < 24000) return '#32CD32'; // Verde limão
        if (altitude < 27000) return '#00FA9A'; // Verde médio
        if (altitude < 30000) return '#00FFFF'; // Ciano
        if (altitude < 33000) return '#1E90FF'; // Azul dodger
        if (altitude < 36000) return '#0000FF'; // Azul
        return '#8A2BE2'; // Azul-violeta para altitudes muito altas
    }

    // Array para armazenar as polylines segmentadas
    const segments = [];

    for (let i = 0; i < polylinePoints.length - 1; i++) {
        const start = polylinePoints[i];
        const end = polylinePoints[i + 1];
        const altitude = altitudes[i];
        const color = getColorFromAltitude(altitude);

        // Cria um segmento da polyline com a cor baseada na altitude
        const segment = L.polyline([start, end], { color, weight: 2 }).addTo(map);
        segments.push(segment);
    }

    // Guarda os segmentos na variável currentPolyline para referência futura
    currentPolyline = L.layerGroup(segments).addTo(map);
}

// Função para atualizar o polyline
async function updatePolyline(sessionId, flightId, latitude, longitude, altitude) {
    const flightRouteUrl = `https://api.infiniteflight.com/public/v2/sessions/${sessionId}/flights/${flightId}/route?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw`;

    try {
        const routeResponse = await fetch(flightRouteUrl);
        const routeData = await routeResponse.json();

        const polylinePoints = routeData.result.map(point => [point.latitude, point.longitude]);
        const altitudes = routeData.result.map(point => point.altitude);

        // Adiciona a posição atual da aeronave como o último ponto
        polylinePoints.push([latitude, longitude]);
        altitudes.push(altitude);

        createPolyline(polylinePoints, altitudes);
    } catch (error) {
        console.error('Erro ao obter dados da rota:', error);
    }
}

const fetchATCData = async (sessionId) => {
    const atcurl = `https://api.infiniteflight.com/public/v2/sessions/${sessionId}/atc?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw`;
    const response = await fetch(atcurl);
    const data = await response.json();
    return data.result || [];
};



const fetchATIS = async (sessionId, airportName) => {
    const atisUrl = `https://api.infiniteflight.com/public/v2/sessions/${sessionId}/airport/${airportName}/atis?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw`;
    const atisResponse = await fetch(atisUrl);
    const atisData = await atisResponse.json();
    return atisData.result || [];
};

const fetchAirportStatus = async (sessionId, airportIcao) => {
    const statusUrl = `https://api.infiniteflight.com/public/v2/sessions/${sessionId}/airport/${airportIcao}/status?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw`;
    const statusResponse = await fetch(statusUrl);
    const statusData = await statusResponse.json();
    return statusData.result || {};
};


// Adiciona um evento de clique ao mapa
map.on('click', function (event) {
    // Verifica se o elemento clicado é um marcador
    if (!event.originalEvent.target.classList.contains('leaflet-marker-icon') &&
        !event.originalEvent.target.classList.contains('leaflet-interactive')) {
        // Se não for um marcador, retrai o sidebar
        document.getElementById('sidebar').classList.remove('show-sidebar');
        document.getElementById('atc-sidebar').classList.remove('show-sidebar');
    }
});

// Adiciona um evento de clique global para fechar o sidebar ao clicar fora dele
document.addEventListener('click', function (event) {
    const sidebar = document.getElementById('sidebar');
    const atcSidebar = document.getElementById('atc-sidebar');

    if (!sidebar.contains(event.target) && !atcSidebar.contains(event.target)) {
        sidebar.classList.remove('show-sidebar');
        atcSidebar.classList.remove('show-sidebar');
    }
});

/// Função para obter dados da API e atualizar os marcadores
async function updateMarkers() {
    try {
        const selectedMode = document.getElementById('map-mode').value;
        const sessionId = {
            'trainner': 'c6b11fef-3aaf-475c-9c17-5bf587438f84',
            'casual': 'ef55b332-8847-47eb-8846-e27bdf8a673b',
            'expert': '99917fd2-bea4-485d-b83e-5094628f33e5'
        }[selectedMode];

        if (!sessionId) {
            console.error('Modo de mapa selecionado inválido.');
            return;
        }

        // Mapeamento dos tipos de ATC para seus nomes
        const atcTypeNames = {
            0: "Ground",
            1: "Tower",
            2: "Unicom",
            3: "Clearance",
            4: "Approach",
            5: "Departure",
            6: "Center",
            7: "ATIS",
            8: "Aircraft",
            9: "Recorded",
            10: "Unknown",
            11: "Unused"
        };

        // Função para desenhar uma estrela de 4 pontas
        function drawStar(map, latlng, size, options) {
            const angle = Math.PI / 4;
            const points = [];
            for (let i = 0; i < 8; i++) {
                const radius = i % 2 === 0 ? size : size / 3; // Ajuste o raio das pontas menores para tornar a estrela mais fina
                points.push([
                    latlng.lat + radius * Math.cos(angle * i) * (180 / Math.PI) / 111320,
                    latlng.lng + radius * Math.sin(angle * i) * (180 / Math.PI) / (111320 * Math.cos(latlng.lat * (Math.PI / 180)))
                ]);
            }
            points.push(points[0]); // Fechar o polígono

            const star = L.polygon(points, options).addTo(map);
            return star;
        }

        // Buscar dados de ATC
        const atcData = await fetchATCData(sessionId);

        //console.log(atcData);

        // Limpa os círculos do ATC antes de adicionar novos
        map.eachLayer(function (layer) {
            if (layer instanceof L.Circle || layer instanceof L.Polygon) {
                map.removeLayer(layer);
            }
        });

        // Agrupar ATCs por aeroporto
        const atcByAirport = atcData.reduce((acc, atc) => {
            const { airportName } = atc;
            if (!acc[airportName]) {
                acc[airportName] = [];
            }
            acc[airportName].push(atc);
            return acc;
        }, {});



        for (const airportName in atcByAirport) {
            const atcs = atcByAirport[airportName];



            // Desenhe a estrela se houver mais de um ATC ativo no aeroporto
            const drawStarIfNeeded = (lat, lng) => {
                if (atcs.length > 1) {
                    drawStar(map, { lat, lng }, 325, { // Ajuste o tamanho para garantir que a estrela fique dentro do círculo
                        color: 'yellow',
                        fillColor: 'yellow',
                        fillOpacity: 0.5,
                        weight: 1
                    });
                }
            };

            for (const atc of atcs) {
                const { latitude, longitude, type } = atc;

                let markerColor, markerRadius;

                switch (type) {
                    case 0: // Ground
                        markerColor = '#1c186e';
                        markerRadius = 60000;
                        break;

                    case 1: // Tower
                        markerColor = 'red';
                        markerRadius = 18520;
                        break;
                    case 5:  // Departure
                    case 4: // Approach
                        markerColor = '#0959c1';
                        markerRadius = 33333;
                        break;

                    default: // Other types
                        markerColor = '#1c186e';
                        markerRadius = 5000;
                }

                // Desenhar a estrela antes de adicionar círculos, exceto para Ground (tipo 7)
                if (type === 1) {
                    drawStarIfNeeded(latitude, longitude);
                }

                const circle = L.circle([latitude, longitude], {
                    color: markerColor,
                    fillColor: markerColor,
                    fillOpacity: 0.05,
                    radius: markerRadius,
                    weight: 1 // Valor da largura da borda reduzido
                }).addTo(map);



                // Adiciona um evento de clique aos círculos do ATC
                circle.on('click', function (event) {
                    event.originalEvent.stopPropagation(); // Interrompe a propagação do evento de clique

                    // Fecha o sidebar do avião, se estiver aberto
                    document.getElementById('sidebar').classList.remove('show-sidebar');

                    document.getElementById('NameAirpot').innerHTML = airportName;

                    // Mapear tipos de ATC ativos
                    const activeAtcs = atcs.map(atc => atcTypeNames[atc.type] || "Unknown").join(', ');
                    document.getElementById('type').innerHTML = `ATCs Ativos: ${activeAtcs}`;

                    // Abre o sidebar do ATC
                    document.getElementById('atc-sidebar').classList.toggle('show-sidebar');
                });
            }

            // Desenhar círculos Ground (tipo 7) por último para garantir que fiquem na frente da estrela
            for (const atc of atcs) {
                const { latitude, longitude, type } = atc;

                if (type === 7) {
                    const circle = L.circle([latitude, longitude], {
                        color: 'darkblue',
                        fillColor: 'darkblue',
                        fillOpacity: 0.05,
                        radius: 60000,
                        weight: 1 // Valor da largura da borda reduzido
                    }).addTo(map);

                    // Adiciona um evento de clique aos círculos do ATC
                    circle.on('click', async function (event) {
                        try {
                            event.originalEvent.stopPropagation(); // Interrompe a propagação do evento de clique

                            // Fecha o sidebar do avião, se estiver aberto
                            document.getElementById('sidebar').classList.remove('show-sidebar');

                            document.getElementById('NameAirpot').innerHTML = airportName;

                            // Mapear tipos de ATC ativos
                            const activeAtcs = atcs.map(atc => atcTypeNames[atc.type] || "Unknown").join(', ');
                            document.getElementById('type').innerHTML = activeAtcs;

                            // Limpar o conteúdo do campo de ATIS antes de adicionar novas informações
                            document.getElementById('atis').innerHTML = '';

                            const atisData = await fetchATIS(sessionId, airportName);
                            document.getElementById('atis').innerHTML += atisData.length > 0 ? atisData : 'ATIS não encontrado';

                            const airportStatus = await fetchAirportStatus(sessionId, airportName);

                            // Atualizar contadores
                            document.getElementById('inboundFlightsCount').innerText = airportStatus.inboundFlightsCount;
                            document.getElementById('outboundFlightsCount').innerText = airportStatus.outboundFlightsCount;

                            // Limpar campo de usernames antes de adicionar novas informações
                            document.getElementById('atcUsername').innerHTML = '';

                            // Comparar frequencyId com frequencia e exibir usernames
                            const atcTypeName = {
                                0: "Ground",
                                1: "Tower",
                                2: "Unicom",
                                3: "Clearance",
                                4: "Approach",
                                5: "Departure",
                                6: "Center",
                                7: "ATIS",
                                8: "Aircraft",
                                9: "Recorded",
                                10: "Unknown",
                                11: "Unused"
                            };

                            // Certifique-se de que o campo está limpo antes de adicionar novas informações
                            document.getElementById('atcUsername').innerHTML = '';

                            airportStatus.atcFacilities.forEach(atc => {
                                const atcType = atcTypeName[atc.type]; // Obtenha o nome do tipo de ATC
                                if (atcType) {
                                    document.getElementById('atcUsername').innerHTML += `${atcType} - ${atc.username} <br>`;
                                }
                            });
                            // Abre o sidebar do ATC
                            document.getElementById('atc-sidebar').classList.toggle('show-sidebar');
                        } catch (error) {
                            console.error('Erro ao carregar dados do ATC:', error);
                            document.getElementById('atis').innerHTML = 'Erro ao carregar ATIS';
                        }
                    });

                }
            }
        }




        const apiUrl = `https://api.infiniteflight.com/public/v2/sessions/${sessionId}/flights?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw`;

        const response = await fetch(apiUrl);
        const data = await response.json();

        if (!data.result || data.result.length === 0) {
            console.error('Nenhum resultado encontrado no JSON retornado pela API.');
            return;
        }

        markerLayer.clearLayers();

        async function userstatus(userid) {
            try {
                const paramentro = { userIds: [userid] };
                const headers = { 'Content-type': 'application/json', Accept: 'text/plain' };
                const url = 'https://api.infiniteflight.com/public/v2/user/stats?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw';

                const response = await fetch(url, {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(paramentro)
                });

                const data = await response.json();
                return data.result;
            } catch (error) {
                console.error('Ocorreu um erro:', error);
                return null;
            }
        }

        const aircraftImageMap = {
            // Aeronaves GA
            '8bafde46-7e6e-44c5-800f-917237c49d75': 'https://i.ibb.co/f4CQhG3/C172.png', // CubCrafters XCub
            '3f17ca35-b384-4391-aa5e-5beececb0612': 'https://i.ibb.co/f4CQhG3/C172.png', // TBM-930
            'e92bc6db-a9e6-4137-a93c-a7423715b799': 'https://i.ibb.co/f4CQhG3/C172.png', // Cirrus SR22 GTS
            '206884f9-38a8-4118-a920-a7dcbd166c47': 'https://i.ibb.co/f4CQhG3/C172.png', // Cessna 208
            'ef677903-f8d3-414f-a190-233b2b855d46': 'https://i.ibb.co/f4CQhG3/C172.png', // Cesna 175

            // Aeronaves Tubor Helice
            '3098345e-1152-4441-96ec-40a71179a24f': 'https://i.ibb.co/YNCDzLB/DH8D.png', // Dash8

            // Aeronave militar
            '0a3edb21-d515-4619-8392-aef51b952ac9': 'https://i.ibb.co/rdZt0cN/F22.png', // F/A-18E Super Hornet
            '81d9ccd4-9c03-493a-811e-8fad3e57bd05': 'https://i.ibb.co/rdZt0cN/F22.png', // A-10
            '8a62f1d0-bca9-494c-bc01-1fb8b7255f76': 'https://i.ibb.co/rdZt0cN/F22.png', // Spitfire
            '849366e1-cb11-4d72-9034-78b11cd026b0': 'https://i.ibb.co/rdZt0cN/F22.png', // F-22
            '7bd8096f-8eae-47b9-8e1a-38dabd2c59c4': 'https://i.ibb.co/rdZt0cN/F22.png', // F-16
            '9bbe741a-6fbe-415b-9eb1-00d45083c7a4': 'https://i.ibb.co/rdZt0cN/F22.png', // F-16
        };

        // Dentro do loop para criar os marcadores
        for (const session of data.result) {
            const { latitude, longitude, heading, callsign, aircraftId, userId } = session;
            let customIcon = L.icon({  // Define customIcon aqui
                iconUrl: 'https://i.ibb.co/zXmYPYf/airplane-1.png',
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            });

            // Verifica se o ID da aeronave está mapeado
            if (aircraftImageMap.hasOwnProperty(aircraftId)) {
                // Se estiver mapeado, atualiza a URL da imagem do marcador
                customIcon = L.icon({
                    iconUrl: aircraftImageMap[aircraftId],
                    iconSize: [32, 32],
                    iconAnchor: [16, 16],
                    popupAnchor: [0, -16]
                });
            }

            const marker = L.marker([latitude, longitude], { icon: customIcon, rotationAngle: heading }).addTo(markerLayer);

            marker.on('click', async function () {
                const flightRouteUrl = `https://api.infiniteflight.com/public/v2/sessions/${sessionId}/flights/${session.flightId}/route?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw`;
                const flightInfoUrl = `https://api.infiniteflight.com/public/v2/sessions/${sessionId}/flights/${session.flightId}/flightplan?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw`;

                try {
                    const [routeResponse, flightInfoResponse] = await Promise.all([
                        fetch(flightRouteUrl),
                        fetch(flightInfoUrl)
                    ]);

                    const routeData = await routeResponse.json();
                    const flightInfo = await flightInfoResponse.json();

                    const flightPlanItems = flightInfo.result.flightPlanItems;
                    const flightPlanNames = flightPlanItems.map(item => item.name).join(', ');

                    document.getElementById('flightplan').innerHTML = flightPlanNames;

                    const polylinePoints = routeData.result.map(point => [point.latitude, point.longitude]);
                    const altitudes = routeData.result.map(point => point.altitude);

                    // Adiciona a posição atual da aeronave como o último ponto
                    polylinePoints.push([latitude, longitude]);
                    altitudes.push(session.altitude);

                    createPolyline(polylinePoints, altitudes);

                    const infoDep = flightPlanItems[0];
                    const infoArr = flightPlanItems[flightPlanItems.length - 1];

                    const totalDistance = getDistanceInNauticalMiles(
                        infoDep.location.latitude,
                        infoDep.location.longitude,
                        infoArr.location.latitude,
                        infoArr.location.longitude
                    );

                    const distance = getDistanceInNauticalMiles(
                        latitude,
                        longitude,
                        infoArr.location.latitude,
                        infoArr.location.longitude
                    );

                    const currentDistance = getDistanceInNauticalMiles(
                        latitude,
                        longitude,
                        infoDep.location.latitude,
                        infoDep.location.longitude
                    );

                    function convertMinutesToHoursAndMinutes(minutes) {
                        const hours = Math.floor(minutes / 60);
                        const remainingMinutes = minutes % 60;
                        return { hours, remainingMinutes };
                    }

                    const percentageTraveled = (currentDistance / totalDistance) * 100;
                    const estimatedArrivalTime = calculateArrivalTime(distance, session.speed);
                    const formattedDistance = distance.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 }) + 'mn';

                    const nomeDoUsuario = userId; // Substitua pelo nome de usuário desejado
                    const resultado = await userstatus(nomeDoUsuario);

                    const flightTime = resultado[0].flightTime;
                    const { hours, remainingMinutes } = convertMinutesToHoursAndMinutes(flightTime);



                    // Sidebar referente ao marcado dos aviaoes

                    document.getElementById('flightNumber').innerHTML = callsign;
                    document.getElementById('infoDep').innerHTML = infoDep.identifier;
                    document.getElementById('infoArr').innerHTML = infoArr.identifier;
                    document.getElementById('AltitudeInfo').innerHTML = 'FL' + session.altitude.toFixed(0).substring(0, 3);
                    document.getElementById('velocidadeInfo').innerHTML = 'FT' + session.speed.toFixed(0).substring(0, 3);
                    document.getElementById('DistanciaMilasInfo').innerHTML = formattedDistance;
                    document.getElementById('ETA').innerHTML = estimatedArrivalTime;
                    document.getElementById('Username').innerHTML = resultado[0].discourseUsername;
                    document.getElementById('virtualOrganization').innerHTML = resultado[0].virtualOrganization;
                    document.getElementById('xp').innerHTML = "XP: " + resultado[0].xp;

                    document.getElementById('flightTime').innerHTML = `Flight time: ${hours}:${remainingMinutes}`;
                    document.getElementById('grade').innerHTML = "grade: " + resultado[0].grade;
                    document.getElementById('onlineFlights').innerHTML = resultado[0].onlineFlights;

                    const progressBar = document.querySelector('.progress-bar');
                    progressBar.style.transition = 'none';
                    progressBar.style.width = percentageTraveled + '%';
                    progressBar.setAttribute('aria-valuenow', percentageTraveled);
                    const svgIcon = document.querySelector('.MuiSvgIcon-root');
                    svgIcon.style.marginLeft = (percentageTraveled - 7) + '%';

                    document.getElementById('sidebar').classList.add('show-sidebar');

                    function updateProgressBar() {
                        percentageTraveled += 10;
                        if (percentageTraveled > 100) {
                            percentageTraveled = 100;
                        }

                        progressBar.style.width = percentageTraveled + '%';
                        progressBar.setAttribute('aria-valuenow', percentageTraveled);
                    }

                    updateProgressBar();
                    setTimeout(updateProgressBar, 5000);
                } catch (error) {
                    console.error('Erro ao obter dados da API:', error);
                }
            });
        }
    } catch (error) {
        console.error('Erro ao obter dados da API:', error);
    }
}

setInterval(updateMarkers, 5000);
