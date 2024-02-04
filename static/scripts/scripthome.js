document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("teacher").addEventListener("click", function() {
        window.location.href = "http://localhost:5000/teacherbot";
    });

    document.getElementById("student").addEventListener("click", function() {
        window.location.href = "http://localhost:5000/studentbot";
    });
});