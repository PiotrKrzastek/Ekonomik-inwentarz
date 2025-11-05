//htmx:afterRequest global listeners

(function () {
    document.addEventListener('htmx:afterRequest', function (evt) {
        // users/partials/table_content related
        if (evt.detail.target.id.startsWith("updateUserForm_")) {
            console.log("EVENT DETAIL:", evt);
            if (!evt.detail.successful) {
                window.showTemporaryAlert('error', 'Wystąpił błąd podczas aktualizacji uprawnień użytkownika.', duration = 3000);
            }
        }

        if (evt.detail.target.id.startsWith("deleteUserForm_")) {
            if (evt.detail.successful) {
                const form = evt.detail.target;
                const userId = form.querySelector('input[name="user_id"]').value;
                const row = document.getElementById(`row_${userId}`);
                if (row) {
                    row.remove();
                }
            } else {
                window.showTemporaryAlert('error', 'Wystąpił błąd podczas usuwania użytkownika.', duration = 3000);
            }

        }

        // users/manage.html related
        if (evt.detail.target.id === "tableContent") {
            console.log("EVENT DETAIL:", evt);
            const form = document.getElementById('createUserForm');
            if (!evt.detail.successful) {
                window.showTemporaryAlert('error', 'Wystąpił błąd podczas dodawania użytkownika. Może już istnieć użytkownik z takim adresem e-mail.');
            }
        }
    })
})();

// htmx:beforeRequest global listeners
(function () {
    document.body.addEventListener('htmx:beforeRequest', function (evt) {
        // users/partials/table_content related
        if (evt.detail.target.id.startsWith("deleteUserForm_")) {
            console.log(evt)
            if (!confirm("Czy na pewno chcesz usunąć tego użytkownika?")) {
                evt.preventDefault();
            }
        }
    });

})();
