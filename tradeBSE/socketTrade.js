const io = require('socket.io-client');

BSE_STREAMER="https://streamlive.bseindia.com"
const socket = io (BSE_STREAMER,{
    upgrade: true, 
    'transports': ['websocket']
});


const manger = new Manager()

socket.on("connect",()=>{
    console.log(socket.connected);
} );


