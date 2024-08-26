function showPage(pageId, element) {
    document.querySelectorAll('.tab-content').forEach(page => page.classList.remove('active-tab-content'));
    document.getElementById(pageId).classList.add('active-tab-content');

    var buttons = document.querySelectorAll('.btn-group .btn');
    buttons.forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
    });
    element.classList.remove('btn-secondary');
    element.classList.add('btn-primary');
}

function confirmSelection() {
    var selectedScenarios = document.getElementById('selectedScenarioText');
    selectedScenarios.innerHTML = '';  // Mevcut içeriği temizle
    var selectedRadio = document.querySelector('.scenario-radio:checked');
    if (selectedRadio) {
        selectedScenarios.innerHTML = selectedRadio.value; // Seçilen senaryoyu göster

        // JSON dosyasını yükleyip tabloya yaz
        var fileName = selectedRadio.value.includes("bosTur") ? "bosYuk.json" : "doluYuk.json";
        loadJson(fileName, selectedRadio.value);
    }
}

function loadJson(file, scenario) {
    fetch(file)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('senaryoTabloBody');
            tableBody.innerHTML = ''; // Mevcut tabloyu temizle

            // Dosyadaki tüm senaryoları döngü ile kontrol edin
            const selectedScenario = data.scenarios.find(s => s.scenario === scenario);

            if (selectedScenario && selectedScenario.movements) {
                selectedScenario.movements.forEach(movement => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${selectedScenario.scenario}</td>
                        <td>${movement.start}</td>
                        <td>${movement.end}</td>
                        <td>${movement.qrcodes.map(qr => qr.id).join(', ')}</td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                console.error('Seçilen senaryo hatalı veya beklenen yapıya sahip değil.');
            }
        })
        .catch(error => console.error('JSON dosyası yüklenemedi:', error));
}
