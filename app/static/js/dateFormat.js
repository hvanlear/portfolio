var DateTime = luxon.DateTime;
var now = DateTime.local()
let displayDates = document.querySelectorAll('.display-date')

function changeDates() {
    displayDates.forEach((date)=> {
    let formattedDate = date.innerHTML.slice(0,10)
    formattedDate = DateTime.fromISO(formattedDate).toFormat('EEEE LLL dd yyyy')
    date.innerHTML = formattedDate
    })
}

changeDates()

