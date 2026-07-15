(function () {
    var slotSelect = document.getElementById("id_class_slot");
    var dateInput = document.getElementById("id_date");
    var dataScript = document.getElementById("class-slots-data");
    if (!slotSelect || !dateInput || !dataScript) return;

    var classSlots = JSON.parse(dataScript.textContent);

    function pad(n) {
        return n < 10 ? "0" + n : "" + n;
    }

    function autoDate(selectedId) {
        var slot = classSlots.find(function (s) {
            return s.id === parseInt(selectedId, 10);
        });
        if (!slot) return "";

        var now = new Date();
        var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        var todayDay = (now.getDay() + 6) % 7; // Convert JS Sun=0 to Mon=0..Sun=6
        var slotDay = slot.day_of_week;

        var daysAhead = slotDay - todayDay;
        if (daysAhead < 0) {
            daysAhead += 7;
        } else if (daysAhead === 0) {
            daysAhead = 7;
        }

        var result = new Date(today);
        result.setDate(result.getDate() + daysAhead);
        return result.getFullYear() + "-" + pad(result.getMonth() + 1) + "-" + pad(result.getDate());
    }

    slotSelect.addEventListener("change", function () {
        if (!this.value) return;
        dateInput.value = autoDate(this.value);
    });
})();
