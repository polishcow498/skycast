window.onload = function () {
    const countrySelect = document.getElementById('iso2');
    const cityInput = document.querySelector('input[name="city"]');

    function enableCityField() {
        if (countrySelect.value === "") {
            cityInput.disabled = true;
        } else {
            cityInput.disabled = false;
        }
    }

    // Initial check in case form is reloaded
    enableCityField();

    // Attach event listener to dropdown
    countrySelect.addEventListener('change', enableCityField);
};
