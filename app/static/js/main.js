// Accordion
function myFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += " w3-theme-d1";
    } else {
        x.className = x.className.replace("w3-show", "");
        x.previousElementSibling.className =
            x.previousElementSibling.className.replace(" w3-theme-d1", "");
    }
}

// Used to toggle the menu on smaller screens when clicking on the menu button
function openNav() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}
// used to make hashtags anchor tag in order to access page display all posts containing the hashtag
const reg = /(\#\w+)/g;
$(document).ready(function () {
    $("p").html(function (_, html) {
        return html.replace(reg,
            '<a style="color: blue;" href="/tag/$1">$1</a>');

    });
});

// used to make @'s of users anchor tags to view users profile
const reg1 = /(\@\w+)/g;
$(document).ready(function () {
    $("p").html(function (_, html) {
        return html.replace(reg1,
            '<a style="color: red;" href="/user/$1">$1</a>');

    });
});


let image = 1;
$("#imageUpload").click(function () {
    // Create file input and upload file
    let input = $(document.createElement("input"));
    input.attr("type", "file");
    input.attr("name", 'picture['+(image++) +']');
    input.trigger("click");
    $("#pictures").append(input);
    input.on("change", () => {
        // Preview image
        let picturePreview = $(document.createElement("img"));
        picturePreview.addClass("w3-half");
        let file = input.toArray()[0].files[0];
        let reader = new FileReader();
        reader.onload = function () {
            picturePreview.attr("src", reader.result);
        };
        reader.readAsDataURL(file);
        $("#picturesDisplay").append(picturePreview);
    });
    return false; // avoiding navigation
});