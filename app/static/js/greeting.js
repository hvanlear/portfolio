const today = new Date();
const day = today.getDay();
const dayList = ["Sunday","Monday","Tuesday","Wednesday ","Thursday","Friday","Saturday"];
console.log(`WELCOME ON ${today}`);
let hour = today.getHours();
const minute = today.getMinutes();
const second = today.getSeconds();
let prepand
let emoji = document.querySelector('.timeEmoji')
let tod = document.querySelector('.tod')

if (hour <= 11){
    tod.innerHTML = `${dayList[day]} morning`
    emoji.innerHTML='&#9749'
} else if(hour >= 12 && hour <= 17){
    tod.innerHTML = `${dayList[day]} afternoon`
    emoji.innerHTML='&#127780'
} else {
    tod.innerHTML = `${dayList[day]} evening`
    emoji.innerHTML='&#127771'
}