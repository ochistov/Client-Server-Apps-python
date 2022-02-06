const http = require('http');
const url = require('url');

http.createServer((request, response) => {
    // console.log('server work');
    if (request.method == 'GET') {

        let urlRequest = url.parse(request.url, true);
        // console.log(urlRequest.query.action);
        // console.log(urlRequest.query.value);
        if (urlRequest.query.action == 'encode') {
            let respEnc = new String();
            let tempVal = urlRequest.query.value;
            for (var i = 0; i < tempVal.length; i++) {
                var hex = tempVal.codePointAt(i).toString(16);
                var result = "\\u" + "0000".substring(0, 4 - hex.length) + hex;
                respEnc += result;
            }
            // console.log(respEnc);
            response.write(respEnc);
            response.end();

        } else if (urlRequest.query.action == 'decode') {
            let respDec = new String();
            let tempVal = urlRequest.query.value;
            try {
                let tempVal1 = tempVal.substr(2);
                let tempList = tempVal1.split('\\u')
                let res = new String();
                for (var i = 0; i < tempList.length; i++) {
                    var dec = parseInt(tempList[i], 16);
                    respDec += String.fromCodePoint(dec);
                }
                // console.log(respDec);
                response.write(respDec);
                response.end();
            } catch {
                respDec = 'Hey! Please dont try to broke this!';
                response.write(respDec);
                response.end();
            }
        } else {
            response.write('Sorry, i dont know this action:(');
            response.end();
        }
    } else {
        response.write('ONLY GET METHOD PLEASE');
        response.end();
    }


}).listen(3000);

