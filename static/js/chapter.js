function deleteChapter() {
    agree = confirm("Are you sure you want to delete this Chapter?");
    if (agree) {
        $.ajax({
            url: "/delete/chapter?bookID={{book['_id']}}&chapterID={{chapter['_id']}}",
            method: "POST",
            success: function(data) {
                window.location.href = "/book/{{book['_id']}}";
            }
        });
    }
}
function renameChapter() {
    name = prompt("Enter new name");
    if (name != null) {
        $.ajax({
            url: "/edit/chapter?bookID={{book['_id']}}&name=" + name + "&chapterID={{chapter['_id']}}",
            method: "POST",
            success: function(data) {
                window.location.href = "/book/{{book['_id']}}/{{chapter['_id']}}";
            }
        });
    }
}