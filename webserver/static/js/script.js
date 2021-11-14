var today = new Date().toISOString().split('T')[0];
document.getElementsByName("date")[0].setAttribute('min', today);

getSelectedTime = ()=>{
    selected_time = document.getElementById("time").value
    
    // Set time to modal form
    document.getElementById("selectedTime").innerHTML = selected_time
}