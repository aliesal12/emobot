document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("teacher").addEventListener("click", function() {
        window.location.href = "http://127.0.0.1:5000/teacherbot";
    });

    document.getElementById("student").addEventListener("click", function() {
        window.location.href = "http://127.0.0.1:5000/studentbot";
    });
});