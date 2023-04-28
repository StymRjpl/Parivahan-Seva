function display() {

    var images = {
    silver: {
    img: "https://i.imgur.com/zCZhcUN.jpg",
    description: "Hyundai ELITE i20 Star Dust",
    price: "5,29000",
    reviews:"3255 reviews",
    emi:"5,222",
    color:"Star Dust",
    transmission:"Manual",
    alloy_wheel:"Yes"
    },
    grey: {
    img: "https://i.imgur.com/6YqPMsz.jpg",
    description: "Hyundai ELITE i20 Fiery Red",
    price: "5,34000",
    reviews:"3155 reviews",
    emi:"5,422",
    color:"Fiery Red",
    transmission:"Manual",
    alloy_wheel:"No"
    
    },
    red: {
    img: "https://i.imgur.com/i0PJKZ3.jpg",
    description: "Hyundai ELITE i20 White",
    price: "5,38000",
    reviews:"2390 reviews",
    emi:"5,822",
    color:"White",
    transmission:"Manual",
    alloy_wheel:"Yes"
    },
    
    blue: {
    img: "https://i.imgur.com/4cz8gxk.jpg",
    description: "Hyundai ELITE i20 Fiery Red",
    price: "5,22000",
    reviews:"2300 reviews",
    emi:"5,022",
    color:"Fiery Red",
    transmission:"Manual",
    alloy_wheel:"No"
    }
    
    };
    
    for (i = 0; i < 4; i++) { if (document.colorpicker.color[i].checked==true) { var checkNumber=document.colorpicker.color[i]; document.stage.src=images[checkNumber.value].img; $("#description").innerHTML=images[checkNumber.value].description; $(".product_price").html(images[checkNumber.value].price); $(".product_name").html(images[checkNumber.value].description); $(".rating-review").html(images[checkNumber.value].reviews); $(".emi_starts").html(images[checkNumber.value].emi); $(".car_color").html(images[checkNumber.value].color); $(".car_transmission").html(images[checkNumber.value].transmission); $(".car_alloy").html(images[checkNumber.value].alloy_wheel); } } }