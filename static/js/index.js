$(document).ready(()=>{
    $("button").click(()=>{
        $("h1").toggle()
        $(".main").animate({
            "margin-top": '100px',
            "margin-left": '100px',
        }, 5000)
    })
})