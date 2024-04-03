function refreshDatabase() {
    var currentPage = window.location.pathname.substring(1);
    console.log("Refreshing database...");
    fetch("/refresh", {
        method: "POST"
    })
    .then(response => {
        console.log("Database refreshed.");
        location.reload();
    })
    .catch(error => console.error('Error:', error));
}
