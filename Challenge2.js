const proto = window.location.protocol === "https:" ? "wss" : "ws";

var ws = new WebSocket(proto + "://" + location.host + "/okws");
var array = [];
ws.onmessage = function (event) {
    array.push(event.data);
    console.log(atob(event.data));
}
const myTimeout = setTimeout(followingInstruction, 500);

function followingInstruction() {
    var arrayToManage = Array(16);
    array.forEach(line => {
        if (line === 'IkVORCI=') {
            var result = 0;
            arrayToManage.forEach(number => {
                result += number;
            });
            console.log(arrayToManage);
            console.log(btoa(result));
            ws.send(btoa(result));
        } else if (line.length < 60) {
            var atobLine = atob(line);
            var arrLine = atobLine.split(' ');

            if (arrLine[0] === '\"ADD') {
                var indexFrom = parseInt(arrLine[2].trim().substr(1));
                var indexTo = parseInt(arrLine[3].trim().substr(1));
                var value = parseInt(arrLine[1].trim());
                arrayToManage[indexTo] = arrayToManage[indexFrom] + value;
            } else if (arrLine[0] === '\"MOV') {
                var indexFrom = parseInt(arrLine[1].trim().substr(1));
                var indexTo = parseInt(arrLine[2].trim().substr(1));
                arrayToManage[indexTo] = arrayToManage[indexFrom];
            } else if (arrLine[0] === '\"STORE') {
                var indexTo = parseInt(arrLine[2].trim().substr(1));
                var value = parseInt(arrLine[1].trim());
                arrayToManage[indexTo] = value;
            }
        }
    });
}