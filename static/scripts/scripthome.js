document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("teacher").addEventListener("click", function() {
        window.location.href = "https://emobot.onrender.com:5000/teacherbot";
    });

    document.getElementById("student").addEventListener("click", function() {
        window.location.href = "https://emobot.onrender.com/studentbot";
    });
});