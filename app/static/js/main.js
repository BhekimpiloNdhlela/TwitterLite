/**
 * Activates the left sidebar for the variers user options
 * @param {String} id Name of the group to show
 */
const myFunction = (id) => {
    let x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += " w3-theme-d1";
    } else {
        x.className = x.className.replace("w3-show", "");
        x.previousElementSibling.className =
            x.previousElementSibling.className.replace(" w3-theme-d1", "");
    }
}

/**
 * Used to toggle the menu on smaller screens when clicking on the menu button
 */
const openNav = () => {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}
// used to make hashtags anchor tag in order to access page display all posts containing the hashtag
// used to make @'s of users anchor tags to view users profile
const hashtag = /(\#\w+)/g;
const atUser = /(\@\w+)/g;
const timestamp = /(\d*\.\d*)/;
$(document.body).ready(function () {

    $(".main").html(function (_, html) {
        return html.replace(hashtag,
            '<a style="color: blue;" href="/tag/$1">$1</a>');

    });

    $(".main").html(function (_, html) {
        return html.replace(atUser,
            '<a style="color: #1c94e0;" href="/profile/$1">$1</a>');
    });

    $(".timestamp").html(function (_, html) {
        return html.replace(html, moment(moment(html)).twitterLong());
    });

    $(document.body).ready(function () {
        var i = 0,
            j = '',
            val = '';
        var list = document.getElementsByTagName("a");
        for (i; i < list.length; i++) {
            j = $(list[i]).attr('href');
            valHash = j.replace('#', '');
            valName = valHash.replace('@', '');
            $(list[i]).attr('href', valHash);
            $(list[i]).attr('href', valName);
        }
    });

});


let image = 1;
$("#imageUpload").click(function () {
    // Create file input and upload file
    console.log("Test");
    let input = $(document.createElement("input"));
    input.attr("type", "file");
    input.attr("name", 'picture[' + (image++) + ']');
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

/**
 * Makes a AJAX get request to like a tweet
 * @param {String} tweetID ID of the tweet
 * @param {this} thisElement A clone of the button from which it called
 */
const likePost = (tweetID, thisElement) => {
    $.get(("/like/" + tweetID)).then((response) => {

        $('#like' + tweetID).attr('onclick', 'unlikePost(\'' + tweetID + '\');');
        $('#like' + tweetID + 'unlike').show();
        $('#like' + tweetID + 'like').hide();
        console.log(response)
        $('#like' + tweetID + 'value').text(response['likes']);

    });
}

const unlikePost = (tweetID, thisElement) => {
    $.get(("/unlike/" + tweetID)).then((response) => {

        $('#like' + tweetID).attr('onclick', 'likePost(\'' + tweetID + '\');');
        $('#like' + tweetID + 'like').show();
        $('#like' + tweetID + 'unlike').hide();
        // }
    });
}

/**
 * Makes a AJAX get request to follow a user
 * @param {String} username Username of the user to follow
 * @param {this} thisElement A clone of the button from which it called
 */
const followUser = (username, thisElement) => {
    $.get(("/follow/" + username)).then((response) => {
        $(thisElement).text(response);
        $(thisElement).attr('href', '/unfollow/' + username);
    });
}

/**
 * Makes a AJAX get request to unfollow a user
 * @param {String} username Username of the user to follow
 * @param {this} thisElement A clone of the button from which it called
 */
const unfollowUser = (username, thisElement) => {
    $.get(("/follow/" + username)).then((response) => {
        $(thisElement).replace('Unfollow', response);
        $(thisElement).attr('href', '/follow/' + username);
    });
}


/**
 * Makes a AJAX get search results
 */
$('#search').keyup(() => {
    $.get(("/search/" + $('#search').val())).then((users) => {
        users['username'].forEach(username => {
            console.log(username)
        })
    });
});

/**
 * Switches a tab in a tabbed environment
 * @param {Event} e Event
 * @param {String} tabName The Tab's name to switch to 
 */
const changeTab = (e, tabName) => {
    let x = document.getElementsByClassName("tab");
    for (let i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    let tabLinks = document.getElementsByClassName("tabLink");
    for (i = 0; i < x.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(" w3-border-blue", "");
    }
    document.getElementById(tabName).style.display = "block";
    e.currentTarget.firstElementChild.className += " w3-border-blue";
}

/**
 * Preview function for Profile pictures
 */
const upload = () => {
    let file = document.getElementById('picture').files[0];
    let image = document.getElementById('image');
    let reader = new FileReader();
    reader.onload = function () {
        image.src = reader.result;
    };
    reader.readAsDataURL(file);
}