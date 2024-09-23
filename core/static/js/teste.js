async function getUserStats(username) {
    try {
        currentPageIndex = 1; // Reset the current page index to 1
        // Prepare request parameters
        const params = { discourseNames: [username] };
        const headers = { 'Content-type': 'application/json', 'Accept': 'text/plain' };
        const url = 'https://api.infiniteflight.com/public/v2/user/stats?apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw';
        // Make the request
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(params),
            headers,
        });
        // Convert the response to JSON
        const { result: userStats } = await response.json();

        // Verifica se o array não é vazio e se o primeiro elemento possui a propriedade userId
        if (userStats && userStats[0] && userStats[0].userId) {
            userId = userStats[0].userId;
            console.log(userId)
            // Get the user flights
            const userFlights = await getUserFlights(userId);
            return [userStats, userFlights];
        } else {
            // Exibe o alerta
            alert('Nome não encontrado');
        }
    } catch (error) {
        console.error(error);
    }
}


async function getUserFlights(userId, page = 1) {
    try {
        const url = `https://api.infiniteflight.com/public/v2/users/${userId}/flights?page=${page}&apikey=nvo8c790hfa9q3duho2jhgd2jf8tgwqw`;
        const response = await fetch(url);
        const { result: userFlights } = await response.json();
        return userFlights;
    } catch (error) {
        console.error(error);
    }
}


getUserStats('Gabriel_f')