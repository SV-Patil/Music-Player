function send_rating(event){
    song = event.target;
    song_id = song.dataset.song_id;
    for(let i=1 ; i<=5;i++){
        if(i<=song.id){
            document.getElementById(i).className = "bi-star-fill";
        }
        else{
            document.getElementById(i).className = "bi-star";
        }
    }
    
    fetch("/rating/"+song_id+"/"+song.id).then(
        response => console.log(response)
    ).catch(
        err => console.log(err)
    )
}


function initialize(){
    rating_buttons = document.querySelectorAll(".bi-star");
    for (const rate_bt of rating_buttons){
        rate_bt.onclick = send_rating;
    }
}